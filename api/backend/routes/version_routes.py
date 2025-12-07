from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for movie routes
versions = Blueprint("version", __name__)


# Get all movies with optional filtering by employee id, first name, last name, and role
# Example: /employee/employees?firstName=Chloe&role=Admin
@versions.route("/versions", methods=["GET"])
def get_all_versions():
    try:
        current_app.logger.info("Starting get_all_versions request")
        cursor = db.get_db().cursor()

        # Get query parameters for filtering
        versionID = request.args.get('versionID')
        createdAt = request.args.get("createdAt")
        publishedAt = request.args.get("publishedAt")
        description = request.args.get("description")
        empID = request.args.get('empID')

        current_app.logger.debug(
            f"Query parameters - versionID: {versionID}, createdAt: {createdAt}, publishedAt: {publishedAt}, description: {description}, empID: {empID}"
        )

        # Prepare the Base query
        query = "SELECT * FROM AppVersions m WHERE 1=1"
        params = []

        # Add filters if provided
        if versionID:
            query += " AND versionID = %s"
            params.append(versionID)
        if createdAt:
            query += """
            AND createdAt = %s
            """
            params.append(createdAt)
        if publishedAt:
            query += " AND publishedAt = %s"
            params.append(publishedAt)
        if description:
            query += " AND description LIKE %s"
            params.append(f"%{description}%")
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
# Example: /version/versions/6
@versions.route("/versions/<int:versionID>", methods=["GET"])
def get_version(versionID):
    try:
        current_app.logger.info(f"Getting get_version request for versionID: {versionID}")
        cursor = db.get_db().cursor()

        # Get version details
        cursor.execute("SELECT * FROM AppVersions WHERE versionID = %s", (versionID,))
        version = cursor.fetchone()

        if not version:
            return jsonify({"error": "Version not found"}), 404

        cursor.close()
        return jsonify(version), 200

    except Error as e:
        current_app.logger.error(f"Database error in get_version: {str(e)}")
        return jsonify({"error": str(e)}), 500