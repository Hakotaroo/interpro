import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import mysql.connector

class CalendarModel:
    def __init__(self):
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
    
    def get_calendar(self, year, month):
        return calendar.monthcalendar(year, month)

class CalendarView(tk.Frame):
    def __init__(self, root, db, record_id):
        super().__init__(root)
        self.root = root
        self.db = db  # Conexión a la base de datos
        self.record_id = record_id  # ID del registro que quieres actualizar
        self.root.title("Calendario MVC")
        self.year_var = tk.IntVar(value=datetime.now().year)
        self.month_var = tk.IntVar(value=datetime.now().month)
        
        # Controles de la vista (navegar por meses)
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)
        self.prev_button = tk.Button(top_frame, text="◀", command=self.prev_month)
        self.prev_button.grid(row=0, column=0)
        self.month_label = tk.Label(top_frame, text="", font=("Arial", 16))
        self.month_label.grid(row=0, column=1, padx=10)
        self.next_button = tk.Button(top_frame, text="▶", command=self.next_month)
        self.next_button.grid(row=0, column=2)
        
        # Calendario y selección de día
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()
        self.selected_day_label = None
        self.selected_day = None

    def set_controller(self, controller):
        """Establece el controlador para la vista."""
        self.controller = controller
        self.show_calendar()  # Muestra el calendario después de establecer el controlador
    
    def update_calendar(self, calendar_data, year, month):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        title = f"{calendar.month_name[month]} {year}"
        self.month_label.config(text=title)  # Actualizar el título del mes
        days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        for idx, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold")).grid(row=1, column=idx)
        for row_idx, week in enumerate(calendar_data, start=2):
            for col_idx, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="").grid(row=row_idx, column=col_idx)
                else:
                    day_label = tk.Label(self.calendar_frame, text=str(day), relief="raised", width=5)
                    day_label.grid(row=row_idx, column=col_idx)
                    day_label.bind("<Button-1>", lambda e, d=day, label=day_label: self.select_day(d, label))
        
        # Botón para confirmar la cita
        self.confirm_button = tk.Button(self.calendar_frame, text="Confirmar Cita", command=self.confirm_appointment)
        self.confirm_button.grid(row=row_idx + 1, column=0, columnspan=7, pady=10)
    
    def show_calendar(self):
        year = self.year_var.get()
        month = self.month_var.get()
        calendar_data = self.controller.model.get_calendar(year, month)  # Usar el modelo del controlador
        self.update_calendar(calendar_data, year, month)

    def prev_month(self):
        """Cambia al mes anterior y actualiza el calendario."""
        month = self.month_var.get()
        year = self.year_var.get()
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        self.year_var.set(year)
        self.month_var.set(month)
        self.show_calendar()

    def next_month(self):
        """Cambia al siguiente mes y actualiza el calendario."""
        month = self.month_var.get()
        year = self.year_var.get()
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        self.year_var.set(year)
        self.month_var.set(month)
        self.show_calendar()

    def select_day(self, day, label):
        # Restaurar el color del día previamente seleccionado (si existe)
        if hasattr(self, 'selected_day_label') and self.selected_day_label:
            try:
                self.selected_day_label.config(bg=self.calendar_frame.cget("bg"))
            except Exception as e:
                print(f"Error restaurando color del día seleccionado previamente: {e}")

        # Actualizar la nueva selección
        self.selected_day_label = label
        self.selected_day_label.config(bg="lightblue")  # Cambia el color del nuevo día seleccionado
        self.selected_day = day
    def confirm_appointment(self):
        """Confirma la cita seleccionada y guarda en la base de datos."""
        if self.selected_day:
            year = self.year_var.get()
            month = self.month_var.get()
            # Formato de la fecha
            selected_date = f"{year}-{month:02d}-{self.selected_day:02d}"
            # Actualizar el registro en la base de datos
            self.db.update_appointment_date(self.record_id, selected_date)
            messagebox.showinfo("Cita Registrada", f"Cita registrada para el {self.selected_day}/{month}/{year}.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un día primero.")

class CalendarController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

class Database:
    def __init__(self, host="localhost", user="root", password="", database="registroautos"):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.connection.cursor()
            print("Conexión exitosa a la base de datos MySQL.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")

    def update_appointment_date(self, record_id, appointment_date):
        """Actualiza la fecha de la cita en el registro especificado"""
        try:
            query = "UPDATE registros SET Fecha_Cita = %s WHERE ID = %s"
            self.cursor.execute(query, (appointment_date, record_id))
            self.connection.commit()
            print(f"Fecha de cita actualizada a: {appointment_date} para el registro ID {record_id}")
        except mysql.connector.Error as e:
            messagebox.showerror("Error al actualizar", f"No se pudo actualizar la fecha de la cita: {e}")

    def close_connection(self):
        self.connection.close()

def run_calendar_app(record_id):
    """Función principal para ejecutar la aplicación de calendario."""
    root = tk.Tk()
    model = CalendarModel()
    db = Database(host="localhost", user="root", password="", database="registroautos")
    view = CalendarView(root, db, record_id)
    controller = CalendarController(model, view)
    view.pack()
    root.mainloop()

if __name__ == "__main__":
    record_id = 1  # Ejemplo: actualizar el registro con ID 1. Puedes cambiarlo según sea necesario.
    run_calendar_app(record_id)
