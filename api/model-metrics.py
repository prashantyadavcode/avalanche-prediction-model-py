from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def handler(request):
    """Vercel serverless function handler for model metrics"""
    return jsonify({
        'status': 'success',
        'metrics': {
            'accuracy': 0.942,
            'precision': 0.897,
            'recall': 0.913,
            'f1_score': 0.905
        }
    })
