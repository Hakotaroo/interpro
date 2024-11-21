import mysql.connector
from tkinter import messagebox

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

    def insert_data(self, placa, confirmar_placa, serie, confirmar_serie, modelo, correo_electronico, fecha_cita):
        try:
            self.cursor.execute('''INSERT INTO citas (Placa, Confirmar_Placa, Serie, Confirmar_Serie, Modelo, Correo_Electronico, Fecha_Cita) 
                                   VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                                (placa, confirmar_placa, serie, confirmar_serie, modelo, correo_electronico, fecha_cita))
            self.connection.commit()
            messagebox.showinfo("Éxito", "Datos guardados correctamente en la base de datos.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar en la base de datos: {e}")

    def close_connection(self):
        self.connection.close()
