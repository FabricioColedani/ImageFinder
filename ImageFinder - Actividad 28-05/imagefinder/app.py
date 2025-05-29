
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        images = Image.query.filter(
            (Image.description.contains(query)) |
            (Image.tags.contains(query))
        ).all()
    else:
        images = []
    return render_template('index.html', images=images, query=query)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    description = request.form['description']
    tags = request.form['tags']
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_image = Image(filename=filename, description=description, tags=tags)
    db.session.add(new_image)
    db.session.commit()
    return 'Imagen subida exitosamente'

def cargar_ejemplos():
    if Image.query.count() == 0:
        ejemplos = [
            {
                "filename": "ejemplo1.jpg",
                "description": "Paisaje de montaña al atardecer",
                "tags": "paisaje,montaña,atardecer"
            },
            {
                "filename": "ejemplo2.jpg",
                "description": "Perro jugando con pelota en el parque",
                "tags": "perro,juego,parque"
            },
            {
                "filename": "ejemplo3.jpg",
                "description": "Bala antigua exhibida en un museo",
                "tags": "bala,museo,historia"
            }
        ]
        for ej in ejemplos:
            imagen = Image(
                filename=ej["filename"],
                description=ej["description"],
                tags=ej["tags"]
            )
            db.session.add(imagen)
        db.session.commit()
        print("🌟 Imágenes de ejemplo cargadas.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        cargar_ejemplos()
    app.run(debug=True)
