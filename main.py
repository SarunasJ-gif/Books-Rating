from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        # new_book = {'title': request.form['title'],
        #             'author': request.form['author'],
        #             'rating': request.form['rating']}
        # all_books.append(new_book)
        new_book = Books(title=request.form['title'], author=request.form['author'], rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route('/edit/id=<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book_edit = Books.query.get(int(book_id))
    title = book_edit.title
    rating = book_edit.rating
    id = book_id
    if request.method == 'POST':
        book_edit.rating = float(request.form['rating'])
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", title=title, rating=rating, book_id=id)


@app.route('/delete/<book_id>')
def delete_book(book_id):
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
