CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    show_time TEXT NOT NULL,
    total_seats INTEGER NOT NULL,
    booked_seats INTEGER DEFAULT 0,
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER,
    customer_name TEXT NOT NULL,
    seats INTEGER NOT NULL,
    FOREIGN KEY(show_id) REFERENCES shows(id)
);
