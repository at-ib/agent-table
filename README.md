# AI Agent - Gemini-Powered Data Analysis

A Python-based AI agent that uses Google's Gemini Large Language Model to find, download, and analyze data files based on user queries.

## Phase 1 Features (Current)

- **Query Understanding**: Uses Gemini to interpret user queries and suggest data sources
- **File Discovery**: Identifies potential data files (CSV, Excel, JSON) from Gemini's suggestions
- **Data Download**: Downloads files from URLs with proper error handling
- **Data Reading**: Supports CSV, Excel (.xlsx, .xls), and JSON file formats
- **Data Preview**: Generates comprehensive data previews for analysis planning
- **Analysis Description**: Uses Gemini to describe what analysis should be performed

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Run the Agent**:
   ```bash
   # Interactive mode
   python main_orchestrator.py
   
   # Direct query
   python main_orchestrator.py "What are the population trends in major US cities?"
   ```

## Usage Examples

- "What are the population trends in major US cities?"
- "Show me data about global CO2 emissions by country"
- "Find information about stock market performance in 2023"

## Project Structure

- `main_orchestrator.py` - Main control flow and user interface
- `gemini_interactions.py` - Gemini API communication and prompting
- `file_handler.py` - File download, reading, and data preparation
- `config.py` - Configuration and environment setup
- `downloads/` - Directory for downloaded data files (auto-created)

## Current Limitations

- Phase 1 implementation focuses on basic workflow
- Limited to URLs directly suggested by Gemini
- No web search integration yet
- Analysis description only (no actual data analysis)

## Next Steps (Phase 2)

- Integrate Gemini's code execution tool for actual data analysis
- Add web search capabilities for finding data sources
- Implement result synthesis and final answer generation
- Enhanced error handling and data validation