
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from sql_connection import DatabaseConnection
from fonts.colors import Colors

class BookingManagementFrame(ctk.CTkFrame):# Define the 'BookingFrame' class, which is a subclass of 'CTkFrame'
    def __init__(self, parent,admin_id=None):
        #The constructor (__init__) method is called when an instance of the class is created.
        #It initializes the frame 
        self.admin_id = admin_id
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.pack_propagate(False)#This disables the "propagation" of the frame's size to its children widgets when using the pack()
        self._conn_ = None
        self._conn_=DatabaseConnection.connection()
        
        #This calls the constructor of the parent class (CTkFrame,
        
        # Header
        self.header = ctk.CTkLabel(self, text="Booking Management", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # Create scrollable frame for bookings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=850, height=600)
        self.scrollable_frame.place(x=20, y=70)
        
        # call load bookings method
        self.load_bookings(self.admin_id)

    def load_bookings(self,admin_id):
        try:
            # Clear existing bookings
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
                # connection and sql queries
            
            self._conn_=DatabaseConnection.connection()
            cursor = self._conn_.cursor()
            query = """SELECT 
                    b.id, 
                    p.full_name AS passenger_name, 
                    b.pickup, 
                    b.dropoff, 
                    b.ride_date, 
                    b.ride_time, 
                    b.fare
                FROM 
                    bookings b
                LEFT JOIN 
                    passengers p
                ON 
                    b.passenger_id = p.id -- Correct join condition
                WHERE  
                    b. ride_status='Pending';
            """
            cursor.execute(query)
            bookings = cursor.fetchall()
            
            # if data is empty on database
            if not bookings:
                self.no_pending_rides()
                 
            # else showing booking details
            else:
                for booking in bookings:
                    self.create_booking_card(booking,admin_id)
                    
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")                
   
   
    def no_pending_rides(self):
        # self.scrollable_frame.pack(fill="both", expand=True)  # Make parent frame fill the entire window.
        card = ctk.CTkFrame(self.scrollable_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(card, text=f"No bookings found !").pack(side="left", padx=10)

    def create_booking_card(self, booking,admin):
        card = ctk.CTkFrame(self.scrollable_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")

        # Booking details
        ctk.CTkLabel(card, text=f"Booking ID : {booking[0]}", font=ctk.CTkFont(size=14, weight="bold")).place(x=20, y=20)
        ctk.CTkLabel(card, text=f"Passenger : {booking[1]}", font=ctk.CTkFont(size=14)).place(x=20, y=50)
        ctk.CTkLabel(card, text=f"From : {booking[2]} → To : {booking[3]}", font=ctk.CTkFont(size=14)).place(x=20, y=80)
        ctk.CTkLabel(card, text=f"Date : {booking[4]}  Time: {booking[5]}", font=ctk.CTkFont(size=14)).place(x=20, y=110)

        # Assign driver button
        assign_button = ctk.CTkButton(card,text="Assign Driver",width=120,fg_color=Colors.GREEN_BUTTON,
                                      hover_color=Colors.GREEN_BUTTON_HOVER,
                                      command=lambda: self.assign_driver(booking[0],admin))
        assign_button.place(x=600, y=50)

    def assign_driver(self,booking_id,admin_id):
        self.assign_window = AssignDriverWindow(self,admin_id, booking_id,booking_frame=self)
        
class AssignDriverWindow(ctk.CTkToplevel):
    def __init__(self, parent,admin_id, booking_id,booking_frame):
        super().__init__(parent)
        self._conn_ = None
        self._conn_=DatabaseConnection.connection()
        
        self.title("Assign Driver")
        self.geometry("400x400")
        self.booking_id = booking_id
        self.booking_frame = booking_frame # Store the reference to BookingManagementFrame
        
        # Position the window in front of the parent
        self.transient(parent)
        self.grab_set()  # Disable interactions with the parent until this window is closed


        ctk.CTkLabel(self, text="Available Drivers", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        # Create scrollable frame for available drivers
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=350, height=400)
        self.scrollable_frame.pack(pady=10)

        self.load_available_drivers(admin_id)

    def load_available_drivers(self,admin):
        try:
            cursor = self._conn_.cursor()
            query = "SELECT * FROM drivers WHERE driver_status = 'Online'"
            cursor.execute(query)
            drivers = cursor.fetchall()
            print(f"Driver in drivers")
            if not drivers:
                self.no_driver_available() 
            else:
                for driver in drivers:
                    self.create_driver_option(driver,admin)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    
    # function to create frames of drivers 

    def create_driver_option(self, driver,admin):
        self.scrollable_frame.pack(fill="both", expand=True)  # Make parent frame fill the entire window.

        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="both", expand=True)  # Make the frame fill the parent container.

        ctk.CTkLabel(frame, text=f"{driver[1]} ({driver[0]})", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        
        assign_button = ctk.CTkButton(frame,text="Assign",width=80,fg_color="#2D5A27",hover_color="#1E3D1A",command=lambda: self.assign_driver(driver[0],admin))
        assign_button.pack(side="right", padx=10)

    # function if no any driver is availanle
    def no_driver_available(self):
        self.scrollable_frame.pack(fill="both", expand=True)  # Make parent frame fill the entire window.
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="both", expand=True)  # Make the frame fill the parent container.
        ctk.CTkLabel(frame, text=f"No Drivers Available").pack(side="left", padx=10)
 
    # function to assign driver to the booking
    def assign_driver(self, driver_id,admin_id):
        try:
            cursor = self._conn_.cursor()
            print(self.booking_id)
            
            # Update booking with assigned driver
            update_booking_status = "UPDATE bookings SET driver_id = %s,admin_id=%s, ride_status = 'Assigned' WHERE id = %s"
            cursor.execute(update_booking_status, [driver_id,admin_id, self.booking_id])
            self._conn_.commit()
            messagebox.showinfo("Success", "Driver assigned successfully!")
            
            # Refresh the bookings list in the parent frame
            if self.booking_frame:
                print('hello')
                self.booking_frame.load_bookings(admin_id)
                self.destroy()
            
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
