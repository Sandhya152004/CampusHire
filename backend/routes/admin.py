from flask import Blueprint, jsonify, request

from models.company import Company
from models import db
from models.user import User
from models.student import Student
from models.application import Application
from models.placement_drive import PlacementDrive

from utils.decorators import role_required

from cache import cache

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/companies', methods=['GET'])
@role_required('admin')
def get_companies():

    companies = Company.query.filter_by(
        is_blacklisted=False
    ).all()

    data = []

    for company in companies:

        data.append({

            "id": company.id,

            "company_name": company.company_name,

            "industry": company.industry,

            "location": company.location,

            "website": company.website,

            "approval_status": company.approval_status,

            "rejection_reason": company.rejection_reason,

            "is_blacklisted": company.is_blacklisted

        })

    return jsonify(data), 200

@admin_bp.route('/admin/company/<int:company_id>/reject', methods=['PUT'])
@role_required('admin')
def reject_company(company_id):

    company = Company.query.get(company_id)

    if not company:

        return jsonify({
            "message": "Company not found"
        }), 404


    data = request.get_json()


    company.approval_status = "rejected"


    company.rejection_reason = data.get(
        "reason",
        "No reason provided"
    )


    db.session.commit()


    return jsonify({
        "message":
        "Company rejected successfully"
    }), 200

@admin_bp.route('/admin/company/<int:company_id>/approve', methods=['PUT'])
@role_required('admin')
def approve_company(company_id):

    company = Company.query.get(company_id)

    if not company:

        return jsonify({
            "message": "Company not found"
        }), 404

    company.approval_status = "approved"

    db.session.commit()

    return jsonify({
        "message": "Company approved successfully"
    }), 200

@admin_bp.route('/admin/stats', methods=['GET'])
@role_required('admin')
def admin_stats():

    return jsonify({

        "students":
        Student.query.count(),

        "companies":
        Company.query.count(),

        "drives":
        PlacementDrive.query.count(),

        "applications":
        Application.query.count()

    }), 200

# -------------------------
# VIEW ALL DRIVES
# -------------------------

@admin_bp.route('/admin/drives', methods=['GET'])
@role_required('admin')
def get_all_drives():

    drives = PlacementDrive.query.all()

    data = []

    for drive in drives:

        company = Company.query.get(
            drive.company_id
        )

        applicant_count = Application.query.filter_by(
            drive_id=drive.id
        ).count()

        data.append({

            "id": drive.id,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "company_name": company.company_name,

            "location": drive.location,

            "salary": drive.salary,

            "cgpa_required": drive.cgpa_required,

            "eligible_degree": drive.eligible_degree,

            "eligible_branch": drive.eligible_branch,

            "application_deadline": str(
                drive.application_deadline
            ),

            "number_of_openings": drive.number_of_openings,

            "status": drive.status,

            "is_closed": drive.is_closed,

            "applicant_count": applicant_count,

            "rejection_reason": drive.rejection_reason

        })


    return jsonify(data), 200



# -------------------------
# APPROVE DRIVE
# -------------------------

@admin_bp.route(
    '/admin/drive/<int:drive_id>/approve',
    methods=['PUT']
)
@role_required('admin')
def approve_drive(drive_id):

    drive = PlacementDrive.query.get(
        drive_id
    )


    if not drive:

        return jsonify({
            "message":
            "Drive not found"
        }), 404

    if drive.status != "pending":

        return jsonify({

            "message": "Only pending drives can be approved."

        }), 400
    drive.status = "approved"

    db.session.commit()


    return jsonify({

        "message":
        "Drive approved successfully"

    }), 200




# -------------------------
# REJECT DRIVE
# -------------------------

@admin_bp.route(
    '/admin/drive/<int:drive_id>/reject',
    methods=['PUT']
)
@role_required('admin')
def reject_drive(drive_id):

    drive = PlacementDrive.query.get(
        drive_id
    )


    if not drive:

        return jsonify({
            "message":
            "Drive not found"
        }), 404


    data = request.get_json()

    if drive.status != "pending":

        return jsonify({

            "message": "Only pending drives can be rejected."

        }), 400

    drive.status = "rejected"


    drive.rejection_reason = data.get(
        "reason",
        "No reason provided"
    )


    db.session.commit()


    return jsonify({

        "message":
        "Drive rejected successfully"

    }), 200

@admin_bp.route('/admin/company/<int:company_id>', methods=['GET'])
@role_required('admin')
def get_company_profile(company_id):

    company = Company.query.get(company_id)

    if not company:

        return jsonify({
            "message": "Company not found"
        }), 404

    return jsonify({

        "id": company.id,

        "company_name": company.company_name,

        "industry": company.industry,

        "location": company.location,

        "website": company.website,

        "description": company.description,

        "hr_name": company.hr_name,

        "hr_email": company.hr_email,

        "hr_contact": company.hr_contact,

        "approval_status": company.approval_status,

        "rejection_reason": company.rejection_reason,

        "is_blacklisted": company.is_blacklisted

    }), 200
    
@admin_bp.route('/admin/company/<int:company_id>/drives', methods=['GET'])
@role_required('admin')
def get_company_drives(company_id):

    drives = PlacementDrive.query.filter_by(
        company_id=company_id
    ).all()

    data = []

    for drive in drives:

        data.append({

            "id": drive.id,

            "job_title": drive.job_title,

            "status": drive.status,

            "application_deadline": str(
                drive.application_deadline
            )

        })

    return jsonify(data), 200


