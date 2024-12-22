import customtkinter as ctk
from fonts.colors import Colors
from tkinter import messagebox
import mysql.connector
from sql_connection import DatabaseConnection

class DriverRequestFrame(ctk.CTkFrame):
    def __init__(self, parent,admin=None):
        self.admin=admin
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.pack_propagate(False)
        self._conn_ = None
        self._conn_=DatabaseConnection.connection()
    

        # Header
        self.header = ctk.CTkLabel(self, text="Driver Registration Requests", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # Scrollable frame for requests
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=850, height=600)
        self.scrollable_frame.place(x=20, y=70)

        self.load_driver_requests(self.admin)

    def load_driver_requests(self,admin):
        

        try:
            # Clear existing widgets
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self._conn_=DatabaseConnection.connection()
            cursor=self._conn_.cursor()
            query="SELECT id,full_name,phone_number,email,user_password,address,license_number,vehicle_number,gender FROM driver_request WHERE request_status='Requested'"
            cursor.execute(query)
            driver_data=cursor.fetchall()
            driver_requests = []  # Initialize the variable to avoid UnboundLocalError
                # Map the data to a list of dictionaries
            driver_requests = [
                {
                    "id":row[0],
                    "name": row[1],
                    "number": row[2],
                    "email": row[3],
                    "user_password": row[4],
                    "address": row[5],
                    "license_number": row[6],
                    "vehicle_number": row[7],
                    "gender": row[8]
                }
                for row in driver_data
            ]


        except mysql.connector.Error as e:
            # Handle database connection or execution errors
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        except Exception as ex:
            # Handle any other unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}")

        finally:    
            cursor.close()


        # Display pending requests
        if driver_requests:
            for idx, driver in enumerate(driver_requests):
                self.create_request_card(driver, idx,admin)
        else:
            self.no_requests_found()

    def create_request_card(self, driver, idx,admin):
        # Create a card for each driver request
        card = ctk.CTkFrame(self.scrollable_frame, width=800, height=150)
        card.pack(pady=10, padx=10, fill="x")  # Ensure card stretches horizontally

        # Driver details (horizontal layout)
        details_frame = ctk.CTkFrame(card, width=800)  # Set width explicitly
        details_frame.pack(fill="x", padx=10, pady=10)  # Allow horizontal stretching

        # Driver details
        ctk.CTkLabel(details_frame, text=f"Name: {driver['name']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"Contact: {driver['number']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"Email: {driver['email']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"Address: {driver['address']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"License Number: {driver['license_number']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"Vehicle Number: {driver['vehicle_number']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(details_frame, text=f"Gender: {driver['gender']}", font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)


        approve_btn = ctk.CTkButton(details_frame, text="Approve", fg_color=Colors.GREEN_BUTTON,hover_color=Colors.GREEN_BUTTON_HOVER, command=lambda: self.approve_driver(driver, idx,admin))
        approve_btn.pack(side="left", padx=10,pady=(5,20))

        reject_btn = ctk.CTkButton(details_frame, text="Reject", fg_color=Colors.RED,hover_color=Colors.HOVER_RED, command=lambda: self.reject_driver(driver, idx,admin))
        reject_btn.pack(side="left", padx=10,pady=(5,20))

    def no_requests_found(self):
        card = ctk.CTkFrame(self.scrollable_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(card, text="No pending driver registration requests !").pack(side="left", padx=10)


    def approve_driver(self, driver, idx,admin):
        # Save approved driver to the database
        try:
            cursor = self._conn_.cursor()
            query1 = """INSERT INTO drivers (full_name, phone_number, email, user_password, address, license_number, vehicle_number, gender,admin_id,request_id) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s)"""
            cursor.execute(query1, (driver["name"], driver["number"], driver["email"], driver["user_password"],driver["address"], driver["license_number"], driver["vehicle_number"], driver["gender"],admin,driver['id']))
            self._conn_.commit()
            query2=""" UPDATE driver_request SET request_status='Approved',admin_id=%s WHERE email=%s AND user_password=%s"""
            cursor.execute(query2,(admin,driver['email'],driver['user_password']))
            self._conn_.commit()
            messagebox.showinfo("Success", f"Driver {driver['name']} approved and added to the system")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to approve driver: {e}")


        self.load_driver_requests(admin)

    def reject_driver(self,driver, idx,admin):
        try:
            cursor = self._conn_.cursor()
            
            query2=""" UPDATE driver_request SET request_status='Rejected',admin_id=%s WHERE email=%s AND user_password=%s"""
            cursor.execute(query2,(admin,driver['email'],driver['user_password']))
            self._conn_.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to approve driver: {e}")
        finally:
            messagebox.showinfo("Rejected", "Driver request rejected!")
            self.load_driver_requests(admin)
