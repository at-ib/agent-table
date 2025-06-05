"""
Gemini API interactions module for the AI Agent.
Handles communication with Google's Gemini LLM via the google-genai SDK.
"""

import re
import google.genai as genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import requests
from config import GEMINI_API_KEY


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = "gemini-2.0-flash"
        self.google_search_tool = Tool(
            google_search=GoogleSearch()
        )

    def get_gemini_response(self, prompt_text, context_data=None, use_search=False):
        """
        Send a prompt to Gemini and get response.

        Args:
            prompt_text (str): The instruction or question for Gemini
            context_data (str, optional): Additional context data
            tools_config (dict, optional): Configuration for tool usage
            use_search (bool): Whether to enable Google Search tool

        Returns:
            str: Gemini's response text
        """
        try:
            if context_data:
                full_prompt = f"{prompt_text}\n\nContext:\n{context_data}"
            else:
                full_prompt = prompt_text

            config = GenerateContentConfig(
                response_modalities=["TEXT"],
            )
            
            if use_search:
                config.tools = [self.google_search_tool]

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=full_prompt,
                config=config
            )
            return response
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return None

    def prompt_for_search_strategy(self, user_query):
        """
        Ask Gemini to refine a user query into a prompt that is likely to provide a link to the right data table.

        Args:
            user_query (str): The original user query

        Returns:
            str: Gemini's suggested search strategy
        """
        prompt = f"""
        You are an AI assistant helping to prompt an LLM to find data files for analysis. 
        
        User query: "{user_query}"
        
        Please create a prompt that will help find relevant data files. The LLM that will be prompted is Gemini and
        it will be using the Google Search tool to search the web if it thinks that search is necessary.

        The prompt should be in the form of a question that is likely to lead to a data file.
        """

        return self.get_gemini_response(prompt)

    def prompt_for_web_links(self, search_strategy):
        """
        Ask Gemini to search for data which should return URLs which are entry points to finding the data by traversing links.

        Args:
            search_strategy (str): The search strategy to use

        Returns:
            str: Gemini's search results and discovered URLs
        """
        prompt = f"""
        Using the following search strategy, find web pages that might lead to data files:
        
        Search strategy:
        {search_strategy}
        
        Please:
        1. Search for relevant web pages
        2. Identify pages that might contain links to data files
        3. Note any data repositories, government sites, or research databases mentioned
        4. List the most promising URLs that could lead to downloadable data
        
        Focus on finding entry points that might contain links to actual data files.
        """

        return self.get_gemini_response(prompt, use_search=True)

    def prompt_for_file_url(self, user_query, web_content):
        """
        Ask Gemini to analyze web content and identify the most promising URL to follow to find a data file.

        Args:
            web_content (str): The web content and URLs discovered

        Returns:
            str: Gemini's analysis and recommended file URL
        """
        prompt = f"""
        You are browsing the web in order to answer the question '{user_query}'. 
        To answer the question you must find the most appropriate data file in CSV or XLSX format. You have reached the 
        page with the following content. You can either follow a link to another page or download a file from the page.
        Return the URL of the file you would choose to download, or the link you would choose to follow next in order to
        look for a data file.
        
        Web content:
        {web_content}
        
        Return just the URL if you find a good match, or explain what additional information is needed.
        """

        return self.get_gemini_response(prompt)

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

        response = self.get_gemini_response(prompt)
        return response.text if response else None

    def prompt_gemini_for_tool_based_analysis(self, prepared_data_input, analysis_description, user_query):
        """
        Instruct Gemini to use its code execution tool to perform the described analysis.

        Args:
            prepared_data_input (str): The data to analyze
            analysis_description (str): Description of the analysis to perform
            user_query (str): Original user query

        Returns:
            str: Results of the analysis
        """
        prompt = f"""
        Perform the following analysis on the provided data:
        
        User query: "{user_query}"
        
        Analysis description:
        {analysis_description}
        
        Data to analyze:
        {prepared_data_input}
        
        Please:
        1. Write and execute the necessary code to perform the analysis
        2. Show the results of the analysis
        3. Explain any important findings or patterns
        
        Use Python with pandas for data manipulation and analysis.
        """

        response = self.get_gemini_response(prompt)
        return response.text if response else None

    def prompt_for_final_summary(self, tool_analysis_result, user_query):
        """
        Ask Gemini to synthesize the analysis results into a user-friendly answer.

        Args:
            tool_analysis_result (str): Results from the tool-based analysis
            user_query (str): Original user query

        Returns:
            str: Final summary of the analysis
        """
        prompt = f"""
        Create a user-friendly summary of the analysis results:
        
        Original query: "{user_query}"
        
        Analysis results:
        {tool_analysis_result}
        
        Please provide:
        1. A clear answer to the user's query
        2. Key findings and insights
        3. Any important caveats or limitations
        4. Suggestions for further analysis if relevant
        
        Make the summary easy to understand and directly address the user's original question.
        """

        response = self.get_gemini_response(prompt)
        return response.text if response else None

    def extract_urls(self, web_content):
        """
        Extract URLs from web content returned by Gemini. Gemini returns urls in markdown format [url_label](url).
        
        Args:
            web_content (str): The web content containing markdown formatted URLs
            
        Returns:
            list[str]: List of URLs without their labels
        """
        url_matches = re.findall(r'\[(.*?)\]\((.*?)\)', web_content)
        return [url for _, url in url_matches]


def main():
    gemini_client = GeminiClient()
    user_query = "What is the female population of England aged 40-45"
    print(f"User query: {user_query}")
    search_strategy = gemini_client.prompt_for_search_strategy(user_query)
    print("Search strategy:")
    print(search_strategy.text)
    web_links = gemini_client.prompt_for_web_links(search_strategy.text)
    print("Web links:")
    print(web_links.text)
    urls = gemini_client.extract_urls(web_links.text)
    print("URLs:")
    print(urls)
    url = urls[0]
    print(f"URL: {url}")
    web_content = requests.get(url).text
    print("Web content:")
    print(web_content)
    file_url = gemini_client.prompt_for_file_url(user_query, web_content)
    print("File URL:")
    print(file_url.text)

if __name__ == "__main__":
    main()