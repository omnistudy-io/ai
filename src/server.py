from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os
import json
import re
from socketserver import ThreadingMixIn

from stores import DocStore, TextStore
from summary import Summary
from qgen import QuestionGeneration
from gpt import GPT
from qtype import *
from videos import VideoFinder

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
        if self.path == '/date':
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
        elif self.path == '/videos':
            print("/videos")
            self.do_videos()

    def json_response(self, ok, code, msg, desc, data = {}):
        """Send a json response with the passed in parameters"""
        response = {"ok": ok, "code": code, "message": msg, "description": desc, "data": data}
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_date(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"<b> Hello World!</b><br>Current date: " + str(datetime.date.today()).encode("utf-8"))

    def do_summarize(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))

        print(post_body['doc_paths'])
        print(post_body['length'])

        docstore = DocStore(post_body['doc_paths'])
        print(docstore.docs)
        chat = Summary(docstore.docs, length=post_body['length'])
        answer = chat.run()['output_text']
        self.json_response(True, 200, "Document(s) summarized succesfully", "", { "answer": answer })

    def do_qgen(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))

        docstore = DocStore(post_body['doc_paths'])
        chat = QuestionGeneration(
            docstore.docs, 
            num_questions=post_body['num_questions'], 
            question_types=[QuestionFactory.create_from_code(code) for code in post_body['question_types']]
        )
        result = chat.run()
        response = result['output_text']
        answer = json.loads(response)
        self.json_response(True, 200, "Document(s) summarized succesfully", "", answer)

    def do_gpt(self):
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))

        docstore = DocStore(post_body['doc_paths'])
        chat = GPT(
            docstore.docs, 
            question=post_body['question']
        )
        response = chat.run()['output_text']
        self.json_response(True, 200, "Question answered succesfully", "", { "answer": response })

    def do_videos(self):
        print("Received new request for videos")
        content_length = int(self.headers['Content-Length'])
        post_body = json.loads(self.rfile.read(content_length))

        description = post_body['description']
        docstore = TextStore("description", description)
        chat = VideoFinder(
            docs=docstore.docs
        )
        response = chat.run()['output_text']
        answer = json.loads(response)
        self.json_response(True, 200, "Videos generated succesfully", "", answer)

class ThreadedServer(ThreadingMixIn, HTTPServer):
    pass

print('Started httpserver on port', port)
server = ThreadedServer(('', port), ServerHandler)

#Wait forever for incoming http requests
server.serve_forever()
