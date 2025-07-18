from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth import role_required
from app.chroma_service import store_chunks
from app.models import add_document, get_documents_by_user, log_action
from PyPDF2 import PdfReader

user_bp = Blueprint('user', __name__)

@user_bp.route('/upload', methods=['POST'])
@jwt_required()
@role_required('user')
def upload():
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

@user_bp.route('/my-uploads', methods=['GET'])
@jwt_required()
@role_required('user')
def my_uploads():
    user_id = get_jwt_identity()
    uploads = get_documents_by_user(user_id)
    return jsonify(uploads), 200
