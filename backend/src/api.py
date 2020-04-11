import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drinks_short():
    drinks=Drink.query.all()
    drinks_formatted=[d.short() for d in drinks]
    return jsonify({
        'success':True,
        'drinks':drinks_formatted
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_long(payload):
    drinks=Drink.query.all()
    drinks_formatted=[d.long() for d in drinks]
    return jsonify({
        'success':True,
        'drinks':drinks_formatted
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=["POST"])
@requires_auth('post:drinks')
def drinks_create(payload):
    body = request.get_json()
    new_title= body.get('title')
    new_recipe=body.get('recipe')
    
    if new_title is None or new_recipe is None:
        abort(400)    
    
    drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
    drink.insert()

    return jsonify({
        'success':True,
        'drinks':[drink.long()]
    })



'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=["PATCH"])
@requires_auth('patch:drinks')
def drinks_patch(payload,id):
    drink=Drink.query.get(id)
    if drink is None:
        abort(404)

    try:
        body = request.get_json()
        new_title= body.get('title')
        new_recipe=body.get('recipe')
        if new_title is not None:
            drink.title=new_title
        if new_recipe is not None:
            drink.recipe=json.dumps(new_recipe)
        drink.update()

        return jsonify({
            'success':True,
            'drinks':[drink.long()]
        })
    except:
        abort(422)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=["DELETE"])
@requires_auth('delete:drinks')
def drinks_delete(payload,id):
    drink=Drink.query.get(id)
    if drink is None:
        abort(404)

    try:
        drink.delete()
        return jsonify({
            'success':True,
            'delete':id
        })
    except:
        abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404

@app.errorhandler(400)
def badrequest(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(405)
def methodnotallow(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405

@app.errorhandler(401)
def authentication(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "authentication error"
    }), 401

@app.errorhandler(403)
def permission(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "no permission"
    }), 403