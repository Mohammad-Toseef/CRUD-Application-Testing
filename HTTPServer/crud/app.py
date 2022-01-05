"""
CRUD Application using FLASK framework .
Author - Mohammad Toseef
"""
import os

from flask import Flask, render_template
from flask import request, flash

from .database import Connection

app = Flask(__name__)
app.secret_key = "flash message"
TABLE_NAME = ''
FILE_NAME = ''
connection = Connection()
connection.connect()


@app.route("/")
def index():
    """
    :return: output the homepage while server is running
    """

    return render_template("home.html")


@app.route("/upload_file", methods=['POST'])
def upload_file():
    """
    Uploads file to the database
    :return: Success page
    """
    file = request.files['filename']
    app.FILE_NAME = file.filename
    file.save(os.path.join(os.path.dirname(__file__), f'data\\{file.filename}'))
    app.TABLE_NAME = "_".join(file.filename.split('.'))
    connection.upload_file(file.filename)
    data = Connection.select_statement()
    return render_template("Success.html", data=data, msg='File uploaded Successfully')


@app.route("/add", methods=['POST', 'GET'])
def add():
    """
    renders add.html on Get request ,
    renders Success.html when row_data has been added on post request
    renders add.html with error message when row_data is not proper
    """
    columns = connection.table_columns
    if request.method == 'POST':
        message = connection.add_row(request.form.to_dict())
        if message:
            flash(message, 'error')
            return render_template("add.html", columns=columns)
        data = connection.select_statement()
        return render_template("Success.html", data=data, msg='Record added Successfully')
    return render_template("add.html", columns=columns)


@app.route('/update/<record_id>', methods=['POST', 'GET'])
def update(record_id):
    """
    GET request : renders edit page
    POST request : makes record update request to database and renders Success.html

    :param record_id: unique id of the record to be updated
    :return: GET - edit.html / POST - Success.html

    """
    if request.method == 'POST':
        Connection.update(request.form.to_dict(), record_id)
        data = connection.select_statement()
        return render_template("Success.html", data=data, msg='Record Updated Successfully')
    data = connection.select_statement(record_id)
    return render_template("edit.html", data=data[1], headers=Connection.table_columns)


@app.route('/delete/<record_id>')
def delete(record_id):
    """
    deletes record for the given id from DB
    :param record_id: id that recognize the row uniquely
    :return: renders Success.html
    """
    data, msg = connection.delete_row(record_id)
    return render_template("Success.html", data=data, msg=msg)


app.debug = True
app.run(port=5000)
