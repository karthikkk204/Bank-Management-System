#flash is for mesages
import time
from tokenize import Double
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL,MySQLdb

from flask_login import UserMixin
# for encription and dicreption 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_manager,LoginManager
from flask_login import login_required, current_user
from flask_mail import Mail

# importing pandas module
import pandas as pd
from datetime import datetime
from decimal import Decimal
from flask import make_response, Response
import pdfkit
import mysql.connector
from datetime import date
import json
import smtplib
from flask_redmail import RedMail
import amount_in_words
import util

params = ""
with open('config.json', 'r') as fp:
    params = json.load(fp)["params"]

deleteSelectedFlag = 0;

def deleteAll():
    deleteSelectedFlag = 1

# we have to set the local server (Db connection)
local_server=True
# initialise the app
app = Flask(__name__)
# we can give scret key
app.secret_key = "chitti"

#SMTP (Simple Mail Transfer protocall)  MAIL SERVER SETTINGS
"""
app.config.update (
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT="465",
    MAIL_USER_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
"""

# config this app to flask mail
#mail = Mail(app)

from email.mime.text import MIMEText
import smtplib
def send_email(subject, message, posts,to_mail):
    from_email="chitti.chindirala@gmail.com"
    from_passwd = "tmrovzjoxkxooqdo"
    #to_email=posts.unitemail + ",nrcreddyblr@gmail.com"
    if(to_mail == "forconfirmation"):
        to_email=posts.bankemailid + posts.zonalofficemail
    else:
        to_email=posts.unitemail + posts.bankemailid
    subject=subject
    message = message

    msg = MIMEText(message, "html")
    #print(type(msg))
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = "no-reply@gmail.com"
    #port number = 587
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_passwd)
    gmail.send_message(msg)

#send_email()
"""
app.config["EMAIL_HOST"] = "smtp.gmail.com"
app.config["EMAIL_PORT"] = 587

app.config["EMAIL_USERNAME"] = params['gmail-user']
app.config["EMAIL_PASSWORD"] = "tmrovzjoxkxooqdo"

app.config["EMAIL_SENDER"] = "chitti.chindirala@gmail.com"

email = RedMail(app)
"""
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bms'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysqlGlobal = MySQL(app)



#this is for getting unique user access
login_manager = LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# we have to configure our database what we created in MySql Dabase, through xampp ->mySql->admin
#app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql://username:password@localhost/databse_table_name'
#while installing xampp, you have not given user name and a password, by default
# for all people username is root, say no passwd given then remove the passwd name in the above line
# and we creted databse name as hms (hospital management system) in the databse_table_name , we have to give that

# this way we have to initialize the databse and its url
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bms'
# now we have create DB instance by giveing the app
db=SQLAlchemy(app)


#here we have to create db models that is table using class
# why we gave Test, is our table name in Database, we always give first leter capital
# we have to crete Models in main.py for all the tables which we have created in through MySql admin
# We have to give the table name which is created in DB , in with First letter is Capital in Main.py
# signup form
class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(1000))

# Unit registeration form
# the parameter nullable=False means the field is manadatory before storing it into DB
class Bankguarantee(db.Model):
   sid=db.Column(db.Integer, primary_key=True)
   unitname=db.Column(db.String(50))
   unitemail=db.Column(db.String(50))
   gender=db.Column(db.String(10))
   unitaddress=db.Column(db.String(6000))
   unitnumber=db.Column(db.String(12))
   bankheadname=db.Column(db.String(50))
   bankname=db.Column(db.String(50))
   bankemailid=db.Column(db.String(50))
   bankphonenumber=db.Column(db.String(20))
   bankaddress=db.Column(db.String(6000))
   bgnumber=db.Column(db.String(20))
   bgdate=db.Column(db.String(50))
   stampnumber=db.Column(db.String(20))
   validperiod=db.Column(db.String(20))
   claimperiod=db.Column(db.String(20))
   amount=db.Column(db.DECIMAL(20,2))
   accountnumber=db.Column(db.String(20))
   securityvalue=db.Column(db.DECIMAL(20,2))
   submitdate=db.Column(db.String(50))
   renewaldate=db.Column(db.String(50))
   claimamount=db.Column(db.DECIMAL(20,2))
   zonalbankname=db.Column(db.String(50))
   zonalofficemail=db.Column(db.String(75))
   zocontactprsnname=db.Column(db.String(50))
   zophonenumber=db.Column(db.String(50))
   zoaddress=db.Column(db.String(600))
   renewalprocessed=db.Column(db.String(10))
   zoprocessed=db.Column(db.String(10))
  

# patinets registeration form
# the parameter nullable=False means the field is manadatory before storing it into DB
class Units(db.Model):
   uid=db.Column(db.Integer, primary_key=True)
   email=db.Column(db.String(50))
   name=db.Column(db.String(50))
   gender=db.Column(db.String(50))
   slot=db.Column(db.String(50))
   time=db.Column(db.String(50),nullable=False)
   date=db.Column(db.String(50),nullable=False)
   disease=db.Column(db.String(50))
   dept=db.Column(db.String(50))
   number=db.Column(db.String(50))

class Triger(db.Model):
    tid=db.Column(db.Integer, primary_key=True)
    pid=db.Column(db.Integer)
    email=db.Column(db.String(50), unique=True)
    name=db.Column(db.String(50))
    action=db.Column(db.String(50))
    timestamp=db.Column(db.String(50))

@app.route("/tables", methods=['POST'])
def table():
    # converting csv to html
    global file
    if request.method == "POST":
        file=request.files["file"]
        #print(file)
        fileName = file.filename
        data = pd.read_csv(fileName)
        with open(fileName) as fp:
            first = True
            for line in fp.readlines():
                unit_list = []
                bank_list = []
                bg_list = []
                other_list = []
                security_val = 0.0
                submission_date = ""
                renewal_date = ""
                claim_upto = 0.0
                amount = 0.0
                if first:
                    first = False
                else:
                    values = line.split("\"")
                    #print(values)
                    index = 1
                    for value in values:
                        if(len(value.strip()) <= 1):
                            continue
                        if(index == 1):
                            unit_list = value.split(",")
                        elif(index == 2):
                            bank_list = value.split(",")
                        elif(index == 3):
                            bg_list = value.split(",")
                        elif(index == 4):
                            other_list = value.split(",")
                        index = index + 1
                '''
                print(unit_list)
                print(bank_list)
                print(bg_list)
                print(other_list)
                '''                
                if(len(unit_list) == 0):
                    continue
                if(len(unit_list[4:]) > 0):
                    changed_list = str(unit_list[4:]).replace("[","").replace("]","")
                    changed_list = changed_list.replace("'","")
                if(len(bank_list[1:]) > 0):
                    changed_bank_list = str(bank_list[1:]).replace("[","").replace("]","")
                    changed_bank_list = changed_bank_list.replace("'","")
                if(len(bg_list[1]) > 0):
                    bg_date_object = datetime.strptime(bg_list[1], '%d-%m-%Y').date()
                if(len(bg_list[4]) > 0):
                    amount = float(bg_list[4])
                if(len(other_list[1]) > 0):
                    security_val = float(other_list[1])
                if(len(other_list[2]) > 0):
                    submit_date_object = datetime.strptime(other_list[2], '%d-%m-%Y').date()
                if(len(other_list[3]) > 0):
                    renewal_date_object = datetime.strptime(other_list[3], '%d-%m-%Y').date()
                if(len(other_list[4]) > 0):
                    claim_upto = float(other_list[4])
                query=db.engine.execute(f"INSERT INTO `bankguarantee` (`unitname`,`unitemail`,`gender`,`unitnumber`,`unitaddress`,`bankname`,`bankaddress`,`bgnumber`,`bgdate`,`stampnumber`,`validperiod`,`amount`,`securityvalue`,`submitdate`,`renewaldate`,`claimamount`) VALUES('{unit_list[0]}','{unit_list[1]}','{unit_list[2]}','{unit_list[3]}','{changed_list}','{bank_list[0]}','{changed_bank_list}','{bg_list[0]}','{bg_date_object}', '{bg_list[2]}','{bg_list[3]}','{amount}','{security_val}','{submit_date_object}','{renewal_date_object}','{claim_upto}')")

        #print(data)
        #print(type(data))
        return render_template('tables.html', tables=[data.to_html()], titles=[''])
    
