import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from sql_connection import DatabaseConnection
from fonts.colors import Colors

class DriverManagementFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, width=parent.winfo_width(), height=parent.winfo_height())
        self.pack_propagate(False)
        self._conn_=DatabaseConnection.connection()
        

        # Header
        self.header = ctk.CTkLabel(self, text="Driver Management", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.place(x=20, y=20)

        # Create scrollable frame for drivers
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=850, height=600)
        self.scrollable_frame.place(x=20, y=70)

        self.load_drivers()

    def load_drivers(self):

        try:
            # Clear existing widgets
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self._conn_=DatabaseConnection.connection()
            cursor = self._conn_.cursor()
            query = "SELECT * FROM drivers"
            cursor.execute(query)
            drivers=[]
            drivers = cursor.fetchall()
            cursor.close()


        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        if drivers:
            for driver in drivers:
                self.create_driver_card(driver)
        else:
            self.no_drivers_found()
        
    def no_drivers_found(self):
        card = ctk.CTkFrame(self.scrollable_frame, height=150)
        card.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(card, text="No drivers found !").pack(side="left", padx=10)



    def create_driver_card(self, driver):
        card = ctk.CTkFrame(self.scrollable_frame, height=120)
        card.pack(pady=10, padx=10, fill="x")

        # Driver details
        ctk.CTkLabel(card, text=f"Driver ID: {driver[0]}", font=ctk.CTkFont(size=14, weight="bold")).place(x=20, y=20)
        ctk.CTkLabel(card, text=f"Name: {driver[1]}", font=ctk.CTkFont(size=14)).place(x=20, y=50)
        ctk.CTkLabel(card, text=f"Status: {driver[8]}", font=ctk.CTkFont(size=14)).place(x=20, y=80)

        # Delete button
        delete_button = ctk.CTkButton(card,text="Delete Driver",width=120,
                                      fg_color=Colors.RED,hover_color=Colors.HOVER_RED,
                                      command=lambda: self.delete_driver(driver[0]))
        delete_button.place(x=600, y=40)

    def delete_driver(self, driver_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this driver?"):
            try:
                cursor = self._conn_.cursor()
                query = "DELETE FROM drivers WHERE id = %s"
                cursor.execute(query, [driver_id])
                self._conn_.commit()
                messagebox.showinfo("Success", "Driver deleted successfully!")
                self.load_drivers()  # Refresh the list
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
