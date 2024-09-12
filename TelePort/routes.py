
from numpy import source
from TelePort import app
from flask import render_template, request
from TelePort.forms import loginEmployee, placeOrder, signUpManager, loginManager, signUpCustomer, \
    loginCustomer, createEmployee, createOffice,addTruck, trackConsignment,viewBill, viewTruckStatus, branchConsignmentDetails
from TelePort.models import Consignment, Customer, Manager, Employee, Office, Truck
import datetime
from TelePort import db
from flask import Flask,flash, redirect, url_for,session
from flask_login import login_user, logout_user
from flask_session import Session
import json
import plotly
import plotly.express as px
import os
# app = Flask(__name__)
@app.route('/')
@app.route('/home')
def index():
    if 'manager' in session:
        session.pop('manager', None)
    if 'customer' in session:
        session.pop('customer', None)
    if 'employee' in session:
        session.pop('employee', None)
    if 'consignment' in session:
        session.pop('consignment', None)
    if 'office' in session:
        session.pop('office', None)
    if 'truck' in session:
        session.pop('truck', None)
    logout_user()
    session['name'] = ""
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/signup_manager', methods = ['GET', 'POST'])
def signup_manager():
    
    length = len(Manager.query.all())
    if length >= 1:
            flash('Manager already exists', 'danger')
            return redirect(url_for('login_manager'))
    form = signUpManager()
    if form.validate_on_submit():
        
        manager = Manager(managerID = 1+len(Manager.query.all()), name = form.Name.data, 
                          address = form.address.data, phoneNumber = form.phoneNumber.data, 
                          email = form.email.data, password = form.password1.data)
        db.session.add(manager)
        db.session.commit()
        if form.errors == {}:
            flash(f'Success! You are signed up as: {manager.name}', category='success')
        return redirect(url_for('login_manager'))
        
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
        
    return render_template('signup_manager.html', form = form)

@app.route('/login_manager', methods = ['GET', 'POST'])
def login_manager():
    form = loginManager()
    if form.validate_on_submit():
        attempted_manager = Manager.query.filter_by(email = form.email.data).first()
        
        if attempted_manager and attempted_manager.check_password_correction(form.password.data):
            session['manager'] = (attempted_manager)
            session['name'] = attempted_manager.name
            login_user(attempted_manager)
            flash(f'Success! You are logged in as: {attempted_manager.name}', category='success')
            # print(attempted_manager.name)
            return redirect(url_for('manager_actions2'))
        else:
            flash('Invalid email or password! Please try again', category='danger')
    return render_template('login_manager.html', form = form)

@app.route('/logout')
def logout_page():
    if 'manager' in session:
        session.pop('manager', None)
    if 'customer' in session:
        session.pop('customer', None)
    if 'employee' in session:
        session.pop('employee', None)
    if 'consignment' in session:
        session.pop('consignment', None)
    if 'office' in session:
        session.pop('office', None)
    if 'truck' in session:
        session.pop('truck', None)
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('index'))

@app.route('/login_employee', methods = ['GET', 'POST'])
def login_employee():
    form = loginEmployee()
    if form.validate_on_submit():
        attempted_employee = Employee.query.filter_by(email = form.email.data).first()
        if attempted_employee and attempted_employee.check_password_correction(form.password.data):
            session['employee'] = (attempted_employee)
            session['name'] = attempted_employee.name
            login_user(attempted_employee)
            flash(f'Success! You are logged in as: {attempted_employee.name}', category='success')
            return redirect(url_for('employee_actions'))
        else:
            flash('Invalid email or password! Please try again', category='danger')
    return render_template('login_employee.html', form = form)

@app.route('/signup_customer', methods = ['GET', 'POST'])
def signup_customer():
    form = signUpCustomer()
    if form.validate_on_submit():
        customer = Customer(customerID = 1+len(Customer.query.all()), name = form.name.data, 
                            address = form.address.data, branchID = form.branchID.data, phoneNumber = form.phoneNumber.data, 
                            email = form.email.data, password = form.password1.data)
        db.session.add(customer)
        db.session.commit()
        if form.errors == {}:
            flash(f'Success! You are signed up as: {customer.name}', category='success')
        return redirect(url_for('login_customer'))
        
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return render_template('signup_customer.html', form = form)


