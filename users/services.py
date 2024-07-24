from .models import db, User

def create_user(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

def update_user(user_id, data):
    user = User.query.get(user_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user.to_dict()

def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

def get_users():
    users = User.query.all()
    return [user.to_dict() for user in users]

def search_users(name):
    users = User.query.filter(User.name.ilike(f'%{name}%')).all()
    return [user.to_dict() for user in users]