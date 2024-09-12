from copyreg import dispatch_table
from email.policy import default
# import queue
from TelePort import db
from TelePort import bcrypt
from TelePort import log_manage
from flask_login import UserMixin
import datetime
from sqlalchemy.sql import func
@log_manage.user_loader
def load_manager(managerID):
    return Manager.query.get(int(managerID))

@log_manage.user_loader
def load_employee(employeeID):
    return Employee.query.get(int(employeeID))

# @log_manage.user_loader
# def load_customer(customerID):
#     return Customer.query.get(int(customerID))

class Consignment(db.Model):
    consignmentID = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer, unique=False, nullable=False)
    purchaseDate = db.Column(db.DateTime, default = datetime.datetime.now())
    deliveryDate = db.Column(db.DateTime, default = datetime.datetime.now())
    # sender = db.relationship('Sender', backref='consignment', lazy=True)
    # receiver = db.relationship('Receiver', backref='consignment', lazy=True)
    senderID = db.Column(db.Integer, nullable = False)
    receiverID = db.Column(db.Integer, nullable = False)
    sourceAddress = db.Column(db.String(1200), unique=False, nullable=False)
    sourceOfficeID = db.Column(db.Integer, nullable = False)
    # sourceOffice = db.relationship('Office')
    destinationAddress = db.Column(db.String(1200), unique=False, nullable=False)
    destinationOfficeID = db.Column(db.Integer, nullable = False)
    # destinationOffice = db.relationship('Office')
    revenue = db.Column(db.Integer, unique=False, nullable=False, default = 0)
    truckAssigned = db.Column(db.Integer, unique=False, nullable=False, default = 0)
    # truckAssigned = db.relationship('Truck')
    status = db.Column(db.String(1200), unique=False, nullable=False, default = "In Transit")
    def __repr__(self):
        return '<Consignment %r>' % self.consignmentID
    

class Customer(db.Model, UserMixin):
    # __abstract__ = True
    customerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(1200), unique=False, nullable=False)
    branchID = db.Column(db.Integer, nullable = False)
    phoneNumber = db.Column(db.String(1200), unique=False, nullable=False)
    email = db.Column(db.String(1200), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    consignments = db.Column(db.String(1200), unique=False, default = "")
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def get_id(self):
        return self.customerID


class Employee(db.Model, UserMixin):
    employeeID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1200), unique=False, nullable=False)
    address = db.Column(db.String(1200), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # branchID = db.Column(db.String(80), unique=False, nullable=False)
    branchID = db.Column(db.Integer, nullable = False)
    # branch = db.relationship('Office')
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    def __repr__(self):
        return '<Employee %r>' % self.name
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def get_id(self):
        return self.employeeID

class Manager(db.Model, UserMixin):
    managerID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    address = db.Column(db.String(1200), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(1200), unique=False, nullable=False)
    email = db.Column(db.String(1200), unique=True, nullable=False)
    # branchID = db.Column(db.String(80), unique=False, nullable=False)
    # branch = db.relationship('Office', backref='manager', lazy = True)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    def __repr__(self):
        return '<Manager %r>' % self.name
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    def get_id(self):
        return self.managerID

class Office(db.Model):
    officeID = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(1200), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(120), unique=False)
    # managerID = db.Column(db.Integer, db.ForeignKey('Manager.managerID'))
    # manager = db.Column(db.Integer, db.ForeignKey('Manager.managerID'))
    numTrucks = db.Column(db.Integer, unique=False,  default = 0)
    numEmployees = db.Column(db.Integer, unique=False,  default = 0)
    volumeHandled = db.Column(db.Integer, unique=False,  default = 0)
    presentVolume = db.Column(db.Integer, unique=False,  default = 0)
    revenue = db.Column(db.Integer, unique=False,  default = 0)
    idleWaitingTime = db.Column(db.Integer, unique=False,  default = 0) 
    # orders = []
    order_map = {}
    volume_map = {}
    total_orders = db.Column(db.String(1200), unique=False, default = "") 
    
    rate = db.Column(db.Integer, unique=False,  nullable = False)
    def __repr__(self):
        return '<Office %r>' % self.officeID

class Truck(db.Model):
    truckID = db.Column(db.Integer, primary_key=True)
    # currentBranch = db.Column(db.String(80), unique=False, nullable=False)
    # currentBranch = db.relationship('Office', backref='truck', lazy=True)
    currentBranchID = db.Column(db.Integer, unique=False, nullable=False)
    numConsignments = db.Column(db.Integer, unique=False,  default = 0)
    prevDispatchDate = db.Column(db.DateTime, default = datetime.datetime.now())
    waitingTime = db.Column(db.Float, unique=False,  default = 0.0)
    # waitingTime = db.Column(db.Integer, unique=False,  default = 0)
    # status = db.Column(db.String(80), unique=False,  default = "idle")

# db.create_all()