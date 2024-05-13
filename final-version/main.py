# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib

# Initialize the app from Flask
app = Flask(__name__, template_folder="templates", static_folder="templates")  # template location

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
    
    This is an auxiliary function that shows the page that anyone can choose the place he want to search before login. 

    Returns:
        str: Rendered HTML template for the search place display page.
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
      
@app.route('/logout')
def public_logout():
    return render_template('/index.html')

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
        ins = 'INSERT INTO client (email, name, password, phone_number, city) VALUES (%s, %s, %s, %s, %s)'
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
# after log in
# client home page
@app.route("/client_home", methods=["GET"])
def client_home():
    """
    Display the homepage for logged in client
    
    This function display the client homepage if he sucessfully logged in. 

    Returns:
        str: Rendered HTML template for the client home page.
    """
    return render_template("client_home/client_home.html")

# client search event: before search
@app.route("/client_search_event_display", methods=["GET","POST"])
def client_search_event_display():
    """
    Display the viw event display page on client side
    
    This is an auxiliary function that shows the page that client can choose the event he want to search. 

    Returns:
        str: Rendered HTML template for the search event display page.
    """
    return render_template("client_home/client_search_event.html")


# bo search event: after search
@app.route("/client_search_event_form", methods=["GET","POST"])
def client_search_event_form():
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
            return render_template("client_home/client_search_event.html", events=data) 
        else:
            error = 'No such event'
            return render_template("client_home/client_search_event.html", error=error)   

@app.route("/register_event", methods=['GET', 'POST']) 
def register_event():
    """
    Handles the registration of events by clients.

    Retrieves events searched by the logged-in client so that he
        is assisted with a visual panel to choose which event to join (no additional search),
        insert the selected event from the database into paticipation table upon form submission,
        and renders a success message or 
        refreshes the search list if deletion is successful.

    :return: Renders a success message.
    :rtype: str
    """
    # identify the current user
    client_email = session["email"] 

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    if request.method == "POST":
        event_id = request.form["event_id"]

        cursor = conn.cursor()
        query_check_registration = 'select p.id from client c inner join\
            participate p on p.client_id = c.id inner join events e on e.id = p.event_id where p.client_id = %s and e.id = %s'
        cursor.execute(query_check_registration, (client_id, event_id))
        registration = cursor.fetchone()
        cursor.close()
        
        if (registration):
            error = "You are already registered for this event."
            return render_template("/client_home/client_search_event.html", error=error)
        else:
            cursor = conn.cursor()
            query_check_full = "SELECT current_ppl, max_ppl FROM events WHERE id = %s"
            cursor.execute(query_check_full, (event_id,))
            event = cursor.fetchone()
            cursor.close()

            if int(event['current_ppl']) >= int(event['max_ppl']):
                error = "This event is already full."
                return render_template("/client_home/client_search_event.html", error=error)

            cursor = conn.cursor()
            q_rsvp = "INSERT INTO participate (client_id, event_id) VALUES (%s, %s)"
            cursor.execute(q_rsvp, (client_id, event_id))
            conn.commit()
            cursor.close()

            cursor = conn.cursor()
            q_rsvp = "UPDATE events SET current_ppl = %s WHERE id = %s"
            cursor.execute(q_rsvp, (str(int(event['current_ppl'])+1), event_id))
            conn.commit()
            cursor.close()

            return render_template('/client_home/client_register_successful.html')

    # render the delete review page with review owned by the client
    # return render_template("client_home/client_search_event.html", events=events)
    
@app.route("/client_view_bo", methods=['GET', 'POST']) 
def client_view_bo():
    """
    Handles the viewing of business owner profile of the event.

    Retrieves bo profile searched by the logged-in client so that he
        is assisted with a visual panel to choose to follow the bo or not.

    :return: Renders a bo profile page.
    :rtype: str: Rendered HTML template for the bo profile display page.
    """
    # identify the current user

    if request.method == "POST":
        event_id = request.form["event_id"]

        cursor = conn.cursor()
        query_check_bo = 'select b.id, b.name, b.company_name, b.city, b.description from events as e, businessowner as b where e.owner_id = b.id and e.id = %s'
        cursor.execute(query_check_bo, (event_id))
        view_bo = cursor.fetchone()
        cursor.close()
        
        if (view_bo):
            bos_list = [view_bo]
            return render_template("client_home/client_view_bo.html",bos=bos_list)
        else:
            error = "There is an error for the business owner profile"
        return render_template("client_home/client_view_bo.html",error=error)
          
