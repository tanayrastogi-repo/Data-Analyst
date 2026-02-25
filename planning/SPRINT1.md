# SPRINT 1: The "Walking Skeleton"
These stories focus on Test Driven Development (TDD) establishing the core loop: **Upload Data $\rightarrow$ Ask Question $\rightarrow$ Get Calculated Answer**.

### **Sprint 1 User Stories**

#### **Story 1.1: Data Ingestion Interface**

*This story focuses on the mechanics of getting the file into the system.*

As a **Data Analyst**
I need **an interface to upload a CSV file**
So that **the system can access my specific dataset for analysis.**

**Assumptions and Details**:

* Supported file format is strictly `.csv` for this sprint.
* The application is running locally (localhost).
* We are using `marimo` for the frontend interface.

**Acceptance Criteria**:
Given **the application is running in the browser**
When **I drag and drop a valid CSV file (e.g., `titanic.csv`) into the upload area**
Then **the system should display a "File Uploaded Successfully" confirmation**
And **store the file in the project's temporary data directory.**

---

#### **Story 1.2: Data Preview & Verification**

*This ensures the data isn't just "uploaded" but actually "readable" by pandas.*

As a **Data Analyst**
I need **to see a preview of the first few rows of the uploaded data**
So that **I can verify the headers and data types were interpreted correctly.**

**Assumptions and Details**:

* The file has been successfully uploaded (dependency on Story 1.1).
* The system uses `polars` to read the file.

**Acceptance Criteria**:
Given **a CSV file has been uploaded**
When **the processing is complete**
Then **I should see a data table displaying the first 5 rows (head) of the dataset**
And **I should see the total row and column count (e.g., "891 rows, 12 columns").**

---

#### **Story 1.3: Natural Language Question Answering**

*This is the core "feature" of the MVP—connecting the LLM to the data.*

As a **Data Analyst**
I need **to ask a plain English question about the dataset**
So that **I can get specific statistics without writing Python code myself.**

**Assumptions and Details**:

* Questions will be simple "Level 1" queries (e.g., "What is the average age?", "How many unique cities?").
* The system uses an LLM (Gemini) to convert text to code.

**Acceptance Criteria**:
Given **the Titanic dataset is loaded**
When **I type "What is the maximum fare paid?" into the chat box**
Then **the system should return the correct numeric answer (e.g., "512.3292")**
And **the answer should be derived from actual calculation, not LLM guessing.**

---

#### **Story 1.4: Transparency & Verification (Show the Code)**

*This builds trust. The user needs to know the answer wasn't hallucinated.*

As a **Data Analyst**
I need **to see the Python code that was executed**
So that **I can trust the logic used to derive the answer.**

**Assumptions and Details**:

* The LLM generates Python code to answer the question.
* This code is executed in a local sandbox/REPL.

**Acceptance Criteria**:
Given **the system has provided an answer to my question**
When **I view the response card**
Then **I should see a code block (e.g., `df['Fare'].max()`) displayed alongside the text answer.**

---

#### **Story 1.5: Basic Error Handling**

*The "Unhappy Path". If the user asks for a column that doesn't exist, the app shouldn't crash.*

As a **Data Analyst**
I need **to receive a helpful error message if I ask about missing data**
So that **I know to rephrase my question or check the column names.**

**Assumptions and Details**:

* Users might misspell column names (e.g., "Cost" instead of "Fare").

**Acceptance Criteria**:
Given **the dataset has a column named "Fare" but NOT "Cost"**
When **I ask "What is the average Cost?"**
Then **the system should NOT crash**
And **it should respond with a message indicating that the column "Cost" was not found in the dataset.**

---
