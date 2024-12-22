import customtkinter as ctk
from tkinter import messagebox
from fonts.colors import Colors
from sql_connection import DatabaseConnection
import bcrypt

class Login(ctk.CTkFrame):
    def __init__(self, parent, controller,shared_data):
        super().__init__(parent)
        self.controller = controller
        self.shared_data = shared_data
        self.configure(fg_color=Colors.GREEN)
        self._conn_=DatabaseConnection.connection() # Protected
        self.login_ui()
    
    def login_ui(self):
        
        # Back Button
        self.back_button = ctk.CTkButton(self,text="Back",width=80,height=32,corner_radius=16,fg_color="black",hover_color="#333333",command=lambda: self.controller.show_frame("StartFrame"))
        self.back_button.place(x=20, y=20)  # Position at the top-left corner
        self.title = ctk.CTkLabel(self,text="Log In",font=("Montserrat Bold", 24),text_color="black")
        self.title.place(relx=0.43, y=40, anchor="n")  # Centered at the top

        # Email Label
        self.email_label = ctk.CTkLabel(self,text="Email",font=("Montserrat Bold", 14),text_color="black")
        self.email_label.place(relx=0.35, y=140)

        # Email Entry
        self.email_entry = ctk.CTkEntry(self,width=300,height=40,border_width=0,fg_color="#ffffff",text_color='black',placeholder_text="Enter your email address")
        self.email_entry.place(relx=0.35, y=180)

        # Password Label
        self.password_label = ctk.CTkLabel(self,text="Password",font=("Montserrat Bold", 14),text_color="black")
        self.password_label.place(relx=0.35, y=260)

        # Password Entry
        self.password_entry = ctk.CTkEntry(self,width=300,height=40,border_width=0,fg_color="#ffffff",text_color='black',placeholder_text="Enter your password",show="*")
        self.password_entry.place(relx=0.35, y=300)

        # Login Button
        self.login_button = ctk.CTkButton(self,width=120,height=40,text="Log In",font=("Arial Bold", 14),corner_radius=20,fg_color="black",hover_color="#333333",command=self.login)
        self.login_button.place(relx=0.4, y=400)

    def login(self): 
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.customer=None # initializing attributes
        self.driver=None
        self.admin=None
        # Validation: Check if both email and password are provided
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return False # Exit the function if validation fails
        try:
            self._conn_=DatabaseConnection.connection() # connection for dynamic changes
            
            # Attempt to connect to the MySQL database
            with self._conn_.cursor() as cursor:
                # Check for passenger login
                query1 = "SELECT id, user_password FROM passengers WHERE email = %s"
                cursor.execute(query1, (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                    self.customer = result[0]  # Passenger ID

                # Check for driver login
                query2 = "SELECT id, user_password FROM drivers WHERE email = %s"
                cursor.execute(query2, (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                    self.driver = result[0]  # Driver ID

                # Check for admin login
                query3 = "SELECT id, user_password FROM admins WHERE email = %s"
                cursor.execute(query3, (email,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
                    self.admin = result[0]  # Admin ID

        except Exception as e:
            # Log the error if needed (optional)
            print(f"Error during login: {e}")
            messagebox.showerror("Error", "An unexpected error occurred. Please try again.")
            return False  # Exit the function if an error occurs

        # Handle login results
        if self.admin:
            self.shared_data["admin_id"] = self.admin  # Store admin ID for later use
            messagebox.showinfo("Success", "Successfully Logged In!")
            self.controller.show_frame("AdminDashboard")
        elif self.customer:
            self.shared_data["passenger_id"] = self.customer  # Store passenger ID for later use
            messagebox.showinfo("Success", "Successfully Logged In!")
            self.controller.show_frame("PassengerDashboard")
        elif self.driver:
            self.shared_data["driver_id"] = self.driver  # Store driver ID for later use
            messagebox.showinfo("Success", "Successfully Logged In!")
            self.controller.show_frame("DriverDashboard")
        else:
            # If no matches were found
            messagebox.showerror("Error", "Invalid email or password!")
            