@app.route('/client_follow_bo', methods=['GET', 'POST'])
def follow():
    """
    The function checks if the client has already followed the specified business owner. If not, it
    inserts a new record in the 'follow' table to establish this relationship. If the client has already followed the
    business owner, it displays an error message.
    
    :return: Redirects to a success page 'client_home/client_follow_successful.html'.
    :rtype: str
    """
    client_email = session["email"] 

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    if request.method == "POST":
        bo_id = request.form["bo_id"]

        cursor = conn.cursor()
        query_check_follow = 'select f.id from client c inner join\
            follow f on f.following_id = c.id inner join businessowner b on f.prime_id = b.id where c.id = %s and b.id = %s'
        cursor.execute(query_check_follow, (client_id, bo_id))
        follow = cursor.fetchone()
        cursor.close()
        
        if (follow):
            error = "The business owner is already followed."
            return render_template("client_home/client_view_bo.html", error=error)
        else:
            cursor = conn.cursor()
            q_map = "INSERT INTO follow (prime_id, following_id) VALUES (%s, %s)"
            cursor.execute(q_map, (bo_id, client_id))
            conn.commit()
            cursor.close()

            return render_template("client_home/client_follow_successful.html")


# public search place: before search
@app.route("/client_search_place_display", methods=['GET', 'POST'])
def client_search_place_display():
    """
    Display the viw place display page
    
    This is an auxiliary function that shows the page that clients can choose the place he want to search before login. 

    Returns:
        str: Rendered HTML template for the search place display page.
    """
    return render_template('client_home/client_search_place.html')


@app.route('/client_search_place_form', methods=['GET', 'POST'])
def client_search_place_form():
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
        return render_template("client_home/client_search_place.html", places=data)  # a url in app.route
    else:
        error = 'no such place'
        return render_template("client_home/client_search_place.html", error=error)

def refresh_place_client(client_email):
    cursor = conn.cursor()
    q_get_places = "select p.id, p.name, p.location_long, p.location_lati, p.city\
        from map m join place p on p.id = m.place_id where m.client_id = (select distinct id from client where email = %s)"
    cursor.execute(q_get_places, (client_email))
    events = cursor.fetchall()
    cursor.close()
    return events
    
@app.route('/client_label_place_to_map', methods=['GET', 'POST'])
def label():
    """
    Handles the labeling of places by clients.

    Add places searched by the logged-in client so that he
        is assisted with a visual panel to choose wether to 
        insert to map in the database map table upon form submission,
        and renders a success message.

    :return: Renders a success message.
    :rtype: str
    """
    client_email = session["email"] 

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    if request.method == "POST":
        place_id = request.form["place_id"]

        cursor = conn.cursor()
        query_check_map = 'select m.id from client c inner join\
            map m on m.client_id = c.id inner join place p on p.id = m.place_id where m.client_id = %s and p.id = %s'
        cursor.execute(query_check_map, (client_id, place_id))
        maped = cursor.fetchone()
        cursor.close()
        
        if (maped):
            error = "The place is already maped."
            return render_template("client_home/client_search_place.html", error=error)
        else:
            cursor = conn.cursor()
            q_map = "INSERT INTO map (client_id, place_id) VALUES (%s, %s)"
            cursor.execute(q_map, (client_id, place_id))
            conn.commit()
            cursor.close()

            message = "Joined map successfully."

            # refresh the page
            places = refresh_place_client(client_email)
            return render_template("client_home/client_search_place.html", places = places, message = message)

    # render the delete review page with review owned by the client
    return render_template("client_home/client_search_place.html", places=places)

