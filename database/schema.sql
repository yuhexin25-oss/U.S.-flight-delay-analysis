CREATE TABLE IF NOT EXISTS airports (
    iata VARCHAR PRIMARY KEY,
    airport_name VARCHAR,
    city VARCHAR,
    state VARCHAR,
    latitude DOUBLE,
    longitude DOUBLE,
    hub_classification VARCHAR,
    runway_count INTEGER
);

CREATE TABLE IF NOT EXISTS flights (
    flight_date DATE,
    carrier VARCHAR,
    origin VARCHAR,
    destination VARCHAR,
    departure_delay DOUBLE,
    arrival_delay DOUBLE,
    cancelled BOOLEAN,
    diverted BOOLEAN,
    carrier_delay DOUBLE,
    weather_delay DOUBLE,
    nas_delay DOUBLE,
    security_delay DOUBLE,
    late_aircraft_delay DOUBLE
);

CREATE OR REPLACE VIEW airport_performance AS
SELECT
    origin AS airport,
    COUNT(*) AS total_flights,
    ROUND(AVG(arrival_delay), 2) AS average_arrival_delay,
    ROUND(MEDIAN(arrival_delay), 2) AS median_arrival_delay,
    ROUND(100 * AVG(cancelled::INTEGER), 2) AS cancellation_rate
FROM flights
GROUP BY origin;

CREATE OR REPLACE VIEW route_performance AS
SELECT
    origin,
    destination,
    COUNT(*) AS total_flights,
    ROUND(AVG(arrival_delay), 2) AS average_arrival_delay
FROM flights
GROUP BY origin, destination;

