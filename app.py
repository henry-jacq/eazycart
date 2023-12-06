from flask import Flask, render_template, request, redirect, url_for, session
from config import wrapper as wp

app = Flask(__name__)

app.secret_key = "eazycart"

@app.route("/")
def index():
    if session.get('user') == None:
        return redirect(url_for('login_page')) 
    return render_template("index.html", page_name="Home", user_data=session.get('user'))

@app.route("/login", methods=['POST', 'GET'])
def login_page():
    if session.get('user'):
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        res = wp.validate_credentials(email, password)
        if res:
            session['user'] = res
            return redirect(url_for("index", user_data=res))
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

if __name__=="__main__":
    app.run(debug=True)