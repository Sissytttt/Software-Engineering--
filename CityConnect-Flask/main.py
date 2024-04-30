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
                       db='db_final',  # db name
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
    full = request.form["full"]  # required
    score = request.form["score"] # optional
    price = request.form["price"] # optional

    cursor = conn.cursor()

    # executes query

    if len(price) == 0:
        if len(score) == 0:
            query = 'SELECT * FROM event WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = f.arrival_airport and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
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

# register
@app.route('/register_client')
def register_client():
    return render_template('register/register_client.html')

# Authenticates the register
@app.route('/registerAuth_client', methods=['GET', 'POST'])
def registerAuth_client():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    building = request.form['building']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    passport = request.form['passport']
    passport_exp = request.form['passport_exp']
    passport_country = request.form['passport_country']
    birth = request.form['birth']

    # cursor used to send queries
    cursor = conn.cursor()

    # executes query
    query = 'SELECT email FROM client WHERE email = %s'  # check for no same email
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/register_.html', error=error)

    else:
        ins = 'INSERT INTO client VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            username, name, password, building, street, city, state, phone, passport, passport_exp, passport_country,
            birth))
        conn.commit()
        cursor.close()
        return render_template('index.html')


      
# ----------------------------------------------------------------------

@app.route('/register_business_owner')
def register_business_owner():
    return render_template('register/register_business_owner.html')


# Authenticates the register
@app.route('/registerAuth_business_owner', methods=['GET', 'POST'])
def registerAuth_owner():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    airline = request.form["airline"]

    # cursor used to send queries
    cursor = conn.cursor()

    # executes query
    query = 'SELECT email FROM business_owner WHERE email = %s'  # check for no same email
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/register_business_owner.html', error=error)

    else:
        # check if this airline exists in the db, foreign constraints
        check_airline = 'SELECT airline_name FROM airline where %s in (select airline_name FROM airline)'
        cursor.execute(check_airline, (airline))
        check_data = cursor.fetchall()

        if len(check_data) == 0:
            ins = 'INSERT INTO airline VALUES(%s)'
            cursor.execute(ins, (airline))

        query = 'SELECT max(business_owner_id) as id FROM business_owner'  # check for no same email
        cursor.execute(query)
        # stores the results in a variable
        data2 = cursor.fetchone()

        ins = 'INSERT INTO business_owner VALUES(%s, MD5(%s), %s)'
        cursor.execute(ins, (username, password, str(int(data2['id']) + 1)))

        ins = 'INSERT INTO business_owner_work_for VALUES(%s, %s)'
        cursor.execute(ins, (username, airline))

        conn.commit()
        cursor.close()
        return render_template('index.html')


# --------------------------------------------------------------------------
# log in
@app.route('/log_in_client')
def log_in_client():
    return render_template('log_in/log_in_client.html')

# Authenticates the login
# 既可以向外展示，也可以获取数据
@app.route('/client_auth', methods=['GET', 'POST'])
def loginAuth_client():
    # grabs information from the forms
    # get
    username = request.form["username"]  # 对应html 文件的form class
    password = request.form['password']

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query
    query = 'SELECT * FROM client WHERE email = %s and password = MD5(%s)'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if data is not None:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        session['username'] = username
        return redirect('/client_home')  # a url in app.route
    else:client
        # returns an error message to the html page
        error = 'Invalid username or password'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("log_in/log_in_client.html", error=error)


      
# -------------------------------------------------------------

@app.route('/client_home')
def client_home():
    return render_template('client_page/client_home.html', username=session['username'])


@app.route("/client_flight_search", methods=['GET', 'POST'])
def client_flight_search():
    return render_template('client_page/client_flight_search.html')


