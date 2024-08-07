#!/usr/bin/env python3
# server/app.py

# Standard library imports

# Remote library imports
from flask import Flask, request, jsonify, session, make_response, render_template
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate


# from flask_jwt_extended import create_access_token, jwt_required
# from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy.exc import IntegrityError

# Add your model imports
from models import User, Book, Library, Bookgenre, Genre, Review
import pytesseract
import base64

# Local imports
from config import app, db, api

# Envioronmental stuff for deployment
# from dotenv import load_dotenv
# load_dotenv()

# Routes Go Here

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

# This is dubious for some reason.
# @app.before_request
# def check_if_logged_in():
#     if not session['user_id']
#         and request.endpoint != 'document_list' :
#         return {'error': 'Unauthorized'}, 401

@app.route('/')
def index():
    return 'Welcome to the GreatReads Server!'

@app.route('/firstbook')
def firstbook():
    book = Book.query.first()
    book_dict = book.to_dict()
    return make_response(book_dict, 200)

# @app.route('/allbooks')
# def allbooks():
#     books = []
#     for book in Book.query.all():
#         book_dict = {
#             "title": book.title,
#             "author": book.author,
#             "cover_id": book.cover_id,
#             "cover_img": book.cover_img,
#             "description": book.description,
#             "edition_count": book.edition_count,
#             "first_publish_year": book.first_publish_year,
#             "genre": book.genre,
#             "olid": book.olid,
#             "reviews": book.reviews,
#             "subject_places": book.subject_places,
#             "subject_times": book.subject_times,
#             "subjects": book.subjects,
#         }
#         books.append(book_dict)
    
#     response = make_response(
#         jsonify(books), 200
#     )

#     return response

@app.route('/books/<int:id>')
def book_by_id(id):
    book = Book.query.filter(Book.id == id).first()
    if book:
        body =  book.to_dict()
        status = 200
    else:
        body = {'message': f'Sorry, Book {id} not found.'}
        status = 404
    return make_response(body, status)

class AllBooks(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Book.query.all()] 
        response = make_response(
            response_dict_list,
            200,
        )
        return response
    
class Login(Resource):
    def get(self):
        pass

    def post(self):
        params = request.json
        user = User.query.filter(User.username == params.get('username')).first()
        if not user:
            return make_response ({"Error": "User not found."}, 401)
        if user.authenticate(params.get('password')):
            session['user_id'] = user.id
            return make_response(user.to_dict(rules=()))  
            # Add Serialization Rules Later
        else:
            return make_response({"Error": "Invalid Password"}, 401)

class CheckSession(Resource):
    def get (self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return { 'message': '401: Not Authorized'}, 401
        
class Signup(Resource):
    def post(self):
        params = request.get_json()
        f_name= params.get('f_name')
        l_name= params.get('l_name')
        username = params.get('username')
        password = params.get('password')
        email = params.get('email')
        image_url = params.get('image_url')
        bio = params.get('bio')
        user = User(
            f_name=f_name,
            l_name=l_name,
            username = username,
            email = email,
            image_url = image_url,
            bio = bio,
        )
        user.password_hash = password
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return make_response(user.to_dict(), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error":"422 Unprocessable Entity", "details": str(e)}, 422)
        
class Logout(Resource):
    def delete(self): # just add this line!
        print("trying to log out here")
        # session['user_id'] = None
        session.pop('user_id', None)
        # return {'message': '204: No Content'}, 204
        return make_response({}, 204)
    
class Home(Resource):
    def get(self):
        pass

class Users(Resource):
    def get(self):
        pass

class UserById(Resource):
    def get(self, id):
        user = db.session.get(User, id)
        if user:
            return make_response(user.to_dict(rules=()), 200)
            # add serialization rules later
        else:
            return make_response({'error': 'User not found'}, 404)
    

class AddBook(Resource):
    def post(self):
        try:
            data = request.json
            booktoadd = Book(
                title= data['title'],
                author= data['author'],
                cover_id= data['cover_id'],
                cover_img= data['cover_img'],
                subjects= data['subjects'],
                subject_places= data['subject_places'],
                subject_times=data['subject_times'],
                edition_count=data['edition_count'],
                first_publish_year=data['first_publish_year'],
                olid=data['olid'],
                average_rating=data['average_rating'],
                description=data['description'],
                genre=data['genre']
            )
            db.session.add(booktoadd)

            # Do something more here to add this book to the user's library? before returning?

            return make_response(booktoadd.to_dict(rules=()), 201)
        
        except Exception as e:
            app.logger.error(f"Error adding Book: {e}")
            return make_response({"error": "Could not add Book", "details": str(e)}, 400)

class Books(Resource):
    def get(self):
        books = Book.query.all()
        book_list = [book.to_dict(rules =()) for book in books]
        return make_response(book_list, 200)

class BookById(Resource):
    def get(self, id):
        book = db.session.get(Book,id)
        if book:
            return make_response(book.to_dict(rules=()), 200)
        else:
            return make_response({'error': 'Sorry, Book not found'}, 404)
    
    def patch(self,id):
        book = db.session.get(Book, id)
        if book:
            params = request.json
            print(params)
            for attr in params:
                setattr(book, attr, params[attr])
            db.session.commit()
            # Do something more here before returing?
            return make_response(book.to_dict(rules = ()), 204)
        else:
            return make_response({'error': 'Sorry, Book not found'}, 404)
    
    def delete(self,id):
        book = db.session.get(Book,id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return make_response({"message": "Book deleted successfully."}, 204)
        else:
            return make_response({"error": "Book not found"}, 404)

# class MyLibrary(Resource):
#     def get(self,id):
#         books = 


api.add_resource(Home, '/')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(AllBooks, '/allbooks')
api.add_resource(Users, '/user')
api.add_resource(UserById, '/user/<int:id>')
api.add_resource(AddBook, '/addbook')
api.add_resource(Books, '/books')
api.add_resource(BookById, '/books/<int:id>')

# api.add_resource(MyLibrary, '/mylibrary')

if __name__ == '__main__':
    app.run(port=5555, debug=True)