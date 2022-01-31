from db.migrations.create_table import db

class TaskDetailModel(db.Model):
    __tablename__ = "task_details"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.BigInteger)
    finish_time = db.Column(db.BigInteger)
    task_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")

    def __init__(self, task_name, start_time):
        self.start_time = start_time
        # self.finish_time = finish_time
        self.task_name = task_name
        # self.user_id = user_id
    
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_name(cls, taskName):
        return cls.query.filter_by(task_name=taskName).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id" : self.id,
            "task_name" : self.task_name,
            "start_time" : self.start_time
        }
