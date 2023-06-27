from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3


app = Flask(__name__)
 
 
app.secret_key = 'your secret key'


@app.route('/', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        query = "SELECT * FROM users WHERE username=? AND password=?"
        result = c.execute(query, (username, password)).fetchone()

        conn.close()

        if result:
            # The username and password are correct
            session['username'] = username
            return redirect('/Home')
        else:
            # The username and password are incorrect
            return "Incorrect username or password. Try again."

    return render_template("login.html")

@app.route('/Home')
def home():
    if 'username' in session:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT ROLL_NO,NAME,GENDER,BUS_NO,BUS_ROUTE,SEMESTER,VALID_UPTO,PHONE_NO,SEAT_NO FROM busdetails WHERE ROLL_NO='{session['username']}'")
        student_info = c.fetchone()
        conn.close()
        return render_template('index.html')#, ROLL_NO=student_info[0], NAME=student_info[1],GENDER=student_info[2],BUS_NO=student_info[3],BUS_ROUTE=student_info[4],SEMESTER=student_info[5],VALID_UPTO=student_info[6],PHONE_NO=student_info[7],SEAT_NO=student_info[8])
    return redirect('/login')

@app.route('/cart')
def cart():
    if 'men' not in session:
        session['cart']=[]
    if request.method == 'POST':
        product_id=request.form(product_id)
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f"SELECT name,price,images FROM products WHERE id='product_id'")
        product=c.fetchone()
        conn.close()
        session['cart'].append({'id' : product[0] , 'name' : product[1] , 'price' : product[2] , 'image' : product[4]})
    cart_items=session['cart']
    return render_template('cart.html', cart_items=cart_items)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
        




