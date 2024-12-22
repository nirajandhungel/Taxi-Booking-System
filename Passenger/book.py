import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from sql_connection import DatabaseConnection

class BookingFrame(ctk.CTkFrame): # Define the 'BookingFrame' class, which is a subclass of 'CTkFrame'
    def __init__(self, parent,passenger_id=None):

        #The constructor (__init__) method is called when an instance of the class is created.
        #It initializes the frame and stores the passenger_id if provided.
        self.passenger_id = passenger_id
        self._conn_=DatabaseConnection.connection()
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())

        # Make the frame expand to fill the parent
        self.pack_propagate(False)
        self. booking_ui()
        
    def booking_ui(self):

        # Header
        self.header = ctk.CTkLabel(self,text="Book a Ride",font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # Locations
        pick_locations = ["Kathmandu", "Pokhara", "Lalitpur", "Bhaktapur", "Biratnagar"]
        drop_locations = ["Pokhara",  "Lalitpur", "Bhaktapur", "Biratnagar","Kathmandu"]

        # Pickup location
        ctk.CTkLabel(self,text="Pickup Location:",font=ctk.CTkFont(size=14)).place(x=20, y=90)

        self.pickup_entry = ctk.CTkComboBox(self,width=400,values=pick_locations,command=self.update_fare)
        self.pickup_entry.place(x=140, y=90)

        # Dropoff location
        ctk.CTkLabel(self,text="Dropoff Location:",font=ctk.CTkFont(size=14)).place(x=20, y=140)

        self.dropoff_entry = ctk.CTkComboBox(self,width=400,values=drop_locations,command=self.update_fare)
        self.dropoff_entry.place(x=140, y=140)

        # Date Entry
        ctk.CTkLabel(self,text="Date:",font=ctk.CTkFont(size=14)).place(x=20, y=200)

        # Year Entry
        self.year_entry = ctk.CTkComboBox(self,width=100,values=[str(datetime.now().year)])
        self.year_entry.place(x=140, y=200)

        # Month Entry
        self.month_entry = ctk.CTkComboBox(self,width=100,values=[str(i).zfill(2) for i in range(1, 13)])
        self.month_entry.place(x=270, y=200)

        # Day Entry
        self.day_entry = ctk.CTkComboBox(self,width=100,values=[str(i).zfill(2) for i in range(1, 32)])
        self.day_entry.place(x=380, y=200)
        
        ctk.CTkLabel(self,text="Time:",font=ctk.CTkFont(size=14)).place(x=580, y=200)
        
        
        # Time Entry
        self.hour_entry = ctk.CTkComboBox(self, width=100, values=[str(i).zfill(2) for i in range(24)])
        self.hour_entry.place(x=650, y=200)

        # Minute Entry
        self.minute_entry = ctk.CTkComboBox(self, width=100, values=[str(i).zfill(2) for i in range(60)])
        self.minute_entry.place(x=790, y=200)

        # Vehicle type
        ctk.CTkLabel(self,text="Vehicle Type:",font=ctk.CTkFont(size=14)).place(x=20, y=290)

        self.vehicle_var = ctk.StringVar(value="Standard")
        vehicle_types = ["Standard", "Premium", "Luxury"]
        
        # frame of vehicle type
        vehicle_frame = ctk.CTkFrame(self, width=650, height=40)
        vehicle_frame.place(x=140, y=280)
        
        #looping to add radio button
        for i, v_type in enumerate(vehicle_types,start=1):
            ctk.CTkRadioButton(vehicle_frame,text=v_type,variable=self.vehicle_var,value=v_type,fg_color="#2D5A27",command=self.update_fare).place(x=i*150, y=10)

        fare_frame = ctk.CTkFrame(self, width=650, height=40)
        fare_frame.place(x=140, y=380)
        
        # Fare estimate
        self.fare_label = ctk.CTkLabel(fare_frame,text="Estimated Fare: Rs 0.00",font=ctk.CTkFont(size=16, weight="bold"))
        self.fare_label.place(x=250, y=5)
        # Initialize fare
        self.update_fare()

        # Book button
        self.book_button = ctk.CTkButton(self,text="Book Ride",width=440,fg_color="#2D5A27",hover_color="#1E3D1A",command=self.book_ride)
        self.book_button.place(x=220, y=480)
        self.selected_fare = 0.00

    def update_fare(self, *args):
        # Fare calculation based on vehicle type
        base_fare = {
            "Standard": 1000,
            "Premium": 2000,
            "Luxury": 3000
        }
        
        self.selected_fare = base_fare[self.vehicle_var.get()] # store taxi-type fare in selected_fare
        
        if self.pickup_entry.get() and self.dropoff_entry.get():# Add distance-based fare if locations are selected
            
            # storing pickup and dropoff location
            pickup = self.pickup_entry.get()
            dropoff = self.dropoff_entry.get()
            
            #Fare calculations
            if pickup == dropoff:
                self.selected_fare = 0.00
            elif( pickup == "Kathmandu" and dropoff=="Pokhara") or ( dropoff == "Kathmandu" and pickup=="Pokhara"):# 2000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 2000
            elif( pickup == "Kathmandu" and dropoff=="Lalitpur") or ( dropoff == "Kathmandu" and pickup=="Lalitpur"):# 500 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 500
            elif( pickup == "Kathmandu" and dropoff=="Bhaktapur") or ( dropoff == "Kathmandu" and pickup=="Bhaktapur"):# 500 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 500
            elif( pickup == "Kathmandu" and dropoff=="Biratnagar") or ( dropoff == "Kathmandu" and pickup=="Biratnagar"):# 3000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 3000
            elif( pickup == "Pokhara" and dropoff=="Lalitpur") or ( dropoff == "Pokhara" and pickup=="Lalitpur"):# 2000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 2000
            elif( pickup == "Pokhara" and dropoff=="Bhaktapur") or ( dropoff == "Pokhara" and pickup=="Bhaktapur"):# 2000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 2000
            elif( pickup == "Pokhara" and dropoff=="Biratnagar") or ( dropoff == "Pokhara" and pickup=="Biratnagar"):# 2000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 2000
            elif( pickup == "Lalitpur" and dropoff=="Bhaktapur") or ( dropoff == "Lalitpur" and pickup=="Bhaktapur"):# 500 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 500
            elif( pickup == "Lalitpur" and dropoff=="Biratnagar") or ( dropoff == "Lalitpur" and pickup=="Biratnagar"):# 3000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 3000
            elif( pickup == "Bhaktapur" and dropoff=="Biratnagar") or ( dropoff == "Bhaktapur" and pickup=="Biratnagar"):# 3000 Rs added to base_fare for this distance
                self.selected_fare = self.selected_fare + 3000
                
        self.fare_label.configure(text=f"Estimated Fare: Rs {self.selected_fare:.2f}")
    
    # on clicking the book button this function is called
    def book_ride(self):
        # setting up all the entries
        pickup = self.pickup_entry.get()
        dropoff = self.dropoff_entry.get()
        date = f"{self.year_entry.get()}-{self.month_entry.get()}-{self.day_entry.get()}"
        time = f"{self.hour_entry.get()}:{self.minute_entry.get()}"
        vehicle = self.vehicle_var.get()
        fare=self.selected_fare
        ride_status="Pending"
        id=self.passenger_id
        # Display a confirmation dialog to the user
        confirmation_message = f"Do you want to book the ride with the following details?\n\nPickup: {pickup}\nDropoff: {dropoff}\nDate: {date}\nTime: {time}\nVehicle: {vehicle}\nFare: {fare}"

        if(fare>0):
        # Ask for user confirmation
            response = messagebox.askyesno("Confirm Booking", confirmation_message)
            if response:
                # mysql connection and sending dadta to bookings table
                try:
                    with  self._conn_.cursor() as cursor:
                        query = "INSERT INTO bookings (passenger_id, pickup,dropoff,ride_date,ride_time,vehicle_type,fare,ride_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query,(id,pickup,dropoff,date,time,vehicle,fare,ride_status))
                        self._conn_.commit()

                except Exception as e:
                    messagebox.showerror("Error", f"An unexpected error occurred: {e}")
                finally:
                    messagebox.showinfo("Success", "Taxi Booked successfully!")
        else:
            messagebox.showerror("Error","Invalid Booking")
