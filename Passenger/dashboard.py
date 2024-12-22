import customtkinter as ctk
from PIL import Image,ImageTk
import os
from Passenger.book import BookingFrame
from Passenger.profile import ProfileFrame
from Passenger.history import RideHistoryFrame
from fonts.colors import Colors

class PassengerDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller, shared_data=None):
        super().__init__(parent)
        self.shared_data = shared_data
        self.controller = controller
    
        self.passenger_id = self.shared_data.get("passenger_id", None)
        # self.update_id(self.passenger_id)
        # Get initial passenger ID
        print(f"Passenger ID after update id in Passenger Dashboard : {self.passenger_id}")  # Debugging

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, height=800, corner_radius=0)
        self.sidebar.place(x=0, y=0)
        
        # Taxi image
        # Load and resize the image
        sahara_path = os.path.join(os.path.dirname(__file__), "..", "assets", "sahara3.png")
        sahara_image = Image.open(sahara_path)
        resized_sahara_image = sahara_image.resize((250, 85))  # Resize to 100x100 pixels (adjust as needed)

        # Convert the resized image to PhotoImage
        self.sahara_photo = ImageTk.PhotoImage(resized_sahara_image)

        # Create and place the label
        self.sahara_label = ctk.CTkLabel(self.sidebar, image=self.sahara_photo, text="")
        self.sahara_label.place(x=110, y=50, anchor="center")

        # Navigation buttons
        nav_items = ["Book Ride", "Ride Details", "Profile"]
        self.nav_buttons = []

        for i, item in enumerate(nav_items):
            button = ctk.CTkButton(
                self.sidebar, text=item, width=160, 
                fg_color=Colors.GREEN_BUTTON,
                hover_color=Colors.GREEN_BUTTON_HOVER,
                command=lambda x=item: self.switch_frame(x)
            )
            button.place(x=20, y=100 + i * 50)
            self.nav_buttons.append(button)

        # Logout Button
        logout = ctk.CTkButton(
            self.sidebar, text='Log Out', width=160, fg_color=Colors.RED,
            hover_color=Colors.HOVER_RED, command=lambda: controller.show_frame('Login')
        )
        logout.place(x=20, y=700)

        # Main content area
        self.main_frame = ctk.CTkFrame(self, width=960, height=760)
        self.main_frame.place(x=220, y=20)

        # Initialise frames
        self.frames = {
            "Book Ride": BookingFrame(self.main_frame,self.passenger_id),
            "Ride Details": RideHistoryFrame(self.main_frame, self.passenger_id),
            "Profile": ProfileFrame(self.main_frame, self.passenger_id)
        }

        # Show default frame
        self.current_frame = self.frames["Book Ride"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
    def update_id(self, passenger_id=None):
        """Update the passenger_id and refresh the user profile."""
        self.passenger_id = passenger_id
        print(f"Passenger id inside update id {self.passenger_id}")
        # Reinitialize frames with the updated passenger_id
        self.frames = {
            "Book Ride": BookingFrame(self.main_frame, self.passenger_id),
            "Ride Details": RideHistoryFrame(self.main_frame, self.passenger_id),
            "Profile": ProfileFrame(self.main_frame, self.passenger_id)
        }

        # Update the currently displayed frame
        if self.current_frame:
            self.current_frame.place_forget()
    
        # Default frame to show after update
        self.current_frame = self.frames["Book Ride"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
    def switch_frame(self, frame_name):
        # Hide current frame
        self.current_frame.place_forget()

        # Show selected frame
        self.current_frame = self.frames[frame_name]
        # Refresh the frame if it has a refresh method
        if hasattr(self.current_frame, "connection_and_history"):
            self.current_frame.connection_and_history()
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
        