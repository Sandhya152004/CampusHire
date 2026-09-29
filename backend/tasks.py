from celery_config import celery
from datetime import date, timedelta
from flask_mail import Message
from mail import mail
from models.user import User


@celery.task
def add(x, y):

    return x + y

import os
import pandas as pd

from models import db
from models.application import Application
from models.student import Student
from models.company import Company
from models.placement_drive import PlacementDrive


@celery.task
def export_student_applications(student_id):

    applications = (

        db.session.query(

            Application,
            PlacementDrive,
            Company

        )

        .join(
            PlacementDrive,
            Application.drive_id == PlacementDrive.id
        )

        .join(
            Company,
            PlacementDrive.company_id == Company.id
        )

        .filter(
            Application.student_id == student_id
        )

        .all()

    )

    rows = []

    for application, drive, company in applications:

        rows.append({

            "Student ID": student_id,

            "Company": company.company_name,

            "Drive": drive.job_title,

            "Status": application.status,

            "Applied On": application.applied_at,

            "Interview Date": application.interview_date

        })

    df = pd.DataFrame(rows)

    os.makedirs("exports", exist_ok=True)

    filepath = f"exports/student_{student_id}.csv"

    df.to_csv(filepath, index=False)

    student = Student.query.get(student_id)

    if student:

        user = User.query.get(student.user_id)

        if user:

            msg = Message(

                subject="CSV Export Ready",

                recipients=[user.email]

            )

            msg.body = f"""
    Hello {student.full_name},

    Your placement application history has been exported successfully.

    File:
    {filepath}

    You can now download it from the Placement Portal.

    Regards,
    Placement Portal
    """

            mail.send(msg)

    return filepath

@celery.task
def export_company_applications(company_id):

    applications = (

        db.session.query(

            Application,
            Student,
            PlacementDrive

        )

        .join(
            Student,
            Application.student_id == Student.id
        )

        .join(
            PlacementDrive,
            Application.drive_id == PlacementDrive.id
        )

        .filter(
            PlacementDrive.company_id == company_id
        )

        .all()

    )

    rows = []

    for application, student, drive in applications:

        rows.append({

            "Student Name": student.full_name,

            "Degree": student.degree,

            "Branch": student.branch,

            "CGPA": student.cgpa,

            "Drive": drive.job_title,

            "Status": application.status,

            "Applied On": application.applied_at,

            "Interview Date": application.interview_date

        })

    os.makedirs("exports", exist_ok=True)

    filepath = f"exports/company_{company_id}.csv"

    pd.DataFrame(rows).to_csv(filepath, index=False)

    return filepath

@celery.task
def send_interview_reminders():

    tomorrow = date.today()

    applications = Application.query.filter(
        Application.interview_date == tomorrow
    ).all()

    for application in applications:

        student = Student.query.get(
            application.student_id
        )

        if not student:
            continue

        user = User.query.get(
            student.user_id
        )

        if not user:
            continue

        drive = PlacementDrive.query.get(
            application.drive_id
        )

        msg = Message(

            subject="Interview Reminder",

            recipients=[user.email]

        )

        msg.body = f"""
Hello {student.full_name},

This is a reminder that your interview is scheduled for tomorrow.

Job Title: {drive.job_title}

Date: {application.interview_date}

Time: {application.interview_time}

Location: {application.interview_location}

Good luck!

Placement Portal
"""

        mail.send(msg)

    return f"Sent {len(applications)} reminder(s)"

from datetime import datetime


@celery.task
def send_monthly_report():

    total_drives = PlacementDrive.query.count()

    total_students = Student.query.count()

    total_applications = Application.query.count()

    total_selected = Application.query.filter_by(
        status="offer"
    ).count()

    html = f"""
    <html>

    <body>

    <h2>Placement Portal Monthly Report</h2>

    <hr>

    <table border="1" cellpadding="8">

        <tr>
            <th>Total Students</th>
            <td>{total_students}</td>
        </tr>

        <tr>
            <th>Total Placement Drives</th>
            <td>{total_drives}</td>
        </tr>

        <tr>
            <th>Total Applications</th>
            <td>{total_applications}</td>
        </tr>

        <tr>
            <th>Total Offers</th>
            <td>{total_selected}</td>
        </tr>

    </table>

    <br>

    <p>

    Generated on:
    {datetime.now().strftime("%d-%m-%Y %H:%M")}

    </p>

    </body>

    </html>
    """

    admin = User.query.filter_by(
        email="admin@placement.com"
    ).first()

    if admin:

        msg = Message(

            subject="Monthly Placement Activity Report",

            recipients=[admin.email]

        )

        msg.html = html

        mail.send(msg)

    return "Monthly report sent successfully"