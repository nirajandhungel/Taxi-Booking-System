import customtkinter as ctk
from sql_connection import DatabaseConnection
from Starting.start import Start
from Starting.login_signup import StartFrame
from Starting.register_signup import RegisterSignup
from Passenger.signup import PassengerSignUp
from Driver.registration import DriverRegistration
from Passenger.dashboard import PassengerDashboard
from Driver.dashboard import DriverDashboard
from Starting.login import Login
from Admin.dashboard import AdminDashboard
import os


ctk.set_appearance_mode("light")  # Appearance mode
ctk.set_default_color_theme("green")  # Theme color

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__() #Calls the initializer of the parent class (ctk.CTk) 
        self.title("Sahara")
        self.geometry("800x600")  # Default size
        self.minsize(800, 600)   # Minimum size to avoid shrinking
        # Load the icon
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "sahara_icon.ico")
        self.iconbitmap(icon_path)  # Set the custom icon
        DatabaseConnection.connection()

        # Data dictionary to store id when logged in
        self.shared_data = {
            "passenger_id": None,
            "driver_id": None,
            "admin_id": None,
        }
        print(f'{self.shared_data}, In main.py')

        # Create container frame for all screens
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Configure row/column weights for responsiveness
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # Dictionary to store frames
        self.initialized_frames = set()  # Track initialized frames

        # Frame classes (lazy loading setup)
        self.frame_classes = {
            "Start": Start,
            "StartFrame": StartFrame,
            "RegisterSignup": RegisterSignup,
            "PassengerSignUp": PassengerSignUp,
            "DriverRegistration": DriverRegistration,
            "PassengerDashboard": PassengerDashboard,
            "DriverDashboard": DriverDashboard,
            "Login": Login,
            "AdminDashboard": AdminDashboard
        }

        self.show_frame("Start")  # Shows the initial frame

#The show_frame method abstracts away the complexity of switching between frames.

    def show_frame(self, page_name):
        """Display the specified frame, initializing it if necessary."""
        if page_name not in self.initialized_frames:
            # Initialize the frame and pass shared data
            frame_class = self.frame_classes[page_name]  # Initializse the frame by fetching the frame class from the frame_classes dictionary
            frame = frame_class(parent=self.container, controller=self, shared_data=self.shared_data) 
            # Create an instance of the frame class, passing the container (parent), controller, 
            #controller refers to the current instance of the class
            self.frames[page_name] = frame 
            # Store the initialized frame in the frames dictionary with the page_name as the key
            frame.grid(row=0, column=0, sticky="nsew")
            # east west north south
            self.initialized_frames.add(page_name) #Marks the frame as initialized by adding the page_name to the initialized_frames set.
        frame = self.frames[page_name]
        # If showing the ProfileFrame, update the passenger_id
        if page_name == "PassengerDashboard" and "passenger_id" in self.shared_data:
            frame.update_id(self.shared_data["passenger_id"])
        # If showing the ProfileFrame, update the passenger_id
        if page_name == "DriverDashboard" and "driver_id" in self.shared_data:
            frame.update_id(self.shared_data["driver_id"])
        # If showing the ProfileFrame, update the passenger_id
        if page_name == "AdminDashboard" and "admin_id" in self.shared_data:
            frame.update_id(self.shared_data["admin_id"])

        frame.tkraise()  # Bring the frame to the front
#Different types of frames can be displayed using the same show_frame method,
# demonstrating the ability to handle different classes through a single interface.

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