@app.route('/client_search', methods=['GET', 'POST'])
def client_search():
    dept_city = request.form["dept_city"]  # now required to fill in
    dept_airport = request.form["dept_airport"]
    arrival_city = request.form["arrival_city"]  # now required to fill in    type str
    arrival_airport = request.form["arrival_airport"]
    date = request.form["date"]  # now required to fill in

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query

    if len(dept_airport) == 0:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = f.arrival_airport and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = %s and f.departure_time > %s  and a1.airport_city = ' \
                    '%s and a2.airport_city = %s '
            cursor.execute(query, (arrival_airport, date, dept_city, arrival_city))
    else:
        query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                '%s and f.arrival_airport = %s and f.departure_time > %s  and ' \
                'a1.airport_city = %s and a2.airport_city = %s '
        cursor.execute(query, (dept_airport, arrival_airport, date, dept_city, arrival_city))

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
        return render_template("client_page/client_search_result.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such flight'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("client_page/client_flight_search.html", error=error)


@app.route('/customer_display_purchased', methods=['GET', 'POST'])
def customer_display_purchased():
    username = session['username']
    cursor = conn.cursor()
    query = "SELECT p.purchase_date, t.flight_num, t.airline_name FROM purchases as p, ticket as t WHERE p.ticket_id " \
            "= t.ticket_id and p.customer_email = %s "
    cursor.execute(query, (username))
    data = cursor.fetchall()  # list(dict())
    cursor.close()
    if len(data) == 0:
        error = "You don't have a purchase record"
        return render_template("customer_page/customer_display_purchased.html", error=error)
    else:
        return render_template("customer_page/customer_display_purchased.html", posts=data)  # a url in app.route

@app.route('/customer_ticket_view', methods=['GET', 'POST']) # view map
def customer_ticket_view():
    cursor = conn.cursor()

    query = 'SELECT * FROM flight WHERE status = "Upcoming"'
    cursor.execute(query)
    data = cursor.fetchall()  # list(dict())

    cursor.close()

    return render_template("customer_page/customer_purchase_ticket.html", posts=data)  # a url in app.route


@app.route("/customer_purchase_ticket", methods=['GET', 'POST']) #rsvp add to map
def customer_purchase_ticket():
    username = request.form["username"]
    flight_num = request.form["flight_num"]

    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE status = "Upcoming"'
    cursor.execute(query)
    data = cursor.fetchall()  # list(dict())


    query_check = "select email from customer"
    cursor.execute(query_check)
    check = cursor.fetchall()
    # print(check)
    # print(type(check[0]))

    check2 = []
    for item in check:
        check2.append(item["email"])
    if username not in check2:
        error = "Sorry, you are booking ticket for someone not registered !"
        return render_template("customer_page/customer_purchase_ticket.html", posts=data, error=error)

    query_check2 = "select flight_num from flight"
    cursor.execute(query_check2)
    check_f = cursor.fetchall()
    check3 = []
    for item in check_f:
        check3.append(item["flight_num"])
    if int(flight_num) not in check3:
        error = "Sorry, you input a wrong flight number !"
        return render_template("customer_page/customer_purchase_ticket.html", posts=data, error=error)


    # check seat availability
    query1 = "select count(ticket_id) as c from ticket where flight_num = %s"
    cursor.execute(query1, (flight_num))
    current_occupied = cursor.fetchall()  # list(dict())

    query2 = "select seats from flight as f, airplane as a where a.airplane_id = f.airplane_id and flight_num = %s"
    cursor.execute(query2, (flight_num))
    available = cursor.fetchall()  # list(dict())

    if current_occupied[0]["c"] < available[0]["seats"]:
        query3 = "select max(ticket_id) as next_id from purchases"
        cursor.execute(query3)
        ticket_id = cursor.fetchall()
        ticket_id = ticket_id[0]["next_id"]

        query_n = "select distinct airline_name from flight where flight_num = %s"
        cursor.execute(query_n, (flight_num))
        airline = cursor.fetchall()

        ins2 = 'INSERT INTO  ticket VALUES(%s, %s , %s)'
        cursor.execute(ins2, (str(ticket_id + 1), airline[0]["airline_name"], flight_num))

        ins1 = 'INSERT INTO purchases VALUES(%s, %s, NULL, CURRENT_DATE())'
        cursor.execute(ins1, (str(ticket_id + 1), username))
        conn.commit()
        cursor.close()
        return render_template('customer_page/customer_purchase_successful.html')
    else:
        error = "Sorry, there is no vacant seat on this flight !"
        return render_template('customer_page/customer_purchase_ticket.html', posts=data, error=error)


@app.route('/customer_track', methods=['GET', 'POST'])
def customer_track():
    data3 = None
    return render_template("customer_page/customer_track_my_spending.html", data3=data3)


@app.route("/customer_track_my_spending", methods=['GET', 'POST'])
def customer_track_spending():
    username = session["username"]
    start = request.form["start_date"]
    end = request.form['end_date']

    cursor = conn.cursor()

    query1 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() AND customer_email = %s "
    cursor.execute(query1, (username))
    sum_past_year = cursor.fetchone()

    query2 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN %s " \
             "AND %s AND customer_email = %s "
    cursor = conn.cursor()
    cursor.execute(query2, (start, end, username))
    sum_period = cursor.fetchone()

    query3 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() AND customer_email = %s "
    query4 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND customer_email = %s "
    query5 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND customer_email = %s "
    query6 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND customer_email = %s "
    query7 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND customer_email = %s "
    query8 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE purchase_date BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND customer_email = %s "

    cursor = conn.cursor()
    cursor.execute(query3, (username))
    sum_1_month = cursor.fetchone()
    cursor.execute(query4, (username))
    sum_2_month = cursor.fetchone()
    cursor.execute(query5, (username))
    sum_3_month = cursor.fetchone()
    cursor.execute(query6, (username))
    sum_4_month = cursor.fetchone()
    cursor.execute(query7, (username))
    sum_5_month = cursor.fetchone()
    cursor.execute(query8, (username))
    sum_6_month = cursor.fetchone()

    data_temp = [sum_1_month["total"], sum_2_month["total"], sum_3_month["total"], sum_4_month["total"],
             sum_5_month["total"], sum_6_month["total"]]
    data3 = []
    for item in data_temp:
        if item is None:
            item = 0
            data3.append(item)
        else:
            data3.append(int(item))

    return render_template("customer_page/customer_track_my_spending.html", data1=sum_past_year, data2=sum_period,
                           data3=data3)
    
# -----------------------------------------------------------
# ------------------------------------------------------------


@app.route('/log_in_business_owner')
def log_in_business_owner():
    return render_template('log_in/log_in_business_owner.html')


# Authenticates the login
# 既可以向外展示，也可以获取数据
@app.route('/business_owner_auth', methods=['GET', 'POST'])
def loginAuth_business_owner():
    # grabs information from the forms
    # get
    username = request.form["username"]  # 对应html 文件的form class
    password = request.form['password']

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query
    # query = 'SELECT * FROM booking_agent_work_for as a, booking_agent as b WHERE a.email = b.email ' \
    #         'and b.email = %s and b.password = MD5(%s) '
    query = 'SELECT * FROM business_owner WHERE email = %s and password = MD5(%s) '
    # and a.airline_name = "Jet Blue"
    cursor.execute(query, (username, password))
    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if (data):
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        session['username'] = username
        return redirect('/business_owner_home')  # a url in app.route
    else:
        # returns an error message to the html page
        error = 'Invalid username or password'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("log_in/log_in_business_owner.html", error=error)


@app.route('/business_owner_home')
def business_owner_home():
    return render_template('business_owner_page/business_owner_home.html', username=session['username'])


@app.route("/business_owner_flight_search", methods=['GET', 'POST'])
def business_owner_flight_search():
    return render_template('business_owner_page/business_owner_flight_search.html')


@app.route('/business_owner_search', methods=['GET', 'POST'])
def business_owner_search():
    dept_city = request.form["dept_city"]  # now required to fill in
    dept_airport = request.form["dept_airport"]
    arrival_city = request.form["arrival_city"]  # now required to fill in    type str
    arrival_airport = request.form["arrival_airport"]
    date = request.form["date"]  # now required to fill in

    cursor = conn.cursor()

    # executes query


    if len(dept_airport) == 0:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = f.arrival_airport and f.departure_time >= %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = %s and f.departure_time >= %s  and a1.airport_city = ' \
                    '%s and a2.airport_city = %s '
            cursor.execute(query, (arrival_airport, date, dept_city, arrival_city))
    else:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    '%s and f.arrival_airport = f.arrival_airport and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (dept_airport, date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    '%s and f.arrival_airport = %s and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (dept_airport, arrival_airport, date, dept_city, arrival_city))

    data = cursor.fetchall()  # list(dict())
    cursor.close()
    error = None
    if len(data) > 0:
        return render_template("business_owner_page/business_owner_search_result.html", posts=data)  # a url in app.route
    if len(data) == 0:
        error = 'no such flight'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("business_owner_page/business_owner_flight_search.html", error=error)


# -----------------------------------------------------------
# ------------------------------------------------------------
search event + view map
search place
log in
register
authentication

client ---

register event
cancel register

label and unlabel place from collection

post event review
delete event review
rate event

get followers (a table with id, follower, followee)
follow - only follow business owner (owner - event - client)
unfollow


business owner ---
create event
update event
delete event


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
