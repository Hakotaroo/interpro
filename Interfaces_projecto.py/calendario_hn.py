import tkinter as tk
from tkinter import ttk, messagebox


class HoyNoCirculaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hoy No Circula")
        self.root.geometry("400x450")
        self.root.configure(bg="#FFF8E7")

        # Diccionario de restricciones por último dígito de la placa
        self.restricciones = {
            "1": "Lunes", "2": "Lunes",
            "3": "Martes", "4": "Martes",
            "5": "Miércoles", "6": "Miércoles",
            "7": "Jueves", "8": "Jueves",
            "9": "Viernes", "0": "Viernes"
        }

        self.crear_widgets()

    def crear_widgets(self):
        # Título de la aplicación
        titulo = tk.Label(
            self.root, text="Tabla: Hoy No Circula",
            font=("Arial", 16, "bold"), bg="#FDE2E4", fg="#5D3FD3"
        )
        titulo.pack(pady=10)

        # Estilo para la tabla
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("mystyle.Treeview", background="#F3E5F5", foreground="black", rowheight=25)
        estilo_tabla.map("mystyle.Treeview", background=[("selected", "#FFCCCB")])

        # Tabla para mostrar restricciones
        self.tabla = ttk.Treeview(self.root, columns=("digito", "dia"), show="headings", style="mystyle.Treeview")
        self.tabla.heading("digito", text="Último Dígito")
        self.tabla.heading("dia", text="Día de Restricción")

        # Llenado de datos en la tabla
        for digito, dia in self.restricciones.items():
            self.tabla.insert("", "end", values=(digito, dia))
        self.tabla.pack(pady=10)

        # Campo de entrada para la placa
        label_placa = tk.Label(self.root, text="Ingrese la placa:", bg="#FFF8E7", font=("Arial", 12))
        label_placa.pack()

        self.entry_placa = tk.Entry(self.root, font=("Arial", 12), bg="#FFEBEE", fg="black")
        self.entry_placa.pack(pady=5)

        # Botón para verificar la placa
        btn_verificar = tk.Button(self.root, text="Verificar", command=self.verificar_placa, bg="#D1C4E9", font=("Arial", 12))
        btn_verificar.pack(pady=10)

    def verificar_placa(self):
        try:
            # Obtener el texto ingresado
            placa = self.entry_placa.get().strip()

            # Validar que no esté vacío
            if not placa:
                raise ValueError("El campo de la placa está vacío. Por favor, ingrese una placa válida.")

            # Validar que el último carácter sea un dígito
            if not placa[-1].isdigit():
                raise ValueError("La placa debe terminar en un número.")

            # Obtener el último dígito y buscar el día de restricción
            digito = placa[-1]
            dia = self.restricciones.get(digito, "No encontrado")

            # Mostrar el resultado en un cuadro de diálogo
            if dia == "No encontrado":
                raise KeyError(f"No se encontró una restricción para el dígito {digito}.")
            messagebox.showinfo("Resultado", f"El coche con placa {placa} no circula el {dia}.")

        except ValueError as e:
            # Manejar errores de validación
            messagebox.showerror("Error", str(e))
        except KeyError as e:
            # Manejar errores de búsqueda en el diccionario
            messagebox.showerror("Error", str(e))
        except Exception as e:
            # Manejar cualquier otro error inesperado
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {str(e)}")


def ejecutar_hoy_no_circula():
    root = tk.Tk()
    app = HoyNoCirculaApp(root)
    root.mainloop()
