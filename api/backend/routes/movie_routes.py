from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Create a Blueprint for filmfinder routes
filmfinder = Blueprint("filmfinder", __name__)

