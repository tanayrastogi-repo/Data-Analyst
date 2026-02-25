import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import os
    import polars as pl
    from typing import Annotated, TypedDict
    from langgraph.graph import StateGraph, START, END
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
    from dotenv import load_dotenv

    return (
        BaseMessage,
        ChatGoogleGenerativeAI,
        END,
        HumanMessage,
        START,
        StateGraph,
        TypedDict,
        mo,
        os,
        pl,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Insight-3: Data Analyst Agent
    """).center()
    return


@app.cell
def _(agent_info, graph_viz, mo):
    mo.hstack([graph_viz, agent_info], gap=2, align="start", widths=[1, 2]).callout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. UPLOAD DATA
    ---

    Add data that you want to analyze. Currently we accept follwing file formats:
    * CSV
    """)
    return


@app.cell
def _(mo):
    # 1. File Upload
    upload_widget = mo.ui.file(label="Upload CSV File", filetypes=[".csv"], kind="area")
    return (upload_widget,)


@app.cell
def _(load_csv_from_bytes, mo, upload_widget):
    file_content = upload_widget.contents()
    if file_content:
        try:
            df = load_csv_from_bytes(file_content)
            data_view = mo.ui.table(df, label="Loaded Data", page_size=5)
        except Exception as e:
            data_view = mo.md(f"Error loading CSV: {e}").callout(kind="danger")
    else:
        data_view = mo.md("No data loaded yet.")
    return (data_view,)


@app.cell
def _(data_view, mo, upload_widget):
    # Combine Upload + Preview
    upload_area = mo.hstack([upload_widget, data_view], widths=[1, 1])
    upload_area
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. AGENTIC ANALYSIS
    ---

    First select the model that you want to use for analysis. Currently we only support the google models. Select a model from the list table below.
    """)
    return


@app.cell
def _(model_selector):
    model_selector
    return


@app.cell
def _(mo, run_agent, selected_model_name):
    # --- Bottom Row: Chat Interface ---

    def chat_response(messages, config):
        user_msg = messages[-1].content
        # Use the currently selected model from the top row's state
        return run_agent(prompt=user_msg, model_name=selected_model_name)

    chat_interface = mo.ui.chat(
        chat_response,
        prompts=[
            "What are the columns?",
            "Give me a summary",
            "Plot the distribution of age",
        ],
        show_configuration_controls=False,
    )

    chat_interface
    return


@app.cell
def _(mo):
    # Info Markdown
    agent_info=mo.md("""
    ### About Insight-3

    **Insight-3** is an autonomous Data Analyst agent designed to help you explore and understand your data.

    *   **Upload** your dataset (CSV).
    *   **Select** a powerful Gemini model.
    *   **Ask** questions in natural language.

    The agent uses **LangGraph** to orchestrate reasoning and **Polars** for high-performance data processing.
    """)
    return (agent_info,)


@app.cell
def _(list_supported_models, mo):
    # Model Selection (Needed for Graph)
    try:
        models_info = list_supported_models()
        # Default to a Flash model if possible
        initial_idx = 0
        for i, m in enumerate(models_info):
            if "flash" in m["Name"].lower():
                initial_idx = i
                break

        model_selector = mo.ui.table(
            models_info,
            selection="single",
            label="Choose A LLM Agent ",
            initial_selection=[initial_idx],
            page_size=6,
        ).callout()
    except ValueError as e:
        model_selector = mo.md(f"**Error:** {str(e)}").callout(kind="danger")
    return (model_selector,)


@app.cell
def _(get_agent_graph, mo, model_selector):
    # Graph Visualization (Dependent on Model Selector)
    selected_model_name = "models/gemini-1.5-flash"  # Default fallback
    if isinstance(model_selector, mo.ui.table) and model_selector.value:
        selected_model_name = model_selector.value[0]["Name"]

    graph = get_agent_graph(selected_model_name)
    graph_viz = mo.mermaid(graph.get_graph().draw_mermaid())
    return graph_viz, selected_model_name


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### UTILS
    ---
    """)
    return


