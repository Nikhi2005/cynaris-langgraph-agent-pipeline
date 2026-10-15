# LangGraph Stateful Agent Pipeline

## Internship Project
Cynaris Solutions AI/ML Internship

## Project Objective
Build a stateful multi-step agent pipeline using LangGraph with
conditional branching, memory, and human-in-the-loop checkpoints
for business workflow automation.

## Week 1 - Day 1
### Setup Completed

- Created project workspace
- Created Python virtual environment
- Installed LangGraph
- Installed LangChain Core
- Installed LangChain OpenAI
- Verified LangGraph installation successfully

## Verification

LangGraph was successfully imported and the output was:

`LangGraph ready`


## Week 1 - Day 2

### Codebase Exploration

#### 1. Top-Level Project Structure

ai-ml-internship/
├── screenshots/
│   └── Day1_LangGraph_Setup.png
├── .gitignore
└── README.md

#### 2. Folder and File Descriptions

- `screenshots/` — Stores screenshots documenting project progress.
- `.gitignore` — Specifies files and folders Git should ignore.
- `README.md` — Contains the project objective, setup information, and progress documentation.
- `venv/` — Python virtual environment containing installed dependencies. Excluded from Git.
- `.git/` — Git repository metadata used for version control.

#### 3. Main Entry Point

No main application entry-point file, such as `main.py` or `app.py`, has been created yet.

#### 4. Key Python Modules

No application-specific Python modules have been created yet. The three key modules will be documented when they exist.

#### 5. Configuration and Environment Variables

No project-specific configuration file or environment variable setup has been identified yet.

#### Summary

The project setup and version control are complete. The current repository contains project documentation and screenshots. Application code and its configuration are yet to be created.


## Week 1 - Day 3: Map Data Flow in LangGraph

### 1. Workflow Objective

The pipeline will process customer complaints, identify the main issue and sentiment, prepare an appropriate response, and require human approval before a response is marked ready to send.

### 2. Data Flow Diagram

Customer Complaint
        |
        v
  Receive Input
        |
        v
 Analyze Complaint
 (issue, sentiment,
 previous attempts)
        |
        v
  Set Priority
        |
        v
  Draft Response
        |
        v
  Human Review
        |
        v
  +----- Decision -----+
  |                    |
Approved             Rejected
  |                    |
  v                    v
Mark Ready       Revise Response
to Send                 |
  |                     |
  v                     +----> Human Review
Final Output

### 3. Planned Graph Nodes

- **Receive Input:** Accept and store the original customer complaint.
- **Analyze Complaint:** Identify the issue, sentiment, and previous support attempts.
- **Set Priority:** Assign a priority using the available issue details and history.
- **Draft Response:** Prepare a polite, relevant response without making unsupported promises.
- **Human Review:** Pause for a human to approve or reject the draft.
- **Revise Response:** Use the reviewer's feedback to improve a rejected draft.
- **Final Output:** Record the approved response and mark it ready to send.

### 4. State Information

The shared graph state is planned to contain:

- `complaint`: Original customer message.
- `issue`: Identified customer problem.
- `sentiment`: Detected sentiment.
- `contact_count`: Number of previous support attempts, when known.
- `priority`: Assigned complaint priority.
- `draft_response`: Response prepared by the agent.
- `review_status`: Pending, approved, or rejected.
- `review_feedback`: Human review comments.
- `final_response`: Approved response, when available.

### 5. Nodes, Edges, and Conditional Routing

- **Nodes** perform individual processing steps.
- **Edges** connect nodes and determine the next step.
- **Conditional routing** sends the workflow along different paths based on a decision.
- An approved response proceeds to the final output.
- A rejected response returns for revision and another human review.

### 6. State and Human-in-the-Loop

The graph state carries complaint details, analysis results, response drafts, and review feedback between nodes. Human review prevents a rejected or unapproved draft from being marked ready to send.

The implementation will be added and tested incrementally in the following tasks.


## Week 1 - Day 4: Load Sample Data

### Dataset

Created `data/sample_dataset.csv` containing 10 illustrative customer complaints and 5 columns:

- `complaint`: Original customer message.
- `contact_count`: Number of reported support contacts.
- `issue`: Complaint category.
- `sentiment`: Positive, Neutral, or Negative.
- `priority`: Example priority label.

### Data Loading and Inspection

Created `load_sample_data.py` to load the CSV using pandas and inspect its structure.

**Verified output:**
- Rows: 10
- Columns: 5
- Data types: 4 text columns and 1 integer column
- Preview: First 5 rows displayed successfully

### Evidence

Screenshot: `screenshots/Day4_Sample_Data_Load.png`

**Note:** The dataset contains illustrative examples and labels. The priority and sentiment values have not been generated or validated by a trained AI model.