@app.route('/login_customer', methods = ['GET', 'POST'])
def login_customer():
    form = loginCustomer()
    if form.validate_on_submit():
        attempted_customer = Customer.query.filter_by(email = form.email.data).first()
        if attempted_customer and attempted_customer.check_password_correction(form.password.data):
            session['customer'] = (attempted_customer)
            session['name'] = attempted_customer.name
            login_user(attempted_customer)
            flash(f'Success! You are logged in as: {attempted_customer.name}', category='success')
            return redirect(url_for('customer_actions'))
        else:
            flash('Invalid email or password! Please try again', category='danger')
    return render_template('login_customer.html', form = form)

@app.route('/manager_actions')
def manager_actions():
    return render_template('manager_actions.html')

@app.route('/manager_actions2', methods = ['GET', 'POST'])
def manager_actions2():
    form2 = viewTruckStatus()
    form3 = branchConsignmentDetails()
    if  "form2-submit" in request.form:
        if form2.validate_on_submit():
            truck = Truck.query.filter_by(truckID = form2.truckID.data).first()
            session['truck'] = truck
            return redirect(url_for('view_truck_status'))
    if form2.errors != {}:
        for err_msg in form2.errors.values():
            flash(err_msg, category='danger')

    if "form3-submit" in request.form:
        if form3.validate_on_submit():
            office = Office.query.filter_by(officeID = form3.branchID.data).first()
            session['office'] = office
            return redirect(url_for('branch_consignment_details'))
    return render_template('manager_actions2.html', form2 = form2, form3 = form3)

@app.route('/branch_consignment_details', methods = ['GET', 'POST'])
def branch_consignment_details():
    sent = Consignment.query.filter_by(sourceOfficeID = session['office'].officeID).all()
    received = Consignment.query.filter_by(destinationOfficeID = session['office'].officeID).all()
    return render_template('view_branch_consignment_details.html', sent = sent, received = received)

@app.route('/view_bill', methods = ['GET', 'POST'])
def view_bill():
    return render_template('view_bill2.html')

@app.route('/view_truck_status')
def view_truck_status():
    list = Consignment.query.filter_by(truckAssigned = session['truck'].truckID).all()
    return render_template('view_truck_status.html',list = list)

@app.route('/employee_actions')
def employee_actions():
    return render_template('employee_actions.html')

@app.route('/customer_actions', methods = ['GET', 'POST'])
def customer_actions():
    form1 = viewBill()
    form2 = trackConsignment()
    if  "form-submit" in request.form:
        if form1.validate_on_submit():
            consignment = Consignment.query.filter_by(consignmentID = form1.consignmentID.data).first()
            session['consignment'] = consignment
            return redirect(url_for('view_bill'))
        if form1.errors != {}:
            for err_msg in form1.errors.values():
                flash(err_msg, category='danger')  
    elif "form2-submit" in request.form:
        if form2.validate_on_submit():
            consignment = Consignment.query.filter_by(consignmentID = form2.consignmentID.data).first()
            session['consignment'] = consignment
            # print(2)
            # return render_template('customer_actions.html', form1=form1, form2 = form2, show_modal = True)
            return redirect(url_for('track_consignment'))
        if form2.errors != {}:
            for err_msg in form2.errors.values():
                flash(err_msg, category='danger')
    
    return render_template('customer_actions.html', form1 = form1, form2=form2)

