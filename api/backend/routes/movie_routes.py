from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for filmfinder routes
filmfinder = Blueprint("filmfinder", __name__)

# Get all movies with optional filtering by year, genre, and duration
# Example: /filmfinder/movies?year=2016&genre=Action
@filmfinder.route("/movies", methods=["GET"])
def get_all_movies():
    try:
        current_app.logger.info('Starting get_all_movies request')
        cursor = db.get_db().cursor()
        
        # Get query parameters for filtering
        
    except Error as e:
        current_app.logger.error(f'Database error in get_all_movies: {str(e)}')
        return jsonify({"error": str(e)}), 500