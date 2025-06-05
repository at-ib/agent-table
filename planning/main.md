# Project Plan: AI Agent (Gemini-Powered with Tool-Based Analysis)

**Version:** 1.5
**Date:** May 30, 2025

## 1. Project Goal

Develop a Python-based AI agent that uses the Gemini Large Language Model to:

1. Understand user queries related to finding information and data.

2. Leverage Gemini's capabilities to identify relevant information sources and potential data files online.

3. Download identified data files (CSV, Excel, JSON).

4. Read and parse these files.

5. Utilize Gemini to determine necessary calculations or analyses on the data.

6. Leverage Gemini's code execution tool to perform these analyses on the provided data.

7. Provide a coherent answer to the user based on the analysis results from Gemini.

## 2. Core Workflow & Modules

The agent will operate through a sequence of interactions between Python control logic and the Gemini API (via the `google-genai` Python package), including invoking Gemini's code execution tool.

Overall Flow:
User Query -> Gemini (Understand & Plan Search/File ID) -> Python (follow links to find appropriate file) -> Python (File Download) -> Python (File Read/Parse) -> Python (Prepare Data for Gemini Tool) -> Gemini (Execute Analysis using its Code Execution Tool) -> Gemini (Synthesize Result from Tool Output) -> Output to User.

Key Python Modules/Functions to Implement:

1. `main_orchestrator.py` (Control Flow):

   * Manages the overall sequence of operations.

   * Handles user input.

   * Calls Gemini for different reasoning and tool execution steps using functions from `gemini_interactions.py`.

   * Invokes other Python utility functions for file handling and data preparation.

   * Formats and presents the final output synthesized by Gemini.

2. `gemini_interactions.py` (LLM Interface using `google-genai`):

   * Initializes and configures the Gemini client from the `google-genai` package.

   * `get_gemini_response(prompt_text, context_data=None, tools_config=None)`:

     * Constructs the appropriate request structure for the `google-genai` SDK.

     * Sends prompts to the Gemini API using the SDK.

     * Handles API request/response logic, including parsing responses that might indicate tool usage or results from tool execution.

     * `prompt_text`: The specific instruction or question for Gemini.

     * `context_data`: Optional data (e.g., search results summaries, data previews) to provide context.

     * `tools_config`: Configuration for enabling and guiding Gemini's tool use (e.g., specifying the code interpreter) as supported by the SDK.

   * Specific prompting functions for:

     * `prompt_for_search_strategy(user_query)`: Asks Gemini to refine a user query into a prompt that is likely to provide a link to the right data table.

     * `prompt_for_web_content(search_strategy)`: Asks Gemini to search for data which should return URLs which are entry points to finding the data by traversing links.

     * `prompt_for_file_url(web_content)`: Asks Gemini to analyze web content (the result of google searches) and identify the most promising URL to follow to find a data file or the URL for a data file.

     * `prompt_for_data_analysis_description(data_preview, user_query)`: Shows Gemini a preview of the data and the user query, asking it to describe the analysis or calculations needed.

     * `prompt_gemini_for_tool_based_analysis(prepared_data_input, analysis_description, user_query)`: Instructs Gemini (via the SDK) to use its code execution tool to perform the described analysis on the `prepared_data_input`. The `prepared_data_input` might be the data itself (if small enough) or a reference/handle if Gemini's tool can access data contextually. This prompt will specify that the code interpreter tool should be used, according to the SDK's method for enabling tools.

     * `prompt_for_final_summary(tool_analysis_result, user_query)`: Asks Gemini to synthesize the results obtained from its code execution tool into a user-friendly answer.

3. `file_handler.py` (File Operations):

   * `download_file(url, save_path)`:

     * Uses the `requests` library to download a file.

     * Saves the file locally.

     * Includes error handling.

   * `read_data_file(file_path)`:

     * Detects file type (CSV, XLSX, JSON).

     * Uses `pandas` to read CSV and Excel into a DataFrame.

     * Uses `json` module (and `pandas`) for JSON files.

     * Returns data (preferably pandas DataFrame).

     * Handles file reading errors.

   * `prepare_data_for_gemini_tool(data_frame, max_size_mb=1)`:

     * Takes a pandas DataFrame.

     * Converts it into a string format suitable for Gemini's code execution tool input (e.g., CSV string, JSON string).

     * Checks data size; if too large, it might summarize, sample, or indicate that a file reference mechanism (if available with Gemini's tool) should be used.

     * Returns the prepared data string or a reference.

4. `config.py`:

   * Stores API keys (Gemini API key handled securely, typically via environment variables when using the SDK).

   * Download paths, other configurations.

## 3. Steps

1. Implement `gemini_interactions.py`.

2. Implement `file_handler.py`: `download_file`, `read_data_file` (CSV initially), and basic `prepare_data_for_gemini_tool` (e.g., get headers and first few rows as string).

3. Implement `main_orchestrator.py` (Initial version):

   * Takes user query.

   * Calls Gemini (via SDK) for search strategy/potential file URL.

   * Calls `download_file`, then `read_data_file`.

   * Calls `prepare_data_for_gemini_tool` to get a preview.

   * Calls Gemini with `prompt_for_data_analysis_description` using the data preview.

   * Prints Gemini's suggested analysis description.

5. Testing: With known public CSV files and SDK integration.
