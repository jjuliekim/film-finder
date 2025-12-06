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


