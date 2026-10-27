
from pathlib import Path
from typing import TypedDict

import pandas as pd

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.sqlite import SqliteSaver


# --------------------------------------------------
# 1. Project paths
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "sample_dataset.csv"
OUTPUT_PATH = PROJECT_DIR / "results" / "week1_results.csv"
CHECKPOINT_PATH = PROJECT_DIR / "checkpoints.sqlite"


# --------------------------------------------------
# 2. Shared state passed between graph nodes
# --------------------------------------------------

class ComplaintState(TypedDict):
    complaint: str
    issue: str
    sentiment: str
    contact_count: int
    priority: str
    draft_response: str
    review_status: str
    review_attempts: int


# --------------------------------------------------
# 3. Node 1: Analyze the complaint
# --------------------------------------------------

def analyze_complaint(state: ComplaintState):
    print("\n--- Node 1: Analyze Complaint ---")
    print("Complaint:", state["complaint"])
    print("Issue:", state["issue"])
    print("Sentiment:", state["sentiment"])

    return {}


# --------------------------------------------------
# 4. Node 2: Display the complaint priority
# --------------------------------------------------

def set_priority(state: ComplaintState):
    print("\n--- Node 2: Set Priority ---")
    print("Contact count:", state["contact_count"])
    print("Priority:", state["priority"])

    return {}


# --------------------------------------------------
# 5. Node 3: Draft a response
# --------------------------------------------------

def draft_response(state: ComplaintState):
    print("\n--- Node 3: Draft Response ---")

    if state["sentiment"].lower() == "negative":
        response = (
            f"We're sorry for the inconvenience with your "
            f"{state['issue'].lower()}. We understand your concern "
            f"and appreciate your patience. Our support team will "
            f"review your issue and assist you further."
        )
    else:
        response = (
            f"Thank you for contacting us about your "
            f"{state['issue'].lower()}. We appreciate you reaching out "
            f"and are happy to assist you."
        )

    print("Draft response:", response)

    return {"draft_response": response}


# --------------------------------------------------
# 6. Node 4: Pause for human review
# --------------------------------------------------

def human_review(state: ComplaintState):
    print("\n--- Node 4: Human Review ---")
    print("Draft response:", state["draft_response"])
    print("Review attempt:", state["review_attempts"] + 1, "of 3")

    # Pause the workflow and request a human decision.
    decision = interrupt({
        "draft_response": state["draft_response"],
        "message": "Approve or reject this response.",
        "allowed_decisions": ["approved", "rejected"],
    })

    # Validate the decision received when the workflow resumes.
    if not isinstance(decision, str):
        raise ValueError("The review decision must be text.")

    decision = decision.strip().lower()

    if decision not in ("approved", "rejected"):
        raise ValueError(
            "Invalid decision. Enter 'approved' or 'rejected'."
        )

    return {
        "review_status": decision,
        "review_attempts": state["review_attempts"] + 1,
    }


# --------------------------------------------------
# 7. Decide what happens after human review
# --------------------------------------------------

def route_after_review(state: ComplaintState):
    if state["review_status"] == "approved":
        return "approved"

    if state["review_attempts"] >= 3:
        return "max_attempts_reached"

    return "rejected"


# --------------------------------------------------
# 8. Node 5: Revise a rejected response
# --------------------------------------------------

def revise_response(state: ComplaintState):
    print("\n--- Node 5: Revise Response ---")

    revised_response = (
        f"We apologize for the inconvenience regarding your "
        f"{state['issue'].lower()}. Your concern is important to us, "
        f"and our support team will review it again."
    )

    print("Revised response:", revised_response)

    return {
        "draft_response": revised_response,
        "review_status": "",
    }


# --------------------------------------------------
# 9. Build the LangGraph workflow
# --------------------------------------------------

graph_builder = StateGraph(ComplaintState)

graph_builder.add_node("analyze_complaint", analyze_complaint)
graph_builder.add_node("set_priority", set_priority)
graph_builder.add_node("draft_response", draft_response)
graph_builder.add_node("human_review", human_review)
graph_builder.add_node("revise_response", revise_response)

# Normal workflow edges
graph_builder.add_edge(START, "analyze_complaint")
graph_builder.add_edge("analyze_complaint", "set_priority")
graph_builder.add_edge("set_priority", "draft_response")
graph_builder.add_edge("draft_response", "human_review")

# Conditional routing after human review
graph_builder.add_conditional_edges(
    "human_review",
    route_after_review,
    {
        "approved": END,
        "rejected": "revise_response",
        "max_attempts_reached": END,
    },
)

# Review a revised response again
graph_builder.add_edge("revise_response", "human_review")


# --------------------------------------------------
# 10. Load the sample dataset
# --------------------------------------------------

def load_initial_state() -> ComplaintState:
    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("The sample dataset contains no complaints.")

    # Process the first complaint in the dataset.
    row = df.iloc[0]

    return {
        "complaint": str(row["complaint"]),
        "issue": str(row["issue"]),
        "sentiment": str(row["sentiment"]),
        "contact_count": int(row["contact_count"]),
        "priority": str(row["priority"]),
        "draft_response": "",
        "review_status": "",
        "review_attempts": 0,
    }


# --------------------------------------------------
# 11. Run and resume the workflow
# --------------------------------------------------

def main():
    # Ensure the output directory exists.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # A stable thread ID identifies this workflow's checkpoints.
    config = {
        "configurable": {
            "thread_id": "complaint-001"
        }
    }

    initial_state = load_initial_state()

    # SQLite stores checkpoints so interrupted execution can resume.
    with SqliteSaver.from_conn_string(str(CHECKPOINT_PATH)) as checkpointer:

        complaint_graph = graph_builder.compile(
            checkpointer=checkpointer
        )

        print("Starting LangGraph workflow...")

        # Start the workflow.
        result = complaint_graph.invoke(initial_state, config)

        # Continue whenever the graph pauses for human review.
        while result.get("__interrupt__"):

            interrupt_info = result["__interrupt__"][0].value

            print("\n--- Human Review Required ---")
            print("Draft response:", interrupt_info["draft_response"])

            while True:
                decision = input(
                    "Approve or reject? (approved/rejected): "
                ).strip().lower()

                if decision in ("approved", "rejected"):
                    break

                print("Please enter 'approved' or 'rejected'.")

            # Resume the same graph using the saved checkpoint.
            result = complaint_graph.invoke(
                Command(resume=decision),
                config,
            )

        # The graph has now finished.
        final_state = result

        # Save the final result, including the review decision.
        result_df = pd.DataFrame([final_state])
        result_df.to_csv(OUTPUT_PATH, index=False)

        print("\n--- Workflow Complete ---")
        print("Result saved to:", OUTPUT_PATH)
        print("Final priority:", final_state["priority"])
        print("Review status:", final_state["review_status"])
        print("Review attempts:", final_state["review_attempts"])
        print("Final response:", final_state["draft_response"])

        if final_state["review_status"] == "approved":
            print("Outcome: The response was approved.")
        else:
            print(
                "Outcome: The response was not approved "
                "within the allowed review attempts."
            )

        print("Checkpoint database:", CHECKPOINT_PATH)


# --------------------------------------------------
# 12. Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()
