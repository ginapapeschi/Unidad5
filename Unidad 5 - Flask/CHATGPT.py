from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)

class Repartidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)

class Paquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeroenvio = db.Column(db.String(50), unique=True, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    nomdestino = db.Column(db.String(100), nullable=False)
    dirdestino = db.Column(db.String(200), nullable=False)
    entregado = db.Column(db.Boolean, default=False)
    observaciones = db.Column(db.Text)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    idtransporte = db.Column(db.Integer, db.ForeignKey('transporte.id'))
    idrepartidor = db.Column(db.Integer, db.ForeignKey('repartidor.id'))

class Transporte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numerotransporte = db.Column(db.String(50), unique=True, nullable=False)
    fechahorasalida = db.Column(db.DateTime, nullable=False)
    fechahorallegada = db.Column(db.DateTime)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)

# No es necesario crear las tablas si la base de datos ya existe
# with app.app_context():
#     db.create_all()

@app.route('/sucursales', methods=['POST'])
def add_sucursal():
    data = request.get_json()
    nueva_sucursal = Sucursal(
        numero=data['numero'],
        provincia=data['provincia'],
        localidad=data['localidad'],
        direccion=data['direccion']
    )
    db.session.add(nueva_sucursal)
    db.session.commit()
    return jsonify({'mensaje': 'Sucursal agregada exitosamente'}), 201

@app.route('/repartidores', methods=['POST'])
def add_repartidor():
    data = request.get_json()
    nuevo_repartidor = Repartidor(
        nombre=data['nombre'],
        dni=data['dni'],
        idsucursal=data['idsucursal']
    )
    db.session.add(nuevo_repartidor)
    db.session.commit()
    return jsonify({'mensaje': 'Repartidor agregado exitosamente'}), 201

@app.route('/paquetes', methods=['POST'])
def add_paquete():
    data = request.get_json()
    nuevo_paquete = Paquete(
        numeroenvio=data['numeroenvio'],
        peso=data['peso'],
        nomdestino=data['nomdestino'],
        dirdestino=data['dirdestino'],
        idsucursal=data['idsucursal']
    )
    db.session.add(nuevo_paquete)
    db.session.commit()
    return jsonify({'mensaje': 'Paquete agregado exitosamente'}), 201

@app.route('/transportes', methods=['POST'])
def add_transporte():
    data = request.get_json()
    nuevo_transporte = Transporte(
        numerotransporte=data['numerotransporte'],
        fechahorasalida=datetime.strptime(data['fechahorasalida'], '%Y-%m-%d %H:%M:%S'),
        idsucursal=data['idsucursal']
    )
    db.session.add(nuevo_transporte)
    db.session.commit()
    return jsonify({'mensaje': 'Transporte agregado exitosamente'}), 201

if __name__ == '__main__':
    app.run(debug=True)
