from models import db

class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    full_name = db.Column(db.String(100), nullable=False)

    
    degree = db.Column(
        db.String(100)
    )
    
    branch = db.Column(db.String(100))
    
    cgpa = db.Column(db.Float)

    graduation_year = db.Column(db.Integer)

    phone_number = db.Column(db.String(20))

    skills = db.Column(db.String(500))

    resume_path = db.Column(db.String(255))
    
    is_blacklisted = db.Column(
    db.Boolean,
    default=False
    )

    blacklist_reason = db.Column(
        db.String(255)
    )