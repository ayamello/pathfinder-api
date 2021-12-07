from app.configs.database import db


users_paths = db.Table('users_paths',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('path_id', db.Integer, db.ForeignKey('paths.id'))
)

