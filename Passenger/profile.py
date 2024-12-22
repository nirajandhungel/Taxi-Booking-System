import customtkinter as ctk  # Importing CustomTkinter for enhanced UI components
from tkinter import messagebox  # Importing messagebox for error and success dialogs
from sql_connection import DatabaseConnection  # Importing the custom database connection module
from fonts.colors import Colors  # Importing custom colour constants

class ProfileFrame(ctk.CTkFrame):
    """
    A frame to display and manage passenger profiles.
    """
    def __init__(self, parent, passenger_id=None):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.passenger_id = passenger_id  # Storing the passenger ID for later use
        print(f"Passenger id in profile frame: {self.passenger_id}")
        
        self._conn_ = DatabaseConnection.connection()  # Establishing a database connection
        self.user_profile()  # Display the profile UI
    
    def user_profile(self):
        """
        Displays the passenger's profile information.
        """
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        self._conn_ = DatabaseConnection.connection()  # Refreshing the database connection
        try:
            with self._conn_.cursor() as cursor:
                query = "SELECT * FROM passengers WHERE id = %s"
                cursor.execute(query, (self.passenger_id,))
                self.details = cursor.fetchone()  # Fetching the user's details
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        
        # Header
        self.header = ctk.CTkLabel(self, text="Passenger Profile", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # User details
        self.user_data = [
            ("Name", self.details[1]),
            ("Phone", self.details[2]),
            ("Email", self.details[3]),
            ("Home Address", self.details[5]),
            ("Gender", self.details[6]),
            ("Age", self.details[7]),
            ("Rating", "4.9★")
        ]

        # Display the user information
        for i, (label, value) in enumerate(self.user_data, start=1):
            ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=14)).place(x=20, y=20 + i * 50)
            ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=14, weight="bold")).place(x=200, y=20 + i * 50)

        # Edit Profile button
        self.edit_button = ctk.CTkButton(
            self, 
            text="Edit Profile", 
            width=440, 
            fg_color=Colors.GREEN_BUTTON, 
            hover_color=Colors.GREEN_BUTTON_HOVER, 
            command=self.edit_profile
        )
        self.edit_button.place(x=20, y=500)
    
    def edit_profile(self):
        """
        Opens the Edit Profile window.
        """
        self.edit_window = EditProfileWindow(self, self.passenger_id)

class EditProfileWindow(ctk.CTkToplevel):
    """
    A window for editing the user's profile information.
    """
    def __init__(self, parent, id=None):
        super().__init__(parent)
        self.id = id  # Storing the passenger ID
        self.parent = parent  # Reference to the parent frame
        self._conn_ = DatabaseConnection.connection()  # Establishing a database connection
        self.title("Edit Profile")
        self.geometry("500x600")
        self.resizable(False, False)  # Prevent resizing the window
        
        try:
            with self._conn_.cursor() as cursor:
                query = "SELECT * FROM passengers WHERE id = %s"
                cursor.execute(query, (self.id,))
                self.details = cursor.fetchone()  # Fetching the user's details
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        # Title Label
        title_label = ctk.CTkLabel(self, text="Edit Profile", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.place(x=250, y=20, anchor="center")

        # Editable user fields
        self.user_data = [
            ("Name", self.details[1]),
            ("Email", self.details[4]),
            ("Phone", self.details[2]),
            ("Home Address", self.details[5]),
            ("Gender", self.details[6]),
            ("Age", self.details[7])
        ]

        # Creating input fields for user data
        self.inputs = {}
        y_position = 80
        for label, value in self.user_data:
            # Label
            label_widget = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=14))
            label_widget.place(x=50, y=y_position, anchor="w")
            
            # Input field
            entry_widget = ctk.CTkEntry(self, width=250)
            entry_widget.insert(0, value)
            entry_widget.place(x=160, y=y_position, anchor="w")
            self.inputs[label] = entry_widget
            
            y_position += 50

        # Confirm button
        self.confirm_button = ctk.CTkButton(
            self, 
            text="Confirm Profile", 
            command=self.validate_and_update_profile, 
            fg_color=Colors.GREEN_BUTTON, 
            hover_color=Colors.GREEN_BUTTON_HOVER, 
            width=200
        )
        self.confirm_button.place(x=250, y=y_position + 30, anchor="center")

        # Position the window relative to the parent
        self.transient(parent)
        self.grab_set()  # Restrict interactions with the parent until this window is closed

    def validate_and_update_profile(self):
        """
        Validates user input and updates the profile information in the database.
        """
        # Extract updated data from input fields
        updated_data = {label: entry.get() for label, entry in self.inputs.items()}

        # Basic validation
        if not all(updated_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        if "@" not in updated_data["Email"]:
            messagebox.showerror("Error", "Invalid email address!")
            return
        if not updated_data["Phone"].isdigit() or len(updated_data["Phone"]) != 10:
            messagebox.showerror("Error", "Invalid phone number!")
            return

        try:
            with self._conn_.cursor() as cursor:
                # Update query
                query = """UPDATE passengers SET full_name = %s, email = %s, phone_number = %s, address = %s, gender = %s, age = %s WHERE id = %s"""
                cursor.execute(
                    query, 
                    (
                        updated_data["Name"], 
                        updated_data["Email"], 
                        updated_data["Phone"], 
                        updated_data["Home Address"], 
                        updated_data["Gender"], 
                        updated_data["Age"], 
                        self.id
                    )
                )
                self._conn_.commit()  # Save changes
                messagebox.showinfo("Success", "Profile updated successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return

        # Close the window and refresh the parent frame
        self.destroy()
        self.parent.user_profile()
