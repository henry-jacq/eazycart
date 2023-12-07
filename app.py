from flask import Flask, render_template, request, redirect, url_for, session
from config import wrapper as wp

app = Flask(__name__)

app.secret_key = "eazycart"

@app.route("/")
def index():
    if session['user'] == None:
        return redirect(url_for('login_page'))
    
    return render_template("index.html", page_name="Home", userData=session['user'], products=wp.get_products())

@app.route("/login", methods=['POST', 'GET'])
def login_page():
    if session.get('user'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        res = wp.validate_credentials(email, password)
        if res != False:
            session['user'] = res
            return redirect(url_for("index"))
        else:
            return render_template("login.html", err_msg="Invalid Credentials", header_inc=False, page_name="Login")
    else:
        return render_template("login.html", err_msg=None, header_inc=False, page_name="Login")

@app.route("/register", methods=['POST', 'GET'])
def register_page():
    if session.get('user'):
        return redirect(url_for('index')) 
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['pass']
        res = wp.create_customer(fname, lname, email, password)
        if res:
            return redirect(url_for("get_name", name=request.form['pass']))
        else:
            return render_template("register.html", err_msg="Failed to register", header_inc=False, page_name="Register")
    else:
        return render_template("register.html", err_msg=None, header_inc=False, page_name="Register")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        pass
    else:
        return render_template("cart.html", page_name="Cart")

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        pass
    else:
        return render_template("orders.html", page_name="Orders")

@app.route("/wishlist", methods=["GET", "POST"])
def wishlist():
    if request.method == "POST":
        pass
    else:
        return render_template("wishlist.html", page_name="Wishlist")

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        pass
    else:
        return render_template("wishlist.html", page_name="Wishlist")

if __name__=="__main__":
    app.run(debug=True)