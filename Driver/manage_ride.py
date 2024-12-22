import customtkinter as ctk
from tkinter import messagebox
from sql_connection import DatabaseConnection

class ManageRidesFrame(ctk.CTkFrame):
    def __init__(self, parent,driver_id=None):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self._conn_=DatabaseConnection.connection()
        self.driver_id = driver_id
        print(f"Driver id me {self.driver_id}")
        
        # Make the frame expand to fill the parent
        self.pack_propagate(False)

        # Status selector
        ctk.CTkLabel(self,text="Status:",font=ctk.CTkFont(size=14,weight="bold")).place(x=20, y=30)
        self.status_var = ctk.StringVar(value="Online")  # Default value set to "Offline"
        status_frame = ctk.CTkFrame(self, width=300, height=40)
        status_frame.place(x=80, y=20)

        # Create radio buttons
        self.offline_radio = ctk.CTkRadioButton(status_frame, text="Offline", variable=self.status_var,
                                                value="Offline", fg_color="#2D5A27", command=self.update_status)
        self.offline_radio.place(x=20, y=10)
        self.online_radio = ctk.CTkRadioButton(status_frame, text="Online", variable=self.status_var,
                                               value="Online", fg_color="#2D5A27", command=self.update_status)
        self.online_radio.place(x=150, y=10)

        ctk.CTkLabel(self,text="Upcoming Rides",font=ctk.CTkFont(size=18, weight="bold")).place(x=20, y=100)

        # Upcoming rides section
        self.create_upcoming_rides_section()
    def create_upcoming_rides_section(self):
        
        self.upcoming_frame = ctk.CTkScrollableFrame(self, width=850, height=600)
        self.upcoming_frame.place(x=20, y=130)

        # Sample upcoming rides
        try:
            # Clear existing bookings
            for widget in self.upcoming_frame.winfo_children():
                widget.destroy()
                
            cursor = self._conn_.cursor()
            query = """SELECT 
                    b.id,
                    c.full_name AS customer_name, 
                    c.phone_number AS customer_number, 
                    b.pickup, 
                    b.dropoff, 
                    b.ride_date, 
                    b.ride_time, 
                    b.fare
                FROM 
                    bookings b
                LEFT JOIN 
                    passengers c
                ON 
                    b.passenger_id = c.id -- Correct join condition
                WHERE  
                    b.driver_id = %s AND ride_status =%s ;"""
                    
            print(self.driver_id)
            print(f"Driver id me {self.driver_id}")
            
            cursor.execute(query,(self.driver_id,"Assigned"))
            bookings = cursor.fetchall()
            print(bookings)
            print(f"Driver id me {bookings}")
            

            if not bookings:
                self.no_pending_rides() 
                
            else:
                for booking in bookings:
                    self.create_booking_card(booking)
        finally:
            print("Upcoming rides")
    
    def no_pending_rides(self):
        card = ctk.CTkFrame(self.upcoming_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")
 
        ctk.CTkLabel(card, text=f"No Rides are assigned").pack(side="left", padx=10)
            
    def create_booking_card(self, booking):
        card = ctk.CTkFrame(self.upcoming_frame, height=200)
        card.pack(pady=10, padx=10, fill="x")

        # Booking details
        ctk.CTkLabel(card, text=f"Booking ID: {booking[0]}", font=ctk.CTkFont(size=14, weight="bold")).place(x=20, y=10)
        ctk.CTkLabel(card, text=f"Passenger: {booking[1]}", font=ctk.CTkFont(size=14)).place(x=20, y=40)
        ctk.CTkLabel(card, text=f"Phone Number: {booking[2]}", font=ctk.CTkFont(size=14)).place(x=20, y=70)
        ctk.CTkLabel(card, text=f"From: {booking[3]} → To: {booking[4]}", font=ctk.CTkFont(size=14)).place(x=20, y=100)
        ctk.CTkLabel(card, text=f"Date: {booking[5]} : {booking[6]}", font=ctk.CTkFont(size=14)).place(x=20, y=130)
        ctk.CTkLabel(card, text=f"Fare: {booking[7]}", font=ctk.CTkFont(size=14)).place(x=20, y=160)

        # Assign driver button
        pending_button = ctk.CTkButton(card,text="Assigned",width=120,fg_color="#0a56f0",)
        pending_button.place(x=650, y=50)
            
    def update_status(self):
        status = self.status_var.get()
        
        driver_id=self.driver_id
        # Update status in database
        try:
            with  self._conn_.cursor() as cursor:
                query="UPDATE drivers SET driver_status = %s WHERE id = %s "
                cursor.execute(query,(status,driver_id))
            
            
            
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            print("Booking Data inserted into database")

    def start_ride(self):
        messagebox.showinfo("Ride Started", "Ride has been started successfully!")

    def complete_ride(self):
        messagebox.showinfo("Ride Completed", "Ride has been completed successfully!")
        
