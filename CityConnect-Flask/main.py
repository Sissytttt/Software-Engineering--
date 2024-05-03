# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib

# Initialize the app from Flask
# 首先引入了Flask包，并创建一个Web应用的实例”app”
app = Flask(__name__, template_folder="templates", static_folder="templates/static")  # template location

# Configure MySQL
# 数据库对象
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='software_engineering',  # db name
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# ---------------------------------------------------------------
# --------------------------------------------------------------
# Define a route to hello function
# 表示地址为“/”路径时就调用下方的函数
@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

# -----------------------------------------------------------
# --------------------------------------------------------------

# search
@app.route("/public_place_search", methods=['GET', 'POST'])
def public_place_search():
    return render_template('place_search.html')


@app.route('/place_search', methods=['GET', 'POST'])
def place_search():
    city = request.form["city"]  # now required to fill in
    name = request.form["name"]  # now required to fill in    type str

    cursor = conn.cursor()

    # executes query

    if len(city) == 0:
        query = 'SELECT * FROM place WHERE name = %s '
        cursor.execute(query, (name))

    else:
        query = 'SELECT * FROM place WHERE name = %s and city = %s '
        cursor.execute(query, (name, city))

    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchall()  # list(dict())
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if len(data) > 0:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        return render_template("place_search.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such place'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("place_search.html", error=error)
      
@app.route("/public_event_search", methods=['GET', 'POST'])
def public_event_search():
    return render_template('event_search.html')


@app.route('/event_search', methods=['GET', 'POST'])
def event_search():
    name = request.form["name"]  # now required to fill in    type str
    time = request.form["time"]  # required
    score = request.form["score"] # optional
    price = request.form["price"] # optional

    cursor = conn.cursor()

    # executes query

    if len(price) == 0:
        if len(score) == 0:
            query = 'SELECT * FROM event WHERE name = %s and time > %s '
            cursor.execute(query, (name, time))
        else:
            query = 'SELECT * FROM event WHERE name = %s and time > %s  and score > %s '
            cursor.execute(query, (name, time, score))

    else:
        if len(score) == 0:
            query = 'SELECT * FROM event WHERE name = %s and time > %s and price < %s'
            cursor.execute(query, (name, time, price))
        else:
            query = 'SELECT * FROM event WHERE name = %s and time > %s and score > %s and price < %s'
            cursor.execute(query, (name, time, score, price))

    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchall()  # list(dict())
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if len(data) > 0:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        return render_template("event_search.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such event'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("event_search.html", error=error)

# view map
@app.route("/public_view_map", methods=['GET', 'POST'])
def public_view_map():
    return render_template('view_map.html')


@app.route('/view_map', methods=['GET', 'POST'])
def view_map():
    username = request.form["username"]  # now required to fill in

    cursor = conn.cursor()

    # executes query
    query = 'SELECT p.website FROM place as p, map as m, client as c WHERE c.username = %s '\
            'and c.id = m.client_id and p.id = m.place_id'
    cursor.execute(query, (username))

    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchall()  # list(dict())
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if len(data) > 0:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        return render_template("view_map.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such place'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("view_map.html", error=error)
      
# # register
# @app.route('/register_client')
# def register_client():
#     return render_template('register/register_client.html')

# # Authenticates the register
# @app.route('/registerAuth_client', methods=['GET', 'POST'])
# def registerAuth_client():
#     # grabs information from the forms
#     username = request.form['username']
#     password = request.form['password']
#     name = request.form['name']
#     phone = request.form['phone']
#     city = request.form['city']

#     # cursor used to send queries
#     cursor = conn.cursor()

#     # executes query
#     query = 'SELECT username FROM client WHERE username = %s'  # check for no same username
#     cursor.execute(query, (username))
#     # stores the results in a variable
#     data = cursor.fetchone()
#     # use fetchall() if you are expecting more than 1 data row
#     error = None

#     if (data):
#         # If the previous query returns data, then user exists
#         error = "This user already exists"
#         return render_template('register/register_.html', error=error)

#     else:
#         ins = 'INSERT INTO client VALUES(%s, MD5(%s), %s, %s, %s)'
#         cursor.execute(ins, (username, password, name, phone, city))
#         conn.commit()
#         cursor.close()
#         return render_template('index.html')


    

# --------------------------------------------------------------------------
# # log in
# # @app.route('/log_in_bo')
# # def log_in_bo():
# #     return render_template('log_in/log_in_client.html')

# # Authenticates the login
# # 既可以向外展示，也可以获取数据
# @app.route('/client_auth', methods=['GET', 'POST'])
# def loginAuth_client():
#     # grabs information from the forms
#     # get
#     username = request.form["username"]  # 对应html 文件的form class
#     password = request.form['password']

#     # cursor used to send queries
#     # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
#     cursor = conn.cursor()

#     # executes query
#     query = 'SELECT * FROM client WHERE email = %s and password = MD5(%s)'
#     cursor.execute(query, (username, password))
#     # stores the results in a variable
#     # fetchone 即每次只读一行
#     data = cursor.fetchone()
#     # use fetchall() if you are expecting more than 1 data row
#     cursor.close()
#     error = None
#     # if data is not none
#     if data is not None:
#         # creates a session for the the user
#         # 创造一个会话
#         # session is a built in
#         session['username'] = username
#         return redirect('/client_home')  # a url in app.route
#     else:
#         # returns an error message to the html page
#         error = 'Invalid username or password'
#         # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
#         return render_template("log_in/log_in_client.html", error=error)


# # log in
# @app.route('/log_in_client')
# def log_in_client():
#     return render_template('log_in/log_in_client.html')

# # Authenticates the login
# # 既可以向外展示，也可以获取数据
# @app.route('/client_auth', methods=['GET', 'POST'])
# def loginAuth_client():
#     # grabs information from the forms
#     # get
#     username = request.form["username"]  # 对应html 文件的form class
#     password = request.form['password']

#     # cursor used to send queries
#     # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
#     cursor = conn.cursor()

#     # executes query
#     query = 'SELECT * FROM client WHERE email = %s and password = MD5(%s)'
#     cursor.execute(query, (username, password))
#     # stores the results in a variable
#     # fetchone 即每次只读一行
#     data = cursor.fetchone()
#     # use fetchall() if you are expecting more than 1 data row
#     cursor.close()
#     error = None
#     # if data is not none
#     if data is not None:
#         # creates a session for the the user
#         # 创造一个会话
#         # session is a built in
#         session['username'] = username
#         return redirect('/client_home')  # a url in app.route
#     else:
#         # returns an error message to the html page
#         error = 'Invalid username or password'
#         # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
#         return render_template("log_in/log_in_client.html", error=error)


      
# # -------------------------------------------------------------

# @app.route('/client_home')
# def client_home():
#     return render_template('client_page/client_home.html', username=session['username'])


# # @app.route("/client_place_search", methods=['GET', 'POST'])
# # def client_place_search():
# #     return render_template('place_search.html')
  

# # @app.route("/client_event_search", methods=['GET', 'POST'])
# # def client_event_search():
# #     return render_template('event_search.html')

# @app.route("/register_event", methods=['GET', 'POST']) 
# def register_event():
#     username = request.form["username"]
#     id = request.form["id"]

#     cursor = conn.cursor()
#     query = 'SELECT * FROM event WHERE id = %s'
#     cursor.execute(query, (id))
#     data = cursor.fetchall()  # list(dict())
#     event_id = data['id']
   
#     query_client = "SELECT id FROM client WHERE username = %s"
#     cursor.execute(query_client, (username,))
#     client_result = cursor.fetchone()
#     client_id = client_result['id']
    
#     if event_id is None:
#         error = "Sorry, no such event exists!"
#         return render_template("client_home/register_event.html", error=error)
      
#     query_check_registration = 'SELECT p.id FROM event as e, participate as p, client as c '\
#         'WHERE c.username = %s AND c.id = p.client_id AND e.id = p.event_id'
#     cursor.execute(query_check_registration, (username, event_id))
#     registration = cursor.fetchone()

#     if registration:
#         error = "You are already registered for this event."
#         return render_template("client_home/register_event.html", error=error)

#     # Register the user for the event
#     query_register = 'INSERT INTO participate (client_id, event_id) VALUES (%s, %s)'
#     cursor.execute(query_register, (client_id, event_id))
#     conn.commit()  # Commit to save the changes

#     success_message = "You have successfully registered for the event."
#     return render_template("client_home/register_event.html", success=success_message)

      
# @app.route("/cancel_register", methods=['GET', 'POST'])
# def cancle_register():
#     username = request.form["username"]
#     id = request.form["id"]

#     # Create a database cursor
#     cursor = conn.cursor()

#     # Check if the event exists
#     query_check_event = 'SELECT * FROM event WHERE id = %s'
#     cursor.execute(query_check_event, (id))
#     event = cursor.fetchall()
#     event_id = event['id']
   
#     query_client = "SELECT id FROM client WHERE username = %s"
#     cursor.execute(query_client, (username,))
#     client_result = cursor.fetchone()
#     client_id = client_result['id']

#     if event_id is None:
#         error = "Event not found."
#         return render_template("client_home/cancel_register.html", error=error)

#     # Check if the user is registered for the event
#     query_check_registration = "SELECT p.id FROM participate as p, client as c, event as e WHERE c.username = %s AND c.id = p.client_id AND p.event_id = %s"
#     cursor.execute(query_check_registration, (username, event_id))
#     registration = cursor.fetchone()

#     if registration is None:
#         error = "No registration found for this user and event."
#         return render_template("client_home/cancel_register.html", error=error)

#     # If the event and registration exist, delete the registration
#     query_delete_registration = 'DELETE FROM participate WHERE client_id = %s AND event_id = %s'
#     cursor.execute(query_delete_registration, (client_id, event_id))
#     conn.commit()  # Commit the transaction to make sure changes are saved

#     success_message = "Registration cancelled successfully."
#     return render_template("client_home/cancel_register.html", success=success_message)
  

# @app.route('/get_followers', methods=['GET', 'POST'])
# def get_followers():
#     prime_id = request.form["prime_id"]
#     cursor = conn.cursor()
#     query = 'SELECT following_id FROM follow WHERE prime_id = %s'
#     cursor.execute(query, (prime_id))
#     data = cursor.fetchall()  # list(dict())
#     cursor.close()
    
#     return render_template("client_home/get_followers.html", posts=data)

  
# @app.route('/follow', methods=['GET', 'POST'])
# def follow():
#     owner_id = request.form["id"]
#     client_id = request.form["id"]

#     cursor = conn.cursor()
#     query = 'SELECT * FROM businessowner WHERE id = %s'
#     cursor.execute(query, (owner_id))
#     data = cursor.fetchone()
#     # owner_id = data['id']
   
#     query_client = "SELECT id FROM client WHERE username = %s"
#     cursor.execute(query_client, (client_id))
#     client_result = cursor.fetchone()
#     # client_id = client_result['id']
    
#     query_id = 'SELECT MAX(id) AS max_id FROM follow'
#     cursor.excute(query_id)
#     result = cursor.fetchone()
#     max_id = result[0] if result[0] is not None else 0
    
#     if data is None:
#         error = "Sorry, no such business owner!"
#         return render_template("client_home/follow.html", error=error)
#     if client_result is None:
#         error = "Sorry, no such user!"
#         return render_template("client_home/follow.html", error=error)
      
#     query_check_registration = 'SELECT * FROM follow WHERE following_id = %s AND prime_id = %s'
#     cursor.execute(query_check_registration, (client_id, owner_id))
#     registration = cursor.fetchone()

#     if registration:
#         error = "You are already following this business owner."
#         return render_template("client_home/follow.html", error=error)

#     # Register the user for the event
#     query_register = 'INSERT INTO participate (id, following_id, prime_id) VALUES (%s, %s)'
#     cursor.execute(query_register, (max_id + 1, client_id, owner_id))
#     conn.commit()  # Commit to save the changes 
    

# @app.route('/unfollow', methods=['GET', 'POST'])
# def unfollow():
#     business_owner = request.form["id"]
#     client = request.form["id"]
    
#     cursor = conn.cursor()

#     # Check if the user is registered for the event
#     query_check_registration = 'SELECT * FROM follow WHERE prime_id = %s AND following_id = %s'
#     cursor.execute(query_check_registration, (business_owner, client))
#     registration = cursor.fetchone()

#     if registration is None:
#         error = "You have not followed this business owner"
#         return render_template("client_home/unfollow.html", error=error)

#     # If the event and registration exist, delete the registration
#     query_delete_registration = 'DELETE FROM follow WHERE following_id = %s AND prime_id = %s'
#     cursor.execute(query_delete_registration, (client, business_owner))
#     conn.commit()  # Commit the transaction to make sure changes are saved

#     success_message = "Unfollowed successfully."
#     return render_template("client_home/follow.html", success=success_message)


# @app.route('/customer_ticket_view', methods=['GET', 'POST']) # view map
# def customer_ticket_view():
#     cursor = conn.cursor()

#     query = 'SELECT * FROM flight WHERE status = "Upcoming"'
#     cursor.execute(query)
#     data = cursor.fetchall()  # list(dict())

#     cursor.close()

#     return render_template("customer_page/customer_purchase_ticket.html", posts=data)  # a url in app.route


# @app.route('/customer_track', methods=['GET', 'POST'])
# def customer_track():
#     data3 = None
#     return render_template("customer_page/customer_track_my_spending.html", data3=data3)


# @app.route("/customer_track_my_spending", methods=['GET', 'POST'])
# def customer_track_spending():
#     username = session["username"]
#     start = request.form["start_date"]
#     end = request.form['end_date']

#     cursor = conn.cursor()

#     query1 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() AND customer_email = %s "
#     cursor.execute(query1, (username))
#     sum_past_year = cursor.fetchone()

#     query2 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN %s " \
#              "AND %s AND customer_email = %s "
#     cursor = conn.cursor()
#     cursor.execute(query2, (start, end, username))
#     sum_period = cursor.fetchone()

#     query3 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() AND customer_email = %s "
#     query4 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND customer_email = %s "
#     query5 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND customer_email = %s "
#     query6 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND customer_email = %s "
#     query7 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND customer_email = %s "
#     query8 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
#              "DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND customer_email = %s "

#     cursor = conn.cursor()
#     cursor.execute(query3, (username))
#     sum_1_month = cursor.fetchone()
#     cursor.execute(query4, (username))
#     sum_2_month = cursor.fetchone()
#     cursor.execute(query5, (username))
#     sum_3_month = cursor.fetchone()
#     cursor.execute(query6, (username))
#     sum_4_month = cursor.fetchone()
#     cursor.execute(query7, (username))
#     sum_5_month = cursor.fetchone()
#     cursor.execute(query8, (username))
#     sum_6_month = cursor.fetchone()

#     data_temp = [sum_1_month["total"], sum_2_month["total"], sum_3_month["total"], sum_4_month["total"],
#              sum_5_month["total"], sum_6_month["total"]]
#     data3 = []
#     for item in data_temp:
#         if item is None:
#             item = 0
#             data3.append(item)
#         else:
#             data3.append(int(item))

#     return render_template("customer_page/customer_track_my_spending.html", data1=sum_past_year, data2=sum_period,
#                            data3=data3)
    
# -----------------------------------------------------------
# ------------------------------------------------------------
# # event review
# @app.route('/post_event_review')
# def post_event_review():
#     return render_template('review/post_event_review.html')
  
# @app.route("/client_post_event_review", methods=['GET', 'POST']) 
# def client_post_event_review():
#     user_id = request.form["user_id"]
#     event_id = request.form["event_id"]
#     content = request.form["content"]
#     rating = request.form["rating"]
#     price = request.form["price"]

#     cursor = conn.cursor()

#     query_check = "select id from client"
#     cursor.execute(query_check)
#     check = cursor.fetchall()
#     # print(check)
#     # print(type(check[0]))

#     check1 = []
#     for item in check:
#         check1.append(item["user_id"])
#     if int(user_id) not in check1:
#         error = "Sorry, user_id not existed !"
#         return render_template("review/post_event_review.html", error=error)

#     query_check2 = 'SELECT * FROM event WHERE id = %s'
#     cursor.execute(query_check2, event_id)
#     check_f = cursor.fetchall()
#     check3 = []
#     for item in check_f:
#         check3.append(item["event_id"])
#     if int(event_id) not in check3:
#         error = "Sorry, you input a wrong event id !"
#         return render_template("review/post_event_review.html", error=error)

#     query3 = "select max(id) as next_id from review"
#     cursor.execute(query3)
#     review_id = cursor.fetchall()
#     review_id = review_id[0]["next_id"]


#     ins = 'INSERT INTO review VALUES(%s, %s, %s, %s, %s, %s, CURRENT_DATE())'
#     cursor.execute(ins, (str(review_id + 1), event_id, user_id, content, rating, price))
#     conn.commit()
#     cursor.close()
#     return render_template('client_page/client_purchase_successful.html')
  
# @app.route("/delete_review", methods=['GET', 'POST'])
# def cancle_register():
#     user_id = request.form["user_id"]
#     event_id = request.form["event_id"]

#     # Create a database cursor
#     cursor = conn.cursor()

#     query_check = "select id from client"
#     cursor.execute(query_check)
#     check = cursor.fetchall()
#     # print(check)
#     # print(type(check[0]))

#     check1 = []
#     for item in check:
#         check1.append(item["user_id"])
#     if int(user_id) not in check1:
#         error = "Sorry, user_id not existed !"
#         return render_template("client/client_home.html", error=error)

#     query_check2 = 'SELECT * FROM review WHERE event_id = %s and client_id = %s'
#     cursor.execute(query_check2, event_id, user_id)
#     check_f = cursor.fetchall()
#     if check_f is None:
#         error = "Sorry, you have not post any reviews for this event !"
#         return render_template("review/post_event_review.html", error=error)

#     # If the event and registration exist, delete the registration
#     query_delete_review = 'DELETE FROM review WHERE client_id = %s AND event_id = %s'
#     cursor.execute(query_delete_review, (user_id, event_id))
#     conn.commit()  # Commit the transaction to make sure changes are saved

#     success_message = "Review cancelled successfully."
#     return render_template("client_home/cancel_register.html", success=success_message)
# -----------------------------------------------------------

# ----------------------------------------------------------------------

@app.route('/register_bo')
def register_business_owner():
    return render_template('register/bo_register.html')

# Authenticates the register
@app.route('/register_auth_bo', methods=['GET', 'POST'])
def registerAuth_bo():
    # all required
    email = request.form["email"]
    company_name = request.form["company_name"]
    name = request.form["name"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]
    city = request.form["city"]

    cursor = conn.cursor()
    
    # check for duplicate owner
    query = 'SELECT * FROM businessowner WHERE email = %s' 
    cursor.execute(query, (email))
    data = cursor.fetchone()
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/bo_register.html', error=error)
    else:
        ins = 'INSERT INTO businessowner (email, company_name, name, password, phone_number, city) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, company_name, name, password, phone_number, city))
        conn.commit()
        cursor.close()
        flash("Register Sucessful!")
        return render_template('index.html')
    
@app.route('/login_bo')
def log_in_business_owner():
    return render_template('log_in/bo_login.html')

@app.route('/login_auth_bo', methods=['GET', 'POST'])
def loginAuth_business_owner():
    email = request.form["email"] 
    password = request.form['password']

    cursor = conn.cursor()

    query = 'SELECT * FROM businessowner WHERE email = %s and password = %s'
    cursor.execute(query, (email, password))
    data = cursor.fetchone()
   
    cursor.close()
    error = None
    if (data):
        session['email'] = email
        return redirect(url_for('bo_home'))  
    else:
        error = 'Invalid username or password'
        return render_template("log_in/bo_login.html", error=error)
    
# ------------------------------------------------------------

@app.route("/bo_home", methods=["GET"])
def bo_home():
    return render_template("bo_page/bo_home.html")

@app.route("/bo_view_event_display", methods=["GET","POST"])
def bo_view_my_event_display():
    return render_template("bo_page/bo_view_event.html")

@app.route("/bo_view_event", methods=["GET","POST"])
def bo_view_my_event():
    bo_email = session["email"]

    # get this bo_id
    cursor = conn.cursor()
    q_bo_id = "SELECT id FROM businessowner WHERE email = %s"
    cursor.execute(q_bo_id, (bo_email,))
    bo_id = cursor.fetchone()["id"]
    cursor.close()
    
    cursor = conn.cursor()
    q_get_events = "select e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name from businessowner b inner join events e on e.owner_id = b.id inner join place p on p.id = e.place_id where e.owner_id = %s"
    cursor.execute(q_get_events, (bo_id,))
    events = cursor.fetchall()
    cursor.close()
    
    if (events):
        return render_template("bo_page/bo_view_event.html",events=events)
    else:
        error = "You currently owned no event, please create one!"
        return render_template("bo_page/bo_view_event.html",error=error)

@app.route("/bo_search_event_display", methods=["GET","POST"])
def bo_search_event_display():
    return render_template("bo_page/bo_search_event.html")

@app.route("/bo_search_event_form", methods=["GET","POST"])
def bo_search_event_form():
    if request.method == "POST":
        name = request.form["name"]  # required
        time = request.form["time"]  # required
        score = request.form["score"] # optional
        price = request.form["price"] # optional

        cursor = conn.cursor()

        # executes query
        name = '%' + name + '%'
        if len(price) == 0:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name LIKE lower(%s) AND DATE(time) >= %s'
                cursor.execute(query, (name, time))
            else:
                query = 'SELECT * FROM events WHERE name like = lower(%s) and date(time) >= %s  and score >= %s '
                cursor.execute(query, (name, time, score))

        else:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name like lower(%s) and date(time) >= %s and price =< %s'
                cursor.execute(query, (name, time, price))
            else:
                query = 'SELECT * FROM events WHERE name like lower(%s) and date(time) >= %s and score >= %s and price =< %s'
                cursor.execute(query, (name, time, score, price))

        data = cursor.fetchall() 
        cursor.close()
        error = None
        if (data):
            return render_template("bo_page/bo_search_event.html", events=data) 
        else:
            error = 'No such event'
            return render_template("bo_page/bo_search_event.html", error=error)
    
# when front end finished, add the bo log out, and title as bo greeting
    

@app.route("/bo_create_event_form", methods=["GET", "POST"])
def bo_create_event_form():
    # Fetch place names from the database
    cursor = conn.cursor()
    cursor.execute("select name from place")
    place_names = [row for row in cursor.fetchall()]
    cursor.close()

    if request.method == "POST":
        bo_email = session["email"]
        event_name = request.form["e_name"]
        event_time = request.form["e_time"]
        event_descript = request.form["e_descript"]
        event_max_ppl = request.form["e_max_ppl"]
        event_current_ppl = 0
        event_score = 0
        event_price = request.form["e_price"]
        event_place = request.form["e_place"]
        print(event_place)
        event_owner = bo_email

        # get this bo_id
        cursor = conn.cursor()
        q_bo_id = "SELECT id FROM businessowner WHERE email = %s"
        cursor.execute(q_bo_id, (bo_email,))
        bo_id = cursor.fetchone()["id"]
        cursor.close()

        # event with same name by this owner cannot be created
        cursor = conn.cursor()
        q_check_ename = "SELECT name FROM events WHERE owner_id = %s"
        cursor.execute(q_check_ename, (bo_id,))
        all_event_name = cursor.fetchall() # list of dict
        cursor.close()

        # check event with the same time and location cannot be created
        cursor = conn.cursor()
        q_check_timeloc = "SELECT COUNT(id) as count FROM events WHERE time = %s AND place_id IN \
            (SELECT id FROM place WHERE name = %s)"
        cursor.execute(q_check_timeloc, (event_time, event_place))
        n_dup_event = cursor.fetchone()["count"]
        cursor.close()

        if {"name":event_name} in all_event_name or n_dup_event >= 1:
            error =  "Failed! Event already exists!"
            return render_template("bo_page/bo_home.html", error=error)
        else:
            cursor = conn.cursor()
            q_p_id = "SELECT id FROM place WHERE name = %s"
            cursor.execute(q_p_id, (event_place,))
            place_id = cursor.fetchone()
            cursor.close()

            cursor = conn.cursor()
            q_create_event = "INSERT INTO events (name, time, description, max_ppl, current_ppl, score, price, place_id, owner_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(q_create_event, (event_name, event_time, event_descript, event_max_ppl, event_current_ppl,
                                             event_score, event_price, place_id["id"], bo_id))
            conn.commit()
            cursor.close()
            message = "You have successfully created an event"
            return render_template("bo_page/bo_home.html", message=message)

    return render_template("bo_page/bo_create_event.html", place_names=place_names)


@app.route("/bo_delete_event_form", methods=["GET", "POST"])
def bo_delete_event_form():
    bo_email = session["email"]
    
    # list all events this BO has
    cursor = conn.cursor()
    q_get_events = "SELECT e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        FROM events e JOIN place p ON p.id = e.place_id WHERE e.owner_id = (SELECT DISTINCT id FROM businessowner WHERE email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        event_id = request.form["event_id"]

        cursor = conn.cursor()
        q_delete_event = "DELETE FROM events WHERE id = %s"
        cursor.execute(q_delete_event, (event_id,))
        conn.commit()
        cursor.close()

        return redirect(url_for("bo_delete_event_form"))

    # Render the delete event page with events owned by the business owner
    return render_template("bo_page/bo_delete_event_form.html", events=events)


@app.route("/bo_modify_event_form", methods=["GET", "POST"])
def bo_modify_event_form():
    bo_email = session["email"]

    # list all his event
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        from events e join place p on p.id = e.place_id where e.owner_id = (select distinct id from businessowner where email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()
    
    if request.method == "POST":
        event_name = request.form["event_name"]
        parameter_to_modify = request.form["parameter_to_modify"]
        new_value = request.form["new_value"]
        new_time = request.form["new_time"]

        if parameter_to_modify == 'time':
            new_value = new_time

        cursor = conn.cursor()
        q_n_event= "SELECT * FROM events WHERE name = %s"
        cursor.execute(q_n_event, (event_name))
        n_event = cursor.fetchall()
        cursor.close()

        # has the same event name exist:
        if (n_event):
            print(event_name)
            cursor = conn.cursor()
            q_modify_event = f"update events set {parameter_to_modify}"
            print(q_modify_event)
            q_modify_event = q_modify_event+" = %s where name = %s"
            print(q_modify_event)
            cursor.execute(q_modify_event, (new_value, event_name))
            conn.commit()
            cursor.close()

            # message = "Event modified sucesfully!"
            return redirect(url_for("bo_modify_event_form"))
        else:
            error = "Failed to modify event, duplicate event name"
            return render_template("bo_page/bo_modify_event.html", evemts=events, message=error, event_name=event_name)

    return render_template("bo_page/bo_modify_event.html", events=events)


@app.route('/bo_logout')
def bo_logout():
    session.pop('email')
    return render_template('/index.html')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)


# -----------------------------------------------------------
# ------------------------------------------------------------
# search event + view map
# search place
# log in
# register
# authentication

# client ---

# register event
# cancel register

# label and unlabel place from collection

# post event review
# delete event review
# rate event

# get followers (a table with id, follower, followee)
# follow - only follow business owner (owner - event - client)
# unfollow


# business owner ---
# create event
# update event
# delete event


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('index.html')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
