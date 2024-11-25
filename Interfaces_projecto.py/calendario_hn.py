from flask import Flask, jsonify, request
import re

class HoyNoCircula:
    def __init__(self):
        # Diccionario de restricciones
        self.restricciones = {
            "1": "Lunes", "2": "Lunes",
            "3": "Martes", "4": "Martes",
            "5": "Miércoles", "6": "Miércoles",
            "7": "Jueves", "8": "Jueves",
            "9": "Viernes", "0": "Viernes"
        }

    def verificar_placa(self, placa):
        try:
            # Validación de entrada
            if not placa:
                raise ValueError("La placa no puede estar vacía.")
            if not re.match(r"^[A-Za-z0-9]+$", placa):
                raise ValueError("La placa debe contener solo caracteres alfanuméricos.")
            if not placa[-1].isdigit():
                raise ValueError("La placa debe terminar en un número.")

            # Extraer último dígito y determinar día
            digito = placa[-1]
            dia = self.restricciones.get(digito, "No encontrado")
            return f"El coche con placa {placa} no circula el {dia}."
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception:
            return "Error: Ha ocurrido un error inesperado al procesar la placa."

class HoyNoCirculaApp:
    def __init__(self):
        self.hoy_no_circula = HoyNoCircula()
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return jsonify({
                "message": "Bienvenido a la API Hoy No Circula",
                "usage": "Envíe una solicitud POST a /verificar con el campo 'placa'."
            })

        @self.app.route('/verificar', methods=['POST'])
        def verificar():
            try:
                data = request.get_json()
                if not data or 'placa' not in data:
                    raise ValueError("El campo 'placa' es obligatorio en el cuerpo de la solicitud.")
                
                placa = data['placa'].strip()
                resultado = self.hoy_no_circula.verificar_placa(placa)
                return jsonify({"success": True, "result": resultado})
            except ValueError as e:
                return jsonify({"success": False, "error": str(e)})
            except Exception:
                return jsonify({"success": False, "error": "Error inesperado en el servidor."})

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == "__main__":
    app = HoyNoCirculaApp()
    app.run()
