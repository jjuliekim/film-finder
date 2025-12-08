from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for movie routes
employees = Blueprint("employee", __name__)


# Get all employees with optional filtering by employee id, first name, last name, and role
# Example: /employee/employees?firstName=Chloe&role=Admin
@employees.route("/employees", methods=["GET"])
def get_all_employees():
    try:
        current_app.logger.info("Starting get_all_employees request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        empID = request.args.get("empID")
        firstName = request.args.get("firstName")
        lastName = request.args.get("lastName")
        role = request.args.get("role")

        current_app.logger.debug(
            f"Query parameters - empID: {empID}, firstName: {firstName}, lastName: {lastName}, role: {role}"
        )

        # Prepare the Base query
        query = "SELECT * FROM Employees WHERE 1=1"
        params = []

        # Add filters if provided
        if empID:
            query += " AND empID = %s"
            params.append(empID)
        if firstName:
            query += " AND firstName = %s"
            params.append(firstName)
        if lastName:
            query += " AND lastName = %s"
            params.append(lastName)
        if role:
            query += " AND role = %s"
            params.append(role)

        current_app.logger.debug(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        employees = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved {len(employees)} employees")
        cursor.close()
        return jsonify(employees), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_all_employees: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific employee
# Example: /employee/employees/6
@employees.route("/employees/<int:empID>", methods=["GET"])
def get_employee(empID):
    try:
        current_app.logger.info(f"Getting get_employee request for empID: {empID}")
        cursor = db.get_db().cursor()

        # Get employee details
        cursor.execute("SELECT * FROM Employees WHERE empID = %s", (empID,))
        employee = cursor.fetchone()

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        cursor.close()
        return jsonify(employee), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_employee: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all versions with optional filtering
# Example: /employee/versions?empID=29
@employees.route("/versions", methods=["GET"])
def get_all_versions():
    try:
        current_app.logger.info("Starting get_all_versions request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        publishedAt = request.args.get("publishedAt")
        empID = request.args.get("empID")

        current_app.logger.debug(
            f"Query parameters - publishedAt: {publishedAt}, empID: {empID}"
        )

        # Prepare the Base query
        query = "SELECT * FROM AppVersions WHERE 1=1"
        params = []

        # Add filters if provided
        if publishedAt:
            query += " AND publishedAt = %s"
            params.append(publishedAt)
        if empID:
            query += " AND empID = %s"
            params.append(empID)

        current_app.logger.debug(f"Executing query: {query} with params: {params}")
        cursor.execute(query, params)
        versions = cursor.fetchall()

        current_app.logger.info(f"Successfully retrieved {len(versions)} versions")
        cursor.close()
        return jsonify(versions), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_all_versions: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get detailed information about a specific version
# Example: /employee/versions/6
@employees.route("/versions/<int:versionID>", methods=["GET"])
def get_version(versionID):
    try:
        current_app.logger.info(
            f"Getting get_version request for versionID: {versionID}"
        )
        cursor = db.get_db().cursor()

        # Get version details
        cursor.execute("SELECT * FROM AppVersions WHERE versionID = %s", (versionID,))
        version = cursor.fetchone()

        cursor.close()
        return jsonify(version), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_version: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Get all saved searches for an employee
# Example: /employees/searches?empID=6
@employees.route("/searches", methods=["GET"])
def get_saved_searches():
    try:
        empID = request.args.get("empID")
        current_app.logger.info(
            f"Getting get_saved_searches request for empID: {empID}"
        )
        cursor = db.get_db().cursor()

        # Get search details
        cursor.execute(
            """
            SELECT * FROM FilteredSearches fs
            JOIN SavedSearches ss 
            ON ss.searchID = fs.searchID
            WHERE (ss.empID = %s)""",
            (empID,),
        )
        searches = cursor.fetchall()

        cursor.close()
        return jsonify(searches), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_saved_searches: {str(e)}")
        return jsonify({"error": str(e)}), 500
