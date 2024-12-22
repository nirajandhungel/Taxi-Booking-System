import customtkinter as ctk
from tkinter import messagebox
from fonts.colors import Colors
from sql_connection import DatabaseConnection

class RideHistoryFrame(ctk.CTkFrame):
    def __init__(self, parent,passenger_id=None):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.passenger_id = passenger_id
        self._conn_=DatabaseConnection.connection()
        self.connection_and_history()
        
    def connection_and_history(self): 
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
    
        # Initialize ride details list
        self._conn_=DatabaseConnection.connection()
        self.pending_ride_details = []
        self.other_status_ride_details = []
        cursor = self._conn_.cursor()
        query="""SELECT 
                    b.id, 
                    d.full_name AS driver_name, 
                    b.pickup, 
                    b.dropoff, 
                    b.ride_date, 
                    b.ride_time, 
                    b.vehicle_type, 
                    b.fare,
                    b.ride_status
                FROM 
                    bookings b
                LEFT JOIN 
                    drivers d
                ON 
                    b.driver_id = d.id -- Correct join condition
                WHERE  
                    b.passenger_id = %s;
            """
    
        cursor.execute(query,[self.passenger_id])
        self.dets = cursor.fetchall()
        
        # Header
        self.header = ctk.CTkLabel(self,text="Ride History",font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(pady=(20, 10))  # Space around the header

        # Create scrollable frame for ride history
        self.scrollable_frame = ctk.CTkScrollableFrame(self,width=int(self.winfo_width() * 0.95),height=600)
        self.scrollable_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        
        # Process fetched data into ride_details format
        if self.dets:
            for ride in self.dets:
                ride_dict = {
                    "id":ride[0],
                    "driver": ride[1],  # Assuming column 4 is the driver name
                    "from": ride[2],  # Assuming column 5 is the 'from' location
                    "to": ride[3],  # Assuming column 6 is the 'to' location
                    "date": ride[4],  # Assuming column 7 is the date
                    "time": ride[5],  # Assuming column 8 is the time
                    "vehicle": ride[6],  # Assuming cloumn 9 is vehicle type
                    "fare": f"Rs {ride[7]}",  # Assuming column 10 is the fare
                    "status": ride[8]  # Assuming column 11 is the ride status
                }
                # Check the status of the ride and categorize it
                if ride_dict["status"] == "Pending" or ride_dict["status"] == "Assigned" :
                    self.pending_ride_details.append(ride_dict)  # Add to pending rides
                else:
                    self.other_status_ride_details.append(ride_dict)  # Add to other status rides            
        else:
                self.no_ride_history() 
                

        # Sample ride history
        for i, ride in enumerate(self.pending_ride_details):
            self.pending_ride_card(ride)
        for i, ride in enumerate(self.other_status_ride_details):
            self.other_status_ride_card(ride)
            
    def no_ride_history(self):
        self.scrollable_frame.pack(fill="both", expand=True)  # Make parent frame fill the entire window.
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="both", expand=True)  # Make the frame fill the parent container.
        ctk.CTkLabel(frame, text=f"No Ride history").pack(side="left", padx=10)

    def pending_ride_card(self, ride):
        # Card container
        card = ctk.CTkFrame(self.scrollable_frame,width=int(self.scrollable_frame.winfo_width() * 0.95),height=160)
        card.pack(pady=10, padx=10, fill="x")  # Add padding and fill horizontally

        # Date and status (placed at the top of the card)
        header_frame = ctk.CTkFrame(card, height=30)
        header_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(header_frame,text=f"Date: {ride['date']}   {ride['time']}",font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

        status_color = "#0000ff"  # Blue for pending
            
        ctk.CTkLabel(header_frame,text=ride["status"],text_color=status_color,font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=10)
        # Driver information
        ctk.CTkLabel(card,text=f"Driver: {ride['driver']}",font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)

        # Route information
        ctk.CTkLabel(card,text=f"From: {ride['from']}",).pack(pady=(5, 0), anchor="w", padx=10)
        ctk.CTkLabel(card,text=f"To: {ride['to']}").pack(pady=(5, 0), anchor="w", padx=10)
        
        # Fare information
        ctk.CTkLabel(card,text=f"Fare: {ride['fare']}",font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 10), anchor="w", padx=10)
        
        # Buttons placed at the top of the card
        footer_frame = ctk.CTkFrame(card, height=30)
        footer_frame.pack(pady=5, fill="x")
        ctk.CTkButton(footer_frame,text="Complete",hover_color=Colors.GREEN_BUTTON_HOVER,
                      width=90,fg_color=Colors.GREEN_BUTTON,font=ctk.CTkFont(size=16, weight="bold") ,
                      command=lambda: self.complete_ride(ride['id'],ride['driver'])).pack(side="left")
        ctk.CTkButton(footer_frame,text="Cancel",hover_color=Colors.HOVER_RED,
                      width=90,fg_color=Colors.RED,font=ctk.CTkFont(size=16, weight="bold") ,
                      command=lambda: self.cancel_ride(ride['id'])).pack(side="right")
    def complete_ride(self,id,driver):
        print(driver)
        response = messagebox.askyesno("Confirm Complete", "Are you sure you want to complete the ride ?")
        if response:  
            if not driver: 
                messagebox.showerror("Error", "Can't complete ride without driver ! ")
                
            else:
                cursor=self._conn_.cursor()
                cursor.execute("UPDATE bookings SET ride_status='Completed' WHERE id = %s",(id,))
                self._conn_.commit()
                self.connection_and_history()# for dynamic changes 
                messagebox.showinfo("Success", "Ride completed ! ")
    def cancel_ride(self,id):
        response = messagebox.askyesno("Confirm ", "Are you sure you want to cancel the ride ?")
        if response:
            cursor=self._conn_.cursor()
            cursor.execute("UPDATE bookings SET ride_status='Cancelled' WHERE id = %s",(id,))
            self._conn_.commit()
            self.connection_and_history() # for dynamic changes
            messagebox.showinfo("Success", "Ride cancelled ! ")

    
    def other_status_ride_card(self, ride):
        # Card container
        card = ctk.CTkFrame(self.scrollable_frame,width=int(self.scrollable_frame.winfo_width() * 0.95),height=160)
        card.pack(pady=10, padx=10, fill="x")  # Add padding and fill horizontally

        # Date and status (placed at the top of the card)
        header_frame = ctk.CTkFrame(card, height=30)
        header_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(header_frame,text=f"Date: {ride['date']}   {ride['time']}",font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        status_color = None
        status_color = Colors.GREEN_BUTTON if  ride["status"] == "Completed" else Colors.RED 
        ctk.CTkLabel(header_frame,text=ride["status"],text_color=status_color,font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=10)
        # Driver information
        ctk.CTkLabel(card,text=f"Driver: {ride['driver']}",font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)
        # Route information
        ctk.CTkLabel(card,text=f"From: {ride['from']}",).pack(pady=(5, 0), anchor="w", padx=10)
        ctk.CTkLabel(card,text=f"To: {ride['to']}").pack(pady=(5, 0), anchor="w", padx=10)
        # Fare information
        ctk.CTkLabel(card,text=f"Fare: {ride['fare']}",font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 10), anchor="w", padx=10)
