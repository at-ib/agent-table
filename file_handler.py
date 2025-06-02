"""
File handling module for the AI Agent.
Handles downloading, reading, and preparing data files for analysis.
"""

import os
import json
import requests
import pandas as pd
from urllib.parse import urlparse
from config import DOWNLOAD_PATH


class FileHandler:
    def __init__(self):
        self.download_path = DOWNLOAD_PATH

    def download_file(self, url, save_path=None):
        """
        Download a file from a URL and save it locally.

        Args:
            url (str): URL of the file to download
            save_path (str, optional): Local path to save the file

        Returns:
            str: Path to the downloaded file, or None if failed
        """
        try:
            if not save_path:
                # Generate filename from URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename or "." not in filename:
                    filename = "downloaded_file.csv"
                save_path = os.path.join(self.download_path, filename)

            print(f"Downloading file from: {url}")

            # Download with headers to appear like a browser
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Save the file
            with open(save_path, "wb") as f:
                f.write(response.content)

            print(f"File downloaded successfully to: {save_path}")
            return save_path

        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error downloading file: {e}")
            return None

    def read_data_file(self, file_path):
        """
        Read a data file and return as pandas DataFrame.
        Supports CSV, Excel (XLSX), and JSON files.

        Args:
            file_path (str): Path to the data file

        Returns:
            pandas.DataFrame: The data, or None if failed
        """
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None

            file_ext = os.path.splitext(file_path)[1].lower()

            print(f"Reading file: {file_path}")

            if file_ext == ".csv":
                # Try different encodings for CSV files
                encodings = ["utf-8", "latin-1", "cp1252"]
                for encoding in encodings:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding)
                        print(f"Successfully read CSV with {encoding} encoding")
                        return df
                    except UnicodeDecodeError:
                        continue
                print("Failed to read CSV with any encoding")
                return None

            elif file_ext in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
                print("Successfully read Excel file")
                return df

            elif file_ext == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Try to convert to DataFrame
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                elif isinstance(data, dict):
                    # If it's a dict, try to find the main data array
                    for key, value in data.items():
                        if isinstance(value, list) and len(value) > 0:
                            df = pd.DataFrame(value)
                            break
                    else:
                        # If no list found, convert the dict itself
                        df = pd.DataFrame([data])
                else:
                    print("JSON structure not suitable for DataFrame conversion")
                    return None

                print("Successfully read JSON file")
                return df

            else:
                print(f"Unsupported file format: {file_ext}")
                return None

        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def prepare_data_for_gemini_tool(self, data_frame, max_size_mb=1):
        """
        Prepare data for Gemini's code execution tool.
        Returns a preview of the data suitable for analysis description.

        Args:
            data_frame (pandas.DataFrame): The data to prepare
            max_size_mb (float): Maximum size in MB for data preview

        Returns:
            str: Formatted data preview
        """
        try:
            if data_frame is None or data_frame.empty:
                return "No data available"

            # Get basic info about the dataset
            info = []
            info.append(f"Dataset shape: {data_frame.shape[0]} rows, {data_frame.shape[1]} columns")
            info.append(f"Column names: {list(data_frame.columns)}")

            # Get data types
            info.append("\nColumn types:")
            for col, dtype in data_frame.dtypes.items():
                info.append(f"  {col}: {dtype}")

            # Get first few rows
            info.append("\nFirst 5 rows:")
            preview_rows = data_frame.head().to_string()
            info.append(preview_rows)

            # Get basic statistics for numeric columns
            numeric_cols = data_frame.select_dtypes(include=["number"]).columns
            if len(numeric_cols) > 0:
                info.append("\nBasic statistics for numeric columns:")
                stats = data_frame[numeric_cols].describe().to_string()
                info.append(stats)

            # Check for missing values
            missing = data_frame.isnull().sum()
            if missing.any():
                info.append("\nMissing values:")
                for col, count in missing.items():
                    if count > 0:
                        info.append(f"  {col}: {count} missing")

            return "\n".join(info)

        except Exception as e:
            print(f"Error preparing data for Gemini: {e}")
            return f"Error processing data: {str(e)}"
