from models import db


class Company(db.Model):

    __tablename__ = "companies"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    # Company Details
    company_name = db.Column(
        db.String(150),
        nullable=False
    )

    industry = db.Column(
        db.String(100)
    )

    location = db.Column(
        db.String(150)
    )

    website = db.Column(
        db.String(255)
    )

    description = db.Column(
        db.Text
    )

    logo_path = db.Column(
        db.String(255)
    )

    # HR Details
    hr_name = db.Column(
        db.String(100)
    )

    hr_email = db.Column(
        db.String(120)
    )

    hr_contact = db.Column(
        db.String(20)
    )

    # Admin Controls
    approval_status = db.Column(
        db.String(20),
        default="pending"
    )

    rejection_reason = db.Column(
        db.String(255)
    )

    is_blacklisted = db.Column(
        db.Boolean,
        default=False
    )