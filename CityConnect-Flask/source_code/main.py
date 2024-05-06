from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors

app = Flask(__name__, template_folder="se_templates", static_folder="se_templates/static")

conn = pymysql.connect(host = "localhost",
                       user = "root",
                       password="",
                       db = "software_engineering",
                       charset = "utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('bo_page/bo_home.html')

@app.route("/bo_home", methods=["GET"])
def bo_home():
    return render_template("bo_page/bo_home.html")

@app.route("/bo_view_event", methods=["GET","POST"])
def bo_view_my_event():
    bo_email = session["email"]

    cursor = conn.cursor()
    q_get_events = "select e.name, e.time, e.description, e.max_ppl, e.current_ppl, e.score, e.price, p.name as place_name \
        from events e join place p on p.id = e.place_id where e.owner_id = (select distinct id from businessowner where email = %s)"
    cursor.execute(q_get_events, (bo_email,))
    events = cursor.fetchall()
    cursor.close()

    return render_template("/bo_view_event.html",events=events)


@app.route("/bo_search_event_form", methods=["GET"])
def bo_search_event_form():
    # to add bo's search event, copy from the public search
    # to add bo's log out button to that page
    pass

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
        event_owner = bo_email

        # get this bo_id
        cursor = conn.cursor()
        q_bo_id = "SELECT id FROM businessowner WHERE email = %s"
        cursor.execute(q_bo_id, (bo_email,))
        bo_id = cursor.fetchone()[0]
        cursor.close()

        # event with same name by this owner cannot be created
        cursor = conn.cursor()
        q_check_ename = "SELECT name FROM events WHERE owner_id = %s"
        cursor.execute(q_check_ename, (bo_id,))
        all_event_name = cursor.fetchall()
        cursor.close()

        # check event with the same time and location cannot be created
        cursor = conn.cursor()
        q_check_timeloc = "SELECT COUNT(id) FROM events WHERE time = %s AND place_id IN \
            (SELECT id FROM place WHERE name = %s)"
        cursor.execute(q_check_timeloc, (event_time, event_place))
        n_dup_event = cursor.fetchone()[0]
        cursor.close()

        if (event_name,) in all_event_name or n_dup_event >= 1:
            flash('Failed! Event already exists! Please either change event name or change event time and location')
        else:
            cursor = conn.cursor()
            q_create_event = "INSERT INTO events (name, time, description, max_ppl, current_ppl, score, price, place_id, owner_id) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, (SELECT id FROM place WHERE name = %s), %s)"
            cursor.execute(q_create_event, (event_name, event_time, event_descript, event_max_ppl, event_current_ppl,
                                             event_score, event_price, event_place, event_owner))
            conn.commit()
            cursor.close()
            flash("You have successfully created an event")
            return render_template("bo_page/bo_home.html")

    return render_template("bo_page/bo_create_event.html", place_names=place_names)


@app.route("/bo_delete_event_form", methods=["GET", "POST"])
def bo_delete_event_form():
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
        cursor.execute(q_delete_event, (event_id, bo_email))
        conn.commit()
        cursor.close()

        flash("Event deleted successfully.")

        # redirect to same page to refresh event list
        return redirect(url_for("bo_delete_event_form"))

    # render the delete event page with events owned by the business owner
    return render_template("bo_delete_event_form.html", events=events)


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
        event_id = request.form["event_id"]
        parameter_to_modify = request.form["parameter_to_modify"]
        new_value = request.form["new_value"]
        new_time = request.form["new_time"]

        if parameter_to_modify == 'time':
            new_value = new_time

        # modify
        cursor = conn.cursor()
        q_modify_event = f"update events set {parameter_to_modify} = %s where id = %s"
        cursor.execute(q_modify_event, (new_value, event_id))
        conn.commit()
        cursor.close()

        flash("Event modified successfully.")

        # Redirect to the same page to refresh event list
        return redirect(url_for("bo_modify_event_form"))

    # Render the modify event page with events owned by the business owner
    return render_template("bo_modify_event_form.html", events=events)


@app.route('/bo_logout')
def staff_logout():
    session.pop('email')
    return render_template('/index.html')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)