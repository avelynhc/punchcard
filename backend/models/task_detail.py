from db.migrations.create_table import db

class ItemModel(db.Model):
    __tablename__ = "task_details"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.BigInteger)
    finish_time = db.Column(db.BigInteger)
    user_id = db.Column(db.String, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')