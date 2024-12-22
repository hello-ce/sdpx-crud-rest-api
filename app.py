from flask import Flask, jsonify, request
import mysql.connector
import os

app = Flask(__name__)


def ConnectorMysql():
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "myuser"),
        passwd=os.getenv("MYSQL_PASSWORD", "mypassword"),
        database=os.getenv("MYSQL_DATABASE", "mydatabase"),
        auth_plugin="mysql_native_password",
    )
    return mydb


@app.route("/")
def hello_world():
    return "Hello World - Welcome to the User API!"


@app.route("/user", methods=["GET"])
def get_users():
    try:
        mydb = ConnectorMysql()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        mydb.close()
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route("/user/new", methods=["POST"])
def add_user():
    try:
        data = request.get_json()

        mydb = ConnectorMysql()
        cursor = mydb.cursor()
        sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
        values = (data["name"], data["age"])
        cursor.execute(sql, values)
        mydb.commit()

        new_user_id = cursor.lastrowid
        cursor.close()
        mydb.close()

        return jsonify({"id": new_user_id, "message": "User created successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        mydb = ConnectorMysql()
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        mydb.close()
        return jsonify(user)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not data or "name" not in data or "age" not in data:
            return jsonify({"error": "Missing name or age"}), 400

        mydb = ConnectorMysql()
        cursor = mydb.cursor()
        sql = "UPDATE users SET name = %s, age = %s WHERE id = %s"
        values = (data["name"], data["age"], user_id)
        cursor.execute(sql, values)
        mydb.commit()

        if cursor.rowcount == 0:
            cursor.close()
            mydb.close()
            return jsonify({"error": "User not found"}), 404

        cursor.close()
        mydb.close()

        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


@app.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        mydb = ConnectorMysql()
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mydb.commit()

        if cursor.rowcount == 0:
            cursor.close()
            mydb.close()
            return jsonify({"error": "User not found"}), 404

        cursor.close()
        mydb.close()

        return jsonify({"message": "User deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
