# OmniStudy AI
This is the AI module of OmniStudy. It is responsible for the following tasks:
- Generating questions from a given text
- Generating answers to questions from a given text
- Generating summaries of a given text

## Running
Make sure you have Docker Desktop installed. Then, run the following command:
```bash
./run_docker.sh
```

You may have set executable permissions for the script:
```bash
chmod +x run_docker.sh
```

The server will then run on `localhost:8001`.

## API Documentation

### Generate questions
<details>
    <summary><code>POST</code> <code>/qgen</code></summary>

#### Headers
> | name | type | description | 
> | ---- | ----- | ----------- |
> | x-access-token | string | JWT token | 

#### Parameters (JSON)
> | name | type | description | 
> | ---- | ----- | ----------- |
> | doc_paths | array | List of absolute (.pdf) file paths | 
> | num_questions | integer | Number of questions to generate |
> | question_types | array | List of question types to generate |
<details>

<summary>Question types:</summary>

  * `MCQ`: Multiple Choice Questions
  * `SHORT`: Short Answer Questions
  * `FITB`: Fill in the Blanks
  * `TOF`: True or False Questions
</details>

#### Example
```javascript
axios.post(`${baseUrl}/qgen`, {
    doc_paths: ["/path/to/file.pdf", "/path/to/another/file.pdf"],
    num_questions: 5,
    question_types: ["MCQ", "SHORT"]
}, {
    headers: {
        "x-access-token": "your-jwt-token"
    }
}).then(...).catch(...);
```
</details>


### Summarize documents
<details>
    <summary><code>POST</code> <code>/summarize</code></summary>

#### Headers
> | name | type | description | 
> | ---- | ----- | ----------- |
> | x-access-token | string | JWT token | 

#### Parameters (JSON)
> | name | type | description | 
> | ---- | ----- | ----------- |
> | doc_paths | array | List of absolute (.pdf) file paths | 
> | length | integer | Length of the summary [Maximum: 400] |

#### Example
```javascript
axios.post(`${baseUrl}/summarize`, {
    doc_paths: ["/path/to/file.pdf", "/path/to/another/file.pdf"],
    length: 200
}, {
    headers: {
        "x-access-token": "your-jwt-token"
    }
}).then(...).catch(...);
```
</details>


### General chat
<details>
    <summary><code>POST</code> <code>/summarize</code></summary>

#### Headers
> | name | type | description | 
> | ---- | ----- | ----------- |
> | x-access-token | string | JWT token | 

#### Parameters (JSON)
> | name | type | description | 
> | ---- | ----- | ----------- |
> | doc_paths | array | List of absolute (.pdf) file paths | 
> | question | string | The question to ask given the context |

#### Example
```javascript
axios.post(`${baseUrl}/gpt`, {
    doc_paths: ["/path/to/file.pdf", "/path/to/another/file.pdf"],
    question: "Tell me about the documents..."
}, {
    headers: {
        "x-access-token": "your-jwt-token"
    }
}).then(...).catch(...);
```
</details>