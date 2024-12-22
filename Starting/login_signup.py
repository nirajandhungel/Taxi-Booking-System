import customtkinter as ctk
from fonts.colors import Colors
class StartFrame(ctk.CTkFrame):
    def __init__(self, parent, controller,shared_data):
        super().__init__(parent)
        self.controller = controller
        self.shared_data = shared_data
        self.configure(fg_color=Colors.DGREEN)  # Green background

        # login Section
        self.login_label = ctk.CTkLabel(self,text="Already have an account ?",font=("Montserrat", 20),
            text_color="black"
        )
        self.login_label.place(relx=0.5, rely=0.2, anchor="center")  # Positioned near the top centre

        self.login_button = ctk.CTkButton(self,text="Log In",font=("Montserrat Bold", 18),width=200,height=60,hover_color="#333333",
            fg_color="#000000",
            command=lambda: controller.show_frame("Login")
        )
        self.login_button.place(relx=0.5, rely=0.3, anchor="center")  # Below the login label

        # Separator
        self.separator = ctk.CTkFrame(self, height=2, fg_color="gray70", width=600)
        self.separator.place(relx=0.5, rely=0.45, anchor="center")  # Positioned in the middle as a horizontal line

        # Passenger Section
        self.passenger_label = ctk.CTkLabel(self,text="Create a new account ?",font=("Montserrat", 20),text_color="black")
        self.passenger_label.place(relx=0.5, rely=0.55, anchor="center")  # Positioned below the separator

        self.passenger_button = ctk.CTkButton(
            self,
            text="Sign Up",
            font=("Montserrat Bold", 18),
            width=200,
            height=60,
            hover_color="#333333",
            fg_color="#000000",
            command=lambda: controller.show_frame("RegisterSignup")
        )
        self.passenger_button.place(relx=0.5, rely=0.65, anchor="center")  # Below the passenger label