@app.route("/", methods=['POST','GET'])
@login_required
def home():
    return render_template('home.html')
@app.route("/importfile_1", methods=['POST','GET'])
@login_required
def importfileNew():
    import math
    global file
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    if request.method == "POST":
        cursor = connection.cursor()
        file=request.files["file"]
        #print(file)
        fileName = file.filename
        #data = pd.read_csv(fileName)
        #print(data)
        with open(fileName) as fp:
            first = True
            dframe = amount_in_words.readXls(fileName)
            #for row in range(0, data.max_row):
            #data.fillna('', inplace=True)
            
            """
            dframe = data.dropna()
            dframe = data.dropna(axis=0)
            dframe = data.dropna().reset_index(drop=True)
            """
            dframe['Address'] = dframe['Address'].fillna('')
            dframe['Zonal'] = dframe['Zonal'].fillna('')
            dframe['Branch'] = dframe['Branch'].fillna('')
            dframe.dropna(inplace=True)
            dframe.dropna().reset_index(drop=True)
            num_rows = len(dframe['S.No.'].tolist())
            #print(num_rows)
            for row in range(num_rows):
                #print(row)
                try:
                    unitname = dframe['Name of the Unit'][row]
                    unitaddress = dframe['Address'][row]
                    bankname = dframe['Bank Name'][row]
                    bankaddress = dframe['Branch'][row]
                    bankaddress = bankaddress.replace('\n', ' ').replace('\r', '')
                    bgnumber = dframe['BG Description'][row]
                    flag = math.isnan(float(dframe["BG Value"][row]))
                    if(flag == False):
                        amount = float(dframe['BG Value'][row])
                    #bgdate = dframe['BG Date'][row]
                    bgdate = datetime.strftime(dframe['BG Date'][row], '%d-%m-%Y')
                    #validperiod = dframe["BG Valid Upto"][row]
                    validperiod = datetime.strftime(dframe["BG Valid Upto"][row], '%d-%m-%Y')
                    claimamount = 0.0
                    
                    flag = math.isnan(float(dframe["Limit Sanctioned"][row]))
                    if(flag == False):
                        claimamount = float(dframe["Limit Sanctioned"][row])
                    
                    #claimperiod = data["Limit Valid Upto"][row]
                    claimperiod = ""
                    try:
                        claimperiod = datetime.strftime(dframe["Limit Valid Upto"][row], '%d-%m-%Y')
                    except:
                        claimperiod = ""
                    print('unitname', unitname)
                    print('unitname', type(unitname))
                    print('unitaddress', unitaddress)
                    print('unitaddress', type(unitaddress))
                    print('bankname', bankname)
                    print('bankname', type(bankname))
                    print('bankaddress', bankaddress)
                    print('bankaddress', type(bankaddress))
                    print('bgnumber', bgnumber)
                    print('bgnumber', type(bgnumber))
                    print('amount', amount)
                    print('amount', type(amount))
                    print('bgdate', bgdate)
                    print('bgdate', type(bgdate))
                    print('validperiod', validperiod)
                    print('validperiod', type(validperiod))
                    print('claimamount', claimamount)
                    print('claimamount', type(claimamount))
                    print('claimperiod', claimperiod)
                    print('claimperiod', type(claimperiod))
                    unitemail = ""
                    gender = ""
                    unitnumber = ""
                    bankheadname = ""
                    bankemailid = ""
                    bankphonenumber = ""
                    stampnumber = ""
                    accountnumber = ""
                    submitdate = bgdate
                    renewaldate = validperiod
                    securityvalue = ""
                    zonal_details = dframe["Zonal"][row]
                    print('zonal_details', zonal_details)
                    zonal_details = zonal_details.replace('\n', ' ').replace('\r', '')
                    zobankname = zonal_details.split(",")[0]
                    print('zobankname', zobankname)
                    zobankemail = ""
                    zocontactperson = ""
                    zocontacthpone = ""
                    temp_address = zonal_details.split(",")[1:]
                    temp_address = [item.strip() for item in temp_address]
                    zonal_office_address =",".join(temp_address)
                    print('zonal_office_address', zonal_office_address)
                    isrenewed = "No"
                    iszorenewed = "No"
                    query= """INSERT INTO bankguarantee (unitname,unitemail,gender,unitnumber,unitaddress,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,claimamount,zonalbankname,zonalofficemail,zocontactprsnname,zophonenumber,zoaddress,renewalprocessed,zoprocessed) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    input_data = (unitname,unitemail,gender,unitnumber,unitaddress,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,claimamount,zobankname,zobankemail,zocontactperson,zocontacthpone,zonal_office_address,isrenewed,iszorenewed)
                    cursor.execute(query, input_data)
                    connection.commit()
                except:
                    pass
            cursor.close()
            connection.close()
            return redirect('/bgrenewal')
    return render_template('importfile.html')
@app.route("/importfile", methods=['POST','GET'])
@login_required
def importfile():
    global file
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    if request.method == "POST":
        cursor = connection.cursor()
        file=request.files["file"]
        #print(file)
        fileName = file.filename
        #data = pd.read_csv(fileName)
        #print(data)
        #pass
        with open(fileName) as fp:
            first = True
            for line in fp.readlines():
                #print(line)
                #pass
                unit_list = []
                bank_list = []
                bg_list = []
                other_list = []
                zo_address_list = []
                renewal_list = []
                changed_zo_address_list = ""
                changed_renewal_list_str = ""
                changed_renewal_list = []
                security_val = 0.0
                submission_date = ""
                renewal_date = ""
                claim_upto = 0.0
                amount = 0.0
                isrenewed = "No"
                iszorenewed = "No"
                zobankname = ""
                zobankemail = ""
                zocontactperson = ""
                zocontacthpone = ""
                if first:
                    first = False
                else:
                    values = line.split("\"")
                    #print(values)
                    index = 1
                    for value in values:
                        if(len(value.strip()) <= 1):
                            continue
                        if(index == 1):
                            unit_list = value.split(",")
                        elif(index == 2):
                            bank_list = value.split(",")
                        elif(index == 3):
                            bg_list = value.split(",")
                        elif(index == 4):
                            other_list = value.split(",")
                        elif(index == 5):
                            zo_address_list = value.split(",")
                        elif(index == 6):
                            renewal_list = value.split(",")
                        
                        index = index + 1
                
                #print(unit_list)
                #print(bank_list)
                # print(bg_list)
                # print(other_list)
                # print(zo_address_list)
                # print(renewal_list)
                """
                if(len(zo_address_list) > 0):
                    changed_zo_address_list = str(zo_address_list).replace("[","").replace("]","")
                    changed_zo_address_list = changed_zo_address_list.replace("'","")
                """
                if(len(renewal_list) > 0):
                    changed_renewal_list_str = str(renewal_list).replace("[","").replace("]","")
                    changed_renewal_list_str = changed_renewal_list_str.replace("'","")
                    changed_renewal_list = changed_renewal_list_str.split(",")
                """
                # print(changed_zo_address_list)
                # print(type(changed_zo_address_list))
                # print(changed_renewal_list_str)
                # print(type(changed_renewal_list_str))
                # print(changed_renewal_list)
                """
                if(len(unit_list) == 0):
                    continue
                if(len(unit_list[4:]) > 0):
                    changed_list = str(unit_list[4:]).replace("[","").replace("]","")
                    changed_list = changed_list.replace("'","")
                if(len(bank_list[4:]) > 0):
                    #print(bank_list)
                    changed_bank_list = str(bank_list[4:]).replace("[","").replace("]","")
                    changed_bank_list = changed_bank_list.replace("'","")
                if(len(bg_list[1]) > 0):
                    #bg_date_object = datetime.strptime(bg_list[1], '%d-%m-%Y').date()
                    bg_date_object = bg_list[1]
                if(len(bg_list[3]) > 0):
                    #validperiod = datetime.strptime(bg_list[3], '%d-%m-%Y').date()
                    validperiod = bg_list[3]
                if(len(bg_list[4]) > 0):
                    #claimperiod = datetime.strptime(bg_list[4], '%d-%m-%Y').date()
                    claimperiod = bg_list[4]
                if(len(bg_list[5]) > 0):
                    amount = float(bg_list[5])
                if(len(other_list[1]) > 0):
                    security_val = float(other_list[1])
                if(len(other_list[2]) > 0):
                    #submit_date_object = datetime.strptime(other_list[2], '%d-%m-%Y').date()
                    submit_date_object = other_list[2]
                if(len(other_list[3]) > 0):
                    #renewal_date_object = datetime.strptime(other_list[3], '%d-%m-%Y').date()
                    renewal_date_object = other_list[3]
                if(len(other_list[4]) > 0):
                    claim_upto = float(other_list[4])
                if(len(zo_address_list[0]) > 0):
                    zobankname = zo_address_list[0]
                if(len(zo_address_list[1]) > 0):
                    zobankemail = zo_address_list[1]
                if(len(zo_address_list[2]) > 0):
                    zocontactperson = zo_address_list[2]
                if(len(zo_address_list[3]) > 0):
                    zocontacthpone = zo_address_list[3]
                if(len(zo_address_list[4:]) > 0):
                    changed_zo_address_list = str(zo_address_list[4:]).replace("[","").replace("]","")
                    changed_zo_address_list = changed_zo_address_list.replace("'","")
                """
                 if(len(changed_renewal_list) > 0):
                        isrenewed = changed_renewal_list[1].strip()
                    iszorenewed = changed_renewal_list[2].strip('\\n')
                """
                unitname = unit_list[0]
                #print(type(unitname))
                #print(unitname)
                unitemail = unit_list[1]
                gender = unit_list[2]
                unitnumber = unit_list[3]
                bankheadname = bank_list[0]
                bankname = bank_list[1]
                bankemailid = bank_list[3]
                bankphonenumber = bank_list[4]
                bgnumber = bg_list[0]
                stampnumber = bg_list[2]
                validperiod =  bg_list[3]
                claimperiod =  bg_list[4]
                accountnumber = bg_list[6]
                unitaddress = changed_list
                bankaddress = changed_bank_list
                bgdate = bg_date_object
                submitdate = submit_date_object
                renewaldate = renewal_date_object
                securityvalue = security_val
                claimamount = claim_upto
                zonal_office_address = changed_zo_address_list
                query="""INSERT INTO bankguarantee (unitname,unitemail,gender,unitnumber,unitaddress,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,claimamount,zonalbankname,zonalofficemail,zocontactprsnname,zophonenumber,zoaddress,renewalprocessed,zoprocessed) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                input_data = (unitname,unitemail,gender,unitnumber,unitaddress,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,claimamount,zobankname,zobankemail,zocontactperson,zocontacthpone,zonal_office_address,isrenewed,iszorenewed)
                cursor.execute(query, input_data)
                connection.commit()
            cursor.close()
            connection.close()
            return redirect('/bgrenewal')
        #print(data)
        #print(type(data))
    return render_template('importfile.html')

