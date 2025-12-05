from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for movie routes
movies = Blueprint("movie", __name__)


# Get all movies with optional filtering by year, genre, and duration
# Example: /movie/movies?year=2016&genre=Action&duration=2
@movies.route("/movies", methods=["GET"])
def get_all_movies():
    try:
        current_app.logger.info("Starting get_all_movies request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        year = request.args.get("year")
        genre = request.args.get("genre")
        duration = request.args.get("duration")

        current_app.logger.debug(
            f"Query parameters - year: {year}, genre: {genre}, duration: {duration}"
        )

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

        current_app.logger.debug(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        movies = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved {len(movies)} movies")
        cursor.close()
        return jsonify(movies), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_all_movies: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific movie
# Example: /movie/movies/1
@movies.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    try:
        current_app.logger.info(f"Getting get_movie request for movie_id: {movie_id}")
        cursor = db.get_db().cursor()

        # Get movie details
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        movie = cursor.fetchone()

        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        cursor.close()
        return jsonify(movie), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_movie: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all actors featured in a specific movie
# Example: /movie/movies/1/actors
@movies.route("/movies/<int:movie_id>/actors", methods=["GET"])
def get_movie_actors(movie_id):
    try:
        current_app.logger.info(
            f"Getting get_movie_actors request for movie_id: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Get all actors in this movie
        query = """
        SELECT a.actorID, a.firstName, a.lastName FROM Actors a
        JOIN MovieActors ma ON a.actorID = ma.actorID
        WHERE ma.movieID = %s
        """
        cursor.execute(query, (movie_id,))
        actors = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved actors for movie_id: {movie_id}"
        )
        return jsonify(actors), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_movie_actors: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all directors of a specific movie
# Example: /movie/movies/1/directors
@movies.route("/movies/<int:movie_id>/directors", methods=["GET"])
def get_movie_directors(movie_id):
    try:
        current_app.logger.info(
            f"Getting get_movie_directors request for movie_id: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Get all directors of this movie
        query = """
        SELECT d.directorID, d.firstName, d.lastName FROM Directors d
        JOIN MovieDirectors md ON d.directorID = md.directorID
        WHERE md.movieID = %s
        """
        cursor.execute(query, (movie_id,))
        directors = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved directors for movie_id: {movie_id}"
        )
        return jsonify(directors), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_movie_directors: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all trailers for a specific movie
# Example: /movie/movies/1/trailers
@movies.route("/movies/<int:movie_id>/trailers", methods=["GET"])
def get_movie_trailers(movie_id):
    try:
        current_app.logger.info(
            f"Getting get_movie_trailers request for movie_id: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Get all trailers for this movie
        query = "SELECT * FROM Trailers t WHERE t.movieID = %s"
        cursor.execute(query, (movie_id,))
        trailers = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved trailers for movie_id: {movie_id}"
        )
        return jsonify(trailers), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_movie_trailers: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all captions for a specific movie
# Example: /movie/movies/1/captions
# @movies.route("/movies/<int:movie_id>/captions", methods=["GET"])
# def get_movie_captions(movie_id):


# have separate /admins and /users routes
