from email.mime import application

from cache import cache

from flask import Blueprint
from flask import request
from flask import jsonify
from datetime import datetime
from flask import send_file
import os

from flask_jwt_extended import get_jwt_identity

from models import db

from models.user import User
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from models.student import Student

from tasks import export_company_applications

from utils.decorators import role_required

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/dashboard', methods=['GET'])
@role_required('company')
def company_dashboard():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:

        return jsonify({
            "message": "Company not found"
        }),404

    drives = PlacementDrive.query.filter_by(
        company_id=company.id,
        is_closed=False
    ).all()

    active_drives = PlacementDrive.query.filter_by(
        company_id=company.id,
        is_closed=False
    ).count()

    total_applications = 0
    shortlisted = 0
    offer = 0

    recent_drives = []

    recent_applicants = []

    for drive in drives:

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        recent_drives.append({

            "id": drive.id,

            "job_title": drive.job_title,

            "status": drive.status,

            "deadline": str(
                drive.application_deadline
            ),

            "location": drive.location,

            "cgpa_required": drive.cgpa_required,

            "applicants": len(applications)

        })

        applications = Application.query.filter_by(
            drive_id=drive.id
        ).all()

        total_applications += len(applications)

        for application in applications:

            if application.status == "shortlisted":

                shortlisted += 1

            if application.status == "offer":

                offer += 1

            student = Student.query.get(
                application.student_id
            )

            recent_applicants.append({

                "student_id": student.id,

                "student_name": student.full_name,

                "cgpa": student.cgpa,

                "degree": student.degree,

                "job_title": drive.job_title,

                "status": application.status

            })
    return jsonify({

        "company_name":
        company.company_name,

        "active_drives":
        active_drives,

        "applications":
        total_applications,

        "shortlisted":
        shortlisted,

        "offer":
        offer,

        "recent_drives":
        recent_drives[-5:],

        "recent_applicants":
        recent_applicants[-5:]

    }),200

@company_bp.route('/company/drive', methods=['POST'])
@role_required('company')
def create_drive():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:

        return jsonify({
            "message": "Company profile not found"
        }), 404

    if company.approval_status != "approved":

        return jsonify({
            "message": "Company not approved by admin"
        }), 403

    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403

    data = request.get_json()

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data['job_title'],
        job_description=data['job_description'],
        cgpa_required=data['cgpa_required'],
        eligible_degree=data.get(
        'eligible_degree',
        'Any'
        ),
        eligible_branch=data['eligible_branch'],
        application_deadline=datetime.strptime(data['application_deadline'], '%Y-%m-%d'),
        
        skills_required=data.get(
        "skills_required",
        ""
        ),

        salary=data.get(
            "salary"
        ),

        location=data.get(
            "location", 
            'Remote'
        ),
        number_of_openings=data.get(
            "number_of_openings",
            1
        ),

        experience_required=data.get(
            "experience_required",
            "0-1 years"
        ),

        benefits=data.get(
            "benefits"
        ),
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({
        "message": "Placement drive created successfully"
    }), 201
    
@company_bp.route('/company/applications/<int:drive_id>', methods=['GET'])
@role_required('company')
def view_applications(drive_id):

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403

    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()

    if not drive:

        return jsonify({
            "message": "Drive not found"
        }), 404

    applications = Application.query.filter_by(
        drive_id=drive.id
    ).all()

    data = []

    for application in applications:

        student = Student.query.get(
            application.student_id
        )

        data.append({
            "application_id": application.id,
            "student_id": student.id,
            "student_name": student.full_name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "status": application.status,
            "interview_date":
            str(application.interview_date),
            "resume_path": student.resume_path,

            "interview_time":
            application.interview_time,

            "interview_location":
            application.interview_location
        })

    return jsonify(data), 200

@company_bp.route('/company/application/<int:application_id>/status', methods=['PUT'])
@role_required('company')
def update_application_status(application_id):

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()


    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403


    application = Application.query.get(
        application_id
    )


    if not application:

        return jsonify({
            "message": "Application not found"
        }), 404


    drive = PlacementDrive.query.get(
        application.drive_id
    )


    if drive.company_id != company.id:

        return jsonify({
            "message": "Unauthorized"
        }), 403


    # selected and rejected are final states

    if application.status in [
        "placed",
        "rejected"
    ]:

        return jsonify({
            "message": "Final status already reached"
        }), 400


    data = request.get_json()


    new_status = data["status"]


    # status flow validation

    if (
        application.status == "applied"
        and
        new_status not in [
            "shortlisted",
            "rejected"
        ]
    ):

        return jsonify({
            "message": "Invalid status change"
        }), 400


    if (
        application.status == "interview_scheduled"
        and
        new_status not in [
            "offer",
            "rejected"
        ]
    ):

        return jsonify({
            "message": "Invalid status change"
        }), 400

    if (

        application.status == "offer"

        and

        new_status != "placed"

    ):

        return jsonify({

            "message":"Invalid status change"

        }),400

    application.status = new_status


    db.session.commit()


    return jsonify({
        "message": "Application status updated"
    }), 200
    
@company_bp.route('/company/drives', methods=['GET'])
@role_required('company')
def get_company_drives():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403

    drives = PlacementDrive.query.filter_by(
        company_id=company.id
    ).all()

    data = []

    for drive in drives:

        applicant_count = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        data.append({

            "id": drive.id,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "eligible_degree": drive.eligible_degree,

            "eligible_branch": drive.eligible_branch,

            "cgpa_required": drive.cgpa_required,

            "status": drive.status,

            "is_closed": drive.is_closed,

            "application_deadline": str(
                drive.application_deadline
            ),

            "applicant_count": applicant_count

        })

    return jsonify(data), 200

