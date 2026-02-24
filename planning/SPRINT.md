## Sprint Plan
I want to implement this proect in a AGILE Sprint fashion. Here is the structured overview for the project.

### **Sprint 1: The "Walking Skeleton" (Foundations & Simple Q/A)**

**Theme:** *Plumbing & First Breath*
The objective of this sprint is to build the "skeleton" of the application. It won't be smart yet, but it will be functional. It establishes the development environment, the basic UI, and the connection between the LLM and the data.

* **GOAL:** A functional local application where a user can upload a CSV and ask a free-text question to get a Python-calculated answer.
* **FOCUS:**
* **Environment Setup:** Initialize `uv` project, set up `marimo` for the UI, and configure Gemini API keys.
* **Data Ingestion:** Create the logic to read and load a CSV file into a Pandas DataFrame.
* **Basic Agent:** Build a simple LangGraph node that takes a user query (e.g., "How many rows are there?"), converts it to Pandas code, and executes it.


* **EXPECTED OUTCOMES:**
* A running `marimo` notebook/app on `localhost`.
* Successful file upload capability (drag-and-drop).
* **Feature:** "Chat with Data" – The user asks "What is the average age?" and the system returns the correct number by running Python code.
* **Tech Deliverable:** A `langgraph` workflow with a single "Code Execution" node.



---

### **Sprint 2: The "Automated Inspector" (Level 1 & 2 Analysis)**

**Theme:** *Automated Exploration*
Now that the agent can answer questions, we shift to *proactive* analysis. We will implement the structured "Insight Levels" to automatically generate reports without the user having to ask specific questions.

* **GOAL:** The application automatically generates a report covering Column Profiles (Level 1) and Pairwise Relationships (Level 2) upon data upload.
* **FOCUS:**
* **Level 1 Logic:** Implement loops to iterate through columns. If *Continuous* $\rightarrow$ calc mean/max/min. If *Discrete* $\rightarrow$ calc frequency.
* **Level 2 Logic:** Implement correlation checks. If *Cat + Cont* $\rightarrow$ GroupBy averages. If *Cat + Cat* $\rightarrow$ Cross-tabulation.
* **Agent Loop:** Refine the LangGraph to handle multiple tool calls in sequence (generating code for multiple columns).


* **EXPECTED OUTCOMES:**
* **Feature:** "Auto-Profile" button. Clicking it generates a structured text summary of the dataset.
* **Feature:** Bivariate insights (e.g., "People over 50 have 20% higher Income").
* **UI Update:** Display these insights in expandable sections (Markdown) within the Marimo app.



---

### **Sprint 3: The "Deep Diver" (Level 3 Analysis & Self-Correction)**

**Theme:** *Complexity & Resilience*
This is the most mathematically complex sprint. We add the Trivariate analysis and, crucially, the "Self-Correction" mechanism. If the LLM writes bad code (which happens often with complex queries), it must catch the error and fix itself.

* **GOAL:** Implement complex 3-variable analysis and ensure the agent is robust enough to fix its own coding errors.
* **FOCUS:**
* **Level 3 Logic:** Implement prompt logic to look for interactions (e.g., using Decision Trees to find rules like `IF Age > X AND License = Yes THEN...`).
* **Error Handling (Self-Correction):** Update LangGraph. If the code execution tool returns a `Python Error`, loop back to the LLM with the error message to regenerate the code.
* **Visuals:** Allow the agent to generate simple charts (matplotlib/seaborn) to support its insights.


* **EXPECTED OUTCOMES:**
* **Feature:** Complete "Level 3 Insight" generation (A + B $\rightarrow$ C relationships).
* **Feature:** Self-healing agents (The logs show the agent fixing a `KeyError` or `SyntaxError` automatically).
* **Feature:** Charts embedded in the insights (e.g., a scatter plot showing the 3-variable relationship).



---

### **Sprint 4: The "Cloud Commander" (Deployment & Polish)**

**Theme:** *Production & Shipping*
The code works locally; now it needs to work for everyone. This sprint focuses on moving off `localhost`, securing the app, and ensuring it runs in a containerized environment.

* **GOAL:** A secure, publicly accessible URL where users can access the application, hosted on the Cloud.
* **FOCUS:**
* **Containerization:** Create a `Dockerfile` that packages `uv`, `marimo`, and the Python runtime.
* **Infrastructure:** Deploy to a cloud provider (e.g., **Google Cloud Run** is excellent for containerized Python apps).
* **Security:** Ensure API keys are injected via Environment Variables (Secrets Management), not hardcoded.
* **Testing:** Finalize `pytest` suite to ensure the "Analyst" doesn't hallucinate on standard test datasets (like Titanic or Iris).


* **EXPECTED OUTCOMES:**
* **Deliverable:** A live public URL (e.g., `https://my-data-analyst.run.app`).
* **Deliverable:** CI/CD pipeline (GitHub Actions) that runs tests when code is pushed.
* **User Experience:** A polished UI with loading states (spinners) while the agent is "thinking/coding."



---

### **Summary of Value Delivery**

| Sprint | User Value (MVP) | Technical Milestone |
| --- | --- | --- |
| **1** | "I can upload data and ask a specific question." | Basic LangGraph Agent + Marimo UI |
| **2** | "The app tells me the basics about my columns and simple pairs." | Level 1 & 2 Logic + Loop iteration |
| **3** | "The app finds hidden, complex patterns and fixes its own bugs." | Level 3 Logic + Self-Correction Loop |
| **4** | "I can share the link with my boss/team." | Docker + Cloud Deployment |