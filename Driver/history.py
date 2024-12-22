import customtkinter as ctk
from sql_connection import DatabaseConnection
from fonts.colors import Colors

class RideHistoryFrame(ctk.CTkFrame):
    def __init__(self, parent,driver_id=None):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.driver_id=driver_id
        self._conn_=DatabaseConnection.connection()   
        # Initialize ride details list
        ride_details = []
        try:
            cursor = self._conn_.cursor()
            query="""SELECT 
                    c.full_name AS customer_name, 
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
                    passengers c
                ON 
                    b.passenger_id = c.id -- Correct join condition
                WHERE  
                    b.driver_id = %s;
            """
            cursor.execute(query,[self.driver_id])
            self.dets = cursor.fetchall()
            
            
            # Header
            self.header = ctk.CTkLabel(self,text="Ride History",font=ctk.CTkFont(size=24, weight="bold"))
            self.header.pack(pady=(20, 10))

            # Create scrollable frame for ride history
            self.scrollable_frame = ctk.CTkScrollableFrame(self,width=int(self.winfo_width() * 0.95),height=600)
            self.scrollable_frame.pack(padx=20, pady=(0, 20), fill="both", expand=True)
            
            # Process fetched data into ride_details format
            if not self.dets:
                self.no_ride_history() 
                
            else:
                for ride in self.dets:
                    ride_dict = {
                        "passenger": ride[0],  #  column 2 is the Passenger name
                        "from": ride[1],  #  column 5 is the 'from' location
                        "to": ride[2],  #  column 6 is the 'to' location
                        "date": ride[3],  #  column 7 is the date
                        "time": ride[4],  #  column 8 is the time
                        "vehicle": ride[5],  #  cloumn 9 is vehicle type
                        "fare": f"Rs {ride[6]}",  #  column 10 is the fare
                        "status": ride[7]  #  column 11 is the ride status
                    }
                    ride_details.append(ride_dict)  # Add ride dictionary to the list
                
        finally:
            print(self.dets)

        # Sample ride history
        for i, ride in enumerate(ride_details):
            self.create_ride_card(ride)
        
    def no_ride_history(self):
        self.scrollable_frame.pack(fill="both", expand=True)  # Make parent frame fill the entire window.
        frame = ctk.CTkFrame(self.scrollable_frame)
        frame.pack(fill="both", expand=True)  # Make the frame fill the parent container.
        ctk.CTkLabel(frame, text=f"No Ride history").pack(side="left", padx=10)

    def create_ride_card(self, ride):
        # Card container
        card = ctk.CTkFrame(self.scrollable_frame,width=int(self.scrollable_frame.winfo_width() * 0.95),height=160)
        card.pack(pady=10, padx=10, fill="x")

        # Date and status
        header_frame = ctk.CTkFrame(card, height=30)
        header_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(header_frame,text=f"Date: {ride["date"]}",font=ctk.CTkFont(size=14)).pack(side="left", padx=10)

        status_color = None
        if ride["status"] == "Completed":
            status_color = Colors.GREEN  # Green for completed
        elif ride["status"] == "Cancelled":
            status_color = Colors.RED  # Red for cancelled
        elif ride["status"] == "Assigned":
            status_color = Colors.BLUE  # Blue for pending
        
        ctk.CTkLabel(header_frame,text=ride["status"],text_color=status_color,font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=10)

        # Passenger information
        ctk.CTkLabel(card,text=f"Passenger: {ride['passenger']}",font=ctk.CTkFont(size=14)).pack(pady=(5, 0), anchor="w", padx=10)

        # Route information
        ctk.CTkLabel(card,text=f"From: {ride['from']}").pack(pady=(5, 0), anchor="w", padx=10)

        ctk.CTkLabel(card,text=f"To: {ride['to']}").pack(pady=(5, 0), anchor="w", padx=10)

        # Fare information
        ctk.CTkLabel(card,text=f"Fare: {ride['fare']}",font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(5, 10), anchor="w", padx=10)
