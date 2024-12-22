import customtkinter as ctk
from fonts.colors import Colors
from PIL import Image, ImageTk
import os

class RegisterSignup(ctk.CTkFrame):
    def __init__(self, parent, controller,shared_data):
        super().__init__(parent)
        self.controller = controller
        self.shared_data = shared_data

        # Set background colour for the entire frame
        self.configure(fg_color="#E5E5E5")  # Light grey
        # Back Button

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, fg_color=Colors.GREEN, corner_radius=0)
        self.sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)  # Sidebar takes 20% width of the window
        
        # Add sidebar content
        self.add_sidebar_content()

        # Main content area
        self.main_frame = ctk.CTkFrame(self, fg_color="#E5E5E5", corner_radius=0)
        self.main_frame.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)  # Main content takes 80% width of the window

        # Add main content
        self.add_main_content()

    def add_sidebar_content(self):
        # Sidebar Quote Image
        self.back_button = ctk.CTkButton(self.sidebar,text="Back",width=80,height=32,corner_radius=16,fg_color="black",hover_color="#333333",command=lambda: self.controller.show_frame("StartFrame"))
        self.back_button.place(x=20, y=20)  # Position at the top-left corner
        
        
        
        current_dir = os.path.dirname(__file__)  # Directory of this file (A)
        assets_dir = os.path.join(current_dir, "..","assets")  # Go up one level and into assets
        quote_path = os.path.join(assets_dir, "quote3.png")  # Path to the image
        quote_image = Image.open(quote_path).resize((200, 200))  # Resize as needed
        self.quote_photo = ImageTk.PhotoImage(quote_image)
        
        

        self.quote_label = ctk.CTkLabel(self.sidebar, image=self.quote_photo, text="")
        self.quote_label.place(relx=0.5, rely=0.3, anchor="center")  # Centered in the sidebar

        # Sidebar Text
        safety_label = ctk.CTkLabel(
            self.sidebar,
            text="Let's, Get Started!",
            font=("Montserrat", 24, "italic"),
            text_color="black",
        )
        safety_label.place(relx=0.5, rely=0.7, anchor="center")  # Positioned below the image

    def add_main_content(self):
        # Already have an account label
        account_label = ctk.CTkLabel(
            self.main_frame,
            text="Sign Up as a Passenger?",
            font=("Montserrat", 18),
            text_color="black",
        )
        account_label.place(relx=0.5, rely=0.2, anchor="center")

        # Log In button
        login_button = ctk.CTkButton(
            self.main_frame,
            text="Sign Up",
            font=("Montserrat", 16, "bold"),
            fg_color=Colors.GREEN,
            hover_color="#00CC00",
            width=200,
            height=50,
            text_color="black",
            command=lambda: self.controller.show_frame("PassengerSignUp")
        )
        login_button.place(relx=0.5, rely=0.3, anchor="center")

        # Create a new account label
        create_label = ctk.CTkLabel(self.main_frame,text="Register as a Driver ?",font=("Montserrat", 18),text_color="black",
        )
        create_label.place(relx=0.5, rely=0.5, anchor="center")

        # Sign Up button
        signup_button = ctk.CTkButton(
            self.main_frame,
            text="Register",
            font=("Montserrat", 16, "bold"),
            fg_color=Colors.GREEN,
            hover_color="#00CC00",
            width=200,
            height=50,
            text_color="black",
            command=lambda: self.controller.show_frame("DriverRegistration")
        )
        signup_button.place(relx=0.5, rely=0.6, anchor="center")
