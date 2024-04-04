# OmniStudy AI
This is the AI module of OmniStudy. It is responsible for the following tasks:
- Generating questions from a given text
- Generating answers to questions from a given text
- Generating summaries of a given text

## Running
Make sure you have Docker Desktop installed. Then, run the following command:
```bash
./run_docker
```

You may have set executable permissions for the script:
```bash
chmod +x run_docker
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

#### Responses
> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ ok: boolean, message: string, data: { answer: string }`          |

</details>