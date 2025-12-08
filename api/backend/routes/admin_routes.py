from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for admin routes
admins = Blueprint("admin", __name__)


# Get all user info
# Example: /admin/users?forKids=true
def get_bool(val):
    if val in ["true", "1"]:
        return 1
    else:
        return 0
@admins.route("/users", methods=["GET"])
def get_all_users():
    try:
        current_app.logger.info("Starting get_all_users request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        userID = request.args.get("userID")
        DOB = request.args.get("DOB")
        firstName = request.args.get("firstName")
        lastName = request.args.get("lastName")
        gender = request.args.get("gender")
        forKids = get_bool(request.args.get("forKids"))
        forTeens = get_bool(request.args.get("forTeens"))
        forAdults = get_bool(request.args.get("forAdults"))

        current_app.logger.debug(
            f"Query parameters - userID: {userID}, DOB: {DOB}, firstName: {firstName}, lastName: {lastName}, gender: {gender}, forKids: {forKids}, forTeens: {forTeens}, forAdults: {forAdults}"
        )

        # Prepare the Base query
        query = "SELECT * FROM UserProfiles WHERE 1=1"
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
@admins.route("/users/<int:userID>", methods=["GET"])
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
# Example: /admin/tasks/1
@admins.route("/tasks/<int:empID>", methods=["GET"])
def get_tasks(empID):
    try:
        current_app.logger.info(f"Getting get_tasks request for empID: {empID}")
        cursor = db.get_db().cursor()

        # Get task details
        query = """
        SELECT * FROM Tasks WHERE empID = %s
        ORDER BY createdAt DESC
        """
        cursor.execute(query, (empID,))
        tasks = cursor.fetchall()

        cursor.close()
        current_app.logger.info(f"Retrieved tasks for empID: {empID}")
        return jsonify(tasks), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_tasks: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Create a new task
# Required fields: empID, description
# JSON: {"empID": 6, "description": "respond to Iris email" }
# Example: POST /tasks with JSON body
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
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (data["empID"], data["description"]),
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


# Update task status or details
# Example: PUT /admin/tasks/1 with JSON body containing fields to update
@admins.route("/tasks/<int:taskID>", methods=["PUT"])
def update_task(taskID):
    try:
        data = request.get_json()

        # Check if task exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Tasks WHERE taskID = %s", (taskID,))
        if not cursor.fetchone():
            return jsonify({"error": "Task not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["description", "completedAt"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(taskID)
        query = f"UPDATE Tasks SET {', '.join(update_fields)} WHERE taskID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Task updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete a task
# Example: DELETE /admin/tasks/1
@admins.route("/tasks/<int:taskID>", methods=["DELETE"])
def delete_task(taskID):
    try:
        current_app.logger.info(f"Starting delete_task request for ID: {taskID}")
        cursor = db.get_db().cursor()

        # Check if task exists
        cursor.execute("SELECT * FROM Tasks WHERE taskID = %s", (taskID,))
        if not cursor.fetchone():
            return jsonify({"error": "Task not found"}), 404

        # Delete task
        query = "DELETE FROM Tasks WHERE taskID = %s"
        cursor.execute(query, (taskID,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Task with ID {taskID} deleted successfully")
        return jsonify({"message": "Task deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Error deleting task: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all requests for specific employee
# Example: /admin/requests/16
@admins.route("/requests/<int:empID>", methods=["GET"])
def get_requests(empID):
    try:
        current_app.logger.info(f"Getting get_requests request for empID: {empID}")
        cursor = db.get_db().cursor()

        # Get requests details
        cursor.execute("SELECT * FROM Requests WHERE empID = %s", (empID,))
        requests = cursor.fetchall()

        cursor.close()
        return jsonify(requests), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_requests: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Update request status
# Example: PUT /admin/requests/1 with JSON body containing fields to update
@admins.route("/requests/<int:requestID>", methods=["PUT"])
def update_request(requestID):
    try:
        data = request.get_json()

        # Check if request exists
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM Requests WHERE requestID = %s", (requestID,))
        if not cursor.fetchone():
            return jsonify({"error": "Request not found"}), 404

        # Build update query dynamically based on provided fields
        update_fields = []
        params = []
        allowed_fields = ["status"]

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(requestID)
        query = f"UPDATE Requests SET {', '.join(update_fields)} WHERE requestID = %s"

        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Request updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete a request
# Example: DELETE /admin/requests/1
@admins.route("/requests/<int:requestID>", methods=["DELETE"])
def delete_request(requestID):
    try:
        current_app.logger.info(f"Starting delete_request request for ID: {requestID}")
        cursor = db.get_db().cursor()

        # Check if request exists
        cursor.execute("SELECT * FROM Requests WHERE requestID = %s", (requestID,))
        if not cursor.fetchone():
            return jsonify({"error": "Request not found"}), 404

        # Delete request
        query = "DELETE FROM Requests WHERE requestID = %s"
        cursor.execute(query, (requestID,))
        db.get_db().commit()
        cursor.close()

        current_app.logger.info(f"Request with ID {requestID} deleted successfully")
        return jsonify({"message": "Request deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f"Error deleting request: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all messages for specific employee
# Example: /admin/messages?empID=6
@admins.route("/messages", methods=["GET"])
def get_messages():
    try:
        empID = request.args.get("empID")
        current_app.logger.info(f"Getting get_messages request for empID: {empID}")
        cursor = db.get_db().cursor()

        # Get message details
        cursor.execute(
            """
                       SELECT * FROM Messages m 
                       JOIN MessageReceived mr 
                        ON mr.msgID = m.msgID
                       WHERE (mr.receiver = %s
                        OR m.sender = %s)""",
            (empID, empID),
        )
        messages = cursor.fetchall()

        cursor.close()
        return jsonify(messages), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_messages: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Create a new message
# Required fields: content, receiver
# Example: POST /admin/messages with JSON body
@admins.route("/messages", methods=["POST"])
def create_message(): 
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["content", "sender", "receiver"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate receiver is a list
        if not isinstance(data["receiver"], list) or len(data["receiver"]) == 0:
            return jsonify({"error": "Receiver must be a non-empty list"}), 400

        cursor = db.get_db().cursor()

        # Verify sender exists and is an employee
        cursor.execute(
            "SELECT empID FROM Employees WHERE empID = %s", (data["sender"],)
        )
        if cursor.fetchone() is None:
            cursor.close()
            return jsonify({"error": "Employee not found"}), 404

        # Insert new message
        message_query = """
                        INSERT INTO Messages (content, sender)
                        VALUES (%s, %s)
                        """
        cursor.execute(
            message_query,
            (data["content"], data["sender"]),
        )

        new_message_id = cursor.lastrowid

        # Apply receivers
        receiver_query = """
                        INSERT INTO MessageReceived (msgID, receiver)
                        VALUES (%s, %s)
                        """

        for receiver_id in data["receiver"]:
            cursor.execute(receiver_query, (new_message_id, receiver_id))

        db.get_db().commit()
        cursor.close()

        return (
            jsonify(
                {
                    "message": "Message created successfully",
                    "messageID": new_message_id,
                    "num_recipients": len(data["receiver"]),
                }
            ),
            201,
        )
    except Error as e:
        return jsonify({"error": str(e)}), 500