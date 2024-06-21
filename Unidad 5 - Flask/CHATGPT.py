from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Ruta al archivo de base de datos subido
base_dir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(base_dir, 'datos.sqlite3')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    provincia = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    repartidores = db.relationship('Repartidor', backref='sucursal', lazy=True)
    paquetes = db.relationship('Paquete', backref='sucursal', lazy=True)
    transportes = db.relationship('Transporte', backref='sucursal', lazy=True)

class Repartidor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    idsucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    paquetes = db.relationship('Paquete', backref='repartidor', lazy=True)

class Paquete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeroenvio = db.Column(db.String(50), unique=True, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    nomdestinatario = db.Column(db.String(100), nullable=False)
    dirdestinatario = db.Column(db.String(200), nullable=False)
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
    paquetes = db.relationship('Paquete', backref='transporte', lazy=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sucursales', methods=['GET', 'POST'])
def sucursales():
    if request.method == 'POST':
        data = request.form
        if not data or not all(key in data for key in ('numero', 'provincia', 'localidad', 'direccion')):
            return jsonify({'error': 'Datos insuficientes'}), 400
        nueva_sucursal = Sucursal(
            numero=data['numero'],
            provincia=data['provincia'],
            localidad=data['localidad'],
            direccion=data['direccion']
        )
        try:
            db.session.add(nueva_sucursal)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('sucursales'))
    
    sucursales = Sucursal.query.all()
    return render_template('sucursales.html', sucursales=sucursales)

@app.route('/repartidores', methods=['GET', 'POST'])
def repartidores():
    if request.method == 'POST':
        data = request.form
        if not data or not all(key in data for key in ('nombre', 'dni', 'idsucursal')):
            return jsonify({'error': 'Datos insuficientes'}), 400
        nuevo_repartidor = Repartidor(
            nombre=data['nombre'],
            dni=data['dni'],
            idsucursal=data['idsucursal']
        )
        try:
            db.session.add(nuevo_repartidor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('repartidores'))
    
    repartidores = Repartidor.query.all()
    return render_template('repartidores.html', repartidores=repartidores)

@app.route('/paquetes', methods=['GET', 'POST'])
def paquetes():
    if request.method == 'POST':
        data = request.form
        if not data or not all(key in data for key in ('numeroenvio', 'peso', 'nomdestino', 'dirdestino', 'idsucursal')):
            return jsonify({'error': 'Datos insuficientes'}), 400
        nuevo_paquete = Paquete(
            numeroenvio=data['numeroenvio'],
            peso=data['peso'],
            nomdestino=data['nomdestino'],
            dirdestino=data['dirdestino'],
            idsucursal=data['idsucursal']
        )
        try:
            db.session.add(nuevo_paquete)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('paquetes'))
    
    paquetes = Paquete.query.all()
    return render_template('paquetes.html', paquetes=paquetes)

@app.route('/transportes', methods=['GET', 'POST'])
def transportes():
    if request.method == 'POST':
        data = request.form
        if not data or not all(key in data for key in ('numerotransporte', 'fechahorasalida', 'idsucursal')):
            return jsonify({'error': 'Datos insuficientes'}), 400
        try:
            nuevo_transporte = Transporte(
                numerotransporte=data['numerotransporte'],
                fechahorasalida=datetime.strptime(data['fechahorasalida'], '%Y-%m-%dT%H:%M'),
                idsucursal=data['idsucursal']
            )
            db.session.add(nuevo_transporte)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
        return redirect(url_for('transportes'))
    
    transportes = Transporte.query.all()
    return render_template('transportes.html', transportes=transportes)

if __name__ == '__main__':
    app.run(debug=True)
