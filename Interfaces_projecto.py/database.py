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
            # Depurar el error, mostrar más detalles en el mensaje
            print(f"Error: {e}")
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            # Llamada a un método o acción que permita salir o detener el flujo si la conexión no es exitosa
            raise SystemExit("Fallo la conexión a la base de datos")

    def insert_data(self, placa, confirm_placa, serie, confirm_serie, model, email):
        """Inserta los datos del vehículo y retorna el ID del registro insertado"""
        try:
            query = """
            INSERT INTO registros (Placa, Confirmar_Placa, Serie, Confirmar_Serie, Modelo, Correo_Electronico)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (placa, confirm_placa, serie, confirm_serie, model, email))
            self.connection.commit()
            record_id = self.cursor.lastrowid  # Obtener el ID del registro insertado
            return record_id
        except mysql.connector.Error as e:
            print(f"Error al insertar los datos: {e}")
            messagebox.showerror("Error al insertar", f"No se pudo insertar el registro: {e}")
            return None

    def close_connection(self):
        self.connection.close()
