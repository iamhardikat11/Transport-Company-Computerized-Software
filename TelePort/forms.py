from re import sub
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange
from TelePort.models import Consignment, Manager, Employee, Customer, Office, Truck
class signUpManager(FlaskForm):

    Name = StringField(label = 'Name', validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField(label = 'Address', validators=[DataRequired(), Length(min=2, max=100)])
    phoneNumber = StringField(label = 'Contact No.', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password1 = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(label = 'Re-enter Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label = 'Sign Up')

class loginManager(FlaskForm):
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label = 'Login')

class loginEmployee(FlaskForm):
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label = 'Login')

class signUpCustomer(FlaskForm):
    def validate_email(self, email):
        customer = Customer.query.filter_by(email = email.data).first()
        if customer:
            raise ValidationError('Email already exists')
    name = StringField(label = 'Name', validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField(label = 'Address', validators=[DataRequired(), Length(min=2, max=100)])
    branchID = IntegerField(label = 'Branch ID', validators=[DataRequired(), NumberRange(min = 1, max=999999999)])
    phoneNumber = StringField(label = 'Contact No.', validators=[DataRequired(), Length(min=10, max=10)])
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password1 = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(label = 'Re-enter Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label = 'Sign Up')

class loginCustomer(FlaskForm):
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label = 'Login')


class createEmployee(FlaskForm):

    def validate_email(self, email):
        employee = Employee.query.filter_by(email = email.data).first()
        if employee:
            raise ValidationError('Email already exists')
    def validate_branchID(self, branchID):
        branch = Office.query.filter_by(officeID = branchID.data).first()
        if branch is None:
            raise ValidationError('Branch ID does not exist')

    name = StringField(label = 'Name', validators=[DataRequired(), Length(min=2, max=30)])
    address = StringField(label = 'Address', validators=[DataRequired(), Length(min=2, max=100)])
    phoneNumber = StringField(label = 'Contact No.', validators=[DataRequired(), Length(min=10, max=10)])
    branchID = IntegerField(label = 'Branch ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    email = StringField(label = 'Email ID', validators=[DataRequired()])
    password1 = PasswordField(label = 'Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(label = 'Re-enter Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label = 'Add Employee')

class createOffice(FlaskForm):
    def validate_officeID(self, officeID):
        office = Office.query.filter_by(officeID = officeID.data).first()
        if office:
            raise ValidationError('ID already exists')
    officeID = IntegerField(label = 'ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    address = StringField(label = 'Address', validators=[DataRequired(), Length(min=2, max=100)])
    phoneNumber = StringField(label = 'Contact No.', validators=[DataRequired(), Length(min=10, max=10)])
    rate = IntegerField(label = 'Rate', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'Add Office')
    
class addTruck(FlaskForm):
    def validate_truckID(self, truckID):
        truck = Truck.query.filter_by(truckID = truckID.data).first()
        if truck:
            raise ValidationError('ID already exists')
    def validate_currentBranchID(self, currentBranchID):
        branch = Office.query.filter_by(officeID = currentBranchID.data).first()
        if branch is None:
            raise ValidationError('Branch ID does not exist')
    truckID =  IntegerField(label = 'Truck ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    currentBranchID = IntegerField(label = 'Branch ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'Add Truck')

class branchConsignmentDetails(FlaskForm):
    def validate_branchID(self, branchID):
        branch = Office.query.filter_by(officeID = branchID.data).first()
        if branch is None:
            raise ValidationError('Branch ID does not exist')
    branchID = IntegerField(label = 'Branch ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'View Details')
class placeOrder(FlaskForm):

    def validate_senderID(self,senderID):
        sender_ = Customer.query.filter_by(customerID = senderID.data).first()
        if sender_ is None:
            raise ValidationError('Sender ID does not exist')
    def validate_receiverID(self,receiverID):
        receiver_ = Customer.query.filter_by(customerID = receiverID.data).first()
        if receiver_ is None:
            raise ValidationError('Receiver ID does not exist')
    
    senderID = IntegerField(label = 'Sender ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    receiverID = IntegerField(label = 'Receiver ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)]) 
    volume = IntegerField(label = 'Volume', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'Place Order')
        
class viewBill(FlaskForm):
    def validate_consignmentID(self, consignmentID):
        consignment = Consignment.query.filter_by(consignmentID = consignmentID.data).first()
        if consignment is None:
            raise ValidationError('Consignment ID does not exist')
    consignmentID = IntegerField(label = 'Consignment ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'View Bill')
    
class viewTruckStatus(FlaskForm):
    def validate_truckID(self, truckID):
        truck = Truck.query.filter_by(truckID = truckID.data).first()
        if truck is None:
            raise ValidationError('Truck ID does not exist')
    truckID = IntegerField(label = 'Truck ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'View Truck Status')

class trackConsignment(FlaskForm):
    def validate_consignmentID(self, consignmentID):
        consignment = Consignment.query.filter_by(consignmentID = consignmentID.data).first()
        if consignment is None:
            raise ValidationError('Consignment ID does not exist')
    consignmentID = IntegerField(label = 'Consignment ID', validators=[DataRequired(), NumberRange(min=1, max=999999999)])
    submit = SubmitField(label = 'Track Consignment Status')