from db.migrations.create_table import db

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.String)
