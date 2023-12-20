from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from config import wrapper as wp

app = Flask(__name__)

app.secret_key = "eazycart"

@app.route("/")
def index():
    if session.get('user') == None:
        return redirect(url_for('login_page'))

    inCart = wp.product_in_cart(session['user'][0])
    wishlist = wp.product_in_wishlist(session['user'][0])
    return render_template("index.html", page_name="Home", userData=session['user'], products=wp.get_products(), inCart=inCart, wish=wishlist)

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
    total = wp.getOrderSummary(session['user'][0])
    
    if request.method == "GET":
        items = wp.get_cart_items_info(session['user'][0])
        return render_template("cart.html", page_name="Cart", inCart=cartItemsQty, cartItems=items, cart_total=total)

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        orders = wp.get_customer_orders(session['user'][0])
        return render_template("orders.html", page_name="Orders", orders=orders)
    else:
        return redirect(url_for('index'))

@app.route("/wishlist", methods=["GET", "POST"])
def wishlist():
    wlItems = wp.get_wishlist_items(session['user'][0])
    wishlist = wp.get_wishlist_items_info(session['user'][0])

    if request.method == "GET":
        return render_template("wishlist.html", page_name="Wishlist", items=wlItems, wish=wishlist)
    else:
        return redirect(url_for('index'))

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        total = wp.getOrderSummary(session['user'][0])
        return render_template("checkout.html", page_name="Checkout", cart_total=total)
    
@app.route("/checkout/review", methods=["GET", "POST"])
def reviewOrder():
    if request.method == "GET":
        total = wp.getOrderSummary(session['user'][0])
        items = wp.get_cart_items_info(session['user'][0])
        cartItemsQty = wp.get_cart_list(session['user'][0])
        return render_template("review.html", page_name="Order Review", order_total=total, products=items, qty=cartItemsQty)
    
@app.route("/checkout/confirmed", methods=["GET", "POST"])
def placeOrder():
    if request.method == "POST":
        ans = wp.create_order(session['user'][0])
        return render_template("confirm.html", page_name="Order Confirmed", user=session['user'], status=ans)
    else:
        return redirect(url_for("checkout"))

@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]
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
        customer_id = session['user'][0]
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

@app.route("/api/wishlist/add", methods=["POST"])
def add_to_wishlist():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]
        product_id = data['product_id']
        result = wp.add_to_wishlist(customer_id, product_id)
        if result:
            return jsonify({"message": True})
        return jsonify({"message": False})

@app.route("/api/wishlist/remove", methods=["POST"])
def remove_from_wishlist():
    if request.method == "POST":
        data = request.get_json()
        customer_id = session['user'][0]
        product_id = data['product_id']
        result = wp.remove_from_wishlist(customer_id, product_id)
        return jsonify({"message": result})

@app.route("/api/order/remove", methods=["POST"])
def remove_order():
    if request.method == "POST":
        data = request.get_json()
        result = wp.remove_order(data)
        return jsonify({"message": result})

if __name__=="__main__":
    app.run(debug=True)