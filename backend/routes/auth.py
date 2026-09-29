from flask import Blueprint, request, jsonify

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models import db

from models.user import User
from models.student import Student
from models.company import Company


auth_bp = Blueprint(
    'auth',
    __name__
)


# -------------------------
# STUDENT REGISTRATION
# -------------------------

@auth_bp.route('/register/student', methods=['POST'])
def register_student():

    data = request.get_json()

    existing_user = User.query.filter_by(
        email=data['email']
    ).first()

    if existing_user:

        return jsonify({
            "message": "Email already exists"
        }), 400


    hashed_password = generate_password_hash(
        data['password']
    )


    user = User(
        email=data['email'],
        password=hashed_password,
        role='student'
    )

    db.session.add(user)
    db.session.flush()


    student = Student(

        user_id=user.id,

        full_name=data['full_name'],

        degree=data['degree'],

        branch=data['branch'],

        cgpa=data['cgpa'],

        graduation_year=data['graduation_year'],

        phone_number=data.get(
            'phone_number'
        ),

        skills=data.get(
            'skills'
        )

    )


    db.session.add(student)

    db.session.commit()


    return jsonify({
        "message":
        "Student registered successfully"
    }), 201



# -------------------------
# COMPANY REGISTRATION
# -------------------------

@auth_bp.route('/register/company', methods=['POST'])
def register_company():

    data = request.get_json()


    existing_user = User.query.filter_by(
        email=data['email']
    ).first()


    if existing_user:

        return jsonify({
            "message": "Email already exists"
        }), 400



    hashed_password = generate_password_hash(
        data['password']
    )


    user = User(

        email=data['email'],

        password=hashed_password,

        role='company'

    )


    db.session.add(user)
    db.session.flush()



    company = Company(

        user_id=user.id,

        company_name=data['company_name'],

        website=data.get(
            'website'
        ),

        industry=data.get(
            'industry'
        ),

        location=data.get(
            'location'
        ),

        description=data.get(
            'description'
        ),

        hr_name=data.get(
            'hr_name'
        ),

        hr_email=data.get(
            'hr_email'
        ),

        hr_contact=data.get(
            'hr_contact'
        )

    )


    db.session.add(company)

    db.session.commit()


    return jsonify({
        "message":
        "Company registered successfully. Waiting for admin approval."
    }), 201



# -------------------------
# LOGIN
# -------------------------

@auth_bp.route('/login', methods=['POST'])
def login():


    data = request.get_json()


    user = User.query.filter_by(
        email=data['email']
    ).first()



    if not user:

        return jsonify({
            "message":
            "Invalid email or password"
        }), 401



    if not check_password_hash(
        user.password,
        data['password']
    ):

        return jsonify({
            "message":
            "Invalid email or password"
        }), 401



    if user.role == "company":

        company = Company.query.filter_by(
            user_id=user.id
        ).first()

        if not company:

            return jsonify({
                "message":
                "Company profile not found"
            }), 403


        if company.approval_status == "pending":

            return jsonify({

                "message":
                "Company account waiting for admin approval"

            }), 403


        if company.approval_status == "rejected":

            return jsonify({

                "message":
                f"Company rejected: {company.rejection_reason}"

            }), 403
    if user.role == "student":

        student = Student.query.filter_by(
            user_id=user.id
        ).first()

        if not student:

            return jsonify({
                "message": "Student profile not found"
            }), 403

        if student.is_blacklisted:

            return jsonify({
                "message": f"Student account has been blacklisted. Reason: {student.blacklist_reason}"
        }), 403

    access_token = create_access_token(

        identity=str(user.id),

        additional_claims={
            "role": user.role
        }

    )


    return jsonify({

        "token": access_token,

        "role": user.role

    }), 200




# -------------------------
# TEST PROTECTED ROUTE
# -------------------------

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():


    user_id = get_jwt_identity()


    claims = get_jwt()


    return jsonify({

        "message":
        "Protected route working",

        "user_id": user_id,

        "role": claims['role']

    }), 200