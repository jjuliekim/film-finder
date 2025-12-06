from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for user routes
users = Blueprint("user", __name__)


# Create a new review
# Required fields: userID, movieID, reviewText, publishedDate, starRating
# JSON: {"userID": 1, "movieID": 2, "reviewText": "Great movie!", "starRating": 5 }
# Example: POST /user/reviews with JSON body
@users.route("/reviews", methods=["POST"])
def create_review():
    try:
        current_app.logger.info("Starting create_review request")
        data = request.get_json()

        # Validate required fields
        required_fields = ["userID", "movieID", "reviewText", "starRating"]
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new review
        query = """
        INSERT INTO Reviews (userID, movieID, reviewText, publishedDate, starRating)
        VALUES (%s, %s, %s, NOW(), %s)
        """
        cursor.execute(
            query,
            (
                data["userID"],
                data["movieID"],
                data["reviewText"],
                data["starRating"],
            ),
        )

        db.get_db().commit()
        new_review_id = cursor.lastrowid
        cursor.close()

        current_app.logger.info(f"Review created successfully with ID: {new_review_id}")
        return (
            jsonify(
                {"message": "Review created successfully", "review_id": new_review_id}
            ),
            201,
        )
    except Error as e:
        current_app.logger.error(f"Error creating review: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Delete a specific review
# Example: DELETE /user/reviews/1
@users.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    try:
        current_app.logger.info(f"Starting delete_review request for ID: {review_id}")
        cursor = db.get_db().cursor()

        # Check if review exists
        cursor.execute("SELECT * FROM Reviews WHERE reviewID = %s", (review_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Review not found"}), 404

        # Delete review
        query = "DELETE FROM Reviews WHERE reviewID = %s"
        cursor.execute(query, (review_id,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Review with ID {review_id} deleted successfully")
        return jsonify({"message": "Review deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Error deleting review: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all reviews written by a specific user
# Example: GET /user/reviews/users/1
@users.route("/reviews/users/<int:user_id>", methods=["GET"])
def get_user_reviews(user_id):
    try:
        current_app.logger.info(
            f"Starting get_user_reviews request for user ID: {user_id}"
        )
        cursor = db.get_db().cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM UserProfiles WHERE userID = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Get all reviews for the user
        query = """
        SELECT * FROM Reviews WHERE userId = %s
        ORDER BY publishedDate DESC
        """
        cursor.execute(query, (user_id,))
        reviews = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Retrieved reviews for user ID: {user_id}")
        return jsonify(reviews), 200
    except Error as e:
        current_app.logger.error(f"Error retrieving reviews: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all reviews for a specific movie
# Example: GET /user/reviews/movies/1
@users.route("/reviews/movies/<int:movie_id>", methods=["GET"])
def get_movie_reviews(movie_id):
    try:
        current_app.logger.info(
            f"Starting get_movie_reviews request for movie ID: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Get all reviews for the movie
        query = """
        SELECT * FROM Reviews WHERE movieID = %s
        ORDER BY publishedDate DESC
        """
        cursor.execute(query, (movie_id,))
        reviews = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Retrieved reviews for movie ID: {movie_id}")
        return jsonify(reviews), 200
    except Error as e:
        current_app.logger.error(f"Error retrieving reviews: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Create a new list
# Required fields: userID, listName
# JSON: {"userID": 1, "listName": "My Favorite Movies" }
# Example: POST /user/lists with JSON body
@users.route("/lists", methods=["POST"])
def create_list():
    try:
        current_app.logger.info("Starting create_list request")
        data = request.get_json()

        # Validate required fields
        required_fields = ["userID", "listName"]
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new list
        query = """
        INSERT INTO Lists (userID, listName)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (
                data["userID"],
                data["listName"],
            ),
        )

        db.get_db().commit()
        new_list_id = cursor.lastrowid
        cursor.close()

        current_app.logger.info(f"List created successfully with ID: {new_list_id}")
        return (
            jsonify({"message": "List created successfully", "list_id": new_list_id}),
            201,
        )
    except Error as e:
        current_app.logger.error(f"Error creating list: {str(e)}")
        return jsonify({"error": str(e)}), 500
      
      
# Delete a specific list
# Example: DELETE /user/lists/1
@users.route("/lists/<int:list_id>", methods=["DELETE"])
def delete_list(list_id):
    try: 
        current_app.logger.info(f"Starting delete_list request for ID: {list_id}")
        cursor = db.get_db().cursor()

        # Check if list exists
        cursor.execute("SELECT * FROM Lists WHERE listID = %s", (list_id,))
        if not cursor.fetchone():
            return jsonify({"error": "List not found"}), 404

        # Delete list
        query = "DELETE FROM Lists WHERE listID = %s"
        cursor.execute(query, (list_id,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"List with ID {list_id} deleted successfully")
        return jsonify({"message": "List deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Error deleting list: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get a specific list
# Example: /user/lists/1
@users.route("/lists/<int:list_id>", methods=["GET"])
def get_list(list_id):
    try:
        current_app.logger.info(f"Starting get_list request for ID: {list_id}")
        cursor = db.get_db().cursor()

        # Get the list
        query = "SELECT * FROM Lists WHERE listID = %s"
        cursor.execute(query, (list_id,))
        list = cursor.fetchone()
        cursor.close()

        current_app.logger.info(f"Retrieved list with ID: {list_id}")
        return jsonify(list), 200
    except Error as e:
        current_app.logger.error(f"Error retrieving list: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all lists created by a specific user
# Example: GET /user/lists/users/1
@users.route("/lists/users/<int:user_id>", methods=["GET"])
def get_user_lists(user_id):
    try:
        current_app.logger.info(
            f"Starting get_user_lists request for user ID: {user_id}"
        )
        cursor = db.get_db().cursor()

        # Check if user exists
        cursor.execute("SELECT * FROM UserProfiles WHERE userID = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({"error": "User not found"}), 404

        # Get all lists for the user
        query = "SELECT * FROM Lists WHERE userID = %s"
        cursor.execute(query, (user_id,))
        lists = cursor.fetchall()
        cursor.close()

        current_app.logger.info(f"Retrieved lists for user ID: {user_id}")
        return jsonify(lists), 200
    except Error as e:
        current_app.logger.error(f"Error retrieving lists: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Add a movie to a specific list
# Required field: movieID
# JSON: {"movieID": 1 }
# Example: POST /user/lists/1/movies with JSON body
@users.route("/lists/<int:list_id>/movies", methods=["POST"])
def add_movie_to_list(list_id):
    try:
        current_app.logger.info(
            f"Starting add_movie_to_list request for list ID: {list_id}"
        )
        data = request.get_json()

        # Validate required field
        if "movieID" not in data:
            current_app.logger.warning("Missing required field: movieID")
            return jsonify({"error": "Missing required field: movieID"}), 400

        cursor = db.get_db().cursor()

        # Check if list exists
        cursor.execute("SELECT * FROM Lists WHERE listID = %s", (list_id,))
        if not cursor.fetchone():
            return jsonify({"error": "List not found"}), 404

        # Insert movie into list
        query = """
        INSERT INTO ListMovies (listID, movieID)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (
                list_id,
                data["movieID"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Movie added to list ID: {list_id} successfully")
        return jsonify({"message": "Movie added to list successfully"}), 201
    except Error as e:
        current_app.logger.error(f"Error adding movie to list: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Remove a specific movie from a specific list
# Example: DELETE /user/lists/1/movies/2
@users.route("/lists/<int:list_id>/movies/<int:movie_id>", methods=["DELETE"])
def remove_movie_from_list(list_id, movie_id):
    try:
        current_app.logger.info(
            f"Starting remove_movie_from_list request for list ID: {list_id} and movie ID: {movie_id}"
        )
        cursor = db.get_db().cursor()

        # Check if list exists
        cursor.execute("SELECT * FROM Lists WHERE listID = %s", (list_id,))
        if not cursor.fetchone():
            return jsonify({"error": "List not found"}), 404

        # Check if movie exists
        cursor.execute("SELECT * FROM Movies WHERE movieID = %s", (movie_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Movie not found"}), 404

        # Delete movie from list
        query = "DELETE FROM ListMovies WHERE listID = %s AND movieID = %s"
        cursor.execute(query, (list_id, movie_id))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(
            f"Movie ID: {movie_id} removed from list ID: {list_id} successfully"
        )
        return jsonify({"message": "Movie removed from list successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Error removing movie from list: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get details of a specific watch party 
# Example: /user/watchparties/1
@users.route("/watchparties/<int:party_id>", methods=["GET"])
def get_watch_party(party_id):
    try:
        current_app.logger.info(
            f"Starting get_watch_party request for party ID: {party_id}"
        )
        cursor = db.get_db().cursor()

        # Get the watch party
        query = "SELECT * FROM WatchParties WHERE partyID = %s"
        cursor.execute(query, (party_id,))
        party = cursor.fetchone()
        cursor.close()

        current_app.logger.info(f"Retrieved watch party with ID: {party_id}")
        if not party:
            return jsonify({"error": "Watch party not found"}), 404

        return jsonify(party), 200
    except Error as e:
        current_app.logger.error(f"Error retrieving watch party: {str(e)}")
        return jsonify({"error": str(e)}), 500
      
      
# Create a new watch party
# Required fields: userID, movieID, partyDate
# JSON: {"userID": 1, "movieID": 2, "partyDate": "2025-12-31" }
# Example: POST /user/watchparties with JSON body
@users.route("/watchparties", methods=["POST"])
def create_watch_party():
    try: 
        current_app.logger.info("Starting create_watch_party request")
        data = request.get_json()

        # Validate required fields
        required_fields = ["userID", "movieID", "partyDate"]
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new watch party
        query = """
        INSERT INTO WatchParties (userID, movieID, partyDate)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["userID"],
                data["movieID"],
                data["partyDate"],
            ),
        )

        db.get_db().commit()
        new_party_id = cursor.lastrowid
        cursor.close()

        current_app.logger.info(f"Watch party created successfully with ID: {new_party_id}")
        return (
            jsonify({"message": "Watch party created successfully", "party_id": new_party_id}),
            201,
        )
    except Error as e:
        current_app.logger.error(f"Error creating watch party: {str(e)}")
        return jsonify({"error": str(e)}), 500