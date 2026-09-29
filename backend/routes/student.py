from email.mime import application
from cache import cache

from flask import Blueprint, jsonify, request

from flask_jwt_extended import get_jwt_identity

from models import db

from models.student import Student
from models.application import Application
from models.placement_drive import PlacementDrive
from models.company import Company

from utils.decorators import role_required
from werkzeug.utils import secure_filename
import os
from flask import current_app
from tasks import export_student_applications
from flask import send_from_directory
from flask import send_file
import os

from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

student_bp = Blueprint(
    'student',
    __name__
)



@student_bp.route('/student/drives', methods=['GET'])
@role_required('student')
@cache.cached(timeout=300)
def get_drives():

    drives = PlacementDrive.query.filter_by(
        status="approved",
        is_closed=False
    ).all()


    data = []


    for drive in drives:

        data.append({

            "id": drive.id,

            "company": drive.company.company_name,

            "job_title": drive.job_title,

            "job_description": drive.job_description,

            "cgpa_required": drive.cgpa_required,

            "eligible_degree": drive.eligible_degree,

            "eligible_branch": drive.eligible_branch,

            "salary": drive.salary,

            "location": drive.location,

            "skills_required": drive.skills_required,

            "application_deadline": str(
                drive.application_deadline
            )

        })


    return jsonify(data), 200



@student_bp.route('/student/apply/<int:drive_id>', methods=['POST'])
@role_required('student')
def apply_drive(drive_id):


    user_id = int(
        get_jwt_identity()
    )


    student = Student.query.filter_by(
        user_id=user_id
    ).first()


    if not student:

        return jsonify({
            "message":
            "Student profile not found"
        }), 404



    drive = PlacementDrive.query.get(
        drive_id
    )


    if not drive:

        return jsonify({
            "message":
            "Drive not found"
        }), 404



    existing_application = Application.query.filter_by(

        student_id=student.id,

        drive_id=drive.id

    ).first()


    if existing_application:

        return jsonify({
            "message":
            "Already applied to this drive"
        }), 400



    if (
        drive.cgpa_required
        and
        student.cgpa < drive.cgpa_required
    ):

        return jsonify({
            "message":
            "CGPA criteria not satisfied"
        }), 403



    if (
        drive.eligible_degree
        and
        drive.eligible_degree.lower()
        not in ["any", "nil"]
    ):

        if not student.degree:
            return jsonify({
                "message": "Please complete your profile by adding your degree."
            }), 400

        if (
            student.degree.lower()
            !=
            drive.eligible_degree.lower()
        ):

            return jsonify({
                "message":
                "Degree criteria not satisfied"
            }), 403





    if (
        drive.eligible_branch
        and
        drive.eligible_branch.lower()
        not in ["any", "nil"]
    ):

        if (
            student.branch.lower()
            !=
            drive.eligible_branch.lower()
        ):

            return jsonify({
                "message":
                "Branch criteria not satisfied"
            }), 403



    application = Application(

        student_id=student.id,

        drive_id=drive.id,

        status="applied"

    )


    db.session.add(application)

    db.session.commit()


    return jsonify({
        "message":
        "Applied successfully"
    }), 201



@student_bp.route('/student/applications', methods=['GET'])
@role_required('student')
def student_applications():


    user_id = int(
        get_jwt_identity()
    )


    student = Student.query.filter_by(
        user_id=user_id
    ).first()


    applications = Application.query.filter_by(

        student_id=student.id

    ).all()


    data = []


    for application in applications:


        drive = PlacementDrive.query.get(
            application.drive_id
        )


        data.append({

            "application_id": application.id,

            "job_title": drive.job_title,

            "company": Company.query.get(
                drive.company_id
            ).company_name,

            "status": application.status,

            "applied_at": str(
                application.applied_at
            ),

            "interview_date": str(
                application.interview_date
            ) if application.interview_date else None,

            "interview_time": application.interview_time,

            "interview_location": application.interview_location

        })


    return jsonify(data), 200




@student_bp.route('/student/profile', methods=['GET'])
@role_required('student')
def get_student_profile():


    user_id = int(
        get_jwt_identity()
    )


    student = Student.query.filter_by(
        user_id=user_id
    ).first()


    return jsonify({

        "full_name":
        student.full_name,

        "degree":
        student.degree,

        "branch":
        student.branch,

        "cgpa":
        student.cgpa,

        "graduation_year":
        student.graduation_year,

        "phone_number":
        student.phone_number,

        "skills":
        student.skills,
        
        "resume_path": student.resume_path

    }), 200
    
@student_bp.route('/student/profile', methods=['PUT'])
@role_required('student')
def update_student_profile():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    data = request.get_json()

    student.full_name = data.get(
        "full_name",
        student.full_name
    )

    student.degree = data.get(
        "degree",
        student.degree
    )

    student.branch = data.get(
        "branch",
        student.branch
    )

    student.cgpa = data.get(
        "cgpa",
        student.cgpa
    )

    student.graduation_year = data.get(
        "graduation_year",
        student.graduation_year
    )

    student.phone_number = data.get(
        "phone_number",
        student.phone_number
    )

    student.skills = data.get(
        "skills",
        student.skills
    )

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully"
    }), 200
    
