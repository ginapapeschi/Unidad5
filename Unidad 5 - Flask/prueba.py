from flask import *
from datetime import datetime

app = Flask(__name__)

"""
@app.route("/")
@app.route("/<string:lenguaje>")  # Para mostrar la página según el idioma, pasando como cadena el idioma, la cual podría ser una parte variable de la URL.

@app.route("/formulario")
def formulario():
    return render_template("formulario.html")
"""

@app.route("/")
def usuario():
    return render_template('nuevo_usuario.html')

@app.route('/bienvenida/', methods = ['POST', 'GET'])
def bienvenida():
    if request.method == 'POST':
# Verifica si la solicitud HTTP es de tipo POST. Esto ocurre cuando el usuario envía el formulario al hacer click en el botón de envío.

        if request.form ['nombre'] and request.form ['email'] and request.form ['password']:
# Verifica si los campos nombre, email y password fueron ENVIADOS y no están VACÍOS en el formulario.

            diccionarioDATOS = request.form
# Si todos los campos requeridos están presentes y son válidos, se guarda toda la información del formulario en el diccionario "diccionarioDATOS" mediante request.form. Este diccionario contiene los DATOS ENVIADOS por el usuario desde el FORMULARIO.
    
            return render_template('bienvenida.html', datos = diccionarioDATOS, hora = datetime.now().hour)
        else:
            return render_template('nuevo_usuario.html')

# El método POST se utiliza para enviar datos al servidor para que sean procesados. Es ideal para enviar grandes cantidades de datos y datos sensibles, como contraseñas o información de inicio de sesión.




"""
def saludo(lenguaje = "es"):                    
    if lenguaje == "es":
        return render_template("inicioes.html")   # render_template permite procesar un archivo HTML.
    else:
        return render_template("inicioen.html")

                                  # Las variables pueden incluir el TIPO o no.
"""


if __name__ == "__main__":
    app.run(debug=True)     # Usado durante el desarrollo para recarga automática, interfaz de depuración interactiva, y páginas de error detalladas.
