import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from calendario_hn import ejecutar_hoy_no_circula
from inter import MainView
from database import Database  # Asegúrate de tener esta clase correctamente definida

def hoy_no_circula():
    ejecutar_hoy_no_circula()

def abrir_formulario():
    # Crear una nueva ventana
    nueva_ventana = tk.Toplevel(ventana)
    
    # Crear una instancia de la base de datos
    db = Database(host="localhost", user="root", password="", database="registroautos")
    
    # Pasar la instancia de la base de datos a MainView
    app = MainView(nueva_ventana, db)
    app.pack(pady=20)

def cerrar_ventana():
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Opciones")
ventana.geometry("600x500")
ventana.configure(bg="#F5F5F5")  # Color de fondo más claro

# Cargar y configurar la imagen
ruta_imagen = "carro_-ai-brush-removebg-t00ggb6.png"
try:
    imagen = Image.open(ruta_imagen).convert("RGBA")
    imagen = imagen.resize((500, 300))
    imagen_tk = ImageTk.PhotoImage(imagen)
    # Mostrar la imagen en la ventana
    label_imagen = tk.Label(ventana, image=imagen_tk, bd=0, highlightthickness=0)
    label_imagen.image = imagen_tk
    label_imagen.place(x=-250, y=200)
except FileNotFoundError:
    messagebox.showerror("Error", f"No se pudo cargar la imagen desde {ruta_imagen}")

# Estilos de botones
button_style = {
    'font': ("Arial", 12, "bold"),
    'width': 12,
    'height': 2,
}

# Botón "Hoy no Circula"
btn_hoy_no_circula = tk.Button(
    ventana,
    text="Hoy No Circula",
    command=hoy_no_circula,
    bg="#98FB98",  # Color verde claro
    fg="black",
    **button_style
)
btn_hoy_no_circula.place(x=150, y=200)

# Botón "Registrar Cita"
btn_registrar_cita = tk.Button(
    ventana,
    text="Registrar Cita",
    bg="#98FB98",  # Color verde claro
    fg="black",
    command=abrir_formulario,
    **button_style
)
btn_registrar_cita.place(x=350, y=200)

# Botón "Cerrar"
btn_cerrar = tk.Button(
    ventana,
    text="Cerrar",
    command=cerrar_ventana,
    bg="#FF4500",  # Color rojo anaranjado
    fg="white",
    width=8,
    height=1,
    font=("Arial", 12, "bold")
)
btn_cerrar.place(x=500, y=430)

# Encabezados
header_label1 = tk.Label(ventana, text="Bienvenido a la Interfaz", font=("Arial", 20, "bold"), bg="#F5F5F5", fg="#333")
header_label1.pack(pady=(20, 0))

header_label2 = tk.Label(ventana, text="Registro de Citas", font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#333")
header_label2.pack(pady=(5, 20))

header_label3 = tk.Label(ventana, text="Hoy No Circula", font=("Arial", 16, "bold"), bg="#F5F5F5", fg="#333")
header_label3.place(x=200, y=150)

header_label4 = tk.Label(ventana, text="Registrar Cita", font=("Arial", 16, "bold"), bg="#F5F5F5", fg="#333")
header_label4.place(x=410, y=150)

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
