import mysql.connector as conn
import bcrypt
class DatabaseConnection:
    message = ""
    try:
        @staticmethod #doesnt contain any dynamic methods like self.connection()
        def connection():
            # Initial connection without specifying a database
            connect = conn.connect(
                host='localhost',
                user='root', # change username here and at the return statement
                password='2005subash0910'  #  change password here and at the return statement
            )
            if connect.is_connected():
                DatabaseConnection.message = "Connected"
                cursor = connect.cursor()

                # Create the database if it doesn't exist
                cursor.execute("CREATE DATABASE IF NOT EXISTS sahara")
                cursor.execute("USE sahara")
                
                # Create admin table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admins (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        user_password VARCHAR(255) NOT NULL
                    );
                ''')

                # Create user_register table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS passengers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        full_name VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(10) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        user_password VARCHAR(255) NOT NULL,
                        address VARCHAR (255) NOT NULL,
                        gender ENUM('Male', 'Female', 'Others') NOT NULL,
                        age INT
                    );
                ''')

                # Create driver_request table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS driver_request (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        full_name VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(10) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        user_password VARCHAR(255) NOT NULL,
                        address VARCHAR (255) NOT NULL,
                        license_number VARCHAR (255) UNIQUE NOT NULL,
                        vehicle_number VARCHAR (255) UNIQUE NOT NULL,
                        gender ENUM('Male', 'Female', 'Others') NOT NULL,
                        request_status ENUM('Approved','Requested','Rejected'),
                        admin_id INT ,
                        FOREIGN KEY (admin_id) REFERENCES admins(id)
                    );
                ''')
                
                # Create driver table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS drivers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        full_name VARCHAR(255) NOT NULL,
                        phone_number VARCHAR(10) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        user_password VARCHAR(255) NOT NULL,
                        address VARCHAR (255) NOT NULL,
                        license_number VARCHAR (255) NOT NULL,
                        vehicle_number VARCHAR (255) NOT NULL,
                        driver_status ENUM('Online','Offline') NOT NULL,
                        gender ENUM('Male', 'Female', 'Others') NOT NULL,
                        admin_id INT ,
                        request_id INT ,
                        FOREIGN KEY (admin_id) REFERENCES admins(id),
                        FOREIGN KEY (request_id) REFERENCES driver_request(id)
                    );
                ''')

                # Create bookings table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bookings (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        passenger_id INT ,
                        driver_id INT ,
                        admin_id INT ,
                        pickup VARCHAR(255) NOT NULL,
                        dropoff VARCHAR(255) NOT NULL,
                        ride_date VARCHAR(255) NOT NULL,
                        ride_time VARCHAR(255) NOT NULL,
                        vehicle_type VARCHAR(255) NOT NULL,
                        fare VARCHAR(255) NOT NULL,
                        ride_status VARCHAR(255),
                        FOREIGN KEY (passenger_id) REFERENCES passengers(id),
                        FOREIGN KEY (admin_id) REFERENCES admins(id),
                        FOREIGN KEY (driver_id) REFERENCES drivers(id)
                    );
                ''')

                hashed_password1 = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')# Convert password to bytes and hash it
                hashed_password2 = bcrypt.hashpw('pcpscollege'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')# Convert password to bytes and hash it
                
                
                # Insert default admin if not already present
                cursor.execute('''INSERT IGNORE INTO admins (id, email, user_password) VALUES (%s, %s, %s), (%s, %s, %s)'''
                               , (1, 'admin@gmail.com', hashed_password1,2, 'pcpscollege@gmail.com', hashed_password2))
                # Commit the transaction to save changes
                connect.commit()
                cursor.close()
                connect.close()

            # Reconnect and specify the database now that it exists
            connection = conn.connect(
                host='localhost',
                user='root', # username
                password='2005subash0910', # password 
                database='sahara' # name of the database
            )
            return connection
    
    except Exception as e:
        print(e)
