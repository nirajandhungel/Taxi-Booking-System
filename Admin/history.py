import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from sql_connection import DatabaseConnection
from fonts.colors import Colors

#  class of history rides whuch shows all the booking histories
class HistoryRidesFrame(ctk.CTkFrame): 
    def __init__(self, parent):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.pack_propagate(False)
        self._conn_=DatabaseConnection.connection()
        
        # Header
        self.header = ctk.CTkLabel(self, text=" Rides History", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # Create scrollable frame for bookings
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=850, height=600)
        self.scrollable_frame.place(x=20, y=70)

        self.load_history()
    # loading all history
    def load_history(self):
        try:
            # Clear existing bookings
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # connection and sql queries
            self._conn_=DatabaseConnection.connection()
            cursor = self._conn_.cursor()
            query="""SELECT 
                            b.ride_date, 
                            b.ride_time, 
                            b.id, 
                            p.full_name AS passenger_name, 
                            d.full_name AS driver_name, 
                            b.pickup, 
                            b.dropoff, 
                            b.vehicle_type, 
                            b.fare,
                            b.ride_status
                        FROM 
                            bookings b
                        LEFT JOIN 
                            drivers d
                            ON b.driver_id = d.id -- Correct join condition
                        LEFT JOIN 
                            passengers p
                            ON b.passenger_id = p.id -- Correct join condition;
            """
            cursor.execute(query)
            bookings = cursor.fetchall()
            
            # if data is empty on database
            if not bookings:
                self.no_history_rides() 
                
            # else showing booking details
            else:
                for booking in bookings:
                    self.create_booking_card(booking)
        # handling mysql error
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        # at last
    # function of  no any history         
    def no_history_rides(self):
        card = ctk.CTkFrame(self.scrollable_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(card, text=f"No History of rides . Check back later!").pack(side="left", padx=10)

    def create_booking_card(self, booking):
        card = ctk.CTkFrame(self.scrollable_frame,width=int(self.scrollable_frame.winfo_width() * 0.95), height=250)
        card.pack(pady=10, padx=10, fill="x")
        
        # Date and status (placed at the top of the card)
        header_frame = ctk.CTkFrame(card, height=30)
        header_frame.pack(pady=5, fill="x")
      
        # Booking details
        ctk.CTkLabel(header_frame,text=f"Date: {booking[0]}   {booking[1]}",font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        ctk.CTkLabel(card, text=f"Booking ID: {booking[2]}", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 0), anchor="w", padx=10)
        ctk.CTkLabel(card, text=f"Passenger: {booking[3]}", font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)
        ctk.CTkLabel(card, text=f"Driver: {booking[4]}", font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)
        ctk.CTkLabel(card, text=f"From: {booking[5]} → To: {booking[6]}", font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)


        status_colors = Colors.RED if booking[9] == "Cancelled"  else Colors.GREEN if booking[9] == "Completed" else Colors.BLUE
        # Assign driver button
        pending_button = ctk.CTkButton(header_frame,text=booking[9],width=120,fg_color=status_colors,hover_color=status_colors)
        pending_button.pack(side="right")
