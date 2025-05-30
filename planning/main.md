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
User Query -> Gemini (Understand & Plan Search/File ID) -> Python (File Download) -> Python (File Read/Parse) -> Python (Prepare Data for Gemini Tool) -> Gemini (Execute Analysis using its Code Execution Tool) -> Gemini (Synthesize Result from Tool Output) -> Output to User.

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

     * `prompt_for_search_strategy(user_query)`: Asks Gemini to refine a user query into effective search terms or identify key information to look for.

     * `prompt_for_file_url(search_results_summary)`: Asks Gemini to analyze search results (summaries/links) and identify the most promising URL for a data file.

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

## 3. Technology Stack

* Programming Language: Python 3.x

* LLM: Google Gemini API, accessed via the `google-genai` Python SDK, leveraging its Code Execution Tool for analysis.

* HTTP Requests: `requests` library (primarily for file downloads, as SDK handles API calls).

* Data Handling: `pandas`, `NumPy`, `openpyxl`.

* Environment Management: `venv` or `conda`.

* Version Control: Git.

## 4. Simplified Phases

### Phase 1: Core Interaction Loop & File Handling (MVP)

Goal: Agent can take a query, get a file URL suggestion from Gemini, download, read, prepare a data preview, and ask Gemini to describe the analysis needed.

1. Setup: Python environment, install `google-genai` package, configure Gemini API access.

2. Implement `gemini_interactions.py`: Basic `get_gemini_response` using the SDK, `prompt_for_search_strategy`.

3. Implement `file_handler.py`: `download_file`, `read_data_file` (CSV initially), and basic `prepare_data_for_gemini_tool` (e.g., get headers and first few rows as string).

4. Implement `main_orchestrator.py` (Initial version):

   * Takes user query.

   * Calls Gemini (via SDK) for search strategy/potential file URL.

   * Calls `download_file`, then `read_data_file`.

   * Calls `prepare_data_for_gemini_tool` to get a preview.

   * Calls Gemini with `prompt_for_data_analysis_description` using the data preview.

   * Prints Gemini's suggested analysis description.

5. Testing: With known public CSV files and SDK integration.

### Phase 2: Gemini Tool-Based Analysis & Result Synthesis

Goal: Agent can instruct Gemini to perform analysis using its code execution tool (via SDK) and synthesize a final answer.

1. Enhance `file_handler.py`: Improve `prepare_data_for_gemini_tool` to serialize data more effectively (e.g., full CSV string for smaller files).

2. Implement `prompt_gemini_for_tool_based_analysis` in `gemini_interactions.py`: This prompt will clearly instruct Gemini to use its code execution tool, using the mechanisms provided by the `google-genai` SDK for tool invocation.

3. Enhance `main_orchestrator.py`:

   * After getting the analysis description (from Phase 1), and preparing the full data (or a suitable reference/chunk), call `prompt_gemini_for_tool_based_analysis`.

   * The response from Gemini (obtained via the SDK) should now include the output from its code execution.

   * Pass this tool output to Gemini using `prompt_for_final_summary`.

   * Present the final synthesized answer.

4. Refine Prompts: Crucial for effective tool invocation and result interpretation when using the SDK.

5. Expand File Types: Add robust Excel and JSON support in `file_handler.py` and ensure `prepare_data_for_gemini_tool` handles them.

6. Error Handling: For SDK API calls involving tool use and parsing their results.

7. Testing: With various data files, query types, and analysis complexities suitable for Gemini's tool, ensuring SDK interactions are correct.

## 5. Key Considerations for AI Coding Agent

* Clear Prompts for Tool Use: Prompts must clearly instruct Gemini (via the SDK) to use its code execution tool and define the desired analysis on the provided data. Specify expected output formats from the tool if possible.

* Data Input to Gemini's Tool: Understand how data needs to be formatted or referenced for Gemini's code execution tool when using the `google-genai` SDK. This might involve passing data directly in the prompt (if small) or using mechanisms provided by the SDK for tool inputs.

* Parsing Tool Output: The output from Gemini's code execution tool (received via the SDK) will need to be parsed and understood by your Python orchestrator, then potentially used in subsequent prompts (e.g., for summarization).

* Iterative Prompt Engineering: Essential for effective tool invocation and getting accurate analytical results via the SDK.

* Security with Gemini's Code Execution Tool: While Gemini's code execution tool is expected to run in a secure, sandboxed environment on Google's side, understand its capabilities and limitations when accessed via the SDK. Ensure that the data provided to the tool is appropriate and that the prompts clearly define the intended operations to prevent unintended actions or data exposure.

* Gemini's Capabilities & Limitations: Continuously check the latest documentation for the Gemini API and the `google-genai` Python SDK, especially regarding tool use, code execution, supported libraries, execution limits (time, memory), data input methods, and output formats. This will inform how you design your prompts and data preparation steps.
