from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for admin routes
admins = Blueprint("admin", __name__)


# Get all user info
# Example: /admin/users?forKids=true
@admins.route("/users", methods=["GET"])
def get_all_users():
    try:
        current_app.logger.info("Starting get_all_users request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        userID = request.args.get('userID')
        DOB = request.args.get("DOB")
        firstName = request.args.get("firstName")
        lastName = request.args.get("lastName")
        gender = request.args.get('gender')
        forKids = request.args.get('forKids')
        forTeens = request.args.get('forTeens')
        forAdults = request.args.get('forAdults')

        current_app.logger.debug(
            f"Query parameters - userID: {userID}, DOB: {DOB}, firstName: {firstName}, lastName: {lastName}, gender: {gender}, forKids: {forKids}, forTeens: {forTeens}, forAdults: {forAdults}"
        )

        # Prepare the Base query
        query = "SELECT * FROM UserProfiles m WHERE 1=1"
        params = []

        # Add filters if provided
        if userID:
            query += " AND userID = %s"
            params.append(userID)
        if DOB:
            query += """
            AND DOB = %s
            """
            params.append(DOB)
        if firstName:
            query += " AND firstName LIKE %s"
            params.append(f"%{firstName}%")
        if lastName:
            query += " AND lastName LIKE %s"
            params.append(f"%{lastName}%")
        if gender:
            query += " AND gender = %s"
            params.append(gender)
        if forKids:
            query += " AND forKids = %s"
            params.append(forKids)
        if forTeens:
            query += " AND forTeens = %s"
            params.append(forTeens)  
        if forAdults:
            query += " AND forAdults = %s"
            params.append(forAdults)          

        current_app.logger.debug(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        users = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved {len(users)} users")
        cursor.close()
        return jsonify(users), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_all_users: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific user
# Example: /admin/users/6
@admins.route("/admin/users/<int:userID>", methods=["GET"])
def get_user(userID):
    try:
        current_app.logger.info(f"Getting get_user request for userID: {userID}")
        cursor = db.get_db().cursor()

        # Get user details
        cursor.execute("SELECT * FROM UserProfiles WHERE userID = %s", (userID,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        cursor.close()
        return jsonify(user), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_user: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
# Get all tasks for specific employee
# Example: /admin/tasks?empID=6
@admins.route("/admin/tasks", methods=["GET"])
def get_tasks(empID):
    try:
        current_app.logger.info(f"Getting get_tasks request for empID: {empID}")
        cursor = db.get_db().cursor()

        # Get task details
        cursor.execute("SELECT * FROM Tasks WHERE empID = %s", (empID,))
        tasks = cursor.fetchall()

        if not tasks:
            return jsonify({"error": "Tasks not found"}), 404

        cursor.close()
        return jsonify(tasks), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_tasks: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Create a new task
# Required fields: empID, description
# JSON: {"empID": 6, "description": "respond to Iris email" }
# Example: POST /admin/tasks with JSON body
@admins.route("/tasks", methods=["POST"])
def create_task():
    try:
        current_app.logger.info("Starting create_task request")
        data = request.get_json()

        # Validate required fields
        required_fields = ["empID", "description"]
        for field in required_fields:
            if field not in data:
                current_app.logger.warning(f"Missing required field: {field}")
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        # Insert new list
        query = """
        INSERT INTO Tasks (empID, description)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["empID"],
                data["description"]
            ),
        )

        db.get_db().commit()
        new_task_id = cursor.lastrowid
        cursor.close()

        current_app.logger.info(f"Task created successfully with ID: {new_task_id}")
        return (
            jsonify({"message": "Task created successfully", "task_id": new_task_id}),
            201,
        )
    except Error as e:
        current_app.logger.error(f"Error creating task: {str(e)}")
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