@app.route('/create_employee', methods = ['GET', 'POST'])
def create_employee():
    form = createEmployee()
    if form.validate_on_submit():
        employee = Employee(employeeID = 1+len(Employee.query.all()), name = form.name.data,
                            address = form.address.data, phoneNumber = form.phoneNumber.data, 
                            branchID = form.branchID.data,
                            email = form.email.data, password = form.password1.data)
        Office.query.filter_by(officeID = form.branchID.data).first().numEmployees += 1
        db.session.add(employee)
        db.session.commit()
        if form.errors == {}:
            flash(f'Success! You successfully added employee as: {employee.name}', category='success')
        return redirect(url_for('manager_actions2'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    
    return render_template('create_employee.html', form = form)

@app.route('/create_branch', methods = ['GET', 'POST'])
def create_branch():
    form = createOffice()
    if form.validate_on_submit():
        office = Office(officeID = form.officeID.data, address = form.address.data, 
                        phoneNumber = form.phoneNumber.data, numTrucks = 0, numEmployees = 0, 
                        volumeHandled = 0, revenue = 0, idleWaitingTime = 0, rate = form.rate.data)
        db.session.add(office)
        db.session.commit()
        if form.errors == {}:
            flash(f'Success! You successfully added Branch: {office.officeID}', category='success')
        return redirect(url_for('manager_actions2'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    
    return render_template('create_branch.html', form = form)

@app.route('/add_truck', methods = ['GET', 'POST'])
def add_truck():
    form = addTruck()
    if form.validate_on_submit():
        truck = Truck(truckID = form.truckID.data, currentBranchID = form.currentBranchID.data, prevDispatchDate = datetime.datetime.now())
        Office.query.filter_by(officeID = form.currentBranchID.data).first().numTrucks += 1
        db.session.add(truck)
        db.session.commit()
        allot_truck(form.currentBranchID.data)
        if form.errors == {}:
            flash(f'Success! You successfully added Truck: {truck.truckID}', category='success')
        return redirect(url_for('manager_actions2'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')    
    return render_template('add_truck.html', form = form)

@app.route('/view_branch_truck_details', methods = ['GET', 'POST'])
def view_branch_truck_details():
    trucks = Truck.query.filter_by(currentBranchID = session['employee'].branchID).all()
    return render_template('view_branch_truck_details.html', trucks = trucks)

@app.route('/view_branch_consignment_details', methods = ['GET', 'POST'])
def view_branch_consignment_details():
    sent = Consignment.query.filter_by(sourceOfficeID = session['employee'].branchID).all()
    received = Consignment.query.filter_by(destinationOfficeID = session['employee'].branchID).all()
    return render_template('view_branch_consignment_details.html', sent = sent, received = received)

@app.route('/view_branch_customer_details', methods = ['GET', 'POST'])
def view_branch_customer_details():
    customers = Customer.query.filter_by(branchID = session['employee'].branchID).all()
    return render_template('view_branch_customer_details.html', customers = customers)

@app.route('/place_order', methods = ['GET', 'POST'])
def place_order():
    form = placeOrder()
    if form.validate_on_submit():
        destinationofficeID = Customer.query.filter_by(customerID = form.receiverID.data).first().branchID
        destinationAddr = Customer.query.filter_by(customerID = form.receiverID.data).first().address
        sourceofficeID = Customer.query.filter_by(customerID = form.senderID.data).first().branchID
        sourceAddr = Customer.query.filter_by(customerID = form.senderID.data).first().address
        consignment = Consignment(consignmentID = 1+len(Consignment.query.all()), senderID = form.senderID.data,
                                  receiverID = form.receiverID.data,destinationOfficeID = destinationofficeID, 
                                  destinationAddress = destinationAddr, sourceAddress = sourceAddr, purchaseDate = datetime.datetime.now(),
                                  deliveryDate = datetime.datetime.now(),sourceOfficeID = sourceofficeID, volume = form.volume.data)
        sender = Customer.query.filter_by(customerID = form.senderID.data).first()
        sender.consignments += ("S"+str(consignment.consignmentID))
        receiver = Customer.query.filter_by(customerID = form.receiverID.data).first()
        receiver.consignments += ("R"+str(consignment.consignmentID))
        sourceoffice = Office.query.filter_by(officeID = sourceofficeID).first()
        sourceoffice.presentVolume += consignment.volume
        consignment.revenue = consignment.volume * sourceoffice.rate
        sourceoffice.total_orders += ("S"+str(consignment.consignmentID))
        sourceoffice.revenue += consignment.revenue
        destinationoffice = Office.query.filter_by(officeID = destinationofficeID).first()
        destinationoffice.total_orders += ("R"+str(consignment.consignmentID))
        db.session.add(consignment)
        db.session.commit()
        # addedconsignment = Consignment.query.filter_by(consignmentID = consignment.consignmentID).first()
        if destinationofficeID in sourceoffice.order_map.keys():
            sourceoffice.order_map[destinationofficeID].append(consignment.consignmentID)
        else:
            sourceoffice.order_map[destinationofficeID] = [consignment.consignmentID]
        if destinationofficeID in sourceoffice.volume_map.keys():
            sourceoffice.volume_map[destinationofficeID] += consignment.volume
        else:
            sourceoffice.volume_map[destinationofficeID] = consignment.volume
        db.session.commit()
        
        allot_truck(sourceofficeID)
        db.session.commit()
        if form.errors == {}:
            flash(f'Success! You succressfully added Consignment: {consignment.consignmentID}', category='success')
            return redirect(url_for('customer_actions'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')    
    return render_template('place_order.html', form = form)

def allot_truck(sourceofficeID):
        
    sourceoffice = Office.query.filter_by(officeID = sourceofficeID).first()
    print(sourceoffice.volume_map.keys())
    print(sourceoffice.order_map.keys())
    # sourceoffice.volume_map.pop(3)
    # done = 0
    poplist = []
    for destinationid,totalvolume in sourceoffice.volume_map.items():
        truck = Truck.query.filter_by(currentBranchID = sourceofficeID).first()
        
        if truck:
            if totalvolume>=500:
                print(sourceoffice.order_map)
                for orderid in sourceoffice.order_map[destinationid]:
                    order = Consignment.query.filter_by(consignmentID = orderid).first()
                    order.status = "delivered"
                    order.deliveryDate = datetime.datetime.now()
                    order.truckAssigned = truck.truckID
                    truck.numConsignments += 1
                    truck.waitingTime += (datetime.datetime.now() - truck.prevDispatchDate).total_seconds()
                    truck.prevDispatchDate = datetime.datetime.now()
                    truck.currentBranchID = destinationid 
                    sourceoffice.volumeHandled += order.volume
                    sourceoffice.presentVolume -= order.volume
                    db.session.commit()
                sourceoffice.numTrucks -= 1
                Office.query.filter_by(officeID = destinationid).first().numTrucks += 1
                db.session.commit()
                poplist.append(destinationid)
                # sourceoffice.order_map.pop(destinationid)
                # sourceoffice.volume_map.pop(destinationid)
    for destinationid in poplist:
        sourceoffice.order_map.pop(destinationid)
        sourceoffice.volume_map.pop(destinationid)
    
    db.session.commit()
    
    return 


@app.route('/customer_orders_history', methods = ['GET', 'POST'])
def customer_orders_history():
    # session['customer'] = Customer.query.filter_by(customerID = session['customer'].customerID).first()
    sent_idx = []
    recv_idx = []
    
    l = len(session['customer'].consignments)
    i=0
    while(i<l):
        if session['customer'].consignments[i] == "S":
            idx = ""
            i+=1
            while i<l and session['customer'].consignments[i] != "R" and session['customer'].consignments[i] != "S":
                idx += session['customer'].consignments[i]
                i += 1
            sent_idx.append(int(idx))
        elif session['customer'].consignments[i] == "R":
            idx = ""
            i += 1
            while i<l and session['customer'].consignments[i] != "R" and session['customer'].consignments[i] != "S":
                idx += session['customer'].consignments[i]
                i += 1
            recv_idx.append(int(idx))
    sent = []
    recv = []
    for i in sent_idx:
        sent.append(Consignment.query.filter_by(consignmentID = i).first())
    for i in recv_idx:
        recv.append(Consignment.query.filter_by(consignmentID = i).first())
    return render_template('customer_orders_history.html', sent = sent, recv = recv)

@app.route('/track_consignment', methods = ['GET', 'POST'])
def track_consignment():
    return render_template('track_consignment.html')

@app.route('/view_branch_details', methods = ['GET', 'POST'])
def view_branch_details():
    offices = Office.query.all()
    print(len(offices))
    return render_template('view_branch_details.html', offices=offices)

@app.route('/idle_waiting_time_consignment', methods = ['GET', 'POST'])
def idle_waiting_time_consignment():
    consignments = Consignment.query.filter_by(status = "delivered").all()
    idle_waiting_time = 0
    for c in consignments:
        idle_waiting_time += (c.deliveryDate - c.purchaseDate).total_seconds()
    branchID = []
    avgTime = []
    consignments_count = []
    for b in Office.query.all():
        consignmentS = Consignment.query.filter_by(status = "delivered", destinationOfficeID = b.officeID).all()
        idle_waiting_timE = 0
        for C in consignmentS:
            idle_waiting_timE += (C.deliveryDate - C.purchaseDate).total_seconds()
        if len(consignmentS) > 0:
            branchID.append(b.officeID)
            avgTime.append(idle_waiting_timE/len(consignmentS))
            consignments_count.append(len(consignmentS))
#     fig = px.bar(x=branchID, y=avgTime,color_discrete_sequence =['red']*len(avgTime))
#     fig.update_layout(dict(
#   title='Branch Id vs Avg Consignment Delivery Time',
#   xaxis=dict(
#     title=dict(
#       text='Branch Id'
#     )
#   ),
#   yaxis=dict(
#     title=dict(
#       text='Average Time'
#     )
#   )
# ))
#     fig.write_image("./Teleport/static/images/new_plot.png")
    
    print(idle_waiting_time)
    datedic = {}
    length = len(consignments)
    idle_waiting_time //= length
    datedic["year"] = idle_waiting_time//(365*24*60*60)
    datedic["month"] = (idle_waiting_time//(30*24*60*60))%12
    datedic["day"] =   (idle_waiting_time//(24*60*60))%30
    datedic["hour"] = (idle_waiting_time//(60*60))%24
    datedic["minute"] = (idle_waiting_time//60)%60
    datedic["second"] = idle_waiting_time%60
    time_list= []
    for time in avgTime:
        dic = {}
        dic["year"] = time//(365*24*60*60)
        dic["month"] = (time//(30*24*60*60))%12
        dic["day"] =   (time//(24*60*60))%30
        dic["hour"] = (time//(60*60))%24
        dic["minute"] = (time//60)%60
        dic["second"] = time%60
        time_list.append(dic)
    for i in range(len(time_list)):
        time_list[i]["ID"] = branchID[i]
        time_list[i]["count"] = consignments_count[i]
    # idle_waiting_time /= len(consignments)
    return render_template('idle_time_consignment.html',datedic = datedic,time_list= time_list)

@app.route('/idle_truck_waiting_time', methods=["GET", "POST"])
def idle_truck_waiting_time():
    trucks = Truck.query.all()
    total_consignments = 0
    idle_waiting_time = 0
    truckS = []
    truckS_consignments = []
    avgTime = []
    for t in trucks:
        if (t.numConsignments) > 0:
            truckS.append(t.truckID)
            avgTime.append(t.waitingTime/t.numConsignments)
            truckS_consignments.append(t.numConsignments)
        idle_waiting_time += t.waitingTime
        total_consignments += t.numConsignments
        
    # print(idle_waiting_time)
#     fig = px.bar(x=truckS, y=avgTime,color_discrete_sequence =['red']*len(avgTime))
#     fig.update_layout(dict(
#   title='Truck Id vs Avg Truck Idle Time',
#   xaxis=dict(
#     title=dict(
#       text='Truck Id'
#     )
#   ),
#   yaxis=dict(
#     title=dict(
#       text='Average Time'
#     )
#   )
# ))
    # fig.write_image("./Teleport/static/images/new_plot2.png")
    datedic = {}
    idle_waiting_time //= total_consignments
    datedic["year"] = idle_waiting_time//(365*24*60*60)
    datedic["month"] = (idle_waiting_time//(30*24*60*60))%12
    datedic["day"] =   (idle_waiting_time//(24*60*60))%30
    datedic["hour"] = (idle_waiting_time//(60*60))%24
    datedic["minute"] = (idle_waiting_time//60)%60
    datedic["second"] = idle_waiting_time%60
    time_list= []
    for time in avgTime:
        dic = {}
        dic["year"] = time//(365*24*60*60)
        dic["month"] = (time//(30*24*60*60))%12
        dic["day"] =   (time//(24*60*60))%30
        dic["hour"] = (time//(60*60))%24
        dic["minute"] = (time//60)%60
        dic["second"] = time%60
        time_list.append(dic)
    for i in range(len(time_list)):
        # time_list[i]["AvgTime"] = avgTime[i]
        time_list[i]["ID"] = truckS[i]
        time_list[i]["count"] = truckS_consignments[i]
    # idle_waiting_time /= len(consignments)
    return render_template('idle_time_truck.html',datedic = datedic,time_list = time_list)
