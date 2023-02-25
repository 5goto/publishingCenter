from flask import Flask, render_template, url_for, request, redirect, session
import bd_repo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'FDFFJFhfjdfjhugurhg434ff'


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', title="ProFlask")


@app.route('/books', methods=["POST", "GET"])
def books_table():  # put application's code here
    if request.method == "POST":
        print(request.form)

    return render_template('books.html', booksList=bd_repo.getAllBooks())


@app.route('/login', methods=["POST", "GET"])
def login():
    if "userLogged" in session:
        return redirect(url_for("books_table", username=session["userLogged"]))
    elif request.method == "POST" and request.form["username"] == "admin" and request.form["psw"] == "123":
        session["userLogged"] = request.form["username"]
        return redirect(url_for("books_table", username=session["userLogged"]))
    return render_template('login.html')


if __name__ == '__main__':
    app.run()