@app.cell(hide_code=True)
def _(
    BaseMessage,
    ChatGoogleGenerativeAI,
    END,
    HumanMessage,
    START,
    StateGraph,
    TypedDict,
    os,
    pl,
):
    # ------------ LOADING DATAFRAME ------------#
    def load_csv_from_bytes(data: bytes) -> pl.DataFrame:
        """Load CSV data from bytes into a polars DataFrame.

        Args:
            data: Byte content of the CSV file.

        Returns:
            A polars DataFrame containing the CSV data.

        Raises:
            ValueError: If the data is empty.
        """
        if not data or len(data) == 0:
            raise ValueError("CSV data is empty")

        return pl.read_csv(data)


    # ------------ LANGGRAPH AGENT ------------#
    # Class to define the agent memory
    class AgentState(TypedDict):
        messages: list[BaseMessage]

    # Build langgrah agent
    def get_agent_graph(model_name: str, llm=None):
        """Build and return the LangGraph agent graph.

        Args:
            model_name: Name of the Google model to use.
            llm: Optional LLM instance. If None, creates ChatGoogleGenerativeAI.

        Returns:
            The compiled LangGraph graph.
        """
        if llm is None:
            llm = ChatGoogleGenerativeAI(model=model_name)

        def call_model(state: AgentState):
            response = llm.invoke(state["messages"])
            return {"messages": [response]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", call_model)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        return workflow.compile()

    # Given prompt replies back to agent
    def run_agent(prompt: str, model_name: str, llm=None) -> str:
        """Run the LangGraph agent with the given prompt.

        Args:
            prompt: The user's question or command.
            model_name: Name of the Google model to use.
            llm: Optional LLM instance for testing.

        Returns:
            The agent's response as a string.
        """
        # Load the API KEY if we are creating the LLM
        if llm is None and not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment.")

        # Create the langgraph
        app = get_agent_graph(model_name, llm=llm)
        # Run the model
        inputs = {"messages": [HumanMessage(content=prompt)]}
        result = app.invoke(inputs)
        return result["messages"][-1].content


    # ------------ GOOGLE GENAI MODELS ------------#
    def list_supported_models() -> list:
        """List supported Google Generative AI models and their metadata.

        Queries the Google Generative AI API to retrieve available models that support
        content generation. It parses model capabilities (multimodal vs text-only)
        and limits to provide a structured overview.

        Returns:
            A list of dictionaries containing model metadata (Name, Display Name,
            Input/Output Limits, Capabilities, and Description).

        Raises:
            ValueError: If GOOGLE_API_KEY is not found in environment.
        """
        import google.generativeai as genai

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment.")
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

        models_data = []
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                # Determine capabilities based on methods and description
                capabilities = []
                if "generateContent" in m.supported_generation_methods:
                    if (
                        "1.5" in m.name
                        or "flash" in m.name.lower()
                        or "pro" in m.name.lower()
                    ):
                        capabilities.append("Multimodal (Text/Image/Video/Audio)")
                    else:
                        capabilities.append("Text Generation")

                if "embedContent" in m.supported_generation_methods:
                    capabilities.append("Embeddings")

                models_data.append(
                    {
                        "Name": m.name,
                        "Display Name": m.display_name,
                        "Input Token Limit": m.input_token_limit,
                        "Output Token Limit": m.output_token_limit,
                        "Capabilities": ", ".join(capabilities),
                        "Description": m.description,
                    }
                )
        return models_data

    return (
        get_agent_graph,
        list_supported_models,
        load_csv_from_bytes,
        run_agent,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### TESTS
    ---
    """)
    return


@app.cell(hide_code=True)
def _():
    import pytest
    from unittest.mock import patch, MagicMock

    return (MagicMock,)


@app.cell(hide_code=True)
def _(MagicMock, load_csv_from_bytes, pl, run_agent):
    class TestDataIngestion:
        """Tests for Story 1.1: Data Ingestion Interface"""

        @staticmethod
        def test_load_csv_from_bytes_returns_polars_dataframe():
            """Given CSV byte data, when loaded, then should return a polars DataFrame"""
            # CSV Bytes data
            csv_data = b"name,age,city\nAlice,30,NYC\nBob,25,LA"

            result = load_csv_from_bytes(csv_data)

            assert isinstance(result, pl.DataFrame)
            assert result.height == 2
            assert result.columns == ["name", "age", "city"]

    class TestAgent:
        """Tests for the LangGraph Agent"""

        @staticmethod
        def test_run_agent_returns_response():
            """Given a prompt and mock LLM, when run_agent is called, then it should return a string response"""
            # Mock LLM instance
            mock_llm = MagicMock()

            from langchain_core.messages import AIMessage
            mock_llm.invoke.return_value = AIMessage(content="Hello, I am a mock agent!")

            prompt = "Hello, how are you?"
            # We pass the mock_llm directly, bypassing the need for API keys and real requests
            response = run_agent(prompt, "models/gemini-1.5-flash", llm=mock_llm)

            assert isinstance(response, str)
            assert response == "Hello, I am a mock agent!"

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### DEBUGGING
    ---
    """)
    return


if __name__ == "__main__":
    app.run()
