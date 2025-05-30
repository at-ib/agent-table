# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AI Agent project that builds a Python-based system using Google's Gemini Large Language Model. The agent is designed to:

1. Process user queries about finding information and data
2. Use Gemini to identify relevant data sources and files online
3. Download and parse data files (CSV, Excel, JSON)
4. Leverage Gemini's code execution tool to perform data analysis
5. Provide coherent answers based on analysis results

## Architecture

The system follows a modular architecture with clear separation of concerns:

### Core Modules (Planned)

- **`main_orchestrator.py`**: Central control flow that manages the sequence of operations, handles user input, and coordinates between different modules
- **`gemini_interactions.py`**: Interface layer for Gemini API using `google-genai` SDK, including specialized prompting functions for different stages (search strategy, file identification, analysis description, tool-based analysis, result synthesis)
- **`file_handler.py`**: File operations including download, parsing (CSV/Excel/JSON), and data preparation for Gemini's code execution tool
- **`config.py`**: Configuration management including API keys and paths

### Key Workflow

The agent operates through a sequence: User Query → Gemini (Plan & File ID) → Python (File Download/Parse) → Python (Data Preparation) → Gemini (Code Execution Tool Analysis) → Gemini (Result Synthesis) → User Output

## Technology Stack

- **Language**: Python 3.x
- **LLM**: Google Gemini API via `google-genai` Python SDK
- **Data Processing**: pandas, NumPy, openpyxl
- **HTTP**: requests library
- **Environment**: venv or conda

## Development Status

This project is currently in the planning phase. The main planning document is located in `planning/main.md` and outlines a two-phase development approach focusing on core interaction loops and file handling, followed by Gemini tool-based analysis integration.