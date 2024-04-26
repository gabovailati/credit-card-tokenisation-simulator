# Credit Card Tokenization Simulator

## Project Overview
This repository contains a Flask-based API that simulates the credit card tokenization process. It is an educational tool to demonstrate generating and validating tokenized credit card transactions, involving a mock bank server, a mobile payment platform interface, and a merchant's point-of-sale system.

## Features
- **Credit Card Generation**: Generate mock credit card details.
- **Token Generation**: Issue tokens based on credit card details.
- **Token Validation**: Validate tokens for transaction approval.

## Getting Started

### Prerequisites
- Python 3.6+
- Flask
- Flask-SQLAlchemy
- Names

### Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/yourusername/credit-card-tokenization-simulator.git
cd credit-card-tokenization-simulator
pip install flask flask_sqlalchemy names
```

### Running the Application
Start the server by running:
```bash
python bank_api.py
```
The server will start on `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Generate Credit Card
- **URL**: `/generate_card`
- **Method**: `POST`
- **Description**: Generates a new credit card with details such as card number, cardholder name, expiry date, and CVC.
- **Response**:
  ```json
  {
    "card_number": "1234567890123456",
    "name": "John Doe",
    "expiry_date": "12/27",
    "cvc": "123"
  }
  ```

### 2. Generate Token
- **URL**: `/generate_token`
- **Method**: `POST`
- **Data Params**:
  ```json
  { "card_number": "1234567890123456" }
  ```
- **Description**: Generates a token for the provided credit card number.
- **Response**:
  ```json
  { "token": "effe2a8502f3d024df7e746998844062c6f5efe52a2745ddef8c48a4c0f62d5f" }
  ```

### 3. Validate Token
- **URL**: `/validate_token`
- **Method**: `POST`
- **Data Params**:
  ```json
  { "token": "effe2a8502f3d024df7e746998844062c6f5efe52a2745ddef8c48a4c0f62d5f" }
  ```
- **Description**: Validates if the provided token is valid for a transaction.
- **Response**:
  ```json
  { "status": "valid" }
  ```

## Contributors
- [Gabriel Vailati](https://github.com/gabovailati)
