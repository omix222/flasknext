from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
    
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{{"id": {self.id}, "name": "{self.name}"}}'  # JSON形式の文字列を返す


with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return "Hello from Flask!!!"

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.__repr__() for item in items]) 

@app.route('/items', methods=['POST'])
def add_item():
    name = request.json['name']
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    return jsonify(item), 201

if __name__ == '__main__':
    app.run(debug=True)