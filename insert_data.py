# insert_data.py
import sqlite3
import os

def insert_data():
    try:
        conn = sqlite3.connect('D:/NewDestinationFinder/data/destination_finder.db')
        cursor = conn.cursor()

        # Insert into locations table and get the last inserted ID *immediately*
        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Goa', 15.2995, 74.1240, 'Beautiful beaches', 'goa.jpg'))
        goa_id = cursor.lastrowid

        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Shimla', 31.1048, 77.1734, 'Hill station', 'shimla.jpg'))
        shimla_id = cursor.lastrowid

        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Kerala', 8.9003, 76.5812, 'Tropical paradise', 'kerala.jpg'))
        kerala_id = cursor.lastrowid

        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Jaipur', 26.9220, 75.8267, 'Pink City', 'jaipur.jpg'))
        jaipur_id = cursor.lastrowid

        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Udaipur', 24.5854, 73.7125, 'City of Lakes', 'udaipur.jpg'))
        udaipur_id = cursor.lastrowid

        cursor.execute("INSERT INTO locations (name, latitude, longitude, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Manali', 32.2432, 77.1896, 'Mountain Resort', 'manali.jpg'))
        manali_id = cursor.lastrowid

        # Insert into weather_data table (using the CORRECT location IDs)
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (goa_id, '2024-07-01', 32, 25, 0.0, 70, 15, 20, 'Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (shimla_id, '2024-07-01', 22, 15, 10.0, 80, 8, 80, 'Cloudy'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (kerala_id, '2024-07-01', 28, 22, 2.0, 75, 10, 30, 'Partly Cloudy'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (jaipur_id, '2024-07-01', 35, 27, 0.5, 60, 12, 10, 'Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (udaipur_id, '2024-07-01', 33, 26, 1.0, 65, 10, 20, 'Mostly Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (manali_id, '2024-07-01', 18, 10, 15.0, 90, 5, 95, 'Snowy'))

        # Add more weather data for different dates and locations as needed
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (goa_id, '2024-07-02', 33, 26, 1.0, 72, 12, 15, 'Mostly Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (shimla_id, '2024-07-02', 20, 13, 12.0, 85, 5, 90, 'Rainy'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (kerala_id, '2024-07-02', 29, 23, 0.5, 78, 8, 25, 'Partly Cloudy'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (jaipur_id, '2024-07-02', 36, 28, 0.2, 55, 14, 5, 'Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (udaipur_id, '2024-07-02', 34, 27, 0.8, 62, 11, 15, 'Mostly Sunny'))
        cursor.execute("INSERT INTO weather_data (location_id, date, temperature_high, temperature_low, precipitation, humidity, wind_speed, cloud_cover, condition) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (manali_id, '2024-07-02', 15, 8, 18.0, 95, 3, 98, 'Heavy Snow'))

        conn.commit()
        print("Data inserted successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        if conn:
            conn.close()

insert_data()








