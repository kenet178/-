PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS airports (
 id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, city TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS aircraft (
 id INTEGER PRIMARY KEY, model TEXT NOT NULL, capacity INTEGER NOT NULL CHECK(capacity>0)
);
CREATE TABLE IF NOT EXISTS flights (
 id INTEGER PRIMARY KEY, number TEXT NOT NULL UNIQUE,
 origin_id INTEGER NOT NULL REFERENCES airports(id),
 destination_id INTEGER NOT NULL REFERENCES airports(id),
 aircraft_id INTEGER NOT NULL REFERENCES aircraft(id),
 departure TEXT NOT NULL, price REAL NOT NULL CHECK(price>0),
 free_seats INTEGER NOT NULL CHECK(free_seats>=0),
 CHECK(origin_id <> destination_id)
);
CREATE TABLE IF NOT EXISTS passengers (
 id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS tickets (
 id INTEGER PRIMARY KEY, flight_id INTEGER NOT NULL REFERENCES flights(id),
 passenger_id INTEGER NOT NULL REFERENCES passengers(id),
 seat TEXT NOT NULL, UNIQUE(flight_id,seat), UNIQUE(flight_id,passenger_id)
);
CREATE INDEX IF NOT EXISTS idx_flights_departure ON flights(departure);
CREATE INDEX IF NOT EXISTS idx_flights_route ON flights(origin_id,destination_id);
CREATE INDEX IF NOT EXISTS idx_tickets_passenger ON tickets(passenger_id);
