import tkinter as tk
from tkinter import ttk, messagebox
class HoyNoCirculaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hoy No Circula")
        self.root.geometry("400x450")
        self.root.configure(bg="#FFF8E7")
        self.restricciones = {
            "1": "Lunes", "2": "Lunes",
            "3": "Martes", "4": "Martes",
            "5": "Miércoles", "6": "Miércoles",
            "7": "Jueves", "8": "Jueves",
            "9": "Viernes", "0": "Viernes"
        }
        self.crear_widgets()
    def crear_widgets(self):
        titulo = tk.Label(
            self.root, text="Tabla: Hoy No Circula", 
            font=("Arial", 16, "bold"), bg="#FDE2E4", fg="#5D3FD3"
        )
        titulo.pack(pady=10)
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("mystyle.Treeview", background="#F3E5F5", foreground="black", rowheight=25)
        estilo_tabla.map("mystyle.Treeview", background=[("selected", "#FFCCCB")])
        self.tabla = ttk.Treeview(self.root, columns=("digito", "dia"), show="headings", style="mystyle.Treeview")
        self.tabla.heading("digito", text="Último Dígito")
        self.tabla.heading("dia", text="Día de Restricción")
        for digito, dia in self.restricciones.items():
            self.tabla.insert("", "end", values=(digito, dia))
        self.tabla.pack(pady=10)
        label_placa = tk.Label(self.root, text="Ingrese la placa:", bg="#FFF8E7", font=("Arial", 12))
        label_placa.pack()
        self.entry_placa = tk.Entry(self.root, font=("Arial", 12), bg="#FFEBEE", fg="black")
        self.entry_placa.pack(pady=5)
        btn_verificar = tk.Button(self.root, text="Verificar", command=self.verificar_placa, bg="#D1C4E9", font=("Arial", 12))
        btn_verificar.pack(pady=10)
    def verificar_placa(self):
        placa = self.entry_placa.get().strip()
        if placa and placa[-1].isdigit():
            digito = placa[-1]
            dia = self.restricciones.get(digito, "No encontrado")
            messagebox.showinfo("Resultado", f"El coche con placa {placa} no circula el {dia}.")
        else:
            messagebox.showerror("Error", "Ingrese una placa válida que termine en un número.")
def ejecutar_hoy_no_circula():
    root = tk.Tk()
    app = HoyNoCirculaApp(root)
    root.mainloop()