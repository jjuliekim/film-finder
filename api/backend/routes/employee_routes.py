'''
from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for employee routes
employees = Blueprint("employees", __name__)


# Get all movies with optional filtering by year, genre, and duration
# Example: /movie/movies?year=2016&genre=Action&duration=2
@employees.route("/employees", methods=["GET"])
def get_all_employees():

    cursor = db.get_db().cursor()
    the_query = """
        SELECT * FROM Employees;
    """

    cursor.execute(the_query)
    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype='application/json'
    return the_response

'''
from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for movie routes
employees = Blueprint("employees", __name__)


# Get all movies with optional filtering by employee id, first name, last name, and role
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
        role = request.args.get('role')

        current_app.logger.debug(
            f"Query parameters - empID: {empID}, firstName: {firstName}, lastName: {lastName}, role: {role}"
        )

        # Prepare the Base query
        query = "SELECT * FROM Employees m WHERE 1=1"
        params = []

        # Add filters if provided
        if empID:
            query += " AND empID = %s"
            params.append(empID)
        if firstName:
            query += """
            AND firstName = %s
            """
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