import bd_repo
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from autorisation import *
import json
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'FDFFJFhfjdfjhugurhg434ff'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    return UserLogin().fromDB(user_id=id)


@app.route('/')
@login_required
def index():  # put application's code here
    if request.args.get("user"):
        return json.dumps({"user": current_user.get_username()})

    return render_template('index.html', title="Таблицы", user=current_user.get_username())


@app.route('/books', methods=["POST", "GET"])
@login_required
def books_table():  # put application's code here
    if request.args.get("user"):
        return json.dumps({"user": current_user.get_username()})
    if request.args.get("authors"):
        return json.dumps({"authors": json.dumps(bd_repo.getAllWriters())})

    if request.method == "POST":
        if request.args.get("operation") == "add":
            data = request.form.to_dict()
            op_result = bd_repo.addBook(data)
            flash(op_result)
        elif request.args.get("operation") == "remove":
            data = request.form.to_dict()
            op_result = bd_repo.deleteBookById(int(data['title']))
            flash(op_result)
        elif request.args.get("operation") == "update":
            data = request.form.to_dict()
            op_result = bd_repo.changeBook(data)
            flash(op_result)
        elif request.args.get("operation") == "add_autor":
            data = request.form.to_dict()
            op_result = bd_repo.addBookToAutor(data)
            flash(op_result)
        elif request.args.get("operation") == "remove_autor":
            data = request.form.to_dict()
            op_result = bd_repo.removeAutorToBook(data)
            flash(op_result)
    return render_template('books.html', booksList=bd_repo.getAllBooks(), user=current_user.get_username())


@app.route('/writers', methods=["POST", "GET"])
@login_required
def writers_table():  # put application's code here
    if request.method == "POST":
        # bd_repo.deleteWriterById(3)
        if request.args.get("operation") == "add":
            data = request.form.to_dict()
            op_result = bd_repo.addWriter(data)
            flash(op_result)
        elif request.args.get("operation") == "remove":
            data = request.form.to_dict()
            op_result = bd_repo.deleteWriterById(int(data['id']))
            flash(op_result)
        elif request.args.get("operation") == "update":
            data = request.form.to_dict()
            op_result = bd_repo.changeWriter(data)
            flash(op_result)

    return render_template('writers.html', booksList=bd_repo.getAllWriters(), user=current_user.get_username())


@app.route('/orders', methods=["POST", "GET"])
@login_required
def orders_table():  # put application's code here
    if request.method == "POST":
        # bd_repo.deleteWriterById(3)
        if request.args.get("operation") == "add":
            data = request.form.to_dict()
            op_result = bd_repo.addOrder(data)
            flash(op_result)
        elif request.args.get("operation") == "remove":
            data = request.form.to_dict()
            op_result = bd_repo.deleteOrderById(int(data['id']))
            flash(op_result)
        elif request.args.get("operation") == "update":
            data = request.form.to_dict()
            op_result = bd_repo.changeOrder(data)
            flash(op_result)

    return render_template('orders.html', booksList=bd_repo.getAllOrders(), user=current_user.get_username())


@app.route('/customers', methods=["POST", "GET"])
@login_required
def customers_table():  # put application's code here
    if request.method == "POST":
        # bd_repo.deleteWriterById(3)
        if request.args.get("operation") == "add":
            data = request.form.to_dict()
            op_result = bd_repo.addСustomer(data)
            flash(op_result)
        elif request.args.get("operation") == "remove":
            data = request.form.to_dict()
            op_result = bd_repo.deleteCustomerById(int(data['id']))
            flash(op_result)
        elif request.args.get("operation") == "update":
            data = request.form.to_dict()
            op_result = bd_repo.changeCustomer(data)
            flash(op_result)

    return render_template('customers.html', booksList=bd_repo.getAllCustomers(), user=current_user.get_username())


@app.route('/contracts', methods=["POST", "GET"])
@login_required
def contracts_table():  # put application's code here
    if request.args.get("user"):
        return json.dumps({"user": current_user.get_username()})

    if request.method == "POST":
        if request.args.get("operation") == "add":
            data = request.form.to_dict()
            op_result = bd_repo.addСontract(data)
            flash(op_result)
        elif request.args.get("operation") == "remove":
            data = request.form.to_dict()
            op_result = bd_repo.deleteContractById(int(data['title']))
            flash(op_result)
        elif request.args.get("operation") == "update":
            data = request.form.to_dict()
            op_result = bd_repo.changeContract(data)
            flash(op_result)

    return render_template('contracts.html', booksList=bd_repo.getAllContracts(), user=current_user.get_username())


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = bd_repo.getUserByLogin(request.form['username'])
        if user and check_password_hash(user[0][2], request.form['psw']):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for("index"))

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

