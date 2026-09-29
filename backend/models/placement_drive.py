from models import db


class PlacementDrive(db.Model):

    __tablename__ = "placement_drives"
    
    company = db.relationship(
    "Company",
    backref="placement_drives"
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )


    company_id = db.Column(
        db.Integer,
        db.ForeignKey('companies.id'),
        nullable=False
    )


    # Job Information

    job_title = db.Column(
        db.String(150),
        nullable=False
    )


    job_description = db.Column(
        db.Text
    )


    skills_required = db.Column(
        db.String(500)
    )


    experience_required = db.Column(
        db.String(100)
    )


    salary = db.Column(
        db.String(100)
    )


    benefits = db.Column(
        db.Text
    )


    location = db.Column(
        db.String(150)
    )


    number_of_openings = db.Column(
        db.Integer,
        default=1
    )


    # Eligibility

    cgpa_required = db.Column(
        db.Float,
        default=0.0
    )


    eligible_degree = db.Column(
        db.String(100),
        default="Any"
    )


    eligible_branch = db.Column(
        db.String(100),
        default="Any"
    )
    
    eligible_year = db.Column(
        db.Integer,
        default=0
    )


    # Dates

    application_deadline = db.Column(
        db.Date
    )


    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


    # Admin Approval

    status = db.Column(
        db.String(20),
        default="pending"
    )


    rejection_reason = db.Column(
        db.String(255)
    )


    # Company Control

    is_closed = db.Column(
        db.Boolean,
        default=False
    )