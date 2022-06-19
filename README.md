# UDACITRIVIA - The Trivia App

This project is a trivia game designed by Udacity to test students knowledge of API documentation and development. It is the final project for Course 2 of the Fullstack Nanodegree. This project aims to test students knowledge of API development, testing, and documentation while ensuring that students follow HTTP and API development best practices.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

Before starting this project, you should already have Python3,
pip and node installed on your local machines. Pipenv is also recommended to help with virtual environments.

#### Backend

From the backend folder run `pip install requirements.txt`.

If you have pipenv installed, you can use `pipenv install -r requirements.txt` instead of `pip`. This would create a virtual environment in your backend folder and install the project dependencies.

All required packages are provided in the requirements file.

To start the application run the following commands in the backend directory:

On windows cmd

```cmd
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

On windows powershell

```powershell
$env: FLASK_APP="flaskr"
$env: FLASK_ENV="development"
flask run
```

bash

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

The above commands accomplish the following:

- `FLASK_APP=flaskr` command specifies the location of our `__init__.py` file for our application.
- `FLASK_ENV` lets us work in development mode which restarts the server whenever changes are made and shows an interactive debugger in the console.
- `flask run` starts the application

For more information check out the [flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to get started:

```cmd
npm i
npm start
```

By default, the frontend runs on `http://localhost:3000`

### Tests

In order to run the tests navigate into the backend folder and run the following commands:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

If you're running the tests for the first time, leave out the dropdb command.

## API Reference

### Getting Started

- Base URL: This project can only be run locally for now. The backend app is hosted at `http://127.0.0.1:5000/api/v1/` by default. This is set as a proxy in the fronted configuration.

- Authentication: This version of the application doesn't require authentication or API keys.

### Error Handling

All errors are returned as JSON objects in the following format:

```Json
{
    "success": false,
    "error": 404,
    "message": "resource not found"
}
```

The API returns four types of errors for failed requests:

| Error | Description           |
| ----- | --------------------- |
| `400` | Bad Request           |
| `404` | Resource Not Found    |
| `405` | Method Not Allowed    |
| `422` | Unprocessable Request |
| `500` | Internal Server Error |

### Endpoints

#### **GET** /questions

- General:

  - Returns a list question objects, category objects, success value, current_category and total number of questions.
  - Results are paginated in groups of 10. To access different pages, specify page as a query parameter, starting from 1. The default value of page is 1.

- Sample: `curl --location --request GET "http://127.0.0.1:5000/api/v1/questions?page=2"`

```JSON
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### **POST** /questions

- General: Creates a new question based on the submitted question, answer, category and difficulty and returns only a success value.

- Sample: ` curl --location --request POST "http://127.0.0.1:5000/api/v1/questions" --header "Content-Type: application/json" --data-raw "{ \"question\": \"How old is the President of Nigeria\", \"answer\": \"75\", \"difficulty\": 3, \"category\": 2}"`

```JSON
{
  "success": true
}
```

- Search: If a searchTerm is specified, rather than creating a new question, it returns all questions where the searchTerm is a substring of the question. The questions returned are also paginated

- `curl --location --request POST "http://127.0.0.1:5000/api/v1/questions" --header "Content-Type: application/json" --data-raw "{\"searchTerm\":\"who\"}"`

```JSON
"current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### **DELETE** /questions/{id}

- General: Deletes question with the specified id and returns the id of the deleted question and a success value
- `curl --location --request DELETE "http://127.0.0.1:5000/api/v1/questions/2"`

```JSON
{
  "success":true,
  "deleted":2
}
```

#### **GET** /categories

- General: returns an object or dictionary with key of category-id and value of category-type and a success value.
- `curl --location --request GET "http://127.0.0.1:5000/api/v1/categories"`

```JSON
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### **GET** /categories/{id}/questions

- General: It returns all the questions in a given category, total number of questions, current category and a success value. The id refers to the id of the category. The questions are paginated.
- `curl --location --request GET "http://127.0.0.1:5000/api/v1/categories/5/questions"`

```JSON
{
    "current_category": "Entertainment",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### **POST** /quizzes

- General: The quizzes endpoint requires a list of previous questions and an optional quiz category parameter. It returns a new question and a success value. The returned question is not contained in previous questions and is from the specified category (if category is specified).

The expected format for quiz category is shown below

```JSON
{
  "id" : 2,
  "type" : "Art"
}
```

- `curl --location --request POST "http://127.0.0.1:5000/api/v1/quizzes" --header "Content-Type: application/json" --data-raw "{ \"previous_questions\": [2,3,5,4], \"quiz_category\":{\"id\":2, \"type\":\"Art\"} }"`

```JSON
{
    "question": {
        "answer": "75",
        "category": 2,
        "difficulty": 3,
        "id": 41,
        "question": "How old is the President of Nigeria"
    },
    "success": true
}
```

## Deployment N/A

## Authors

- Awe Ayomidipupo
- Udacity

## Acknowledgements

ALX-T, Udacity Team and most importantly God!
