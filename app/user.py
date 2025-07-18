<<<<<<< HEAD
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import role_required
from app.chroma_service import store_chunks
from app.models import add_document, get_documents_by_user, log_action
from PyPDF2 import PdfReader
=======
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from .auth import role_required
from . import mongo
from .chroma_service import store_chunks, search_chunks
from bson import ObjectId
from datetime import datetime, timezone
from PyPDF2 import PdfReader
from .llama_client import generate_answer  
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05

user_bp = Blueprint('user', __name__)

@user_bp.route('/upload', methods=['POST'])
@jwt_required()
@role_required('user')
def upload():
<<<<<<< HEAD
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    user_id = get_jwt_identity()
    filename = file.filename

    # Add doc metadata to Chroma
    doc_id = add_document(filename, user_id)

    # Parse PDF
    reader = PdfReader(file)
    text = ''.join([page.extract_text() or '' for page in reader.pages])

    # Embed and store chunks
    store_chunks(text, doc_id)

    # Log this action
    log_action(user_id, f"Uploaded {filename}")

    return jsonify({'msg': 'Uploaded successfully'}), 200

=======
    file = request.files['file']
    user_id = get_jwt_identity()
    filename = file.filename

    doc = {
        'filename': filename,
        'user_id': ObjectId(user_id),
        'upload_time': datetime.now(timezone.utc)
    }
    result = mongo.db.documents.insert_one(doc)
    doc_id = result.inserted_id

    reader = PdfReader(file)
    text = ''.join([page.extract_text() or '' for page in reader.pages])

    chunks = store_chunks(text, str(doc_id))

    log = {
        'user_id': ObjectId(user_id),
        'action': f'Uploaded {filename}',
        'timestamp': datetime.now(timezone.utc)
    }
    mongo.db.logs.insert_one(log)

    return jsonify({'msg': 'Uploaded successfully'}), 200


>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
@user_bp.route('/my-uploads', methods=['GET'])
@jwt_required()
@role_required('user')
def my_uploads():
    user_id = get_jwt_identity()
<<<<<<< HEAD
    uploads = get_documents_by_user(user_id)
    return jsonify(uploads), 200
=======
    docs = mongo.db.documents.find({'user_id': ObjectId(user_id)})

    uploads = []
    for d in docs:
        uploads.append({
            'filename': d['filename'],
            'upload_time': d['upload_time'].isoformat() if 'upload_time' in d else None
        })

    return jsonify(uploads), 200


@user_bp.route('/search', methods=['GET'])
@jwt_required()
@role_required('user')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    matches = search_chunks(query)
    return jsonify({'matches': matches}), 200


@user_bp.route('/ask', methods=['POST'])
@jwt_required()
@role_required('user')
def ask():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    matches = search_chunks(query)
    context = "\n".join([m['text'] for m in matches])

    answer = generate_answer(context, query)

    return jsonify({'answer': answer, 'matches': matches}), 200
>>>>>>> 0379ebb5a8dcd5c57e5a25378c09d33f164c7f05
