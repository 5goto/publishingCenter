from flask import Flask, render_template, url_for, request, redirect, session
import bd_repo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from autorisation import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FDFFJFhfjdfjhugurhg434ff'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    print("load user")
    return UserLogin().fromDB(user_id=id)


@app.route('/')
@login_required
def index():  # put application's code here
    print(bd_repo.getUserByID("4"))
    return render_template('index.html', title="ProFlask")


@app.route('/books', methods=["POST", "GET"])
@login_required
def books_table():  # put application's code here
    if request.method == "POST":
        print(request.form)

    return render_template('books.html', booksList=bd_repo.getAllBooks())


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = bd_repo.getUserByLogin(request.form['username'])
        print(user)
        if user and check_password_hash(user[0][2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for("books_table"))

    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
