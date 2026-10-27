from pathlib import Path
import pandas as pd
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = PROJECT_DIR / "data" / "sample_dataset.csv"
OUTPUT_PATH = PROJECT_DIR / "results" / "week1_results.csv"


# Shared state passed between graph nodes
class ComplaintState(TypedDict):
    complaint: str
    issue: str
    sentiment: str
    contact_count: int
    priority: str
    draft_response: str


# Node 1: Analyze the complaint
def analyze_complaint(state: ComplaintState):
    print("\n--- Node 1: Analyze Complaint ---")
    print("Complaint:", state["complaint"])
    print("Issue:", state["issue"])
    print("Sentiment:", state["sentiment"])

    return {}


# Node 2: Set priority
def set_priority(state: ComplaintState):
    print("\n--- Node 2: Set Priority ---")
    print("Contact count:", state["contact_count"])
    print("Priority:", state["priority"])

    return {}


# Node 3: Draft a response
def draft_response(state: ComplaintState):
    print("\n--- Node 3: Draft Response ---")

    if state["sentiment"] == "Negative":
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


# Build the LangGraph workflow
graph_builder = StateGraph(ComplaintState)

graph_builder.add_node("analyze_complaint", analyze_complaint)
graph_builder.add_node("set_priority", set_priority)
graph_builder.add_node("draft_response", draft_response)

graph_builder.add_edge(START, "analyze_complaint")
graph_builder.add_edge("analyze_complaint", "set_priority")
graph_builder.add_edge("set_priority", "draft_response")
graph_builder.add_edge("draft_response", END)

complaint_graph = graph_builder.compile()


# Load the dataset and process the first complaint
df = pd.read_csv(DATA_PATH)
row = df.iloc[0]

initial_state: ComplaintState = {
    "complaint": str(row["complaint"]),
    "issue": str(row["issue"]),
    "sentiment": str(row["sentiment"]),
    "contact_count": int(row["contact_count"]),
    "priority": str(row["priority"]),
    "draft_response": "",
}

print("Starting LangGraph workflow...")
final_state = complaint_graph.invoke(initial_state)

# Save the result
result_df = pd.DataFrame([final_state])
result_df.to_csv(OUTPUT_PATH, index=False)

print("\n--- Workflow Complete ---")
print("Result saved to:", OUTPUT_PATH)
print("Final priority:", final_state["priority"])
print("Final response:", final_state["draft_response"])