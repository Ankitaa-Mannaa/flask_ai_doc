from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import role_required
from .chroma_service import search_chunks
from .llama_client import generate_answer  

analyst_bp = Blueprint('analyst', __name__)

<<<<<<< HEAD
# search route
=======
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
@analyst_bp.route('/search', methods=['GET'])
@jwt_required()
@role_required('analyst')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    matches = search_chunks(query)
    return jsonify({'matches': matches}), 200


<<<<<<< HEAD
# ask route
=======
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
@analyst_bp.route('/ask', methods=['GET'])
@jwt_required()
@role_required('analyst')
def ask():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    matches = search_chunks(query)
    context = "\n".join([m['text'] for m in matches])

    answer = generate_answer(query, context)
    return jsonify({'answer': answer, 'matches': matches}), 200
