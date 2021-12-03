from flask_sqlalchemy import SQLAlchemy
 
db =SQLAlchemy()

class BookModel(db.Model):
    __tablename__ = "table"
 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(40))
    isbn = db.Column(db.String(20))
    category = db.Column(db.String(20))
    publishDate = db.Column(db.String(100))
 
    def __init__(self, title,author,isbn,category, publishDate):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.publishDate = publishDate
    def __repr__(self):
        return f"{self.title}:{self.isbn}"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    releasedYear = db.Column(db.String(4))
    formatPri = db.Column(db.String(20))
    formatSec = db.Column(db.String(20))
    genre = db.Column(db.String(100))
    showType = db.Column(db.String(40))