@admin_bp.route(
    '/admin/company/<int:company_id>/deactivate',
    methods=['PUT']
)
@admin_bp.route(
    '/admin/company/<int:company_id>/blacklist',
    methods=['PUT']
)
@role_required('admin')
def deactivate_company(company_id):

    company = Company.query.get(company_id)

    if not company:

        return jsonify({
            "message": "Company not found"
        }),404

    data = request.get_json()

    company.is_blacklisted = True

    company.rejection_reason = data.get(
        "reason",
        "No reason provided"
    )

    db.session.commit()

    return jsonify({

        "message":"Company deactivated successfully"

    }),200
  
    
@admin_bp.route(
    '/admin/companies/blacklisted',
    methods=['GET']
)
@role_required('admin')
def blacklisted_companies():

    companies = Company.query.filter_by(
        is_blacklisted=True
    ).all()

    data = []

    for company in companies:

        data.append({

            "id": company.id,

            "company_name": company.company_name,

            "industry": company.industry,

            "location": company.location,
            
            "website": company.website,
            
            "rejection_reason": company.rejection_reason,

            "is_blacklisted": company.is_blacklisted

        })

    return jsonify(data), 200

@admin_bp.route('/admin/students', methods=['GET'])
@role_required('admin')
def get_students():

    students = Student.query.all()

    data = []

    for student in students:

        data.append({

            "id": student.id,

            "full_name": student.full_name,

            "degree": student.degree,

            "branch": student.branch,

            "cgpa": student.cgpa,

            "graduation_year": student.graduation_year,

            "phone_number": student.phone_number,

            "skills": student.skills,

            "resume_path": student.resume_path,

            "is_blacklisted": student.is_blacklisted,

            "blacklist_reason": student.blacklist_reason

        })

    return jsonify(data), 200

@admin_bp.route('/admin/student/<int:student_id>', methods=['GET'])
@role_required('admin')
def get_student(student_id):

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

        "resume_path": student.resume_path,

        "is_blacklisted": student.is_blacklisted,

        "blacklist_reason": student.blacklist_reason

    }),200
    
@admin_bp.route('/admin/student/<int:student_id>', methods=['GET'])
@role_required('admin')
def get_student_profile(student_id):

    student = Student.query.get(student_id)

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    user = User.query.get(student.user_id)

    return jsonify({

        "id": student.id,

        "full_name": student.full_name,

        "email": user.email,

        "degree": student.degree,

        "branch": student.branch,

        "cgpa": student.cgpa,

        "graduation_year": student.graduation_year,

        "phone_number": student.phone_number,

        "skills": student.skills,

        "resume_path": student.resume_path,

        "is_blacklisted": student.is_blacklisted,

        "blacklist_reason": student.blacklist_reason

    }), 200

@admin_bp.route('/admin/student/<int:student_id>/blacklist', methods=['PUT'])
@role_required('admin')
def blacklist_student(student_id):

    student = Student.query.get(student_id)

    if not student:

        return jsonify({
            "message":"Student not found"
        }),404

    data = request.get_json()

    student.is_blacklisted = True

    student.blacklist_reason = data.get(
        "reason",
        "Violation of placement policy"
    )

    db.session.commit()

    return jsonify({
        "message":"Student blacklisted"
    }),200
    
@admin_bp.route('/admin/student/<int:student_id>/restore', methods=['PUT'])
@role_required('admin')
def restore_student(student_id):

    student = Student.query.get(student_id)

    if not student:

        return jsonify({
            "message":"Student not found"
        }),404

    student.is_blacklisted = False

    student.blacklist_reason = None

    db.session.commit()

    return jsonify({
        "message":"Student restored"
    }),200
    
@admin_bp.route('/admin/reports', methods=['GET'])
@role_required('admin')
def admin_reports():

    total_students = Student.query.count()

    total_companies = Company.query.count()

    approved_companies = Company.query.filter_by(
        approval_status="approved"
    ).count()

    pending_companies = Company.query.filter_by(
        approval_status="pending"
    ).count()

    total_drives = PlacementDrive.query.count()

    active_drives = PlacementDrive.query.filter_by(
        is_closed=False
    ).count()

    closed_drives = PlacementDrive.query.filter_by(
        is_closed=True
    ).count()

    total_applications = Application.query.count()

    shortlisted = Application.query.filter_by(
        status="shortlisted"
    ).count()

    interview = Application.query.filter_by(
        status="interview"
    ).count()

    offer = Application.query.filter_by(
        status="offer"
    ).count()

    rejected = Application.query.filter_by(
        status="rejected"
    ).count()

    return jsonify({

        "total_students": total_students,

        "total_companies": total_companies,

        "approved_companies": approved_companies,

        "pending_companies": pending_companies,

        "total_drives": total_drives,

        "active_drives": active_drives,

        "closed_drives": closed_drives,

        "total_applications": total_applications,

        "shortlisted": shortlisted,

        "interview": interview,

        "offer": offer,

        "rejected": rejected

    }),200
    
@admin_bp.route('/admin/applications', methods=['GET'])
@role_required('admin')
def get_all_applications():

    applications = Application.query.all()

    data = []

    for application in applications:

        student = Student.query.get(
            application.student_id
        )

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        company = Company.query.get(
            drive.company_id
        )

        data.append({

            "application_id": application.id,

            "student_name": student.full_name,

            "company_name": company.company_name,

            "job_title": drive.job_title,

            "status": application.status,

            "cgpa": student.cgpa,

            "branch": student.branch,

            "applied_at": str(
                application.applied_at
            ),

            "interview_date": str(
                application.interview_date
            ) if application.interview_date else None

        })

    return jsonify(data),200

@admin_bp.route('/admin/company/<int:company_id>/restore', methods=['PUT'])
@role_required('admin')
def restore_company(company_id):

    company = Company.query.get(company_id)

    if not company:

        return jsonify({
            "message": "Company not found"
        }), 404

    company.is_blacklisted = False

    db.session.commit()

    return jsonify({
        "message": "Company restored successfully"
    }), 200