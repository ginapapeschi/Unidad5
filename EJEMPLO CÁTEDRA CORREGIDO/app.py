from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Usuario, Comentario

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def inicio():
        return render_template('inicio.html')

    @app.route('/nuevo_usuario', methods=['GET', 'POST'])
    def nuevo_usuario():
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['email']
            password = request.form['password']

            if not nombre or not correo or not password:
                return render_template('error.html', error="Los datos ingresados no son correctos...")
            
            # Verificar si el correo ya está registrado
            usuario_existente = Usuario.query.filter_by(correo=correo).first()
            if usuario_existente:
                return render_template('error.html', error="El correo electrónico ya está registrado")

            # Si el correo no está duplicado, proceder con el registro
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                clave=generate_password_hash(password)
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            return render_template('aviso.html', mensaje="El usuario se registró exitosamente")

        return render_template('nuevo_usuario.html')


    @app.route('/nuevo_comentario', methods=['GET', 'POST'])
    def nuevo_comentario():
        if request.method == 'POST':
            if not request.form['email'] or not request.form['password']:
                return render_template('error.html', error="Por favor ingrese los datos requeridos")
            else:
                usuario_actual = Usuario.query.filter_by(correo=request.form['email']).first()
                if usuario_actual is None:
                    return render_template('error.html', error="El correo no está registrado")
                else:
                    verificacion = check_password_hash(usuario_actual.clave, request.form['password'])
                    if verificacion:
                        return render_template('ingresar_comentario.html', usuario=usuario_actual)
                    else:
                        return render_template('error.html', error="La contraseña no es válida")
        else:
            return render_template('nuevo_comentario.html')

    @app.route('/ingresar_comentario', methods=['GET', 'POST'])
    def ingresar_comentario():
        if request.method == 'POST':
            if not request.form['contenido']:
                return render_template('error.html', error="Contenido no ingresado...")
            else:
                nuevo_comentario = Comentario(
                    fecha=datetime.now(),
                    contenido=request.form['contenido'],
                    usuario_id=request.form['userId']
                )
                db.session.add(nuevo_comentario)
                db.session.commit()
                return render_template('inicio.html')
        return render_template('inicio.html')

    @app.route('/listar_comentarios')
    def listar_comentarios():
        return render_template('listar_comentario.html', comentarios=Comentario.query.all())

    @app.route('/listar_comentarios_usuario', methods=['GET', 'POST'])
    def listar_comentarios_usuario():
        if request.method == 'POST':
            if not request.form['usuarios']:
                return render_template('listar_comentario_usuario.html', usuarios=Usuario.query.all(), usuario_seleccionado=None)
            else:
                return render_template('listar_comentario_usuario.html', usuarios=None, usuario_selec=Usuario.query.get(request.form['usuarios']))
        else:
            return render_template('listar_comentario_usuario.html', usuarios=Usuario.query.all(), usuario_selec=None)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