@app.route("/index", methods=['POST','GET'])
@login_required
def index():
    """
    # to test the database
    a = Bankguarantee.query.all()
    print(a)
    """
    #cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    if request.method == "POST":
        unitname=request.form.get('unitname')
        unitemail=request.form.get('unitemail')
        gender=request.form.get('gender')
        unitaddress=request.form.get('unitaddress')
        unitnumber=request.form.get('unitnumber')
        bankheadname=request.form.get('bankheadname')
        bankname=request.form.get('bankname')
        bankemailid=request.form.get('bankemailid')
        bankphonenumber=request.form.get('bankphonenumber')
        bankaddress=request.form.get('bankaddress')
        bgnumber=request.form.get('bgnumber')
        bgdate=request.form.get('bgdate')
        stampnumber=request.form.get('stampnumber')
        validperiod=request.form.get('validperiod')
        claimperiod=request.form.get('claimperiod')
        amount=request.form.get('amount')
        securityvalue=request.form.get('securityvalue')
        submitdate=request.form.get('submitdate')
        renewaldate=request.form.get('renewaldate')
        #claimamount=request.form.get('claimamount')
        zonalbankname=request.form.get('zonalbankname')
        zonalofficemail=request.form.get('zonalofficemail')
        zocontactprsnname=request.form.get('zocontactprsnname')
        zophonenumber=request.form.get('zophonenumber')
        zoaddress=request.form.get('zoaddress')
        accountnumber=request.form.get('accountnumber')
        renewalprocessed = "No"
        zoprocessed = "No"
        """
        print('unitname = ', unitname)
        print('unitemail = ', unitemail)
        print('gender = ', gender)
        print('unitaddress = ', unitaddress)
        print('bankname = ', bankname)
        print('bankaddress = ', bankaddress)
        """
        
        #insert the query into DB
        # every thing should pass under 'f' string like below
        query = """INSERT INTO bankguarantee (unitname,unitaddress,unitemail,gender,unitnumber,bankheadname,bankname,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,zonalbankname,zoaddress,zonalofficemail,zocontactprsnname,zophonenumber,renewalprocessed,zoprocessed) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        input_data = (unitname,unitaddress,unitemail,gender,unitnumber,bankheadname,bankname,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,zonalbankname,zoaddress,zonalofficemail,zocontactprsnname,zophonenumber,renewalprocessed,zoprocessed)
        cursor.execute(query, input_data)
        connection.commit()
        cursor.close()
        connection.close()
        #query=db.engine.execute(f"INSERT INTO `bankguarantee` (`unitname`,`unitemail`,`gender`,`unitnumber`,`unitaddress`,`bankname`,`bankaddress`,`bgnumber`,`bgdate`,`stampnumber`,`validperiod`,`amount`,`securityvalue`,`submitdate`,`renewaldate`,`claimamount`) VALUES('{unitname}','{unitemail}','{gender}','{unitnumber}','{unitaddress}','{bankname}','{bankaddress}','{bgnumber}','{bgdate}', '{stampnumber}','{validperiod}','{amount}','{securityvalue}','{submitdate}','{renewaldate}','{claimamount}')")
        #mail.send_message(subject,sender=params['gmail-user'], recipients=[email],body='YOUR BOOKING IS CONFIRMED, THANKS FOR CHOOSEING US')
        flash("Record added successfully", "success")
        return redirect('/bgrenewal')
    return render_template('index.html')

@app.route("/sendmailforrenewal/<string:sid>")
def sendmailforrenewal(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"zonaladdress",amount_in_words.splitTheAddress(str(posts.zoaddress)))
    html = render_template('export.html', posts=posts)
    send_email("Bank Gaurantee Renewal", html,posts,"forrenewal")
    flash("B.G. Renewal mail sent successfully", "success")
    value = "Yes"
    sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
    input_data = (value,sid)
    util.runSql(sql_query, input_data)
    return redirect('/forrenewal')
@app.route("/sendmail/<string:sid>")
def sendemail(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"zonaladdress",amount_in_words.splitTheAddress(str(posts.zoaddress)))
    html = render_template('branchconfirmletter.html', posts=posts)
    send_email("Bank Gaurantee Renewal", html,posts,"forconfirmation")
    flash("B.G. Renewal mail sent successfully", "success")
    value = "Yes"
    sql_query = """UPDATE bankguarantee SET zoprocessed=%s WHERE sid=%s"""
    input_data = (value,sid)
    util.runSql(sql_query, input_data)
    
    '''
    mail.send(
        subject="Template example",
        receivers=["chitti.chindirala@gmail.com"],
        html_template="branchconfirmletter.html"
    )
    '''
    """
    email.send(
        subject="Template example",
        recipients=["chitti.chindirala@gmail.com"],
        html= " " "
            <h1>Hi,</h1>
            <p>this is an example.</p>
        " " "
    )
    """
    return redirect('/fordatarenewal')
    
@app.route("/units", methods=['POST','GET'])
def units():
    if request.method == "POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')
        #insert the query into DB
        # every thing should pass under 'f' string like below
        query=db.engine.execute(f"INSERT INTO `Units` (`email`,`doctorname`,`dept`) VALUES('{email}','{doctorname}','{dept}')")
        flash("Unit Details Confirmed", "info")
    return render_template('units.html')
    
@app.route("/banks", methods=['POST','GET'])
def Banks():    
    if request.method == "POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')
        #insert the query into DB
        # every thing should pass under 'f' string like below
        query=db.engine.execute(f"INSERT INTO `Banks` (`email`,`doctorname`,`dept`) VALUES('{email}','{doctorname}','{dept}')")
        flash("Bank Details Confirmed", "info")
    return render_template('bank.html')
    
@app.route("/bg", methods=['POST','GET'])
def bg():
    if request.method == "POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')
        #insert the query into DB
        # every thing should pass under 'f' string like below
        query=db.engine.execute(f"INSERT INTO `bg` (`email`,`doctorname`,`dept`) VALUES('{email}','{doctorname}','{dept}')")
        flash("Bank Guarantee Details Confirmed", "info")
    return render_template('bg.html')
@app.route("/zonaloffice", methods=['POST','GET'])
def zonaloffice():
    if request.method == "POST":
        email=request.form.get('email')
        doctorname=request.form.get('doctorname')
        dept=request.form.get('dept')
        #insert the query into DB
        # every thing should pass under 'f' string like below
        query=db.engine.execute(f"INSERT INTO `zonaloffice` (`email`,`doctorname`,`dept`) VALUES('{email}','{doctorname}','{dept}')")
        flash("Bank Guarantee Details Confirmed", "info")
    return render_template('zonaloffice.html')

@app.route("/sentrenewal", methods=['POST','GET'])
#@login_required
def sentrenewal():
    try:
        #cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
        connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
        cursor = connection.cursor()
        if request.method == 'POST':
            field = request.form['field']
            value = request.form['value']
            sid = request.form['id']
            #print(field)
            #print(value)
            #print(sid)
            sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
            input_data = (value,sid)
            cursor.execute(sql_query, input_data)
            connection.commit()
            cursor.close()
            connection.close()
            success = 1
            return redirect('/renewalstatus')
        else:
            temp_query= "SELECT * FROM `bankguarantee`"
            cursor.execute(temp_query)
            query = cursor.fetchall()
            return render_template('renewalstatus.html', query=query)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

@app.route("/bgrenewal")
@login_required
def bgrenewal():
    # to get the patients registration from the current user    
    cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
    temp_query= "SELECT * FROM `bankguarantee`"
    cur.execute(temp_query)
    query = cur.fetchall()
    return render_template('bgrenewal.html', query=query)
@app.route("/forrenewal")
@login_required
def pendingRenewal():
    # to get the patients registration from the current user
    cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
    temp_query= "SELECT * FROM `bankguarantee`"
    cur.execute(temp_query)
    query = cur.fetchall()
    #print(query)
    """
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    temp_query= "SELECT * FROM bankguarantee"
    cursor.execute(temp_query)
    query = cursor.fetchall()
    print(query)
    """
    today_date = date.today()
    #print('today_date =',today_date)
    """
    #year, month, dat = str(today_date).split('-')
    year = today_date.year
    month = today_date.month
    dat = today_date.day
    print('today_date =',today_date)
    cur_date = str(dat) + '-' + str(month) + '-' + str(year);
    cur_date = datetime.strftime(cur_date, '%d-%m-%Y').date()
    print('cur_date =',cur_date)
    """
    #
    filtered_list = []
    for post in query:
        #print(post)
        renewaldate = post['renewaldate']
        if(renewaldate is None):
            continue
        renewaldate = datetime.strptime(renewaldate, '%d-%m-%Y').date()
        #print('renewaldate=',renewaldate)
        #print(type(renewaldate))
        duration = today_date - renewaldate
        num_days = abs(duration.days)
        renewal_processed = post['renewalprocessed']
        #print(renewal_processed)
        #print(num_days)
        if int(num_days) <= 31 and renewal_processed.lower() == 'no':
            filtered_list.append(post)
    query=tuple(filtered_list)
    #print(query)
    return render_template('renewalstatus.html', query=query)
@app.route("/fordatarenewal")
@login_required
def pendingDataRenewal():
    # to get the patients registration from the current user
    cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
    temp_query= "SELECT * FROM `bankguarantee`"
    cur.execute(temp_query)
    query = cur.fetchall()
    #print(query)
    """
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    temp_query= "SELECT * FROM bankguarantee"
    cursor.execute(temp_query)
    query = cursor.fetchall()
    print(query)
    """
    filtered_list = []
    for post in query:
        renewal_processed = post['renewalprocessed']
        zo_processed = post['zoprocessed']
        if renewal_processed.lower() == "yes" and zo_processed.lower() == "no":
            filtered_list.append(post)
    query=tuple(filtered_list)
    #print(query)
    return render_template('finalrenewalstatus.html', query=query)
"""
@app.route("/search",methods=["POST","GET"])
def serach(): 
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    if request.method == 'POST':
        From = request.form['From']
        to = request.form['to']
        print(From)
        print(to)
        query = "SELECT * from orders WHERE purchased_date BETWEEN '{}' AND '{}'".format(From,to)
        cur.execute(query)
        ordersrange = cur.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', ordersrange=ordersrange)})
    """

@app.route("/zoprocessed/<string:sid>", methods=['POST','GET'])
def zoprocessed(sid):
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    value = "Yes"
    sql_query = """UPDATE bankguarantee SET zoprocessed=%s WHERE sid=%s"""
    input_data = (value,sid)
    cursor.execute(sql_query, input_data)
    connection.commit()
    cursor.close()
    connection.close()
    flash("Updated Zonal Office Confirmation Done successfully", "success")
    return redirect('/fordatarenewal')
@app.route("/updatezorenewalstatus", methods=['POST','GET'])
def updateZORenewalStatus():
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    if request.method == "POST":
        li = request.form['data']
        #print(li)
        li = li.split(',')
        li = li[:-1]
        #print(li)
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/fordatarenewal')
        for sid in li:
            value = "Yes"
            sql_query = """UPDATE bankguarantee SET zoprocessed=%s WHERE sid=%s"""
            input_data = (value,sid)
            cursor.execute(sql_query, input_data)
            connection.commit()
        cursor.close()
        connection.close()
        flash("Updated Zonal Office Confirmation Done successfully", "success")
        return redirect('/fordatarenewal')
    return redirect('/fordatarenewal')
@app.route("/updateRenewalConfirm/<string:sid>", methods=['POST','GET'])
def updateRenewalConfirm(sid):
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    value = "Yes"
    sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
    input_data = (value,sid)
    cursor.execute(sql_query, input_data)
    connection.commit()
    cursor.close()
    connection.close()
    flash("Updated Confirmation Done successfully", "success")
    return redirect('/forrenewal')
@app.route("/updaterenewalstatus", methods=['POST','GET'])
def updateRenewalStatus():
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    print(request.method)
    if request.method == "POST":
        li = request.form['data']
        print(li)
        li = li.split(',')
        li = li[:-1]
        print(li)
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/forrenewal')
        for sid in li:
            value = "Yes"
            sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
            input_data = (value,sid)
            cursor.execute(sql_query, input_data)
            connection.commit()
        cursor.close()
        connection.close()
        flash("Updated Confirmation Done successfully", "success")
        return redirect('/forrenewal')
    return redirect('/forrenewal')

@app.route("/printselected", methods=['POST','GET'])
def printselected():
    if request.method == "POST":
        """
        sid = request.form['data']
        print(sid)
        print(type(sid))
        """
        li = request.form['data']
        print(li)
        li = li.split(',')
        #li = li[:-1]
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/forrenewal')
        for sid in li:
            posts=Bankguarantee.query.filter_by(sid=int(sid)).first()
            setattr(posts,"currentdate",str(date.today()))
            setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
            
            #html = render_template('export.html', posts=posts)
            html = "<p>test</p>"
            options = {
            "orientation": "landscape",
            "page-size": "A4",
            "margin-top": "1.0cm",
            "margin-right": "1.0cm",
            "margin-bottom": "1.0cm",
            "margin-left": "1.0cm",
            "encoding": "UTF-8",
            "disable-local-file-access": None,
            "enable-local-file-access": None,
            "print-media-type": None
            }
            # Build PDF from HTML 
            unitName = posts.unitname + ".pdf"
            print(unitName)
            value = "attachment;filename="+unitName
            pdf = pdfkit.from_string(html, options=options)
            # Download the PDF
            headers = {"Content-Disposition": value}
            #time.sleep(2)
            return Response(pdf, mimetype="application/pdf", headers=headers)
            
        
    return redirect('/forrenewal')
@app.route("/sendconfirmmailselected", methods=['POST','GET'])
def sendconfirmmailselected():
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    if request.method == "POST":
        li = request.form['data']
        print(li)
        li = li.split(',')
        li = li[:-1]
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/forrenewal')
        for sid in li:
            posts=Bankguarantee.query.filter_by(sid=int(sid)).first()
            setattr(posts,"currentdate",str(date.today()))
            setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
            html = render_template('branchconfirmletter.html', posts=posts)
            send_email("Bank Gaurantee Renewal", html, posts,"forconfirmation")
            value = "Yes"
            sql_query = """UPDATE bankguarantee SET zoprocessed=%s WHERE sid=%s"""
            input_data = (value,sid)
            util.runSql(sql_query, input_data)
        flash("B.G. Renewal mails sent successfully", "success")
        return redirect('/fordatarenewal')
    
    return redirect('/fordatarenewal')
@app.route("/sendmailselected", methods=['POST','GET'])
def sendmailselected():
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()
    if request.method == "POST":
        li = request.form['data']
        print(li)
        li = li.split(',')
        li = li[:-1]
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/forrenewal')
        for sid in li:
            posts=Bankguarantee.query.filter_by(sid=int(sid)).first()
            setattr(posts,"currentdate",str(date.today()))
            setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
            html = render_template('export.html', posts=posts)
            send_email("Bank Gaurantee Renewal", html, posts,"forrenewal")
            value = "Yes"
            sql_query = """UPDATE bankguarantee SET renewalprocessed=%s WHERE sid=%s"""
            input_data = (value,sid)
            util.runSql(sql_query, input_data)
        flash("B.G. Renewal mails sent successfully", "success")
        return redirect('/forrenewal')
    
    return redirect('/forrenewal')

# presently deleting selected records
@app.route("/deleteselected", methods=['POST','GET'])
def deleteselected():
    
    connection = mysql.connector.connect(host='localhost',
                                            database='bms',
                                            user='root',
                                        password='')
    cursor = connection.cursor()  
    #print("I am in deleselected")
    if request.method == "POST":
        li = request.form['data']
        #print(li)
        li = li.split(',')
        li = li[:-1]
        num_items = len(li)
        #print(num_items)
        if(len(li) <= 0):
            flash("Records not selected, Please select the records, using check box", "danger")
            return redirect('/bgrenewal')
        for sid in li:
            #print(sid)
            #print(type(sid))
            sql_query = """DELETE FROM bankguarantee WHERE sid= %s""" 
            input_data = (sid,)
            util.runSql(sql_query, input_data)
            #cursor.execute(sql_query, input_data)
            #connection.commit()
        
        flash("Selected Records deleted successfully", "danger")
        return redirect('/bgrenewal')
        #return render_template('bgrenewal.html', query=query)
    
    else:
        temp_query= " " "SELECT * FROM bankguarantee" "  "
        cursor.execute(temp_query)
        query = cursor.fetchall()
        return render_template('bgrenewal.html', query=query)
    
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/export/<string:sid>", methods=['POST','GET'])
def export_report(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"uaddress",amount_in_words.splitTheAddress(str(posts.unitaddress)))
    html = render_template('export.html', posts=posts)
    # Get the HTML output
    #out = render_template("export.html")    
    # PDF options
    options = {
    "orientation": "landscape",
    "page-size": "A4",
    "margin-top": "1.0cm",
    "margin-right": "1.0cm",
    "margin-bottom": "1.0cm",
    "margin-left": "1.0cm",
    "encoding": "UTF-8",
    "disable-local-file-access": None,
    "enable-local-file-access": None,
    "print-media-type": None
    }
    # Build PDF from HTML 
    unitName = posts.unitname + ".pdf"
    #print(unitName)
    value = "attachment;filename="+unitName
    pdf = pdfkit.from_string(html, options=options)
    # Download the PDF
    headers = {"Content-Disposition": value}
    return Response(pdf, mimetype="application/pdf", headers=headers)

@app.route("/exportnew/<string:sid>", methods=['POST','GET'])
def export_report_new(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"zonaladdress",amount_in_words.splitTheAddress(str(posts.zoaddress)))
    html = render_template('exportnew.html', posts=posts)
    # Get the HTML output
    #out = render_template("export.html")    
    # PDF options
    options = {
    "orientation": "landscape",
    "page-size": "A4",
    "margin-top": "1.0cm",
    "margin-right": "1.0cm",
    "margin-bottom": "1.0cm",
    "margin-left": "1.0cm",
    "encoding": "UTF-8",
    "disable-local-file-access": None,
    "enable-local-file-access": None,
    "print-media-type": None
    }
    # Build PDF from HTML 
    unitName = posts.unitname + ".pdf"
    #print(unitName)
    value = "attachment;filename="+unitName
    pdf = pdfkit.from_string(html, options=options)
    # Download the PDF
    headers = {"Content-Disposition": value}
    return Response(pdf, mimetype="application/pdf", headers=headers)

@app.route("/generatepdf/<string:sid>", methods=['POST','GET'])
def download_report(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"uaddress",amount_in_words.splitTheAddress(str(posts.unitaddress)))
    if request.method == "POST":
        if request.form.get('action') == 'print':
            pass
        elif request.form.get('action') == 'close':
            return redirect('/forrenewal')
    #print(posts.bankaddress)
    return render_template('generatepdf.html', posts=posts)
    """
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    html = render_template('generatepdf.html', posts=posts)
    
    if request.method == "POST":
        # Get the HTML output
        
        #out = render_template("export.html")
        
        # PDF options
        options = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
        }
        
        # Build PDF from HTML 
        pdf = pdfkit.from_string(html, options=options)
        

        # Download the PDF
        headers = {"Content-Disposition": "attachment;filename=myname.pdf"}
        return Response(pdf, mimetype="application/pdf", headers=headers) 
    else:    
        posts=Bankguarantee.query.filter_by(sid=sid).first()
        return render_template('generatepdf.html', posts=posts)
    """
@app.route("/generatepdfnew/<string:sid>", methods=['POST','GET'])
def download_report_new(sid):
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    setattr(posts,"currentdate",str(date.today()))
    setattr(posts,"amount_in_words",amount_in_words.words(str(posts.amount)))
    setattr(posts,"address",amount_in_words.splitTheAddress(str(posts.bankaddress)))
    setattr(posts,"zonaladdress",amount_in_words.splitTheAddress(str(posts.zoaddress)))

    if request.method == "POST":
        if request.form.get('action') == 'print':
            pass
        elif request.form.get('action') == 'close':
            return redirect('/bgrenewal')
            
    return render_template('generatepdfnew.html', posts=posts)
@app.route("/edit/<string:sid>", methods=['POST','GET'])
#@login_required
def edit(sid):
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    #print(request.method)
    if request.method == "POST":
        unitname=request.form.get('unitname')
        unitemail=request.form.get('unitemail')
        gender=request.form.get('gender')
        unitaddress=request.form.get('unitaddress')
        unitnumber=request.form.get('unitnumber')
        bankheadname=request.form.get('bankheadname')
        bankname=request.form.get('bankname')
        bankemailid=request.form.get('bankemailid')
        bankphonenumber=request.form.get('bankphonenumber')
        bankaddress=request.form.get('bankaddress')
        bgnumber=request.form.get('bgnumber')
        #bgdate=datetime.strptime(request.form.get('bgdate'), '%d-%m-%Y').date().isoformat()
        bgdate=request.form.get('bgdate')
        stampnumber=request.form.get('stampnumber')
        validperiod=request.form.get('validperiod')
        claimperiod=request.form.get('claimperiod')
        v = Decimal(request.form.get('amount'))
        amount=float(v)
        accountnumber = request.form.get('accountnumber')
        securityvalue=float(Decimal(request.form.get('securityvalue')))
        #submitdate=datetime.strptime(request.form.get('submitdate'), '%d-%m-%Y').date().isoformat()
        submitdate= request.form.get('submitdate')
        #renewaldate=datetime.strptime(request.form.get('renewaldate'), '%d-%m-%Y').date().isoformat()
        renewaldate=request.form.get('renewaldate')
        #claimamount=float(Decimal(request.form.get('claimamount')))
        zonalbankname=request.form.get('zonalbankname')
        zonalofficemail=request.form.get('zonalofficemail')
        zocontactprsnname=request.form.get('zocontactprsnname')
        zophonenumber=request.form.get('zophonenumber')
        zoaddress=request.form.get('zoaddress')
        #db.engine.execute(f"UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}' `stampnumber`='{stampnumber}' `validperiod` = '{validperiod}' `amount` = '{amount}' `securityvalue` = '{securityvalue}' `submitdate` = '{submitdate}' `renewaldate` = '{renewaldate}' `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        #query = "UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}"
        sql_query = """UPDATE bankguarantee SET unitname=%s,unitemail=%s,gender=%s,unitaddress=%s,unitnumber=%s,bankheadname=%s,bankname=%s,bankemailid=%s,bankphonenumber=%s,bankaddress=%s,bgnumber=%s,bgdate=%s,stampnumber=%s,validperiod=%s,claimperiod=%s,amount=%s,accountnumber=%s,securityvalue=%s,submitdate=%s,renewaldate=%s,zonalbankname=%s,zonalofficemail=%s,zocontactprsnname=%s,zophonenumber=%s,zoaddress=%s WHERE sid=%s"""
        temp_data = (unitname,unitemail,gender,unitaddress,unitnumber,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,zonalbankname,zonalofficemail,zocontactprsnname,zophonenumber,zoaddress,sid)
        #cur.execute("UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        cursor.execute(sql_query, temp_data)
        connection.commit()
        cursor.close()
        connection.close()
        flash("Your Data is updated", "success")
        return redirect('/bgrenewal')
    return render_template('edit.html',posts=posts)
@app.route("/confirmationedit/<string:sid>", methods=['POST','GET'])
#@login_required
def confiramationedit(sid):
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    #print(request.method)
    if request.method == "POST":
        unitname=request.form.get('unitname')
        unitemail=request.form.get('unitemail')
        gender=request.form.get('gender')
        unitaddress=request.form.get('unitaddress')
        unitnumber=request.form.get('unitnumber')
        bankheadname=request.form.get('bankheadname')
        bankname=request.form.get('bankname')
        bankemailid=request.form.get('bankemailid')
        bankphonenumber=request.form.get('bankphonenumber')
        bankaddress=request.form.get('bankaddress')
        bgnumber=request.form.get('bgnumber')
        #bgdate=datetime.strptime(request.form.get('bgdate'), '%d-%m-%Y').date().isoformat()
        bgdate=request.form.get('bgdate')
        stampnumber=request.form.get('stampnumber')
        validperiod=request.form.get('validperiod')
        claimperiod=request.form.get('claimperiod')
        v = Decimal(request.form.get('amount'))
        amount=float(v)
        accountnumber = request.form.get('accountnumber')
        securityvalue=float(Decimal(request.form.get('securityvalue')))
        #submitdate=datetime.strptime(request.form.get('submitdate'), '%d-%m-%Y').date().isoformat()
        submitdate= request.form.get('submitdate')
        #renewaldate=datetime.strptime(request.form.get('renewaldate'), '%d-%m-%Y').date().isoformat()
        renewaldate=request.form.get('renewaldate')
        #claimamount=float(Decimal(request.form.get('claimamount')))
        zonalbankname=request.form.get('zonalbankname')
        zonalofficemail=request.form.get('zonalofficemail')
        zocontactprsnname=request.form.get('zocontactprsnname')
        zophonenumber=request.form.get('zophonenumber')
        zoaddress=request.form.get('zoaddress')
        #db.engine.execute(f"UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}' `stampnumber`='{stampnumber}' `validperiod` = '{validperiod}' `amount` = '{amount}' `securityvalue` = '{securityvalue}' `submitdate` = '{submitdate}' `renewaldate` = '{renewaldate}' `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        #query = "UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}"
        sql_query = """UPDATE bankguarantee SET unitname=%s,unitemail=%s,gender=%s,unitaddress=%s,unitnumber=%s,bankheadname=%s,bankname=%s,bankemailid=%s,bankphonenumber=%s,bankaddress=%s,bgnumber=%s,bgdate=%s,stampnumber=%s,validperiod=%s,claimperiod=%s,amount=%s,accountnumber=%s,securityvalue=%s,submitdate=%s,renewaldate=%s,zonalbankname=%s,zonalofficemail=%s,zocontactprsnname=%s,zophonenumber=%s,zoaddress=%s WHERE sid=%s"""
        temp_data = (unitname,unitemail,gender,unitaddress,unitnumber,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,zonalbankname,zonalofficemail,zocontactprsnname,zophonenumber,zoaddress,sid)
        #cur.execute("UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        cursor.execute(sql_query, temp_data)
        connection.commit()
        cursor.close()
        connection.close()
        flash("Your Data is updated", "success")
        return redirect('/fordatarenewal')
    return render_template('confirmationedit.html',posts=posts)
@app.route("/renewaledit/<string:sid>", methods=['POST','GET'])
#@login_required
def renewaledit(sid):
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    posts=Bankguarantee.query.filter_by(sid=sid).first()
    #print(request.method)
    if request.method == "POST":
        unitname=request.form.get('unitname')
        unitemail=request.form.get('unitemail')
        gender=request.form.get('gender')
        unitaddress=request.form.get('unitaddress')
        unitnumber=request.form.get('unitnumber')
        bankheadname=request.form.get('bankheadname')
        bankname=request.form.get('bankname')
        bankemailid=request.form.get('bankemailid')
        bankphonenumber=request.form.get('bankphonenumber')
        bankaddress=request.form.get('bankaddress')
        bgnumber=request.form.get('bgnumber')
        #bgdate=datetime.strptime(request.form.get('bgdate'), '%d-%m-%Y').date().isoformat()
        bgdate=request.form.get('bgdate')
        stampnumber=request.form.get('stampnumber')
        validperiod=request.form.get('validperiod')
        claimperiod=request.form.get('claimperiod')
        v = Decimal(request.form.get('amount'))
        amount=float(v)
        accountnumber = request.form.get('accountnumber')
        securityvalue=float(Decimal(request.form.get('securityvalue')))
        #submitdate=datetime.strptime(request.form.get('submitdate'), '%d-%m-%Y').date().isoformat()
        submitdate= request.form.get('submitdate')
        #renewaldate=datetime.strptime(request.form.get('renewaldate'), '%d-%m-%Y').date().isoformat()
        renewaldate=request.form.get('renewaldate')
        #claimamount=float(Decimal(request.form.get('claimamount')))
        zonalbankname=request.form.get('zonalbankname')
        zonalofficemail=request.form.get('zonalofficemail')
        zocontactprsnname=request.form.get('zocontactprsnname')
        zophonenumber=request.form.get('zophonenumber')
        zoaddress=request.form.get('zoaddress')
        #db.engine.execute(f"UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}' `stampnumber`='{stampnumber}' `validperiod` = '{validperiod}' `amount` = '{amount}' `securityvalue` = '{securityvalue}' `submitdate` = '{submitdate}' `renewaldate` = '{renewaldate}' `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        #query = "UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}"
        sql_query = """UPDATE bankguarantee SET unitname=%s,unitemail=%s,gender=%s,unitaddress=%s,unitnumber=%s,bankheadname=%s,bankname=%s,bankemailid=%s,bankphonenumber=%s,bankaddress=%s,bgnumber=%s,bgdate=%s,stampnumber=%s,validperiod=%s,claimperiod=%s,amount=%s,accountnumber=%s,securityvalue=%s,submitdate=%s,renewaldate=%s,zonalbankname=%s,zonalofficemail=%s,zocontactprsnname=%s,zophonenumber=%s,zoaddress=%s WHERE sid=%s"""
        temp_data = (unitname,unitemail,gender,unitaddress,unitnumber,bankheadname,bankname,bankemailid,bankphonenumber,bankaddress,bgnumber,bgdate,stampnumber,validperiod,claimperiod,amount,accountnumber,securityvalue,submitdate,renewaldate,zonalbankname,zonalofficemail,zocontactprsnname,zophonenumber,zoaddress,sid)
        #cur.execute("UPDATE `bankguarantee` SET `unitname` = '{unitname}', `unitemail` = '{unitemail}', `gender` = '{gender}', `unitaddress` = '{unitaddress}', `unitnumber` = '{unitnumber}', `bankname` = '{bankname}', `bankaddress` = '{bankaddress}', `bgnumber` = '{bgnumber}', `bgdate` = '{bgdate}', `stampnumber`='{stampnumber}', `validperiod` = '{validperiod}', `amount` = '{amount}', `securityvalue` = '{securityvalue}', `submitdate` = '{submitdate}', `renewaldate` = '{renewaldate}', `claimamount` = '{claimamount}' WHERE `bankguarantee`.`sid` = {sid}")
        cursor.execute(sql_query, temp_data)
        connection.commit()
        cursor.close()
        connection.close()
        flash("Your Data is updated", "success")
        return redirect('/forrenewal')
    return render_template('renewaledit.html',posts=posts)

@app.route("/delete/<string:sid>", methods=['POST','GET'])
def delete(sid):
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    #cur.execute(f"DELETE FROM `bankguarantee` WHERE `bankguarantee`.`sid`={sid}")
    sql_query = """DELETE FROM bankguarantee WHERE sid=%s"""
    input_data = (sid,)
    cursor.execute(sql_query,input_data)
    connection.commit()
    cursor.close()
    connection.close()
    #query = cur.fetchall()
    flash("Record Deleted successfully",'danger')
    return redirect('/bgrenewal')

@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # in signup.html in form widget variables id and name, what name is assigned
        #that should be used in the get
        email = request.form.get('email')
        password = request.form.get('password')
        #print(email, password)
        user = User.query.filter_by(email=email).first()
        """
        print(user)
        print(type(user))
        print(user.password)
        print(user.username)
        print(user.email)
        print("********************")
        """
        if(user and check_password_hash(user.password, password)):
            login_user(user)
            # primary is the color, which ever color u want we can give
            flash("Login Sucessful", "primary")
            # redirect to Index page or home page based on our requirement
            return redirect('/bgrenewal')
        else:
            print("Invalid credentials")
            flash("Invalid credentials,please Signup", "danger")
            return render_template("login.html")

    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "warning")
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    connection = mysql.connector.connect(host='localhost',
                                          database='bms',
                                          user='root',
                                          password='')
    cursor = connection.cursor()
    if request.method == "POST":
        # in signup.html in form widget variables id and name, what name is assigned
        #that should be used in the get
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        #print(username, email, password)
        # capital User means Databse Table  name used in ta class
        #leftside email is vriable in Databse table
        #rightside email is above variable from user form
        user = User.query.filter_by(email=email).first()
        """
        print(user)
        print(type(user))
        print(user.password)
        print(user.username)
        print(user.email)
        print("********************")
        
        if(user):
            print("Email is already exists")
            flash("Email is already exists", "warning")
            return redirect("/login")
        """
        # we have insert a record into Db
        # we want to use 'f' string to pass the above form values into database
        encpassword = generate_password_hash(password)
        query = """INSERT INTO user (username,email,password) VALUES (%s,%s,%s)"""
        input_data = (username,email,encpassword)
        cursor.execute(query, input_data)
        connection.commit()
        cursor.close()
        connection.close()
        #new_user = db.engine.execute(f"INSERT INTO `user` (`username`,`email`, `password`) VALUES ('{username}','{email}','{encpassword}')")
        #another method of insert and save the data in DB
        """
        new_user = User(username=username, email=email,password=encpassword)
        db.session.add(new_user)
        db.session.commit()
        """
        flash("Signup Sucess, Please login", "success")
        return render_template('login.html')


    #print("This is get method")
    return render_template('signup.html')

@app.route("/search", methods=['POST', 'GET'])
def search():
    cur = mysqlGlobal.connection.cursor(MySQLdb.cursors.DictCursor)
    temp_query= "SELECT * FROM `bankguarantee`"
    cur.execute(temp_query)
    query = cur.fetchall()
    #print(query)
    ordersrange = {}

    if request.method == 'POST':
        search = request.form.get('search')
        nameFound = ""
        for post in query:
            #print(post)
            renewaldate = post['renewaldate']
            unitname=post['unitname']
            unitemail=post['unitemail']
            unitaddress=post['unitaddress']
            unitnumber=post['unitnumber']
            bankname=post['bankname']
            bgdate=post['bgdate']
            stampnumber=post['stampnumber']
            validperiod=post['validperiod']
            amount = post['amount']
            securityvalue=post['securityvalue']
            submitdate=  post['submitdate']
            renewaldate= post['renewaldate']
            claimamount= post['claimamount']
            zonalbankname=post['zonalbankname']
            zonalofficemail=post['zonalofficemail']
            zocontactprsnname=post['zocontactprsnname']
            zophonenumber=post['zophonenumber']
            renewalprocessed=post['renewalprocessed']
            zoprocessed=post['zoprocessed']
            #print(search)            
            if search in unitname:                
                query = Bankguarantee.query.filter_by(unitname=unitname)
                break
            elif search in unitemail:
                query = Bankguarantee.query.filter_by(unitemail=unitemail)
                break
            elif search in unitaddress:
                query = Bankguarantee.query.filter_by(unitaddress=unitaddress)
                break
            elif search in unitnumber:
                query = Bankguarantee.query.filter_by(unitnumber=unitnumber)
                break
            elif search in bankname:
                query = Bankguarantee.query.filter_by(bankname=bankname)
                break
            elif search == bgdate:
                query = Bankguarantee.query.filter_by(bgdate=bgdate)
                break
            elif search in stampnumber:
                query = Bankguarantee.query.filter_by(stampnumber=stampnumber)
                break
            elif search in validperiod:
                query = Bankguarantee.query.filter_by(validperiod=validperiod)
                break
            elif search in amount:
                query = Bankguarantee.query.filter_by(amount=amount)
                break
            elif search in securityvalue:
                query = Bankguarantee.query.filter_by(securityvalue=securityvalue)
                break
            elif search == submitdate:
                query = Bankguarantee.query.filter_by(submitdate=submitdate)
                break
            elif search == renewaldate:
                query = Bankguarantee.query.filter_by(renewaldate=renewaldate)
                break
            elif search in claimamount:
                query = Bankguarantee.query.filter_by(claimamount=claimamount)
                break
            elif search in zonalbankname:
                query = Bankguarantee.query.filter_by(zonalbankname=zonalbankname)
                break
            elif search in zonalofficemail:
                query = Bankguarantee.query.filter_by(zonalofficemail=zonalofficemail)
                break
            elif search in zocontactprsnname:
                query = Bankguarantee.query.filter_by(zocontactprsnname=zocontactprsnname)
                break
            elif search in zophonenumber:
                query = Bankguarantee.query.filter_by(zophonenumber=zophonenumber)
                break
            elif search in renewalprocessed:
                query = Bankguarantee.query.filter_by(renewalprocessed=renewalprocessed)
                break
            elif search in zoprocessed:
                query = Bankguarantee.query.filter_by(zoprocessed=zoprocessed)
                break
        """
            #renewal_date = request.form.get('search')
            renewal_date = datetime.strptime(request.form.get('search'), '%Y/%m/%d').date()
            print(renewal_date)
            query = "SELECT * from Bankguarantee WHERE renewal_date '{}'".format(renewal_date)
            cur.execute(query)
            ordersrange = cur.fetchall()
        """        
        #return jsonify({'htmlresponse': render_template('search.html', query=query)})
        return render_template('search.html', posts=query)
    return "Done"


@app.route("/details")
@login_required
def details():
    posts = Triger.query.all()
    return render_template('trigers.html', posts=posts)


@app.route("/settings")
def settings():
    if not User.is_authenticated:
        return render_template('login.html')
    else:
        return render_template('settings.html', username=current_user.username)

if __name__ == '__main__':
    #app.run(debug=False, host='127.0.0.1')
    app.run(debug=True)