@company_bp.route('/company/drive/<int:drive_id>', methods=['GET'])
@role_required('company')
def get_drive(drive_id):

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403

    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()
    
    if not drive:

        return jsonify({
            "message": "Drive not found"
        }), 404

    return jsonify({

        "id": drive.id,

        "job_title": drive.job_title,

        "job_description": drive.job_description,

        "cgpa_required": drive.cgpa_required,

        "eligible_degree": drive.eligible_degree,

        "eligible_branch": drive.eligible_branch,

        "application_deadline": str(
            drive.application_deadline
        ),

        "status": drive.status,

        "is_closed": drive.is_closed

    }), 200
    
@company_bp.route('/company/drive/<int:drive_id>', methods=['PUT'])
@role_required('company')
def update_drive(drive_id):

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if company.is_blacklisted:

        return jsonify({
            "message": "Company account has been deactivated"
        }), 403

    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()

    if not drive:

        return jsonify({
            "message": "Drive not found"
        }), 404

    data = request.get_json()

    drive.job_title = data["job_title"]
    drive.job_description = data["job_description"]
    drive.cgpa_required = data["cgpa_required"]
    drive.eligible_degree = data["eligible_degree"]
    drive.eligible_branch = data["eligible_branch"]

    drive.application_deadline = datetime.strptime(
        data["application_deadline"],
        "%Y-%m-%d"
    )

    db.session.commit()

    return jsonify({
        "message": "Drive updated successfully"
    }), 200
    
@company_bp.route('/company/drive/<int:drive_id>/close', methods=['PUT'])
@role_required('company')
def close_drive(drive_id):

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()


    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=company.id
    ).first()


    if not drive:

        return jsonify({
            "message": "Drive not found"
        }), 404


    drive.is_closed = True


    db.session.commit()


    return jsonify({
        "message": "Drive closed successfully"
    }), 200
    
@company_bp.route(
    '/company/application/<int:application_id>/interview',
    methods=['PUT']
)
@role_required('company')
def schedule_interview(application_id):

    user_id = int(
        get_jwt_identity()
    )


    company = Company.query.filter_by(
        user_id=user_id
    ).first()


    application = Application.query.get(
        application_id
    )


    if not application:

        return jsonify({
            "message":
            "Application not found"
        }), 404


    drive = PlacementDrive.query.get(
        application.drive_id
    )


    if drive.company_id != company.id:

        return jsonify({
            "message":
            "Unauthorized"
        }), 403


    if application.status != "shortlisted":

        return jsonify({
            "message":
            "Only shortlisted students can be scheduled"
        }), 400


    data = request.get_json()


    application.interview_date = datetime.strptime(
        data["date"],
        "%Y-%m-%d"
    ).date()


    application.interview_time = data["time"]


    application.interview_location = data["location"]


    application.status = "interview_scheduled"


    db.session.commit()


    return jsonify({

        "message":
        "Interview scheduled successfully"

    }), 200
    
@company_bp.route('/company/profile', methods=['GET'])
@role_required('company')
def company_profile():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    if not company:

        return jsonify({
            "message": "Company not found"
        }),404

    return jsonify({

        "company_name": company.company_name,

        "website": company.website,

        "industry": company.industry,

        "location": company.location,

        "description": company.description,

        "hr_name": company.hr_name,

        "hr_email": company.hr_email,

        "hr_contact": company.hr_contact,

        "approval_status": company.approval_status

    }),200
    
@company_bp.route('/company/profile', methods=['PUT'])
@role_required('company')
def update_company_profile():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(
        user_id=user_id
    ).first()
    
    if not company:
        return jsonify({
            "message": "Company not found"
        }), 404

    data = request.get_json()

    company.company_name = data.get("company_name")
    company.industry = data.get("industry")
    company.location = data.get("location")
    company.website = data.get("website")
    company.description = data.get("description")
    company.hr_name = data.get("hr_name")
    company.hr_email = data.get("hr_email")
    company.hr_contact = data.get("hr_contact")

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200
    
@company_bp.route('/company/student/<int:student_id>', methods=['GET'])
@role_required('company')
def get_student_profile(student_id):

    student = Student.query.get(student_id)

    if not student:

        return jsonify({
            "message": "Student not found"
        }),404

    return jsonify({

        "id": student.id,

        "full_name": student.full_name,

        "degree": student.degree,

        "branch": student.branch,

        "cgpa": student.cgpa,

        "graduation_year": student.graduation_year,

        "phone_number": student.phone_number,

        "skills": student.skills,

        "resume_path": student.resume_path

    }),200
    
@company_bp.route('/company/application/<int:application_id>/placed', methods=['PUT'])
@role_required('company')
def mark_as_placed(application_id):

    application = Application.query.get(application_id)

    if not application:

        return jsonify({
            "message": "Application not found"
        }),404

    application.status = "placed"

    db.session.commit()

    return jsonify({
        "message": "Student marked as placed."
    }),200
    
@company_bp.route(
    "/company/export-applications",
    methods=["POST"]
)
@role_required("company")
def export_company_csv():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    task = export_company_applications.delay(
        company.id
    )

    return jsonify({

        "message": "Export started successfully.",

        "task_id": task.id,

        "filename": f"company_{company.id}.csv"

    }), 202
    
@company_bp.route(
    "/company/export/download",
    methods=["GET"]
)
@role_required("company")
def download_company_export():

    user_id = int(get_jwt_identity())

    company = Company.query.filter_by(
        user_id=user_id
    ).first()

    filepath = f"exports/company_{company.id}.csv"

    if not os.path.exists(filepath):

        return jsonify({

            "message": "Export not ready."

        }),404

    return send_file(

        filepath,

        as_attachment=True,

        download_name=f"company_{company.id}.csv"

    )