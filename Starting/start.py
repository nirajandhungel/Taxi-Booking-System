import customtkinter as ctk  
from fonts.colors import Colors  # Importing custom colour definitions
from PIL import Image, ImageTk  # Importing Pillow for image handling
import os  # for file path handling

class Start(ctk.CTkFrame):
    def __init__(self, parent, controller, shared_data):
        super().__init__(parent)
        self.controller = controller  # Reference to the main application controller
        self.shared_data = shared_data  # Shared data across frames
        self.configure(fg_color=Colors.DGREEN)  # Setting the background colour to dark green

        # Title text
        title_label = ctk.CTkLabel(self, text="Safety, Safety, Safety", font=("Montserrat", 28, "italic"), text_color="black")  # Creating a label for the title
        title_label.place(relx=0.5, rely=0.1, anchor="center")  # Positioning 

        # Taxi image
        taxi_path = os.path.join(os.path.dirname(__file__), "..", "assets", "taxi.png")  
        # Path to the taxi image file
        taxi_image = Image.open(taxi_path)  # Opening the taxi image
        self.taxi_photo = ImageTk.PhotoImage(taxi_image)  # Converting the image for Tkinter
        self.taxi_label = ctk.CTkLabel(self, image=self.taxi_photo, text="")  
        # Creating a label to display the image
        self.taxi_label.place(relx=0.5, rely=0.5, anchor="center")  # Positioning the image label

        # Start label
        button_label = ctk.CTkLabel(
            self, 
            text="Driver or Passenger", 
            font=("Montserrat", 16), 
            text_color="black"
        )  # Label to prompt user choice
        button_label.place(relx=0.5, rely=0.75, anchor="center")  # Positioning the prompt label

        # Start button
        start_button = ctk.CTkButton(self,text="Start",  font=("Montserrat Bold", 16),  width=200,  height=50,  fg_color="black",
            hover_color="#333333",  
            command=lambda: controller.show_frame("StartFrame")  
            # Command to switch to the "StartFrame"
        )
        start_button.place(relx=0.5, rely=0.85, anchor="center")  # Positioning the start button
