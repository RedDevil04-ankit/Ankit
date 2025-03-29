# app.py
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
DATABASE = r'D:/NewDestinationFinder/data/destination_finder.db'

def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/destinations', methods=['GET'])
def get_destinations():
    try:
        min_temp_str = request.args.get('min_temp')
        max_temp_str = request.args.get('max_temp')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_precipitation_str = request.args.get('min_precipitation')
        max_precipitation_str = request.args.get('max_precipitation')
        min_humidity_str = request.args.get('min_humidity')
        max_humidity_str = request.args.get('max_humidity')
        min_wind_speed_str = request.args.get('min_wind_speed')
        max_wind_speed_str = request.args.get('max_wind_speed')
        condition = request.args.get('condition')

        # Parameter Validation and Conversion (Optional Parameters)
        try:
            min_temp = int(min_temp_str) if min_temp_str is not None else None
            max_temp = int(max_temp_str) if max_temp_str is not None else None
        except ValueError:
            return jsonify({"error": "Invalid temperature values. 'min_temp' and 'max_temp' must be integers."}), 400

        try:
            min_precipitation = float(min_precipitation_str) if min_precipitation_str is not None else None
            max_precipitation = float(max_precipitation_str) if max_precipitation_str is not None else None
            min_humidity = float(min_humidity_str) if min_humidity_str is not None else None
            max_humidity = float(max_humidity_str) if max_humidity_str is not None else None
            min_wind_speed = float(min_wind_speed_str) if min_wind_speed_str is not None else None
            max_wind_speed = float(max_wind_speed_str) if max_wind_speed_str is not None else None
        except ValueError:
            return jsonify({"error": "Invalid precipitation, humidity, or wind speed values. Must be numbers."}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        try:
            cur = conn.cursor()
            query = """
                SELECT l.name, l.description, l.image_url,
                       AVG(wd.temperature_high), AVG(wd.temperature_low),
                       AVG(wd.precipitation), AVG(wd.humidity), AVG(wd.wind_speed),
                       wd.condition
                FROM locations l
                JOIN weather_data wd ON l.id = wd.location_id
            """
            params = []
            where_clauses = []

            # Dynamically add filters to the query if parameters are provided
            if start_date and end_date:
                where_clauses.append("STRFTIME('%Y-%m-%d', wd.date) BETWEEN ? AND ?")
                params.extend([start_date, end_date])

            if min_temp is not None and max_temp is not None:
                where_clauses.append("wd.temperature_high BETWEEN ? AND ?")
                params.extend([min_temp, max_temp])

            if min_precipitation is not None and max_precipitation is not None:
                where_clauses.append("wd.precipitation BETWEEN ? AND ?")
                params.extend([min_precipitation, max_precipitation])

            if min_humidity is not None and max_humidity is not None:
                where_clauses.append("wd.humidity BETWEEN ? AND ?")
                params.extend([min_humidity, max_humidity])

            if min_wind_speed is not None and max_wind_speed is not None:
                where_clauses.append("wd.wind_speed BETWEEN ? AND ?")
                params.extend([min_wind_speed, max_wind_speed])

            if condition:
                where_clauses.append("wd.condition LIKE ?")
                params.append(condition)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

            query += " GROUP BY l.id"

            cur.execute(query, tuple(params))
            destinations_tuples = cur.fetchall()
            cur.close()
            conn.close()

            destinations = []
            for d in destinations_tuples:
                destinations.append({
                    "name": d[0],
                    "description": d[1],
                    "image_url": "/images/" + d[2], # updated to serve local images
                    "temperature_high": d[3],
                    "temperature_low": d[4],
                    "precipitation": d[5],
                    "humidity": d[6],
                    "wind_speed": d[7],
                    "condition": d[8]
                })

            return jsonify(destinations)

        except sqlite3.Error as e:
            return jsonify({"error": "Database query failed: " + str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)

if __name__ == '__main__':
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Drop tables if they exist
            cur.execute("DROP TABLE IF EXISTS weather_data")
            cur.execute("DROP TABLE IF EXISTS locations")
            # Create locations table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    description TEXT,
                    image_url TEXT
                )
            """)
            # Create weather_data table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    temperature_high REAL,
                    temperature_low REAL,
                    precipitation REAL,
                    humidity REAL,
                    wind_speed REAL,
                    cloud_cover REAL,
                    condition TEXT,
                    FOREIGN KEY (location_id) REFERENCES locations(id),
                    UNIQUE (location_id, date)
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Tables created (or already existed).")

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    app.run(debug=True, port=5003)
