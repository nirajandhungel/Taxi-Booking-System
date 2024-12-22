import customtkinter as ctk
from PIL import Image,ImageTk
import os
from Admin.manage_booking import BookingManagementFrame
from Admin.manage_driver import DriverManagementFrame
from Admin.driver_request import DriverRequestFrame
from Admin.history import HistoryRidesFrame
from fonts.colors import Colors

#It represents the dashboard view for the admin user. 
class AdminDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller, shared_data):
        super().__init__(parent)
        self.shared_data = shared_data
        self.controller = controller
        
        # Get initial passenger ID
        self.admin_id = self.shared_data.get("admin_id", None)
        print(f"Admin ID at the  Dashboard (initial): {self.admin_id}")  # Debugging

        # Sidebar setup
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
        nav_items = ["Booking Management", "Driver Management", "Rides History", "Driver's Request"]
        self.nav_buttons = []
        
        # self.frames = {}
        for i, item in enumerate(nav_items):
            button=ctk.CTkButton(
                self.sidebar,
                text=item,
                width=160,
                fg_color=Colors.GREEN_BUTTON,
                hover_color=Colors.GREEN_BUTTON_HOVER,
                command=lambda x=item: self.switch_frame(x)
            )
            button.place(x=20, y=100 + i * 50)
            self.nav_buttons.append(button)
            
        # Logout button
        ctk.CTkButton(self.sidebar,text="Log Out",width=160,fg_color=Colors.RED,hover_color=Colors.HOVER_RED,
                      command=lambda: controller.show_frame("Login")).place(x=20, y=700)

        # Main content area
        self.main_frame = ctk.CTkFrame(self, width=960, height=760)
        self.main_frame.place(x=220, y=20)

        # Mapping frame names to their respective classes
        self.frames= {
            "Booking Management": BookingManagementFrame(self.main_frame,self.admin_id),
            "Driver Management": DriverManagementFrame(self.main_frame),
            "Rides History": HistoryRidesFrame(self.main_frame),
            "Driver's Request": DriverRequestFrame(self.main_frame)
        }

        # Load and display the default frame
        self.current_frame = self.frames["Booking Management"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
    
    def update_id(self, admin_id=None):
        """Update the passenger_id and refresh the user profile."""
        self.admin_id = admin_id
        
        # Reinitialize frames with the updated passenger_id
        self.frames= {
            "Booking Management": BookingManagementFrame(self.main_frame,self.admin_id),
            "Driver Management": DriverManagementFrame(self.main_frame),
            "Rides History": HistoryRidesFrame(self.main_frame),
            "Driver's Request": DriverRequestFrame(self.main_frame)
        }
        # Update the currently displayed frame
        if self.current_frame:
            self.current_frame.place_forget()
    
        # Default frame to show after update
        self.current_frame = self.frames["Booking Management"]
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
    def switch_frame(self, frame_name):
        """Switches to the selected frame and updates its content dynamically."""
        # Destroy the current frame if it exists
        self.current_frame.place_forget()
        
        self.current_frame = self.frames[frame_name]
        # Refresh the frame if it has a refresh method
        if hasattr(self.current_frame, "load_bookings"):
            self.current_frame.load_bookings(self.admin_id)
        if hasattr(self.current_frame, "load_history"):
            self.current_frame.load_history()
        if hasattr(self.current_frame, "load_driver_requests"):
            self.current_frame.load_driver_requests(self.admin_id)
        if hasattr(self.current_frame, "load_drivers"):
            self.current_frame.load_drivers()
        
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)
