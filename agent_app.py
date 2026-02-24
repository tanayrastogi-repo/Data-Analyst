import marimo

__generated_with = "0.20.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Insight-3: Data Analyst Agent
    """)
    return


@app.cell
def _(mo):
    upload = mo.ui.file(label="Upload CSV File", filetypes=[".csv"], kind="area")
    upload
    return (upload,)


@app.cell
def _(load_csv_from_bytes, mo, upload):
    file_content = upload.contents()

    if file_content:
        df = load_csv_from_bytes(file_content)
    
        # We combine the success message and the table into one vertical stack
        output = mo.vstack([
            mo.vstack([
                mo.md("## Loaded Dataframe"), 
                mo.ui.table(df.head())
            ]).callout()
        ])
    else:
        output = mo.md("Please upload a CSV file").callout(kind="warn").center()
    output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Utils
    ---
    """)
    return


@app.cell
def _():
    import polars as pl

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

    return load_csv_from_bytes, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tests
    """)
    return


@app.cell
def _():
    import pytest

    return


@app.cell
def _(load_csv_from_bytes, pl):
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

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
