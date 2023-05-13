from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



#SQL Code

# db= sqlite3.connect("books-connection.db")

#Create a cursor which will control database 
# cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

# cursor.execute("INSERT INTO books VALUES (1, 'The Lean StartUp', 'Peter Thiel', '9.5')")
# db.commit()              



#SQLAlchemy Code
app = Flask(__name__)
app.app_context().push() #Runtime error

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id= db.Column(db.Integer, primary_key =True)
    title = db.Column(db.String(250), unique = True, nullable = False)
    author = db.Column(db.String(250), nullable = False)
    rating = db.Column(db.Float(250), nullable = False)

    # This will allow each book object to be identified by its title
    def __repr__(self):
        return f'<Book {self.title}'

db.create_all()

# #Adding Entry to SQL 
# new_book = Book(title= 'The Lean Startup', author='Eric Ries', rating= 9.5)
# db.session.add(new_book)
# db.session.commit()




#Flask Code

@app.route('/')
def home():
    all_books = db.session.query(Book).all() # Retrieve all books from the database
    return render_template('index.html', book=all_books)

@app.route('/books')
def books():
    return render_template('books.html')

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title = request.form["title"],
            author = request.form["author"],
            rating = request.form["rating"],
            # "summary":request.form["summary"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect( url_for('books'))
    return render_template("add.html")

@app.route('/edit')
def edit():
    return render_template('edit.html')


@app.route("/remove", methods=["POST", "GET"])
def remove():
    book_id = request.id.get('id')

    #DELETE A RECORD BY ID
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect( url_for('books'))
        

    # return render_template('remove.html')

if __name__ == "__main__":
    app.run(debug=True)




