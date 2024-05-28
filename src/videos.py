# Imports
import json
from chat import Chat
from stores import TextStore

class VideoFinder(Chat):
    def __init__(self, docs):
        prompt_template = """
            Given the following description for an assignment:
            {context}
            Search YouTube to find the 3 most relevant videos for this assignment. Return only the video URLs in an array of strings.
        """
        super().__init__(prompt_template, docs)
    

# Example usage
if __name__ == "__main__":
    docs = TextStore("description", "Create a NodeJS API from scratch.").docs
    finder = VideoFinder(docs)
    print(finder.run()['output_text'])