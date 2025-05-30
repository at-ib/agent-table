Project Plan: AI Agent (Gemini-Powered)

Version: 1.1
Date: May 30, 2025
1. Project Goal

Develop a Python-based AI agent that uses the Gemini Large Language Model to:

    Understand user queries related to finding information and data.

    Leverage Gemini's capabilities to identify relevant information sources and potential data files online.

    Download identified data files (CSV, Excel, JSON).

    Read and parse these files.

    Utilize Gemini to determine necessary calculations or analyses on the data.

    Execute these analyses (potentially using Python code suggested by Gemini in a safe manner).

    Provide a coherent answer to the user.

2. Core Workflow & Modules

The agent will operate through a sequence of interactions between Python control logic and the Gemini API.

Overall Flow:
User Query -> Gemini (Understand & Plan Search/File ID) -> Python (File Download) -> Python (File Read/Parse) -> Gemini (Determine Analysis) -> Python (Execute Analysis, possibly with Gemini-suggested code) -> Gemini (Synthesize Result) -> Output to User.

Key Python Modules/Functions to Implement:

    main_orchestrator.py (Control Flow):

        Manages the overall sequence of operations.

        Handles user input.

        Calls Gemini for different reasoning steps.

        Invokes other Python utility functions.

        Formats and presents the final output.

    gemini_interactions.py (LLM Interface):

        get_gemini_response(prompt_text, context_data=None):

            Sends prompts to the Gemini API.

            Handles API request/response logic.

            prompt_text: The specific instruction or question for Gemini.

            context_data: Optional data (e.g., search results, file content snippets) to provide context to Gemini.

        Specific prompting functions for:

            prompt_for_search_strategy(user_query): Asks Gemini to refine a user query into effective search terms or identify key information to look for.

            prompt_for_file_url(search_results_summary): Asks Gemini to analyze search results (summaries/links) and identify the most promising URL for a data file.

            prompt_for_data_analysis_steps(data_preview, user_query): Shows Gemini a preview of the data (e.g., headers, first few rows) and the original user query, asking it to outline the analysis steps or calculations needed.

            prompt_for_python_analysis_code(data_preview, analysis_description): (Advanced) Asks Gemini to generate Python (pandas) code to perform the described analysis.

            prompt_for_final_summary(analysis_results, user_query): Asks Gemini to synthesize the analysis results into a user-friendly answer.

    file_handler.py (File Operations):

        download_file(url, save_path):

            Uses the requests library to download a file from a given URL.

            Saves the file to a specified local path.

            Includes error handling for network issues, HTTP errors.

        read_data_file(file_path):

            Detects file type (CSV, XLSX, JSON) based on extension.

            Uses pandas to read CSV and Excel files into a DataFrame.

            Uses the json module (and potentially pandas) to read JSON files.

            Returns the data in a structured format (preferably pandas DataFrame).

            Handles basic file reading errors (e.g., file not found, corrupt file).

    data_analyzer.py (Analysis Execution):

        execute_analysis(data_frame, analysis_instructions_from_gemini):

            Performs predefined pandas operations based on structured instructions from Gemini (e.g., if Gemini says "calculate the sum of 'Sales' column").

        execute_gemini_code(data_frame, python_code_from_gemini): (Requires Strict Security)

            CRITICAL SECURITY NOTE: Executes Python code (presumably pandas operations) suggested by Gemini. This MUST be done in a highly sandboxed and restricted environment to prevent security vulnerabilities. For a simpler agent, this might be limited to very specific, validated operations rather than arbitrary code execution.

            Provides the data_frame as a local variable (e.g., df) to the executed code.

            Returns the result of the code execution (e.g., a new DataFrame, a scalar value).

    config.py:

        Stores API keys (Gemini API key should be handled securely, e.g., via environment variables, not hardcoded).

        Download paths, other configurations.

3. Technology Stack

    Programming Language: Python 3.x

    LLM: Google Gemini API (via google-generativeai Python SDK or direct HTTP requests).

    HTTP Requests: requests library (for file downloads if not handled by a Gemini tool, and for direct Gemini API calls if not using SDK).

    Data Handling: pandas, NumPy, openpyxl.

    Environment Management: venv or conda.

    Version Control: Git.

4. Simplified Phases
Phase 1: Core Interaction Loop & File Handling (MVP)

Goal: Agent can take a query, get a file URL suggestion from Gemini, download, read, and show a preview of the data to Gemini for initial analysis description.

    Setup: Python environment, Gemini API access.

    Implement gemini_interactions.py: Basic get_gemini_response and prompt_for_search_strategy.

    Implement file_handler.py: download_file and read_data_file (for CSV initially).

    Implement main_orchestrator.py (Initial version):

        Takes user query.

        Calls Gemini to get a search strategy/potential file URL (simulating Gemini's search capability for now, or user provides URL).

        Calls download_file.

        Calls read_data_file.

        Calls Gemini with prompt_for_data_analysis_steps, providing a data preview.

        Prints Gemini's suggested analysis steps.

    Testing: With known public CSV files.

Phase 2: Basic Analysis Execution & Refinement

Goal: Agent can execute simple, predefined analyses based on Gemini's suggestions and synthesize a final answer.

    Enhance data_analyzer.py: Implement execute_analysis for a few common, safe operations (e.g., sum, average, count, filter by a single value on a column).

    Enhance main_orchestrator.py:

        After getting analysis steps from Gemini, attempt to map them to functions in execute_analysis.

        Pass results to Gemini using prompt_for_final_summary.

        Present the final summary.

    Refine Prompts: Improve all prompts for clarity and better Gemini responses.

    Expand File Types: Add robust Excel and JSON support in file_handler.py.

    Error Handling: Add more comprehensive error handling throughout.

    Testing: With various data files and query types.

Phase 3: (Optional Advanced) Secure Gemini-Code Execution & Broader Capabilities

Goal: Implement secure execution of Python code suggested by Gemini for more complex analyses.

    Research & Implement Sandboxing: For execute_gemini_code in data_analyzer.py. This is a complex security task.

    Develop prompt_for_python_analysis_code: For Gemini to generate pandas code.

    Integrate Code Execution: Update orchestrator to use this flow if analysis is complex.

    URL Identification from Web Pages: If Gemini's direct URL identification isn't sufficient, implement basic HTML parsing (BeautifulSoup4) in file_handler.py or a new module, guided by Gemini, to find download links on pages.

    Testing: Focus on security and robustness of code execution.

5. Key Considerations for AI Coding Agent

    Clear Prompts: Each call to Gemini needs a well-defined prompt that clearly states the task, the expected output format, and any context.

    Context Window: Be mindful of Gemini's context window limitations when providing data previews or chat history.

    Parsing Gemini's Output: Gemini's responses will be text. Python code will need to parse this text to extract structured information (e.g., a URL, a list of analysis steps, Python code). Requesting JSON or structured output from Gemini can simplify this.

    Iterative Prompt Engineering: Expect to refine prompts multiple times to get the desired behavior from Gemini.

    Security for Code Execution: If allowing Gemini to generate Python code for analysis, this is a major security consideration. The code must be executed in a sandboxed environment with restricted permissions. For a simpler initial agent, avoid direct code execution and rely on Gemini to describe analysis steps that your Python code then implements through predefined, safe functions.

    Gemini's Capabilities: Continuously check the latest capabilities of the Gemini API and any associated tools/functions Google provides, as these might offer more direct ways to achieve search, file understanding, or code execution, potentially simplifying custom Python code.

This simplified plan assumes the AI coding agent (like myself) will be responsible for writing the Python code for the modules described, using Gemini for the "intelligent" parts of the workflow.