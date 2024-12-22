import customtkinter as ctk  
from tkinter import messagebox  
from fonts.colors import Colors  # Importing custom colour definitions
import re  # Importing regex module for validation
from sql_connection import DatabaseConnection  # Importing custom database connection
import mysql.connector  # Importing MySQL connector for database interactions
import bcrypt  # Importing bcrypt for password hashing

class PassengerSignUp(ctk.CTkFrame):
    def __init__(self, parent, controller, shared_data):
        super().__init__(parent)
        self.controller = controller  # Reference to the main application controller
        self.shared_data = shared_data  # Shared data across frames
        self.configure(fg_color=Colors.GREEN)  # Setting the frame's background colour
        self._conn_ = DatabaseConnection.connection()  # Establishing a protected database connection
        self.signup_ui()  # Calling the UI setup method

    def signup_ui(self):
        # Back Button
        self.back_button = ctk.CTkButton(
            self,
            text="Back", 
            width=80, 
            height=32, 
            corner_radius=16, 
            fg_color="black", 
            hover_color="#333333", 
            command=lambda: self.controller.show_frame("RegisterSignup")
        )  # Button to navigate back to the registration screen
        self.back_button.place(x=20, y=20)  # Positioning at the top-left corner

        # Title
        self.title = ctk.CTkLabel(
            self, 
            text="Sign Up", 
            font=("Montserrat Bold", 24), 
            text_color="black"
        )  # Label for the title
        self.title.place(relx=0.46, y=20, anchor="n")  # Centering the title

        # Full Name Entry
        self.name_label = ctk.CTkLabel(
            self, 
            text="Full Name", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the name field
        self.name_label.place(relx=0.18, y=100)

        self.name_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your full name"
        )  # Input field for the full name
        self.name_entry.place(relx=0.18, y=140)

        # Phone Number Entry
        self.phone_label = ctk.CTkLabel(
            self, 
            text="Phone Number", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the phone number field
        self.phone_label.place(relx=0.18, y=220)

        self.phone_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your phone number"
        )  # Input field for the phone number
        self.phone_entry.place(relx=0.18, y=260)

        # Email Entry
        self.email_label = ctk.CTkLabel(
            self, 
            text="Email", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the email field
        self.email_label.place(relx=0.18, y=340)

        self.email_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your email"
        )  # Input field for the email
        self.email_entry.place(relx=0.18, y=380)

        # Password Entry
        self.password_label = ctk.CTkLabel(
            self, 
            text="Set Password", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the password field
        self.password_label.place(relx=0.18, y=460)

        self.password_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your password", 
            show="*"
        )  # Input field for the password with masked input
        self.password_entry.place(relx=0.18, y=500)

        # Address Entry
        self.address_label = ctk.CTkLabel(
            self, 
            text="Home Address", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the address field
        self.address_label.place(relx=0.5, y=100)

        self.address_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your address"
        )  # Input field for the address
        self.address_entry.place(relx=0.5, y=140)

        # Gender Selection
        self.gender_label = ctk.CTkLabel(
            self, 
            text=" Gender", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for gender selection
        self.gender_label.place(relx=0.5, y=220)

        self.gender_var = ctk.StringVar(value="Male")  # Default gender selection variable
        gender_frame = ctk.CTkFrame(self, width=400, height=45, fg_color="white")  
        # Frame for radio buttons
        gender_frame.place(relx=0.5, y=260)

        self.male_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Male", 
            value="Male", 
            variable=self.gender_var
        )  # Radio button for male gender
        self.male_radio.place(x=10, y=12)

        self.female_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Female", 
            value="Female", 
            variable=self.gender_var
        )  # Radio button for female gender
        self.female_radio.place(x=130, y=12)

        self.others_radio = ctk.CTkRadioButton(
            gender_frame, 
            text="Others", 
            value="Others", 
            variable=self.gender_var
        )  # Radio button for other genders
        self.others_radio.place(x=260, y=12)

        # Age Entry
        self.age_label = ctk.CTkLabel(
            self, 
            text="Age", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for the age field
        self.age_label.place(relx=0.5, y=340)

        self.age_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Enter your age"
        )  # Input field for the age
        self.age_entry.place(relx=0.5, y=380)

        # Confirm Password Entry
        self.confirm_password_label = ctk.CTkLabel(
            self, 
            text="Confirm Password", 
            font=("Montserrat Bold", 14), 
            text_color="black"
        )  # Label for confirm password field
        self.confirm_password_label.place(relx=0.5, y=460)

        self.confirm_password_entry = ctk.CTkEntry(
            self, 
            width=400, 
            height=45, 
            border_width=0, 
            fg_color="white", 
            placeholder_text="Confirm your password", 
            show="*"
        )  # Input field for confirming the password
        self.confirm_password_entry.place(relx=0.5, y=500)

        # Sign Up Button
        self.signup_button = ctk.CTkButton(
            self, 
            width=150, 
            height=40, 
            text="Sign Up", 
            font=("Montserrat Bold", 14), 
            text_color='white', 
            corner_radius=5, 
            fg_color="black", 
            hover_color="#006400", 
            command=self.sign_up
        )  # Button to submit the form
        self.signup_button.place(relx=0.46, y=600)

    def sign_up(self):
        # Validate the form data
        if not self.validate():
            return
        
        try:
            cursor = self._conn_.cursor()
            name = self.name_entry.get()
            number = self.phone_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Hash the password
            gender = self.gender_var.get()
            age = self.age_entry.get()
            address = self.address_entry.get()
            query = """INSERT INTO passengers (full_name,phone_number,email,user_password,gender,age,address) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(query, (name, number, email, hashed_password, gender, age, address))
            self._conn_.commit()  # Commit the changes to the database
            print("Successfully Inserted Data in database")
            messagebox.showinfo("Success", "Successfully Signed Up!")
            self.reset_form()  # Reset the form fields
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            self.controller.show_frame('Login')  # Navigate to login frame

    def reset_form(self):
        # Clear all form fields
        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.address_entry.delete(0, "end")

    def validate(self):
        # Validation of user inputs
        name = self.name_entry.get()
        contact = self.phone_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        age = self.age_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not name or not contact or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return False
        
        if not re.match(r"^[0-9]{10}$", contact):
            messagebox.showerror("Error", "Invalid contact number!")
            return False
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format!")
            return False
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return False
        
        if len(password) < 6 or len(password) > 18:
            messagebox.showerror("Error", "Password must be between 6 and 18 characters!")
            return False
        
        if not age.isdigit():
            messagebox.showerror("Error", "Invalid age!")
            return False
        
        age = int(age)
        if age < 5 or age > 100:
            messagebox.showerror("Error", "Invalid age!")
            return False
        
        return True
