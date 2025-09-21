# Smart Task Assistant 🤖📋

An AI-powered task management system that uses natural language processing (NLP) to automatically organize, prioritize, and schedule your tasks. This project demonstrates the practical application of AI to enhance productivity, transforming unstructured text into actionable, prioritized plans.

## 🚀 Features

- **Natural Language Understanding:** Input tasks in plain English (e.g., "Finish slides for meeting next Tue, ~2h, high importance").
- **Automated Parsing & Enrichment:**
  - **Deadline Extraction:** Leverages `dateparser` to identify and parse due dates from natural language.
  - **Duration Estimation:** Uses regex patterns to find and extract time estimates (e.g., "~2h").
  - **Importance Detection:** Identifies priority keywords like "urgent," "ASAP," and "high importance."
- **Intelligent Priority Scoring:** Implements a custom heuristic algorithm that synthesizes deadline urgency, task duration, and explicit importance cues into a single priority score for automated ranking.
- **Interactive Web Dashboard:** Provides a clean, responsive Streamlit interface for adding tasks, reviewing parsed details, and visualizing your automatically sorted priority queue.

## 🛠️ Tech Stack

- **Frontend & Application Framework:** Streamlit
- **Natural Language Processing (NLP):** spaCy
- **Date Parsing:** dateparser
- **Core Language:** Python 3.10+
- **Supporting Libraries:** Regex, Pandas

## 📸 Demonstration

**Input:**
`"Finish quarterly report by next Friday, should take about 4 hours, this is urgent"`

**Parsed Output:**
- **Task:** Finish quarterly report
- **Deadline:** [Date of next Friday]
- **Estimated Duration:** 4 hours
- **Priority Level:** High
- **Calculated Priority Score:** 92/100

![Smart Task Assistant Interface](assets/smart-task-assistant-screenshot.png)

## 📁 Project Structure


## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation & Run

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Auction-s/Assist.git
    cd Assist
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # On macOS/Linux
    python -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies and the spaCy language model:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

4.  **Launch the application:**
    ```bash
    streamlit run app.py
    ```

## 🔬 Lessons Learned

Building this project provided deep practical experience in several key areas:

- **Bridging NLP with Application Logic:** Moving from theoretical NLP concepts to a functional parser required careful prompt engineering and logic design to handle the variability of human language.
- **Heuristic Model Design:** Developed a custom scoring algorithm, which taught valuable lessons in balancing multiple input factors (time, date, keywords) to create a fair and useful priority system.
- **End-to-End Product Development:** This project encompassed everything from backend algorithm design to frontend UI/UX with Streamlit, providing a complete full-stack development experience.
- **The Value of User-Centric Design:** The biggest challenge and lesson was designing the system to be intuitive for the user, ensuring the NLP model interpreted commands in a way that felt natural and predictable.

## ➡️ Future Improvements

- **ML-Powered Prioritization:** Replace the heuristic model with a machine learning model trained on user feedback to learn personalized prioritization habits.
- **Calendar Integration:** Sync deadlines and estimated tasks directly to Google Calendar or Outlook.
- **Project Breakdown:** Extend the NLP to break down complex tasks (e.g., "plan a vacation") into subtasks with individual deadlines.
- **Deployment:** Containerize with Docker and deploy the application on a cloud platform for always-accessible use.
