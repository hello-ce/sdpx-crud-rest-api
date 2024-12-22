import mysql.connector
import os


def ConnectorMysql():
    mydb = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "myuser"),
        passwd=os.getenv("MYSQL_PASSWORD", "mypassword"),
        database=os.getenv("MYSQL_DATABASE", "mydatabase"),
        auth_plugin="mysql_native_password",
    )
    return mydb
