from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os
import json
import re
from socketserver import ThreadingMixIn

from stores import DocStore
from summary import Summary
from qgen import QuestionGeneration
from gpt import GPT
from qtype import *

from chat2 import Chat
from processor import FileUpload
from qgen import Generator

# Get the port from env
port = int(os.environ.get('PORT'))
openai_api_key = os.environ.get('OPENAI_API_KEY')
# Get the port from env
port = int(os.environ.get('PORT'))
openai_api_key = os.environ.get('OPENAI_API_KEY')

class ServerHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == '/time':
            self.do_time()
        elif self.path == '/date':
            self.do_date()

    def do_POST(self):
        if self.path == '/process':
            self.do_process()
        elif self.path == '/summarize':
            self.do_summarize()
        elif self.path == '/qgen':
            self.do_qgen() 
        elif self.path == '/gpt':
            self.do_gpt() 

    def json_response(self, ok, code, msg, desc, data = {}):
        """Send a json response with the passed in parameters"""
        response = {"ok": ok, "code": code, "message": msg, "description": desc, "data": data}
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_time(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"<b> Hello World, API Key= " + os.environ.get("OPENAI_API_KEY") + "!</b><br>Current time: " + str(datetime.datetime.now()).encode("utf-8"))

    def do_date(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"<b> Hello World!</b><br>Current date: " + str(datetime.date.today()).encode("utf-8"))
    def do_upload(self):
        pass
    def do_summarize(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))

        print(post_body['doc_paths'])
        print(post_body['length'])

        docstore = DocStore(post_body['doc_paths'])
        chat = Summary(docstore.docs, length=post_body['length'])
        answer = chat.run()['output_text']
        self.json_response(True, 200, "Document(s) summarized succesfully", "", { "answer": answer })

    def do_qgen(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))
        text = post_body['text']
        num_questions = post_body['num_questions']
        topic_query = post_body['query']
        qgen = Generator()
        response = qgen.run(text_name=text,num_questions=num_questions,topic_query=topic_query)
        self.json_response(True, 200, "Question answered succesfully", "", { "answer": response })
    def do_gpt(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))
        text = post_body['text']
        query = post_body['query']
        gpt = Chat()
        gpt.init_all(text)
        response = gpt.run(text,post_body)
        self.json_response(True, 200, "Question answered succesfully", "", { "answer": response })

    def do_embedding(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))
        textbook_name = post_body['textbook_name']
        file_path = post_body['file_path']   
        embedder = FileUpload()
        embedder.upload(path=file_path,textbook_name=textbook_name)

class ThreadedServer(ThreadingMixIn, HTTPServer):
    pass

print('Started httpserver on port', port)
print('Started httpserver on port', port)
server = ThreadedServer(('', port), ServerHandler)

#Wait forever for incoming http requests
server.serve_forever()