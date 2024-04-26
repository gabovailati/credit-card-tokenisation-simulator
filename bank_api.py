from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
import string
import os
import names
import hashlib
import time

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'bank.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.String(16), unique=True, nullable=False)
    card_name = db.Column(db.String(120), nullable=False)
    expiry_date = db.Column(db.String(5), nullable=False)
    cvc = db.Column(db.String(3), nullable=False)

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)  # SHA256 hash has 64 characters
    card_id = db.Column(db.Integer, db.ForeignKey('credit_card.id'), nullable=False)
    credit_card = db.relationship('CreditCard', backref=db.backref('tokens', lazy=True))

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/generate_card', methods=['POST'])
def generate_card():
    card_number = ''.join(random.choices(string.digits, k=16))
    card_name = names.get_full_name()  # Use the names library to generate a random full name
    expiry_date = '12/27'  # Example expiry date
    cvc = ''.join(random.choices(string.digits, k=3))
    
    new_card = CreditCard(card_number=card_number, card_name=card_name, expiry_date=expiry_date, cvc=cvc)
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify({'card_number': card_number, 'name': card_name, 'expiry_date': expiry_date, 'cvc': cvc}), 201

@app.route('/generate_token', methods=['POST'])
def generate_token():
    card_number = request.json.get('card_number')
    card = CreditCard.query.filter_by(card_number=card_number).first()
    
    if not card:
        return jsonify({'error': 'Invalid card number'}), 404

    # Create a SHA256 token using the current timestamp and the card number
    hasher = hashlib.sha256()
    current_time = str(time.time())
    hasher.update(f'{current_time}{card_number}'.encode('utf-8'))
    token_str = hasher.hexdigest()

    new_token = Token(token=token_str, credit_card=card)
    db.session.add(new_token)
    db.session.commit()
    
    return jsonify({'token': token_str}), 201

@app.route('/validate_token', methods=['POST'])
def validate_token():
    token_str = request.json.get('token')
    token = Token.query.filter_by(token=token_str).first()
    
    if token:
        return jsonify({'status': 'valid'}), 200
    else:
        return jsonify({'status': 'invalid'}), 404

if __name__ == '__main__':
    app.run(debug=True)