# client view his reviews: before view
@app.route("/client_view_review", methods=["GET","POST"])
def client_view_review():
    """
    Display the viw review display page
    
    This is an auxiliary function that shows the page that client can choose if 
        he want to display all his reviews. 

    Returns:
        str: Rendered HTML template for the client's review display page.
    """
    client_email = session["email"]

    # get this client_id
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()
    
    # display all his reviews
    cursor = conn.cursor()
    q_get_reviews = "select r.id, r.content, r.rating, e.name as event_name from client c inner join\
            review r on r.client_id = c.id inner join events e on e.id = r.event_id where r.client_id = %s"
    cursor.execute(q_get_reviews, (client_id,))
    reviews = cursor.fetchall()
    cursor.close()
    
    if (reviews):
        return render_template("client_home/client_view_review.html",reviews=reviews)
    else:
        error = "You currently posted no review, please create one!"
        return render_template("client_home/client_view_review.html",error=error)

def refresh_review_client(client_email):
    cursor = conn.cursor()
    q_get_reviews = "select r.id, r.event_id, r.client_id, r.content, r.rating, e.name as event_name \
        from review r join events e on r.event_id = e.id where r.client_id = (select distinct id from client where email = %s)"
    cursor.execute(q_get_reviews, (client_email))
    reviews = cursor.fetchall()
    cursor.close()
    return reviews

# client delete a review
@app.route("/client_delete_review", methods=["GET", "POST"])
def client_delete_review():
    """
    Handles the deletion of reviews by clients.

    Retrieves reviews owned by the logged-in client so that he
        is assisted with a visual panel to choose which review to delete (no additional search),
        deletes the selected review from the database upon form submission,
        and renders the delete review form with a success message or 
        refreshes the review list if deletion is successful.

    :return: Renders the delete review form with reviews or a success message.
    :rtype: str
    """
    # identify the current user
    client_email = session["email"] 
    
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()
    
    # display all his reviews
    cursor = conn.cursor()
    q_get_reviews = "select r.id, r.content, r.rating, e.name as event_name from client c inner join\
            review r on r.client_id = c.id inner join events e on e.id = r.event_id where r.client_id = %s"
    cursor.execute(q_get_reviews, (client_id,))
    reviews = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        review_id = request.form["review_id"]

        cursor = conn.cursor()
        q_delete_review = "delete from review where id = %s"
        cursor.execute(q_delete_review, (review_id))
        conn.commit()
        cursor.close()

        message = "Review deleted successfully."

        # refresh the page
        reviews = refresh_review_client(client_email)
        return render_template("client_home/client_view_review.html",  reviews = reviews, message = message)

    # render the delete review page with review owned by the client
    return render_template("client_home/client_view_review.html", reviews=reviews)

# client view his reviews: before view
@app.route("/client_view_event", methods=["GET","POST"])
def client_view_event():
    """
    Display the viw event display page
    
    This is an auxiliary function that shows the page that client can choose if 
        he want to display all his events. 

    Returns:
        str: Rendered HTML template for the client's event display page.
    """
    client_email = session["email"]

    # get this client_id
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()
    
    # display all his reviews
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, pl.name as place_name \
        from events e inner join place pl on pl.id = e.place_id inner join participate p on p.event_id = e.id inner join client c on c.id = p.client_id where c.id = %s"
    cursor.execute(q_get_events, (client_id))
    events = cursor.fetchall()
    cursor.close()
    
    if (events):
        return render_template("client_home/client_view_event.html",events=events)
    else:
        error = "You currently joined no events, please join one!"
        return render_template("client_home/client_view_event.html",error=error)
    
# event review
@app.route('/post_event_review', methods=['GET', 'POST'])
def post_event_review():
    """
    Display the review post display page
    
    This is an auxiliary function that shows the page that client can enter the content of the review. 

    Returns:
        str: Rendered HTML template for the client's event display page.
    """
    event_id = request.form["event_id"]
    return render_template('client_home/client_post_review.html', event_id = event_id)

@app.route("/client_post_review", methods=['GET', 'POST']) 
def client_post_event_review():
    """
    Display the viw event display page
    
    This is an auxiliary function that shows the page that client can choose if 
        he want to display all his events. 

    Returns:
        str: Rendered HTML template for the client's event display page.
    """
    client_email = session["email"]

    # get this client_id
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    event_id = request.form["event_id"]
    content = request.form["content"]
    rating = request.form["rating"]

    cursor = conn.cursor()
    ins = 'INSERT INTO review (event_id, client_id, content, rating) VALUES(%s, %s, %s, %s)'
    cursor.execute(ins, (event_id, client_id, content, rating))
    conn.commit()
    cursor.close()
    return render_template('client_home/client_review_successful.html')

