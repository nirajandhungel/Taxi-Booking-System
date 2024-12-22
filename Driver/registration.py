import customtkinter as ctk
from tkinter import messagebox
from fonts.colors import Colors
import re
import mysql.connector
from sql_connection import DatabaseConnection
import bcrypt
# from driver_request import driver_requests

class DriverRegistration(ctk.CTkFrame):
    def __init__(self, parent, controller,shared_data):
        super().__init__(parent)
        self.controller = controller
        self.shared_data = shared_data
        self.configure(fg_color=Colors.GREEN)  # Green background
        self._conn_ = DatabaseConnection.connection()

        # Back Button
        self.back_button = ctk.CTkButton(self, text="Back", width=80, height=32, corner_radius=16, fg_color="black",
                                         hover_color="#333333",command=lambda: self.controller.show_frame("RegisterSignup"))
        self.back_button.place(x=20, y=20)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Driver Registration", font=("Montserrat Bold", 24, "bold"), text_color="black")
        self.title_label.place(relx=0.45, rely=0.1, anchor="center")


        """Create individual input fields with labels."""
        # Full Name
        full_name_label = ctk.CTkLabel(self, text="Full Name", font=("Montserrat Bold", 14), text_color="black")
        full_name_label.place(relx=0.15, rely=0.2)
        self.name_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your full name")
        self.name_entry.place(relx=0.15, rely=0.25)
        # Contact Number
        contact_label = ctk.CTkLabel(self, text="Contact Number", font=("Montserrat Bold", 14), text_color="black")
        contact_label.place(relx=0.15, rely=0.35)
        self.contact_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your contact number")
        self.contact_entry.place(relx=0.15, rely=0.4)
        # Vehicle Number
        vehicle_label = ctk.CTkLabel(self, text="Vehicle Number", font=("Montserrat Bold", 14), text_color="black")
        vehicle_label.place(relx=0.15, rely=0.5)
        self.vehicle_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your vehicle details")
        self.vehicle_entry.place(relx=0.15, rely=0.55)
        # Licence Number
        licence_label = ctk.CTkLabel(self, text="Licence Number", font=("Montserrat Bold", 14), text_color="black")
        licence_label.place(relx=0.15, rely=0.65)
        self.licence_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your licence number")
        self.licence_entry.place(relx=0.15, rely=0.7)
        # Address
        address_label = ctk.CTkLabel(self, text="Address", font=("Montserrat Bold", 14), text_color="black")
        address_label.place(relx=0.45, rely=0.2)
        self.address_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your permanent address")
        self.address_entry.place(relx=0.45, rely=0.25)
        # Email
        email_label = ctk.CTkLabel(self, text="Email", font=("Montserrat Bold", 14), text_color="black")
        email_label.place(relx=0.45, rely=0.35)
        self.email_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Enter your email address")
        self.email_entry.place(relx=0.45, rely=0.4)
        # Set Password
        set_password_label = ctk.CTkLabel(self, text="Set Password", font=("Montserrat Bold", 14), text_color="black")
        set_password_label.place(relx=0.45, rely=0.5)
        self.set_password_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Set password", show="*")
        self.set_password_entry.place(relx=0.45, rely=0.55)
        # Confirm Password
        confirm_password_label = ctk.CTkLabel(self, text="Confirm Password", font=("Montserrat Bold", 14), text_color="black")
        confirm_password_label.place(relx=0.45, rely=0.65)
        self.confirm_password_entry = ctk.CTkEntry(self, width=300, height=40, placeholder_text="Confirm password", show="*")
        self.confirm_password_entry.place(relx=0.45, rely=0.7)
        # Gender Entry
        self.gender_label = ctk.CTkLabel(self,text=" Select your gender",font=("Montserrat Bold",14),text_color="black")
        self.gender_label.place(relx=0.7,rely=0.3)

        # Variable to store the selected gender
        self.gender_var = ctk.StringVar(value="Male")

        self.male_radio = ctk.CTkRadioButton(self,text="Male",value="Male",variable=self.gender_var)
        self.male_radio.place(relx=0.7,rely=0.4)

        self.female_radio = ctk.CTkRadioButton(self,text="Female",value="Female",variable=self.gender_var)
        self.female_radio.place(relx=0.7,rely=0.5)

        self.others_radio = ctk.CTkRadioButton(self,text="Others",value="Others",variable=self.gender_var)
        self.others_radio.place(relx=0.7,rely=0.6)

        
        # Register Button
        self.register_button = ctk.CTkButton(self, text="Register", font=("Montserrat Bold", 16), width=150, height=40,corner_radius=5,
                                             fg_color="black", hover_color="#006400",command=self.register_driver)
        self.register_button.place(relx=0.5, rely=0.85, anchor="center")
        
    def register_driver(self):
        print("Register driver method called!")

        """Register the driver."""
        if not self.validate_driver():
            return
        print("Register driver method called after validaion!") 
        # Collect data

        name= self.name_entry.get()
        number= self.contact_entry.get()
        email= self.email_entry.get()
        password= self.confirm_password_entry.get()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')# Convert password to bytes and hash it
        
        address= self.address_entry.get()
        license_number= self.licence_entry.get()
        vehicle_number= self.vehicle_entry.get()
        gender= self.gender_var.get()
   
        # Add to database
        try:
            with self._conn_.cursor() as cursor:
                query="INSERT INTO driver_request (full_name ,phone_number ,email ,user_password ,address ,license_number ,vehicle_number ,gender,request_status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                cursor.execute(query,(name,number,email,hashed_password,address,license_number,vehicle_number,gender,"Requested"))
                self._conn_.commit()
                # Show success message
                messagebox.showinfo("Success", "Driver registration submitted for approval!")

                # Reset the form (assuming you have a `reset_form` method)
                self.reset_form()
    
        except mysql.connector.Error as e:
            # Handle database connection or execution errors
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        
        except Exception as ex:
            # Handle any other unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {ex}")

        finally:    
            self.reset_form()
            self.controller.show_frame('Login')
    
    def reset_form(self):
        """Reset all input fields and attributes."""
        self.name_entry.delete(0, "end")
        self.contact_entry.delete(0, "end")
        self.vehicle_entry.delete(0, "end")
        self.licence_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.set_password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")
        self.gender_var.set("")
        
    def validate_driver(self):
        """Validate driver input fields."""
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        password = self.set_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        gender=self.gender_var.get()

        if not name or not contact or not email or not password or not gender :
            messagebox.showerror("Error", "All fields are required!")
            return False
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return False
        
        if len(password) < 6 or len(password) > 18:
            messagebox.showerror("Error", "Password must be of length between 6 and 18!")
            return False

        if not re.match(r"^[0-9]{10}$", contact):
            messagebox.showerror("Error", "Invalid contact number!")
            return False

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format!")
            return False
        return True
        
    

    


