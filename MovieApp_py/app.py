from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import FileStorage
from flask_sqlalchemy import SQLAlchemy
from flask_autoindex import AutoIndex
from models import db, BookModel, Movie


app = Flask(__name__)
spath = "E:\Media" # Update your own starting directory here, or leave "/" for parent directory
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

files_index = AutoIndex(app, browse_root=spath, add_url_rules=False)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db.init_app(app)

@app.before_first_request
def create_table():
    db.create_all()





    

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/books')
def books():
    #show all books
    book_list = BookModel.query.all()
    return render_template('books.html', book_list=book_list)

@app.route("/createbook", methods=["GET","POST"])
def createbook():
    # add new item
    if request.method == 'GET':
        return render_template("createbook.html")

    if request.method == "POST":
        id = request.form['id']
        title = request.form.get("title")
        author = request.form.get("author")
        isbn = request.form.get("isbn")
        category = request.form.get("category")
        publishDate = request.form.get("publishDate")
        new_book = BookModel(title=title, author=author, isbn=isbn, category=category, publishDate=publishDate)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("books"))
    else:
        return render_template('books.html')

@app.route('/movies')
def movies():
    # show all movies
    movie_list = Movie.query.all()
    #print(movie_list)
    return render_template('movies.html', movie_list=movie_list)

@app.route("/create", methods=["GET","POST"])
def create():
    # add new item
    if request.method == 'GET':
        return render_template("create.html")

    if request.method == "POST":
        id = request.form['id']
        title = request.form.get("title")
        releasedYear = request.form.get("releasedYear")
        formatPri = request.form.get("formatPri")
        formatSec = request.form.get("formatSec")
        genre = request.form.get("genre")
        showType = request.form.get("showType")
        new_movie = Movie(title=title, releasedYear=releasedYear, formatPri=formatPri, formatSec=formatSec, genre=genre, showType=showType)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("movies"))
    else:
        return render_template('movies.html')
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    movie = Movie.query.filter_by(id=id).first()
    if request.method == 'POST':
        if movie:
            db.session.delete(movie)
            db.session.commit()

            title = request.form['title']
            releasedYear = request.form['releasedYear']
            formatPri = request.form['formatPri']
            formatSec = request.form['formatSec']
            genre = request.form['genre']
            showType = request.form['showType']
            movie = Movie(id = id, title=title, releasedYear=releasedYear, formatPri=formatPri, formatSec=formatSec, genre=genre, showType=showType)
            db.session.add(movie)
            db.session.commit()
            return render_template('update.html/{id}')
        return f"Movie with id ={id} Doesnt exist"
    return render_template("update.html", movie=movie)


@app.route('/files')
@app.route('/files/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

@app.route("/delete/<int:id>")
def delete(id):
    # query db
    movie = Movie.query.filter_by(id=id).first()
    # delete item
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("movies"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_sucess():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
        return 'file uploaded successfully'


app.run(host='localhost', port=5000)