def refresh_event_client(client_email):
    """
    Get updated events list
    
    This is a help function that helps to fetech the updated events list, if there is any rsvp or cancle rsvp events, and thus facilitate page refresh.

    Returns:
        tuple: a tuple of dictionary for events retreived
    """
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()
    
    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, pl.name as place_name \
        from events e inner join place pl on pl.id = e.place_id inner join participate p on p.event_id = e.id inner join client c on c.id = p.client_id where c.id = %s"
    cursor.execute(q_get_events, (client_id))
    events = cursor.fetchall()
    cursor.close()
    return events

@app.route("/client_unrsvp_event", methods=['GET', 'POST'])
def cancle_register():
    """
    It manages the cancellation of a client's registration for an event. It processes the client's request to unregister for a specified event, decrements the current_ppl count in the events table to reflect the cancellation, and deletes the participation record from the participate table. After updating the database, it fetches and displays the updated list of events the client is registered for, along with a success message indicating the successful cancellation.

    Returns: a rendered template with an updated event list of the client and a success message if unregistration is successful.
    """
    client_email = session["email"]

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    cursor = conn.cursor()
    q_get_events = "select e.id, e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, pl.name as place_name \
            from events e inner join place pl on pl.id = e.place_id inner join participate p on p.event_id = e.id inner join client c \
            on c.id = p.client_id where c.id = %s"
    cursor.execute(q_get_events, (client_id,))
    events = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        event_id = request.form["event_id"]

        cursor = conn.cursor()
        q_get_cur = 'SELECT current_ppl FROM events WHERE id = %s'
        cursor.execute(q_get_cur, (event_id))
        cur = cursor.fetchone()
        cursor.close()

        cursor = conn.cursor()
        q_delete_parti = "delete from participate where client_id = %s and event_id=%s"
        cursor.execute(q_delete_parti, (client_id, event_id))
        conn.commit()
        cursor.close()
        
        cursor = conn.cursor()
        q_delete_parti = "UPDATE events SET current_ppl = %s WHERE id = %s"
        cursor.execute(q_delete_parti, (str(int(cur["current_ppl"]) - 1), event_id))
        conn.commit()
        cursor.close()

        message = "UnRSVP successfully."

        events = refresh_event_client(client_email)
        return render_template("client_home/client_view_event.html",  events = events, message = message)

    return render_template("client_home/client_view_event.html", events=events)

@app.route('/client_view_follow', methods=['GET', 'POST'])
def get_following():
    """
    This function retrieves a list of all business owners followed by the client based on their email. It fetches details such as business owner ID, name, company name, city, and description from the 
    'follow' and 'businessowner' tables.

    Returns: Rendered template 'client_home/client_view_follow.html' populated with the details of the business owners.
    """
    client_email = session["email"]

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    cursor = conn.cursor()
    query = 'SELECT b.id, b.name, b.company_name, b.city, b.description FROM follow f inner join businessowner b on f.prime_id=b.id WHERE f.following_id = %s'
    cursor.execute(query, (client_id))
    data = cursor.fetchall()
    cursor.close()

    if (data):
        return render_template("/client_home/client_view_follow.html", bos=data)
    else:
        error = "You currently followed no Business Owner, please follow one!"
        return render_template("client_home/client_view_follow.html",message=error)
   
def refresh_follow_client(client_email):
    """
    Get updated the business owner list followed by client
    
    This is a help function that helps to fetech the updated business owner list followed by client, if there is any following or unfollowing, and thus facilitate page refresh.

    Returns:
        tuple: a tuple of dictionary for business owners retreived
    """
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    cursor = conn.cursor()
    q_get_follows = 'SELECT b.id, b.name, b.company_name, b.city, b.description FROM follow f inner join businessowner b on f.prime_id=b.id WHERE f.following_id = %s'
    cursor.execute(q_get_follows, (client_id))
    events = cursor.fetchall()
    cursor.close()
    return events

