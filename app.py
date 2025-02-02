from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'


# Database Connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Home Page - List Events
@app.route('/')
def index():
    db = get_db()
    events = db.execute("SELECT * FROM events").fetchall()
    return render_template('index.html', events=events)


# Add Event
@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['name']
    description = request.form['description']
    db = get_db()
    db.execute("INSERT INTO events (name, description) VALUES (?, ?)", (name, description))
    db.commit()
    return redirect(url_for('index'))


# Update Event
@app.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    name = request.form['name']
    description = request.form['description']
    db = get_db()
    db.execute("UPDATE events SET name = ?, description = ? WHERE id = ?", (name, description, event_id))
    db.commit()
    return redirect(url_for('index'))


# Delete Event
@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    db = get_db()
    db.execute("DELETE FROM events WHERE id = ?", (event_id,))
    db.commit()
    return redirect(url_for('index'))


# View Shows for an Event
@app.route('/event/<int:event_id>')
def event_details(event_id):
    db = get_db()
    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    shows = db.execute("SELECT * FROM shows WHERE event_id = ?", (event_id,)).fetchall()
    return render_template('event_details.html', event=event, shows=shows)


# Add Show
@app.route('/add_show/<int:event_id>', methods=['POST'])
def add_show(event_id):
    show_time = request.form['show_time']
    total_seats = int(request.form['total_seats'])
    db = get_db()
    db.execute("INSERT INTO shows (event_id, show_time, total_seats) VALUES (?, ?, ?)", (event_id, show_time, total_seats))
    db.commit()
    return redirect(url_for('event_details', event_id=event_id))


# Book Tickets
@app.route('/book_ticket/<int:show_id>', methods=['POST'])
def book_ticket(show_id):
    customer_name = request.form['customer_name']
    seats = int(request.form['seats'])

    db = get_db()
    show = db.execute("SELECT * FROM shows WHERE id = ?", (show_id,)).fetchone()

    if show['booked_seats'] + seats > show['total_seats']:
        return "Not enough seats available!", 400

    db.execute("INSERT INTO tickets (show_id, customer_name, seats) VALUES (?, ?, ?)", (show_id, customer_name, seats))
    db.execute("UPDATE shows SET booked_seats = booked_seats + ? WHERE id = ?", (seats, show_id))
    db.commit()

    return redirect(url_for('event_details', event_id=show['event_id']))


# View Ticket Summary
@app.route('/summary')
def summary():
    db = get_db()
    summary = db.execute("SELECT s.show_time, e.name, s.total_seats, s.booked_seats FROM shows s JOIN events e ON s.event_id = e.id").fetchall()
    return render_template('summary.html', summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
