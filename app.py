from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from config import wrapper as wp

app = Flask(__name__)

app.secret_key = "eazycart"

@app.route("/")
def index():
    if session.get('user') == None:
        return redirect(url_for('login_page'))

    inCart = wp.product_in_cart(session['user'][0])
    # Can't add the product quantity
    return render_template("index.html", page_name="Home", userData=session['user'], products=wp.get_products(), inCart=inCart)

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
            return render_template("login.html", err_msg="Invalid credentials!", header_inc=False, page_name="Login")
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
            return redirect(url_for("login_page"))
        else:
            return render_template("register.html", err_msg="Failed to register!", header_inc=False, page_name="Register")
    else:
        return render_template("register.html", err_msg=None, header_inc=False, page_name="Register")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/cart", methods=["GET", "POST"])
def cart():
    # Products in cart
    cartItemsQty = wp.get_cart_list(session['user'][0])
    
    if request.method == "GET":
        items = wp.get_cart_items_info(session['user'][0])
        return render_template("cart.html", page_name="Cart", inCart=cartItemsQty, cartItems=items)

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
        return render_template("checkout.html", page_name="Checkout")

@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]  # Assuming 'user' is a key in the session
        product_id = data['product_id']
        product_qty = data['product_qty']
        result = wp.add_item_to_cart(customer_id, product_id, product_qty)
        if result:
            return jsonify({"message": True})
        return jsonify({"message": False})

@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]  # Assuming 'user' is a key in the session
        product_id = data['product_id']
        result = wp.remove_from_cart(customer_id, product_id)
        return jsonify({"message": result})
    
@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]
        result = wp.update_cart_items(customer_id, data)
        return jsonify({"message": result})

if __name__=="__main__":
    app.run(debug=True)