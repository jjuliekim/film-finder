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
        SELECT * FROM Actors a
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
@movies.route("/movies/<int:movie_id>/captions", methods=["GET"])
def get_movie_captions(movie_id):
    try:
        current_app.logger.info(
            f"Getting get_movie_captions request for movie_id: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Get all captions for this movie
        query = "SELECT * FROM Captions c WHERE c.movieID = %s"
        cursor.execute(query, (movie_id,))
        captions = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved captions for movie_id: {movie_id}"
        )
        return jsonify(captions), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_movie_captions: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific actor
# Example: /movie/actors/1
@movies.route("/actors/<int:actor_id>", methods=["GET"])
def get_actor(actor_id):
    try:
        current_app.logger.info(f"Getting get_actor request for actor_id: {actor_id}")
        cursor = db.get_db().cursor()

        # Get actor details
        cursor.execute("SELECT * FROM Actors WHERE actorID = %s", (actor_id,))
        actor = cursor.fetchone()

        if not actor:
            return jsonify({"error": "Actor not found"}), 404

        cursor.close()
        return jsonify(actor), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_actor: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all movies with a specific actor
# Example: /movie/actors/1/movies
@movies.route("/actors/<int:actor_id>/movies", methods=["GET"])
def get_actor_movies(actor_id):
    try:
        current_app.logger.info(
            f"Getting get_actor_movies request for actor_id: {actor_id}"
        )
        cursor = db.get_db().cursor()

        # Check if actor exists
        cursor.execute("SELECT * FROM Actors WHERE actorID = %s", (actor_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Actor not found"}), 404

        # Get all movies featuring this actor
        query = """
        SELECT * FROM Movies m
        JOIN MovieActors ma ON m.movieID = ma.movieID
        WHERE ma.actorID = %s
        """
        cursor.execute(query, (actor_id,))
        movies = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved movies for actor_id: {actor_id}"
        )
        return jsonify(movies), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_actor_movies: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get details of all directors
# Example: /movie/directors
@movies.route("/directors", methods=["GET"])
def get_all_directors():
    try:
        current_app.logger.info("Starting get_all_directors request")
        cursor = db.get_db().cursor()

        # Get all directors
        cursor.execute("SELECT * FROM Directors")
        directors = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved {len(directors)} directors")
        cursor.close()
        return jsonify(directors), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_all_directors: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific director
# Example: /movie/directors/1
@movies.route("/directors/<int:director_id>", methods=["GET"])
def get_director(director_id):
    try:
        current_app.logger.info(
            f"Getting get_director request for director_id: {director_id}"
        )
        cursor = db.get_db().cursor()

        # Get director details
        cursor.execute("SELECT * FROM Directors WHERE directorID = %s", (director_id,))
        director = cursor.fetchone()

        if not director:
            return jsonify({"error": "Director not found"}), 404

        cursor.close()
        return jsonify(director), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_director: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all movies directed by a specific director
# Example: /movie/directors/1/movies
@movies.route("/directors/<int:director_id>/movies", methods=["GET"])
def get_director_movies(director_id):
    try:
        current_app.logger.info(
            f"Getting get_director_movies request for director_id: {director_id}"
        )
        cursor = db.get_db().cursor()

        # Check if director exists
        cursor.execute("SELECT * FROM Directors WHERE directorID = %s", (director_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Director not found"}), 404

        # Get all movies directed by this director
        query = """
        SELECT * FROM Movies m
        JOIN MovieDirectors md ON m.movieID = md.movieID
        WHERE md.directorID = %s
        """
        cursor.execute(query, (director_id,))
        movies = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved movies for director_id: {director_id}"
        )
        return jsonify(movies), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_director_movies: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all movies of a specific genre
# Example: /genres/1/movies
@movies.route("/genres/<int:genre_id>/movies", methods=["GET"])
def get_genre_movies(genre_id):
    try:
        current_app.logger.info(
            f"Getting get_genre_movies request for genre_id: {genre_id}"
        )
        cursor = db.get_db().cursor()

        # Check if genre exists
        cursor.execute("SELECT * FROM Genres WHERE genreID = %s", (genre_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Genre not found"}), 404

        # Get all movies in this genre
        query = """
        SELECT * FROM Movies m
        JOIN MovieGenres mg ON m.movieID = mg.movieID
        WHERE mg.genreID = %s
        """
        cursor.execute(query, (genre_id,))
        movies = cursor.fetchall()
        cursor.close()
        current_app.logger.info(
            f"Successfully retrieved movies for genre_id: {genre_id}"
        )
        return jsonify(movies), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_genre_movies: {str(e)}")
        return jsonify({"error": str(e)}), 500
