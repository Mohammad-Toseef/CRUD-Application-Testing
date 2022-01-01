from flask import Flask, render_template
from flask import request, flash
from Database import Connection
from mysql.connector import DataError

app = Flask(__name__)
app.secret_key = "flash message"
table_name = ''
file_name = ''
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
    global table_name, file_name
    file = request.files['filename']
    file_name = file.filename
    file.save(file.filename)
    table_name = "_".join(file.filename.split('.'))
    connection.upload_file(file.filename)
    data = Connection.select_statement()
    return render_template("Success.html", data=data, msg='File uploaded Successfully')


@app.route("/add", methods=['POST', 'GET'])
def add():
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
    # connection.connect()
    if request.method == 'POST':
        Connection.update(request.form.to_dict(), record_id)
        # cursor = connection.my_db.cursor()
        # cursor.execute(query)
        # connection.my_db.commit()
        data = connection.select_statement()

        return render_template("Success.html", data=data, msg='Record Updated Successfully')
    cursor = connection.my_db.cursor()
    cursor.execute('select database();')
    database = cursor.fetchone()
    cursor.execute('SHOW COLUMNS FROM ' + database[0] + '.' + table_name)
    data = cursor.fetchall()
    headers = []
    for row in data:
        headers.append(row[0])
    data = []
    cursor.execute('SELECT * FROM '+table_name+' WHERE id=\''+record_id+'\'')
    data.append(cursor.fetchone())
    return render_template("edit.html", data=data, headers=headers)


@app.route('/delete/<record_id>')
def delete(record_id):
    connection.connect()
    cursor = connection.my_db.cursor()
    cursor.execute('SELECT EXISTS(SELECT * from {0} WHERE id = \'{1}\')'.format(table_name,
                                                                                record_id))
    result = cursor.fetchone()
    if result[0] != 1:
        raise DataError
    cursor.execute('DELETE from '+table_name+' WHERE id=\''+record_id+'\'')
    data = Connection.select_statement()
    connection.my_db.commit()
    return render_template("Success.html", data=data, msg='Record Deleted Successfully')


app.debug = True
app.run(port=5000)
