# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib

# Initialize the app from Flask
app = Flask(__name__, template_folder="templates", static_folder="templates/static")  # template location

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='software_engineering',  # db name
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# ---------------------------------------------------------------
# --------------------------------------------------------------
# Define a route to hello function
@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('/index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("log_in/log_in.html")

# ---------------------------------------------------------------
# --------------------------------------------------------------
# public search event: before search
@app.route("/public_event_search", methods=["GET","POST"])
def public_search_event_display():
    """
    Display the viw event display page
    
    This is an auxiliary function that shows the page that anyone can choose the event he want to search before login. 

    Returns:
        str: Rendered HTML template for the search event display page.
    """
    return render_template("public_search_event.html")


# bo search event: after search
@app.route("/public_search_event_form", methods=["GET","POST"])
def public_search_event_form():
    """
    Processes the search for events based on user input.

    Retrieves search parameters from the form, constructs and executes 
        a SQL query to search for events matching the criteria, and renders 
        the search results or an error message.

    :return: Renders the event search results or an error message.
    :rtype: str
    """

    if request.method == "POST":
        name = request.form["name"]  # required
        time = request.form["time"]  # required
        score = request.form["score"] # optional
        price = request.form["price"] # optional

        cursor = conn.cursor()

        # case
        if len(price) == 0:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s '
                cursor.execute(query, ("%"+name+"%", time))
            else:
                query = 'SELECT * FROM events WHERE like = %s and date(time) > %s  and score > %s '
                cursor.execute(query, ("%"+name+"%", time, score))
        else:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s and price < %s'
                cursor.execute(query, ("%"+name+"%", time, price))
            else:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s and score > %s and price < %s'
                cursor.execute(query, ("%"+name+"%", time, score, price))

        # get result
        data = cursor.fetchall() 
        cursor.close()
        error = None

        if (data):
            return render_template("public_search_event.html", events=data) 
        else:
            error = 'No such event'
            return render_template("public_search_event.html", error=error)

# public search place: before search
@app.route("/public_place_search", methods=['GET', 'POST'])
def public_search_place_display():
    """
    Display the viw place display page
    
    This is an auxiliary function that shows the page that anyone can choose the event he want to search before login. 

    Returns:
        str: Rendered HTML template for the search event display page.
    """
    return render_template('public_search_place.html')


@app.route('/public_search_place_form', methods=['GET', 'POST'])
def public_search_place_form():
    """
    Processes the search for places based on user input.

    Retrieves search parameters from the form, constructs and executes 
        a SQL query to search for places matching the criteria, and renders 
        the search results or an error message.

    :return: Renders the place search results or an error message.
    :rtype: str
    """

    city = request.form["city"]  # required
    name = request.form["name"]  # required

    cursor = conn.cursor()

    query = 'SELECT * FROM place WHERE name = %s and city = %s '
    cursor.execute(query, (name, city))

    data = cursor.fetchall() 
    cursor.close()
    error = None
    # if data is not none
    if (data):
        return render_template("public_search_place.html", places=data)  # a url in app.route
    else:
        error = 'no such place'
        return render_template("public_search_place.html", error=error)
      

# view map
@app.route("/public_view_map", methods=['GET', 'POST'])
def public_view_map():
    return render_template('/client_home/view_map.html')


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
        return render_template("/client_home/view_map.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such place'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("/client_home/view_map.html", error=error)
   
# -----------------------------------------------------------
# --------------------------------------------------------------
# before resgister
@app.route('/register_client')
def register_client():
    """
    Display the register
    
    This is an auxiliary function that helps display the client register page before authentication.

    Returns:
        str: Rendered HTML template for the registration page.
    """

    return render_template('register/client_register.html')

# Authenticates the register for client
@app.route('/register_auth_client', methods=['GET', 'POST'])
def registerAuth_client():
    """
    Authenticates the register
    
    Authenticates the registration of a client. Extracts required information such as email, name, password, phone number, and city
        from the request form. Checks for duplicate client in the database. If the user already exists, renders the registration 
        template with an error message. Otherwise, inserts the new client's information into the database and redirects to the 
        index page after successful registration.

    Returns:
        str: Rendered HTML template for the registration page / homepage.
    """

    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]
    city = request.form["city"]

    cursor = conn.cursor()
    # check for duplicate owner
    query = 'SELECT * FROM client WHERE email = %s' 
    cursor.execute(query, (email))
    data = cursor.fetchone()
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/client_register.html', error=error)
    else:
        ins = 'INSERT INTO businessowner (email, name, password, phone_number, city) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, name, password, phone_number, city))
        conn.commit()
        cursor.close()
        flash("Register Sucessful!")
        return render_template('index.html')

# ----------------------------------------------------------------------    
# before log in
@app.route('/login_client')
def log_in_client():
    """
    Display the log in
    
    This is an auxiliary function that helps display the client log in page before authentication.

    Returns:
        str: Rendered HTML template for the log in page.
    """
    return render_template('log_in/client_login.html')


# Authenticates the log in for business owner
@app.route('/login_auth_client', methods=['GET', 'POST'])
def loginAuth_client():
    """
    Authenticates client login.

    Retrieves email and password from the form, queries the database
        to validate credentials, and redirects to the client home
        page if authentication succeeds. Otherwise, renders the login page
        with an error message.

    :return: Redirects to the client home page if login is successful, 
             otherwise renders the login page with an error message.
    :rtype: str
    """

    email = request.form["email"] 
    password = request.form['password']
    cursor = conn.cursor()

    query = 'SELECT * FROM client WHERE email = %s and password = %s'
    cursor.execute(query, (email, password))
    data = cursor.fetchone()
    cursor.close()
    error = None

    if (data):
        session['email'] = email
        return redirect(url_for('client_home'))  
    else:
        error = 'Invalid username or password'
        return render_template("log_in/client_login.html", error=error)
    
# ----------------------------------------------------------------------    

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------  

      
# -------------------------------------------------------------

@app.route('/client_home')
def client_home():
    return render_template('/client_home/client_home.html', username=session['username'])


# @app.route("/client_place_search", methods=['GET', 'POST'])
# def client_place_search():
#     return render_template('place_search.html')
  

# @app.route("/client_event_search", methods=['GET', 'POST'])
# def client_event_search():
#     return render_template('event_search.html')

@app.route("/register_event", methods=['GET', 'POST']) 
def register_event():
    username = request.form["username"]
    id = request.form["id"]

    cursor = conn.cursor()
    query = 'SELECT * FROM event WHERE id = %s'
    cursor.execute(query, (id))
    data = cursor.fetchall()  # list(dict())
    event_id = data['id']
   
    query_client = "SELECT id FROM client WHERE username = %s"
    cursor.execute(query_client, (username,))
    client_result = cursor.fetchone()
    client_id = client_result['id']
    
    if event_id is None:
        error = "Sorry, no such event exists!"
        return render_template("/client_home/event_search.html", error=error)
      
    query_check_registration = 'SELECT p.id FROM event as e, participate as p, client as c '\
        'WHERE c.username = %s AND c.id = p.client_id AND e.id = p.event_id'
    cursor.execute(query_check_registration, (username, event_id))
    registration = cursor.fetchone()

    if registration:
        error = "You are already registered for this event."
        return render_template("/client_home/event_search.html", error=error)

    # Register the user for the event
    query_register = 'INSERT INTO participate (client_id, event_id) VALUES (%s, %s)'
    cursor.execute(query_register, (client_id, event_id))
    conn.commit()  # Commit to save the changes

    success_message = "You have successfully registered for the event."
    return render_template("/client_home/event_search.html", success=success_message)

      
@app.route("/cancel_register", methods=['GET', 'POST'])
def cancle_register():
    username = request.form["username"]
    id = request.form["id"]
    cursor = conn.cursor()

    # Check if the event exists
    query_check_event = 'SELECT * FROM event WHERE id = %s'
    cursor.execute(query_check_event, (id))
    event = cursor.fetchall()
    event_id = event['id']
    query_client = "SELECT id FROM client WHERE username = %s"
    cursor.execute(query_client, (username,))
    client_result = cursor.fetchone()
    client_id = client_result['id']

    if event_id is None:
        error = "Event not found."
        return render_template("/client_home/event_search.html", error=error)

    # Check if the user is registered for the event
    query_check_registration = "SELECT p.id FROM participate as p, client as c, event as e WHERE c.username = %s AND c.id = p.client_id AND p.event_id = %s"
    cursor.execute(query_check_registration, (username, event_id))
    registration = cursor.fetchone()
    if registration is None:
        error = "No registration found for this user and event."
        return render_template("/client_home/event_search.html", error=error)

    # If the event and registration exist, delete the registration
    query_delete_registration = 'DELETE FROM participate WHERE client_id = %s AND event_id = %s'
    cursor.execute(query_delete_registration, (client_id, event_id))
    conn.commit()
    success_message = "Registration cancelled successfully."
    return render_template("/client_home/event_search.html", success=success_message)
  

# @app.route('/get_followers', methods=['GET', 'POST'])
# def get_followers():
#     prime_id = request.form["prime_id"]
#     cursor = conn.cursor()
#     query = 'SELECT following_id FROM follow WHERE prime_id = %s'
#     cursor.execute(query, (prime_id))
#     data = cursor.fetchall()
#     cursor.close()
    
#     return render_template("/client_home/client_view_follow.html", posts=data)

@app.route('/client_view_follow', methods=['GET', 'POST'])
def get_following():
    following_id = request.form["following_id"]
    cursor = conn.cursor()
    query = 'SELECT prime_id FROM follow WHERE following_id = %s'
    cursor.execute(query, (following_id))
    data = cursor.fetchall()
    cursor.close()
    
    return render_template("/client_home/client_view_follow.html", posts=data)

  
@app.route('/client_follow_bo', methods=['GET', 'POST'])
def follow():
    owner_id = request.form["id"]
    client_id = request.form["id"]

    cursor = conn.cursor()
    query = 'SELECT * FROM businessowner WHERE id = %s'
    cursor.execute(query, (owner_id))
    data = cursor.fetchone()
   
    query_client = "SELECT id FROM client WHERE username = %s"
    cursor.execute(query_client, (client_id))
    client_result = cursor.fetchone()
    
    query_id = 'SELECT MAX(id) AS max_id FROM follow'
    cursor.excute(query_id)
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else 0
    
    if data is None:
        error = "Sorry, no such business owner!"
        return render_template("/client_home/client_view_bo.html", error=error)
    if client_result is None:
        error = "Sorry, no such user!"
        return render_template("/client_home/client_view_bo.html", error=error)
      
    query_check_registration = 'SELECT * FROM follow WHERE following_id = %s AND prime_id = %s'
    cursor.execute(query_check_registration, (client_id, owner_id))
    registration = cursor.fetchone()

    if registration:
        error = "You are already following this business owner."
        return render_template("/client_home/client_view_bo.html", error=error)

    query_register = 'INSERT INTO participate (id, prime_id, following_id) VALUES (%s, %s)'
    cursor.execute(query_register, (max_id + 1, owner_id, client_id))
    conn.commit() 
    

@app.route('/client_unfollow_bo', methods=['GET', 'POST'])
def unfollow():
    business_owner = request.form["id"]
    client = request.form["id"]
    
    cursor = conn.cursor()

    query_check_registration = 'SELECT * FROM follow WHERE prime_id = %s AND following_id = %s'
    cursor.execute(query_check_registration, (business_owner, client))
    registration = cursor.fetchone()

    if registration is None:
        error = "You have not followed this business owner"
        return render_template("/client_home/client_view_bo.html", error=error)

    query_delete_registration = 'DELETE FROM follow WHERE following_id = %s AND prime_id = %s'
    cursor.execute(query_delete_registration, (client, business_owner))
    conn.commit()


@app.route('/client_view_event', methods=['GET', 'POST'])
def client_view_event():
    client_id = request.form.get('client_id')
    cursor = conn.cursor()
    query = 'SELECT event_id FROM participate WHERE client_id = %s'
    cursor.execute(query, (client_id,))
    events = cursor.fetchall()

    cursor.close()

    if not events:
        return render_template("/client_home/client_view_event.html", message="No events found for this client.")
    
    return render_template("/client_home/client_view_event.html", events=events)

@app.route('/client_view_review', methods=['GET', 'POST'])
def client_view_review():
    client_id = request.form.get('client_id')
    cursor = conn.cursor()
    query = 'SELECT event_id, content, rating FROM review WHERE client_id = %s'
    cursor.execute(query, (client_id,))
    reviews = cursor.fetchall()

    cursor.close()

    if not reviews:
        return render_template("/client_home/client_view_review.html", message="No event reviews found for this client.")
    
    return render_template("/client_home/client_view_review.html", reviews=reviews)

@app.route('/client_label_place_to_map', methods=['GET', 'POST'])
def label():
    client_id = request.form["id"]
    place_id = request.form["id"]

    cursor = conn.cursor()
    query = 'SELECT * FROM place WHERE id = %s'
    cursor.execute(query, (place_id))
    data = cursor.fetchone()
   
    query_client = "SELECT id FROM client WHERE id = %s"
    cursor.execute(query_client, (client_id))
    client_result = cursor.fetchone()
    
    query_id = 'SELECT MAX(id) AS max_id FROM map'
    cursor.excute(query_id)
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else 0
    
    if data is None:
        error = "Sorry, no such place!"
        return render_template("/client_home/view_map.html", error=error)
    if client_result is None:
        error = "Sorry, no such user!"
        return render_template("/client_home/view_map.html", error=error)
      
    query_check_registration = 'SELECT * FROM map WHERE client_id = %s AND place_id = %s'
    cursor.execute(query_check_registration, (client_id, place_id))
    registration = cursor.fetchone()

    if registration:
        error = "You have already labeled this place."
        return render_template("/client_home/view_map.html", error=error)

    query_register = 'INSERT INTO map (id, client_id, place_id) VALUES (%s, %s)'
    cursor.execute(query_register, (max_id + 1, client_id, place_id))
    conn.commit()


@app.route('/unlabel', methods=['GET', 'POST'])
def unlabel():
    place = request.form["id"]
    client = request.form["id"]
    
    cursor = conn.cursor()

    # Check if the user is registered for the event
    query_check_registration = 'SELECT * FROM map WHERE place_id = %s AND client_id = %s'
    cursor.execute(query_check_registration, (place, client))
    registration = cursor.fetchone()

    if registration is None:
        error = "You have not labeled this map"
        return render_template("/client_home/view_map.html", error=error)

    # If the event and registration exist, delete the registration
    query_delete_registration = 'DELETE FROM map WHERE client_id = %s AND place_id = %s'
    cursor.execute(query_delete_registration, (client, place))
    conn.commit()


@app.route('/logout')
def logout():
    session.pop('email')
    return render_template('/index.html')

    
# -----------------------------------------------------------
# ------------------------------------------------------------
# event review
@app.route('/post_event_review')
def post_event_review():
    return render_template('/client_home/client_post_review.html')
  
@app.route("/client_post_review", methods=['GET', 'POST']) 
def client_post_event_review():
    user_id = request.form["user_id"]
    event_id = request.form["event_id"]
    content = request.form["content"]
    rating = request.form["rating"]
    price = request.form["price"]

    cursor = conn.cursor()

    query_check = "select id from client"
    cursor.execute(query_check)
    check = cursor.fetchall()

    check1 = []
    for item in check:
        check1.append(item["user_id"])
    if int(user_id) not in check1:
        error = "Sorry, user_id not existed !"
        return render_template("/client_home/client_post_review.html", error=error)

    query_check2 = 'SELECT * FROM event WHERE id = %s'
    cursor.execute(query_check2, event_id)
    check_f = cursor.fetchall()
    check3 = []
    for item in check_f:
        check3.append(item["event_id"])
    if int(event_id) not in check3:
        error = "Sorry, you input a wrong event id !"
        return render_template("/client_home/client_post_review.html", error=error)

    query3 = "select max(id) as next_id from review"
    cursor.execute(query3)
    review_id = cursor.fetchall()
    review_id = review_id[0]["next_id"]


    ins = 'INSERT INTO review VALUES(%s, %s, %s, %s, %s, %s, CURRENT_DATE())'
    cursor.execute(ins, (str(review_id + 1), event_id, user_id, content, rating, price))
    conn.commit()
    cursor.close()
    return render_template('/client_home/client_review_successful.html')
  
@app.route("/delete_review", methods=['GET', 'POST'])
def cancle_register():
    user_id = request.form["user_id"]
    event_id = request.form["event_id"]

    # Create a database cursor
    cursor = conn.cursor()

    query_check = "select id from client"
    cursor.execute(query_check)
    check = cursor.fetchall()
    # print(check)
    # print(type(check[0]))

    check1 = []
    for item in check:
        check1.append(item["user_id"])
    if int(user_id) not in check1:
        error = "Sorry, user_id not existed !"
        return render_template("/client_home/client_post_review.html", error=error)

    query_check2 = 'SELECT * FROM review WHERE event_id = %s and client_id = %s'
    cursor.execute(query_check2, event_id, user_id)
    check_f = cursor.fetchall()
    if check_f is None:
        error = "Sorry, you have not post any reviews for this event !"
        return render_template("/client_home/client_post_review.html", error=error)

    # If the event and registration exist, delete the registration
    query_delete_review = 'DELETE FROM review WHERE client_id = %s AND event_id = %s'
    cursor.execute(query_delete_review, (user_id, event_id))
    conn.commit()  # Commit the transaction to make sure changes are saved

    success_message = "Review cancelled successfully."
    return render_template("/client_home/client_post_review.html", success=success_message)
# -----------------------------------------------------------

# ----------------------------------------------------------------------
# before resgister
@app.route('/register_bo')
def register_business_owner():
    """
    Display the register
    
    This is an auxiliary function that helps display the business owner register page before authentication.

    Returns:
        str: Rendered HTML template for the registration page.
    """

    return render_template('register/bo_register.html')

# Authenticates the register for business owner
@app.route('/register_auth_bo', methods=['GET', 'POST'])
def registerAuth_bo():
    """
    Authenticates the register
    
    Authenticates the registration of a business owner. Extracts required information such as email, company name, name, password, 
        phone number, and city from the request form. Checks for duplicate owner in the database. If the user already exists, renders 
        the registration template with an error message. Otherwise, inserts the new business owner's information into the database 
        and redirects to the index page after successful registration.

    Returns:
        str: Rendered HTML template for the registration page / homepage.
    """

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

# ----------------------------------------------------------------------    
# before log in
@app.route('/login_bo')
def log_in_business_owner():
    """
    Display the log in
    
    This is an auxiliary function that helps display the business owner log in page before authentication.

    Returns:
        str: Rendered HTML template for the log in page.
    """
    return render_template('log_in/bo_login.html')


# Authenticates the log in for business owner
@app.route('/login_auth_bo', methods=['GET', 'POST'])
def loginAuth_business_owner():
    """
    Authenticates business owner login.

    Retrieves email and password from the form, queries the database
        to validate credentials, and redirects to the business owner home
        page if authentication succeeds. Otherwise, renders the login page
        with an error message.

    :return: Redirects to the business owner home page if login is successful, 
             otherwise renders the login page with an error message.
    :rtype: str
    """

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
    
# ----------------------------------------------------------------------
# after log in
# bo home page
@app.route("/bo_home", methods=["GET"])
def bo_home():
    """
    Display the homepage for logged in business owner
    
    This function display the business owner homepage if he sucessfully logged in. 

    Returns:
        str: Rendered HTML template for the bo home page.
    """
    return render_template("bo_page/bo_home.html")


# bo view his event: before view
@app.route("/bo_view_event_display", methods=["GET","POST"])
def bo_view_my_event_display():
    """
    Display the viw event display page
    
    This is an auxiliary function that shows the page that business owner can choose if 
        he want to display all his event. 

    Returns:
        str: Rendered HTML template for the bo's event display page.
    """
    return render_template("bo_page/bo_view_event.html")


# bo view his event: after view
@app.route("/bo_view_event", methods=["GET","POST"])
def bo_view_my_event():
    """
    Displays events owned by the logged-in business owner.

    Retrieves the business owner's email from the session, 
        obtains the corresponding business owner ID from the database,
        retrieves events associated with that ID, and renders the 
        business owner's event view page with the retrieved events 
        if there are any. Otherwise, renders the page with an error message.

    :return: Renders the business owner's event view page with events 
             or an error message.
    :rtype: str
    """

    bo_email = session["email"]

    # get this bo_id
    cursor = conn.cursor()
    q_bo_id = "SELECT id FROM businessowner WHERE email = %s"
    cursor.execute(q_bo_id, (bo_email,))
    bo_id = cursor.fetchone()["id"]
    cursor.close()
    
    # display all his event
    cursor = conn.cursor()
    q_get_events = "select e.name, e.time, e.description, e.max_ppl, \
            e.current_ppl, e.score, e.price, p.name as place_name from businessowner b inner join\
            events e on e.owner_id = b.id inner join place p on p.id = e.place_id where e.owner_id = %s"
    cursor.execute(q_get_events, (bo_id,))
    events = cursor.fetchall()
    cursor.close()
    
    if (events):
        return render_template("bo_page/bo_view_event.html",events=events)
    else:
        error = "You currently owned no event, please create one!"
        return render_template("bo_page/bo_view_event.html",error=error)


# bo search event: before search
@app.route("/bo_search_event_display", methods=["GET","POST"])
def bo_search_event_display():
    """
    Display the viw event display page
    
    This is an auxiliary function that shows the page that business owner can choose the
        event he want to search. 

    Returns:
        str: Rendered HTML template for the bo's search event display page.
    """
    return render_template("bo_page/bo_search_event.html")


# bo search event: after search
@app.route("/bo_search_event_form", methods=["GET","POST"])
def bo_search_event_form():
    """
    Processes the search for events based on user input.

    Retrieves search parameters from the form, constructs and executes 
        a SQL query to search for events matching the criteria, and renders 
        the search results or an error message.

    :return: Renders the event search results or an error message.
    :rtype: str
    """

    if request.method == "POST":
        name = request.form["name"]  # required
        time = request.form["time"]  # required
        score = request.form["score"] # optional
        price = request.form["price"] # optional

        cursor = conn.cursor()

        # case
        if len(price) == 0:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s '
                cursor.execute(query, ("%"+name+"%", time))
            else:
                query = 'SELECT * FROM events WHERE like = %s and date(time) > %s  and score > %s '
                cursor.execute(query, ("%"+name+"%", time, score))
        else:
            if len(score) == 0:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s and price < %s'
                cursor.execute(query, ("%"+name+"%", time, price))
            else:
                query = 'SELECT * FROM events WHERE name like %s and date(time) > %s and score > %s and price < %s'
                cursor.execute(query, ("%"+name+"%", time, score, price))

        # get result
        data = cursor.fetchall() 
        cursor.close()
        error = None

        if (data):
            return render_template("bo_page/bo_search_event.html", events=data) 
        else:
            error = 'No such event'
            return render_template("bo_page/bo_search_event.html", error=error)
        

# bo create an event
@app.route("/bo_create_event_form", methods=["GET", "POST"])
def bo_create_event_form():
    """
    Handles the creation of new events by business owners.

    Fetches available place names from the database and display as 
        multiple choice, so that no unpermitted place name
        is allowed for manual input. Retrieves event details 
        from the form, validates the input, and inserts a new event 
        record into the database if validation passes. Renders 
        the home page with a success message or an error message 
        if event creation fails.

    :return: Renders the home page with a success message or an error message.
    :rtype: str
    """
    # fetch place names from the database
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
            # create record
            cursor = conn.cursor()
            q_create_event = "INSERT INTO events (name, time, description, max_ppl, current_ppl, score, price, place_id, owner_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT id FROM place WHERE name = %s), %s)"
            cursor.execute(q_create_event, (event_name, event_time, event_descript, event_max_ppl, event_current_ppl,
                                             event_score, event_price, event_place, bo_id))
            conn.commit()
            cursor.close()
            message = "You have successfully created an event"
            return render_template("bo_page/bo_home.html", message=message)

    return render_template("bo_page/bo_create_event.html", place_names=place_names)


# help function for page refresh after event is deleted/modified
def refresh_event(bo_email):
    """
    Get updated event information
    
    This is a help function that helps to fetech the updated event information,
        if there is any delete or modification to event, and thus facilitate page refresh.

    Returns:
        tuple: a tuple of dictionary for events retreived
    """
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        from events e join place p on p.id = e.place_id where e.owner_id = (select distinct id from businessowner where email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()
    return events


# bo delete an event
@app.route("/bo_delete_event_form", methods=["GET", "POST"])
def bo_delete_event_form():
    """
    Handles the deletion of events by business owners.

    Retrieves events owned by the logged-in business owner so that he
        is assisted with a visual panel to choose which event to delete (no additional search),
        deletes the selected event from the database upon form submission,
        and renders the delete event form with a success message or 
        refreshes the event list if deletion is successful.

    :return: Renders the delete event form with events or a success message.
    :rtype: str
    """
    # identify the current user
    bo_email = session["email"] 
    
    # list all event this bo has
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        from events e join place p on p.id = e.place_id where e.owner_id = (select distinct id from businessowner where email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        event_id = request.form["event_id"]

        cursor = conn.cursor()
        q_delete_event = "delete from events where id = %s"
        cursor.execute(q_delete_event, (event_id))
        conn.commit()
        cursor.close()

        message = "Event deleted successfully."

        # refresh the page
        events = refresh_event(bo_email)
        return render_template("bo_page/bo_delete_event_form.html",  events = events, message = message)

    # render the delete event page with events owned by the business owner
    return render_template("bo_page/bo_delete_event_form.html", events=events)


# modify event from bo
@app.route("/bo_modify_event_form", methods=["GET", "POST"])
def bo_modify_event_form():
    """
    Handles the modification of events by business owners.

    Retrieves events owned by the logged-in business owner,
        modifies the selected event and event parameter based on user input.
        If the bo want to modify event name, duplicate check is initiated to
        ensure no duplicate event name can exists. Then the function renders
        the modify event form with a success message or an error message.

    :return: Renders the modify event form with events or a success message.
    :rtype: str
    """
        
    bo_email = session["email"]

    # list all his event
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        from events e join place p on p.id = e.place_id where e.owner_id = (select distinct id from businessowner where email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()
    
    if request.method == "POST":
        # get event, evnt parameter, and respective value to modify
        event_name = request.form["event_name"]
        parameter_to_modify = request.form["parameter_to_modify"]
        new_value = request.form["new_value"]
        new_time = request.form["new_time"]

        # handle different input type for time
        if parameter_to_modify == 'time':
            new_value = new_time

        # once update event name, check for duplicate
        if parameter_to_modify == 'name':
            cursor = conn.cursor()
            q_n_event= "SELECT * FROM events WHERE name = %s"
            cursor.execute(q_n_event, (event_name))
            n_event = cursor.fetchall()
            cursor.close()

            # has the same event name exist:
            if len(n_event)>0:
                error = "Failed to modify event, duplicate event name"
                events = refresh_event(bo_email)
                return render_template("bo_page/bo_modify_event.html", evemts=events, message=error, event_name=event_name)
            # modify
            else:
                cursor = conn.cursor()
                q_modify_event = f"update events set {parameter_to_modify} = %s where name = %s"
                cursor.execute(q_modify_event, (new_value, event_name))
                conn.commit()
                cursor.close()
                
                message = "Event modified sucesfully!"
                events = refresh_event(bo_email)
                return render_template("bo_page/bo_modify_event.html", events=events, message=message, event_name=event_name)
        # if not modify name, then direct modify the value
        else:
            cursor = conn.cursor()
            q_modify_event = f"update events set {parameter_to_modify} = %s where name = %s"
            cursor.execute(q_modify_event, (new_value, event_name))
            conn.commit()
            cursor.close()

            message = "Event modified sucesfully!"
            events = refresh_event(bo_email)
            return render_template("bo_page/bo_modify_event.html", events=events, message=message, event_name=event_name)
    
    events = refresh_event(bo_email)
    return render_template("bo_page/bo_modify_event.html", events=events)


# ----------------------------------------------------------------------
# bo log out
@app.route('/bo_logout')
def bo_logout():
    """
    Define the log out function for business owner
    
    This function pops out the current user session if log out is clicked,
        then redirect to the main menu before log in.

    Returns:
        str: Rendered HTML template for the general home page.
    """
    session.pop('email')
    return render_template('/index.html')

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
