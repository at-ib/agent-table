"""
Gemini API interactions module for the AI Agent.
Handles communication with Google's Gemini LLM via the google-genai SDK.
"""

import google.genai as genai
from config import GEMINI_API_KEY


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def get_gemini_response(self, prompt_text, context_data=None, tools_config=None):
        """
        Send a prompt to Gemini and get response.

        Args:
            prompt_text (str): The instruction or question for Gemini
            context_data (str, optional): Additional context data
            tools_config (dict, optional): Configuration for tool usage

        Returns:
            str: Gemini's response text
        """
        try:
            if context_data:
                full_prompt = f"{prompt_text}\n\nContext:\n{context_data}"
            else:
                full_prompt = prompt_text

            response = self.client.models.generate_content(model="gemini-1.5-flash", contents=full_prompt)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return None

    def prompt_for_search_strategy(self, user_query):
        """
        Ask Gemini to refine a user query into effective search terms or identify key information.

        Args:
            user_query (str): The original user query

        Returns:
            str: Gemini's suggested search strategy and potential file URL
        """
        prompt = f"""
        You are an AI assistant helping to find data files for analysis. 
        
        User query: "{user_query}"
        
        Please suggest:
        1. Effective search terms to find relevant data files
        2. Types of data sources that might contain this information
        3. If possible, suggest a specific URL to a publicly available CSV file that contains relevant data
        
        Focus on finding actual downloadable data files (CSV, Excel, JSON) rather than web pages.
        If you know of specific government datasets, research databases, or public data repositories that might have this data, mention them.
        
        Provide your response in a structured format with clear sections for search terms, data sources, and specific URLs if known.
        """

        return self.get_gemini_response(prompt)

    def prompt_for_file_url(self, search_results_summary):
        """
        Ask Gemini to analyze search results and identify the most promising URL for a data file.

        Args:
            search_results_summary (str): Summary of search results

        Returns:
            str: Gemini's analysis and recommended file URL
        """
        prompt = f"""
        You are helping to identify the best data file from search results.
        
        Search results summary:
        {search_results_summary}
        
        Please analyze these results and:
        1. Identify the most promising URL for downloading a data file (CSV, Excel, JSON)
        2. Explain why this URL is the best choice
        3. Provide the exact URL that should be used for downloading
        
        Focus on files that are:
        - Directly downloadable (not requiring registration)
        - In a structured format (CSV, Excel, JSON)
        - From reliable sources
        - Relevant to the original query
        
        Return just the URL if you find a good match, or explain what additional information is needed.
        """

        return self.get_gemini_response(prompt, search_results_summary)

    def prompt_for_data_analysis_description(self, data_preview, user_query):
        """
        Show Gemini a preview of data and ask it to describe needed analysis.

        Args:
            data_preview (str): Preview of the data (headers and first few rows)
            user_query (str): Original user query

        Returns:
            str: Gemini's description of the analysis needed
        """
        prompt = f"""
        You are analyzing data to answer a user's query.
        
        Original user query: "{user_query}"
        
        Data preview:
        {data_preview}
        
        Based on this data structure and the user's query, please describe:
        1. What specific calculations or analysis should be performed
        2. Which columns are most relevant
        3. What steps would be needed to answer the user's question
        4. What the expected output format should be
        
        Be specific about the analytical approach and any data transformations needed.
        """

        return self.get_gemini_response(prompt, data_preview)
