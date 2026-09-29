from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.student import Student
from models.company import Company
from models.placement_drive import PlacementDrive
from models.application import Application
from models.placement import Placement
