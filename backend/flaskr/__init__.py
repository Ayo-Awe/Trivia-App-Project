import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def format_categories(categories):
    result = {}
    for category in categories:
        category = category.format()
        result[category["id"]] = category["type"]
    return result


# paginate questions
def paginate_questions(request,questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        all_questions = [question.format() for question in questions]
        current_questions = all_questions[start:end]

        return current_questions
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )

        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST,DELETE,OPTIONS"
        )

        return response

    """

    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/api/v1/categories", methods=["GET"])
    def get_all_categories():

        # get all categories from database
        categories = Category.query.all()
        #format each category
        formatted_categories = format_categories(categories)

        # return json response with categories
        return jsonify({
            "success":True,
            "categories":formatted_categories
        })


    @app.route("/api/v1/questions", methods=["GET"])
    def get_paginated_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        page = request.args.get("page", 1, type=int)
        formatted_categories = format_categories(categories)

        

        all_questions = [question.format() for question in questions]
        current_questions = paginate_questions(request,questions)

        if(len(current_questions)==0 and page != 1):
            abort(404)

        return jsonify({
            "success":True,
            "total_questions":len(all_questions),
            "questions":current_questions,
            "categories": formatted_categories,
            "current_category": None
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/api/v1/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.get(id)
            if question == None:
                abort(404)

            # delete question from database
            question.delete()

            return (jsonify({
                "success":True,
                "deleted":id,
            }))

        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.


    """

    @app.route("/api/v1/questions", methods =["POST"])
    def create_new_questions():
        body = request.get_json()
        page = request.args.get("page", 1, type=int)

        question = body.get("question",None)
        answer = body.get("answer",None)
        category = body.get("category",None)
        difficulty = body.get("difficulty",None)
        search = body.get("searchTerm",None)

        try:
            if search:
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(search))).all()
                formatted_questions = paginate_questions(request,questions)

                if(len(formatted_questions)==0 and page != 1):
                    abort(404)
                #print(for)

                return jsonify({
                    "success":True,
                    "questions":formatted_questions,
                    "total_questions":len(questions),
                    "current_category": None
                })
            else:
                if (question=="") or (answer == "") or (category == None) or (difficulty == None):
                    abort(400)

                # create a new question object
                new_question = Question(question=question,answer=answer,category=category,difficulty=difficulty)

                # commit new question to the database
                new_question.insert()

                return jsonify({
                "success":True, 
                })

        except Exception as e:
            code = sys.exc_info()[1].code
            if code == 400:
                abort(400)
            else :
                abort(422)



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route("/api/v1/categories/<int:category_id>/questions",methods=["GET"])
    def get_question_by_category(category_id):
        category = Category.query.get(category_id)
        page = request.args.get("page", 1, type=int)

        if category == None:
            abort(404)

        questions = Question.query.filter(Question.category==category_id).all()
        formatted_questions = paginate_questions(request,questions)

        if(len(formatted_questions)==0 and page != 1):
            abort(404)

        return jsonify({
            "success": True,
            "questions": formatted_questions,
            "total_questions": len(questions),
            "current_category": category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route("/api/v1/quizzes",methods = ["POST"])
    def get_quizzes():

        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions",None)
            quiz_category = body.get("quiz_category",None)
            questions = []
            
            # if quiz category not specified get all questions else get question in category  
            if (quiz_category is  None):
                questions = Question.query.all()

            elif quiz_category["id"] ==  0:
                
                questions = Question.query.all()

            else:
                questions = Question.query.filter(Question.category==quiz_category["id"]).all()
                
            question_pool = []

            for que in questions:
                if que.id not in previous_questions:
                    question_pool.append(que)


            if(len(question_pool) == 0):
                random_question = None
            else:
                rand_index = random.randint(0,len(question_pool)-1)
                random_question = question_pool[rand_index].format()

            return jsonify({
                "success":True,
                "question":random_question,
            })
        except:
            print(sys.exc_info())
            abort(422)

            

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def resource_not_found(error):
        return ( 
            jsonify({"success": False,"error": 404,"message": "resource not found"})
            ,404,
            )

    @app.errorhandler(400)
    def bad_request(error):
        return ( 
            jsonify({"success": False,"error": 400,"message": "bad request"})
            ,400,
            )
    
    @app.errorhandler(422)
    def unproccessable_request(error):
        return ( 
            jsonify({"success": False,"error": 422,"message": "unprocessable request"})
            ,422,
            )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return ( 
            jsonify({"success": False,"error": 405,"message": "method not allowed"})
            ,405,
            )

    
    @app.errorhandler(500)
    def internal_server_error(error):
        return ( 
            jsonify({"success": False,"error": 500,"message": "internal server error"})
            ,500,
            )
    return app

