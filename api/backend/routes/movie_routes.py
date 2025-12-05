from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for movie routes
movies = Blueprint("movies", __name__)

# Get all movies with optional filtering by year, genre, and duration
# Example: /movies?year=2016&genre=Action&duration=2
@movies.route("/", methods=["GET"])
def get_all_movies():
    try:
        current_app.logger.info('Starting get_all_movies request')
        cursor = db.get_db().cursor()
        
        # Get query parameters for filtering
        year = request.args.get("year")
        genre = request.args.get("genre")
        duration = request.args.get("duration")
        
        current_app.logger.debug(f'Query parameters - year: {year}, genre: {genre}, duration: {duration}')
        
        # Prepare the Base query
        query = "SELECT * FROM Movies m WHERE 1=1"
        params = []
        
        # Add filters if provided
        if year:
            query += " AND Year = %s"
            params.append(year)
        if genre:
            query += """
            AND m.movieID IN (
              SELECT mg.movieID FROM MovieGenres mg
              JOIN Genres g ON mg.genreID = g.genreID
              WHERE g.name = %s
            )
            """
            params.append(genre)
        if duration:
            query += " AND Duration <= %s"
            params.append(duration)
            
        current_app.logger.debug(f'Executing query: {query} with params: {params}')
        cursor.execute(query, params)
        movies = cursor.fetchall()
        cursor.close()
        
        current_app.logger.info(f'Successfully retrieved {len(movies)} movies')
        return jsonify(movies), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_all_movies: {str(e)}')
        return jsonify({"error": str(e)}), 500
      
      
