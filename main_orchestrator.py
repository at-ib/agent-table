"""
Main orchestrator for the AI Agent.
Manages the overall sequence of operations for Phase 1 implementation.
"""

import sys
from gemini_interactions import GeminiClient
from file_handler import FileHandler


class AIAgent:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.file_handler = FileHandler()

    def process_query(self, user_query):
        """
        Process a user query through the Phase 1 workflow.

        Args:
            user_query (str): The user's question or request

        Returns:
            str: Analysis description from Gemini
        """
        print(f"\n🤖 Processing query: {user_query}")
        print("=" * 50)

        # Step 1: Get search strategy and potential file URL from Gemini
        print("\n📋 Step 1: Getting search strategy from Gemini...")
        search_strategy = self.gemini_client.prompt_for_search_strategy(user_query)

        if not search_strategy:
            return "❌ Failed to get search strategy from Gemini"

        print("✅ Search strategy received:")
        print(search_strategy)

        # Step 2: Extract URL from Gemini's response (simple extraction for Phase 1)
        file_url = self._extract_url_from_response(search_strategy)

        if not file_url:
            print("\n⚠️  No direct URL found in Gemini's response.")
            print("In a full implementation, this would trigger web search.")
            return search_strategy

        print(f"\n📥 Step 2: Attempting to download file from: {file_url}")

        # Step 3: Download the file
        downloaded_file = self.file_handler.download_file(file_url)

        if not downloaded_file:
            return f"❌ Failed to download file from {file_url}"

        # Step 4: Read and parse the file
        print(f"\n📖 Step 3: Reading data file...")
        data_frame = self.file_handler.read_data_file(downloaded_file)

        if data_frame is None:
            return f"❌ Failed to read data from {downloaded_file}"

        print(f"✅ Successfully loaded data with shape: {data_frame.shape}")

        # Step 5: Prepare data preview for Gemini
        print(f"\n🔍 Step 4: Preparing data preview...")
        data_preview = self.file_handler.prepare_data_for_gemini_tool(data_frame)

        # Step 6: Get analysis description from Gemini
        print(f"\n🧠 Step 5: Getting analysis description from Gemini...")
        analysis_description = self.gemini_client.prompt_for_data_analysis_description(data_preview, user_query)

        if not analysis_description:
            return "❌ Failed to get analysis description from Gemini"

        print("\n✅ Analysis description received:")
        print("=" * 50)
        print(analysis_description)
        print("=" * 50)

        return analysis_description

    def _extract_url_from_response(self, response_text):
        """
        Simple URL extraction from Gemini's response.
        In a full implementation, this would be more sophisticated.

        Args:
            response_text (str): Gemini's response text

        Returns:
            str: Extracted URL or None
        """
        import re

        # Look for URLs in the response
        url_pattern = r'https?://[^\s<>"]{2,}'
        urls = re.findall(url_pattern, response_text)

        # Filter for likely data file URLs
        data_extensions = [".csv", ".xlsx", ".xls", ".json"]
        for url in urls:
            for ext in data_extensions:
                if ext in url.lower():
                    return url

        # If no data file URLs found, return the first URL
        return urls[0] if urls else None


def main():
    """
    Main function for testing the Phase 1 implementation.
    """
    print("🚀 AI Agent Phase 1 - Starting...")

    # Check if API key is configured
    try:
        agent = AIAgent()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set your GEMINI_API_KEY in a .env file")
        return

    # Test queries for Phase 1
    test_queries = [
        "What are the population trends in major US cities?",
        "Show me data about global CO2 emissions by country",
        "Find information about stock market performance in 2023",
    ]

    if len(sys.argv) > 1:
        # Use command line argument as query
        user_query = " ".join(sys.argv[1:])
        agent.process_query(user_query)
    else:
        # Interactive mode
        print("\n💡 Enter your query (or type 'quit' to exit):")
        print("Example: 'What are the population trends in major US cities?'")

        while True:
            try:
                user_input = input("\n🔍 Your query: ").strip()

                if user_input.lower() in ["quit", "exit", "q"]:
                    print("👋 Goodbye!")
                    break

                if not user_input:
                    continue

                result = agent.process_query(user_input)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