@student_bp.route('/student/resume', methods=['POST'])
@role_required('student')
def upload_resume():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:

        return jsonify({
            "message": "Student not found"
        }),404

    if 'resume' not in request.files:

        return jsonify({
            "message":"No file uploaded"
        }),400

    file = request.files['resume']

    if file.filename == "":

        return jsonify({
            "message":"No file selected"
        }),400

    filename = secure_filename(

        f"{student.id}_{file.filename}"

    )

    filepath = os.path.join(

        current_app.config["UPLOAD_FOLDER"],

        filename

    )

    print("=" * 50)
    print("UPLOAD FOLDER:", current_app.config["UPLOAD_FOLDER"])
    print("FILEPATH:", filepath)

    file.save(filepath)

    print("FILE EXISTS:", os.path.exists(filepath))
    print("=" * 50)
    
    student.resume_path = filename

    db.session.commit()

    return jsonify({

        "message":"Resume uploaded successfully"

    }),200
    
@student_bp.route('/student/resume', methods=['GET'])
@role_required('student')
def get_resume():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(

        user_id=user_id

    ).first()

    if not student:

        return jsonify({

            "message":"Student not found"

        }),404

    return jsonify({

        "resume_path":student.resume_path

    }),200    

@student_bp.route('/student/dashboard', methods=['GET'])
@role_required('student')
def student_dashboard():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:
        return jsonify({
            "message": "Student not found"
        }), 404

    available_jobs = PlacementDrive.query.filter_by(
        status="approved",
        is_closed=False
    ).count()

    applications = Application.query.filter_by(
        student_id=student.id
    ).all()

    applied = len(applications)
    interviews = 0
    offer = 0

    recent = []
    upcoming = None

    for application in applications:

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        recent.append({
            "job_title": drive.job_title,
            "status": application.status
        })

        if application.status == "interview_scheduled":

            interviews += 1

            if upcoming is None:

                upcoming = {

                    "job_title": drive.job_title,

                    "company": drive.company.company_name if hasattr(drive, "company") else "",

                    "date": str(application.interview_date),

                    "time": application.interview_time,

                    "location": application.interview_location

                }

        if application.status == "offer":
            offer += 1

    return jsonify({

        "student_name": student.full_name,

        "available_jobs": available_jobs,

        "applied": applied,

        "interviews": interviews,

        "offer": offer,

        "upcoming_interview": upcoming,

        "recent_applications": recent[-5:]

    }), 200
    
@student_bp.route('/student/export-applications', methods=['POST'])
@role_required('student')
def export_applications():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:

        return jsonify({
            "message": "Student not found"
        }), 404

    task = export_student_applications.delay(
        student.id
    )

    return jsonify({

        "message": "Export started successfully.",

        "task_id": task.id,
        
        "filename": f"student_{student.id}.csv"

    }), 202
    

@student_bp.route(
    "/student/export/download",
    methods=["GET"]
)
@role_required("student")
def download_export():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:

        return jsonify({
            "message": "Student not found"
        }),404

    filepath = f"exports/student_{student.id}.csv"

    if not os.path.exists(filepath):

        return jsonify({
            "message":"Export not ready yet"
        }),404

    return send_file(

        filepath,

        as_attachment=True,

        download_name=f"student_{student.id}.csv"

    )
    
@student_bp.route(
    "/student/offer-letter/<int:application_id>",
    methods=["GET"]
)
@role_required("student")
def download_offer_letter(application_id):

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(
        user_id=user_id
    ).first()

    if not student:

        return jsonify({
            "message": "Student not found"
        }),404

    application = Application.query.get(application_id)

    if not application:

        return jsonify({
            "message":"Application not found"
        }),404

    if application.student_id != student.id:

        return jsonify({
            "message":"Unauthorized"
        }),403

    if application.status not in ["offer","placed"]:

        return jsonify({
            "message":"Offer letter not available"
        }),400

    drive = PlacementDrive.query.get(application.drive_id)

    company = Company.query.get(drive.company_id)

    styles = getSampleStyleSheet()

    tmp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(tmp.name)

    story = [

        Paragraph(
            "<b>PLACEMENT OFFER LETTER</b>",
            styles["Title"]
        ),

        Paragraph("<br/>",styles["Normal"]),

        Paragraph(
            f"Dear <b>{student.full_name}</b>,",
            styles["Normal"]
        ),

        Paragraph("<br/>",styles["Normal"]),

        Paragraph(

            f"We are pleased to offer you the position of "
            f"<b>{drive.job_title}</b> at "
            f"<b>{company.company_name}</b>.",

            styles["Normal"]

        ),

        Paragraph("<br/>",styles["Normal"]),

        Paragraph(

            f"Location : {company.location}",

            styles["Normal"]

        ),

        Paragraph(

            f"Package : {drive.salary}",

            styles["Normal"]

        ),

        Paragraph("<br/>",styles["Normal"]),

        Paragraph(

            "Congratulations on your placement and we wish you success in your career.",

            styles["Normal"]

        ),

        Paragraph("<br/><br/>",styles["Normal"]),

        Paragraph(

            "<b>Placement Cell</b><br/>"
            "Placement Portal",

            styles["Normal"]

        )

    ]

    doc.build(story)

    return send_file(

        tmp.name,

        as_attachment=True,

        download_name="OfferLetter.pdf"

    )