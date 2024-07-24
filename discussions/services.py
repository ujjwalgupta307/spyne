from .models import db, Discussion, Hashtag, DiscussionHashtag
from datetime import datetime
from .search import add_discussion_to_index, update_discussion_in_index, delete_discussion_from_index, search_discussions

def create_discussion(data):
    discussion = Discussion(
        user_id=data['user_id'],
        text=data['text'],
        image=data.get('image'),
        created_on=datetime.utcnow()
    )
    db.session.add(discussion)
    db.session.commit()
    
    if 'hashtags' in data:
        for tag in data['hashtags']:
            hashtag = Hashtag.query.filter_by(tag=tag).first()
            if not hashtag:
                hashtag = Hashtag(tag=tag)
                db.session.add(hashtag)
                db.session.commit()
            discussion.hashtags.append(hashtag)
        db.session.commit()
    
    add_discussion_to_index(discussion)
    return discussion.to_dict()

def update_discussion(discussion_id, data):
    discussion = Discussion.query.get(discussion_id)
    discussion.text = data.get('text', discussion.text)
    discussion.image = data.get('image', discussion.image)
    db.session.commit()
    
    if 'hashtags' in data:
        discussion.hashtags.clear()
        for tag in data['hashtags']:
            hashtag = Hashtag.query.filter_by(tag=tag).first()
            if not hashtag:
                hashtag = Hashtag(tag=tag)
                db.session.add(hashtag)
                db.session.commit()
            discussion.hashtags.append(hashtag)
        db.session.commit()
    
    update_discussion_in_index(discussion)
    return discussion.to_dict()

def delete_discussion(discussion_id):
    discussion = Discussion.query.get(discussion_id)
    delete_discussion_from_index(discussion)
    db.session.delete(discussion)
    db.session.commit()

def get_discussions():
    discussions = Discussion.query.all()
    return [discussion.to_dict() for discussion in discussions]

def search_discussions_by_text(text):
    return search_discussions(text)

def search_discussions_by_tags(tags):
    discussions = Discussion.query.join(Discussion.hashtags).filter(Hashtag.tag.in_(tags)).all()
    return [discussion.to_dict() for discussion in discussions]