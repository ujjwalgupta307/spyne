from flask import Blueprint, request, jsonify
from .models import Discussion, Hashtag
from app import db
from .search import add_discussion_to_index, update_discussion_in_index, delete_discussion_from_index, search_discussions

discussions_bp = Blueprint('discussions', __name__)

@discussions_bp.route('/', methods=['POST'])
def create_discussion():
    data = request.json
    new_discussion = Discussion(
        user_id=data['user_id'],
        text=data['text'],
        image=data.get('image'),
        created_on=data['created_on']
    )
    db.session.add(new_discussion)
    db.session.commit()
    add_discussion_to_index(new_discussion)
    return jsonify({"message": "Discussion created successfully"}), 201

@discussions_bp.route('/<int:id>', methods=['PUT'])
def update_discussion(id):
    data = request.json
    discussion = Discussion.query.get(id)
    if not discussion:
        return jsonify({"message": "Discussion not found"}), 404
    discussion.text = data['text']
    discussion.image = data.get('image')
    db.session.commit()
    update_discussion_in_index(discussion)
    return jsonify({"message": "Discussion updated successfully"})

@discussions_bp.route('/<int:id>', methods=['DELETE'])
def delete_discussion(id):
    discussion = Discussion.query.get(id)
    if not discussion:
        return jsonify({"message": "Discussion not found"}), 404
    db.session.delete(discussion)
    db.session.commit()
    delete_discussion_from_index(discussion)
    return jsonify({"message": "Discussion deleted successfully"})

@discussions_bp.route('/', methods=['GET'])
def list_discussions():
    tag = request.args.get('tag')
    query = request.args.get('query')
    if tag:
        discussions = Discussion.query.join(Hashtag).filter(Hashtag.tag == tag).all()
    elif query:
        discussions = search_discussions(query)
    else:
        discussions = Discussion.query.all()
    return jsonify([{"id": d.id, "text": d.text, "image": d.image, "created_on": d.created_on} for d in discussions])