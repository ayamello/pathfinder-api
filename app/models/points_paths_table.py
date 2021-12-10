from app.configs.database import db


points_paths = db.Table('points_paths',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('path_id', db.Integer, db.ForeignKey('paths.id')),
    db.Column('point_id', db.Integer, db.ForeignKey('points.id'))
)