@app.route('/client_unfollow_bo', methods=['GET', 'POST'])
def unfollow():
    """
    The function reads the business owner's ID from the form data and the client's email. It then delete the corresponding entry in the 'follow' table where the client is following the business owner. Upon successful deletion, the function updates the list of business owners the client currently follows and displays them along with a success message.

    Returns: Rendered template 'client_home/client_view_follow.html' with the updated list of business owners the client follows and a message indicating successful unfollow.
    """
    business_owner = request.form["bo_id"]
    client_email = session["email"]
    
    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (client_email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    cursor = conn.cursor()
    query_delete_follow = 'DELETE FROM follow WHERE following_id = %s AND prime_id = %s'
    cursor.execute(query_delete_follow, (client_id, business_owner))
    conn.commit()
    cursor.close()
    
    message = "Unfollowed successfully."
    bos = refresh_follow_client(client_email)
    return render_template("client_home/client_view_follow.html", bos = bos, message = message)
    

@app.route('/view_map', methods=['GET', 'POST'])
def view_map():
    """
    This function fetches the places that the client is associated with from the database using the client's email. It queries the 'place' and 'map' tables to gather details about each place including its name, longitude, latitude, and city. 

    Returns: Rendered template: Returns 'client_home/view_map.html' with data about the places.
    """
    email = session["email"]

    cursor = conn.cursor()
    query = 'SELECT p.id, p.name, p.location_long as longitude, p.location_lati as latitude, p.city FROM place as p, map as m, client as c WHERE c.email = %s '\
            'and c.id = m.client_id and p.id = m.place_id'
    cursor.execute(query, (email))

    data = cursor.fetchall()
    cursor.close()
    error = None
    if len(data) > 0:
        return render_template("/client_home/view_map.html", places=data)
    if len(data) == 0:
        error = 'no such place'
        return render_template("/client_home/view_map.html", error=error)

def refresh_map_client(client_email):
    """
    Get updated the map of places labeled by the client
    
    This is a help function that helps to fetech the updated map of places labeled by the client, if there is any labeling or unlabeling, and thus facilitate page refresh.

    Returns:
        tuple: a tuple of dictionary for places retreived
    """
    cursor = conn.cursor()
    query = 'SELECT p.id, p.name, p.location_long as longitude, p.location_lati as latitude, p.city FROM place as p, map as m, client as c WHERE c.email = %s '\
            'and c.id = m.client_id and p.id = m.place_id'
    cursor.execute(query, (client_email,))
    events = cursor.fetchall()
    cursor.close()
    return events

@app.route('/client_unlike_place', methods=['GET', 'POST'])
def unlabel():
    """
    This function retrieves a place's ID from the form data and the client's email. It uses the client's email to fetch their ID and then delete operation to remove the association between the client and the specified place from the 'map' table. After successfully deleting the association, the function refreshes the list of places associated with the client with a success message.

    Returns: Rendered templaten 'client_home/view_map.html' with an updated list of places and a success message confirming the removal.
    """
    place = request.form["place_id"]
    email = session["email"]

    cursor = conn.cursor()
    q_client_id = "SELECT id FROM client WHERE email = %s"
    cursor.execute(q_client_id, (email,))
    client_id = cursor.fetchone()["id"]
    cursor.close()

    cursor = conn.cursor()
    query_delete_registration = 'DELETE FROM map WHERE client_id = %s AND place_id = %s'
    cursor.execute(query_delete_registration, (client_id, place))
    conn.commit()
    cursor.close()

    message = "Unlabel place successfully!"
    places = refresh_map_client(email)
    return render_template("client_home/view_map.html",  places = places, message = message)



@app.route('/client_logout')
def client_logout():
    session.pop('email')
    return render_template('/index.html')

@app.route('/client_home')
def return_client_home():
    session.pop('email')
    return render_template('/index.html')   
# -----------------------------------------------------------
# ------------------------------------------------------------
  
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
    description = request.form["description"]

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
        ins = 'INSERT INTO businessowner (email, company_name, name, password, phone_number, city, description) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (email, company_name, name, password, phone_number, city, description))
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

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
