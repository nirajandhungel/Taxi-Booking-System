import customtkinter as ctk
from fonts.colors import Colors
from PIL import Image,ImageTk
import os
from Driver.profile import ProfileFrame
from Driver.history import RideHistoryFrame
from Driver.manage_ride import ManageRidesFrame


class DriverDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller, shared_data):
        super().__init__(parent)
        self.shared_data = shared_data
        self.controller = controller
        
        # Get initial Driver ID
        self.driver_id = self.shared_data.get("driver_id",None)
        
        print(f'Driver shared data at the top (initial): {self.shared_data}')  # Debugging statement
        print(f'Driver ID at the top (initial): {self.driver_id}')  # Debugging statement

        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, height=800, corner_radius=0)
        self.sidebar.place(x=0, y=0)
        
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
        nav_items = ["Manage Rides", "Ride History", "Profile"]
        self.nav_buttons = []
        
        for i, item in enumerate(nav_items):
            button = ctk.CTkButton(self.sidebar,text=item,width=160,fg_color=Colors.GREEN_BUTTON,hover_color=Colors.GREEN_BUTTON_HOVER,
                                   command=lambda x=item: self.switch_frame(x))
            button.place(x=20, y=100 + i*50)
            self.nav_buttons.append(button)

        # Logout button
        logout = ctk.CTkButton(self.sidebar,text='Log Out',width=160,fg_color=Colors.RED,hover_color=Colors.HOVER_RED,
                               command=lambda: controller.show_frame('Login'))
        logout.place(x=20, y=700)

        # Main content area
        self.main_frame = ctk.CTkFrame(self, width=960, height=760)
        self.main_frame.place(x=220, y=20)

        # Initialize frames
        self.frames = {
            "Manage Rides": ManageRidesFrame(self.main_frame,self.driver_id),
            "Ride History": RideHistoryFrame(self.main_frame,self.driver_id),
            "Profile": ProfileFrame(self.main_frame, self.driver_id)
        }

        # Show default frame
        self.current_frame = self.frames["Manage Rides"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
    def update_id(self, driver_id=None):
        """Update the passenger_id and refresh the user profile."""
        self.driver_id = driver_id
        # Reinitialize frames with the updated passenger_id
        self.frames = {
            "Manage Rides": ManageRidesFrame(self.main_frame,self.driver_id),
            "Ride History": RideHistoryFrame(self.main_frame,self.driver_id),
            "Profile": ProfileFrame(self.main_frame, self.driver_id)
        }

        # Update the currently displayed frame
        if self.current_frame:
            self.current_frame.place_forget()
    
        # Default frame to show after update
        self.current_frame = self.frames["Manage Rides"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)

    def switch_frame(self, frame_name):
        # Hide current frame
        self.current_frame.place_forget()
        
        # Show selected frame
        self.current_frame = self.frames[frame_name]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)

 