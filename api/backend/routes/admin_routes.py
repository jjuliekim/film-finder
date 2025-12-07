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
@admins.route("/admin/<int:userID>", methods=["GET"])
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