# Imports
import json
from chat import Chat
from stores import TextStore

class VideoFinder(Chat):
    def __init__(self, docs):
        prompt_template = """
            Given the following description for an assignment:
            {context}
            Find the most relevant YouTube videos for this assignment. Please return the results in a json array format with the following fields title: string, url: string, publisher: string.
        """
        super().__init__(prompt_template, docs)
    

# Example usage
if __name__ == "__main__":
    docs = TextStore("description", "Create a distributed hash table using the Chord protocol in Java RMI.").docs
    finder = VideoFinder(docs)
    print(finder.run()['output_text'])