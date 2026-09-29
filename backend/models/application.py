from models import db


class Application(db.Model):

    __tablename__ = "applications"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        nullable=False
    )


    drive_id = db.Column(
        db.Integer,
        db.ForeignKey('placement_drives.id'),
        nullable=False
    )


    status = db.Column(
        db.String(30),
        default="applied"
    )


    applied_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )


    # Interview Details

    interview_date = db.Column(
        db.Date
    )

    interview_time = db.Column(
        db.String(20)
    )

    interview_location = db.Column(
        db.String(255)
    )

    feedback = db.Column(
        db.Text
    )

    remarks = db.Column(
        db.Text
    )

    __table_args__ = (

        db.UniqueConstraint(
            'student_id',
            'drive_id',
            name='unique_student_drive'
        ),

    )