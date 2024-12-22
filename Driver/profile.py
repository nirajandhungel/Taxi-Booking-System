import customtkinter as ctk
from fonts.colors import Colors
from tkinter import messagebox
from sql_connection import DatabaseConnection

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, driver_id=None):
        #The constructor method is called when an instance of ProfileFrame is created.
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.driver_id = driver_id
        self._conn_=DatabaseConnection.connection()
        print(f'Driver Id = {self.driver_id} in Profile frame ')
        self.user_profile()
    def user_profile(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        self._conn_=DatabaseConnection.connection()
        try:
            with  self._conn_.cursor() as cursor:
                query = "SELECT * FROM drivers WHERE id = %s"
                cursor.execute(query, [self.driver_id])
                self.details = cursor.fetchone()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
        # Header
        self.header = ctk.CTkLabel(self,text="Driver Profile",font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)
        # Driver information
        self.user_data = [
            ("Name", self.details[1]),
            ("Phone", self.details[2]),
            ("Email", self.details[3]),
            ("Home Address", self.details[5]),
            ("License Number", self.details[6]),
            ("Vehicle Number", self.details[7]),
            ("Status", self.details[8]),
            ("Gender", self.details[9]),
            ("Rating", "4.8★")
        ]

        # Display user information
        for i, (label, value) in enumerate(self.user_data, start=1):
            ctk.CTkLabel(self,text=label,font=ctk.CTkFont(size=14)).place(x=20, y=20 + i * 50)
            ctk.CTkLabel(self,text=value,font=ctk.CTkFont(size=14, weight="bold")).place(x=200, y=20 + i * 50)

        # Edit profile button
        self.edit_button = ctk.CTkButton(self,text="Edit Profile",width=440,fg_color=Colors.GREEN_BUTTON,
                                         hover_color=Colors.GREEN_BUTTON_HOVER,command=self.edit_profile)
        self.edit_button.place(x=20, y=540)

    def edit_profile(self):# edit profile window 
        self.edit_window = EditProfileWindow(self,self.details)
    
class EditProfileWindow(ctk.CTkToplevel):
    """
    EditProfileWindow is a subclass of CTkToplevel which provides a separate window for editing user profiles.
    """
    def __init__(self, parent, dets=None):
        super().__init__(parent)
        self.parent=parent
        self.dets = dets
        self.id=self.dets[0]
        self._conn_ = DatabaseConnection.connection() 
        self.title("Edit Profile")
        self.geometry("500x600")
        self.resizable(False, False)

        # Title Label
        title_label = ctk.CTkLabel(self, text="Edit Profile", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.place(x=250, y=20, anchor="center")

        self.user_data = [
            ("Name", self.dets[1]),
            ("Email", self.dets[3]),
            ("Phone", self.dets[2]),
            ("Home Address", self.dets[5]),
            ("License Number", self.dets[6]),
            ("Vehicle Number", self.dets[7]),
            ("Status", self.dets[8]),
            ("Gender", self.dets[9])
        ]

        # Inputs for user credentials
        self.inputs = {}
        y_position = 80  # Starting position for the labels and entries
        for label, value in self.user_data:
            # Create and place label
            label_widget = ctk.CTkLabel(self, text=label, font=ctk.CTkFont(size=14))
            label_widget.place(x=50, y=y_position, anchor="w")

            # Create and place entry
            entry_widget = ctk.CTkEntry(self, width=250)
            entry_widget.insert(0, value)
            entry_widget.place(x=160, y=y_position, anchor="w")
            self.inputs[label] = entry_widget

            y_position += 50  # Increment y-position for the next label and entry

        # Confirm Profile Button
        self.confirm_button = ctk.CTkButton(self, text="Confirm Profile", command=self.validate_and_update_profile,
                                            fg_color=Colors.GREEN_BUTTON, hover_color=Colors.GREEN_BUTTON_HOVER, width=200)
        self.confirm_button.place(x=250, y=y_position + 30, anchor="center")

        # Position the window in front of the parent
        self.transient(parent)
        self.grab_set()  # Disable interactions with the parent until this window is closed

    def validate_and_update_profile(self):
        """Validate the user inputs and update the user data."""
        # Extract user inputs
        updated_data = {label: entry.get() for label, entry in self.inputs.items()}

        # Perform basic validation
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
            # Update the database
            cursor = self._conn_.cursor()
            # SQL query to update user data
            query = """ UPDATE drivers SET full_name = %s, phone_number = %s, email = %s, address = %s,
                        license_number = %s, vehicle_number=%s, gender = %s WHERE id = %s """


            # Execute the query
            cursor.execute(query, (updated_data["Name"], updated_data["Phone"], updated_data["Email"],
                                   updated_data["Home Address"], updated_data["License Number"],
                                   updated_data["Vehicle Number"], updated_data["Gender"], self.id))
            # Commit the changes
            self._conn_.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
            return
        finally:
            cursor.close()
            
            

        # Close the Edit Profile window
        self.destroy()
        # After updating the profile, call user_profile on the ProfileFrame instance (the parent)
        self.parent.user_profile()  # Call user_profile on the parent instance (ProfileFrame)

