import os
import pymysql

from flask import *
from werkzeug.utils import secure_filename

from src.database import *

app = Flask(__name__)

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'knowyourroad12@gmail.com'
app.config['MAIL_PASSWORD'] = 'knowyourROAD#123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

@app.route('/login', methods=['POST'])
def login():
    username = request.form['uname']
    password = request.form['password']
    qry = "SELECT * FROM login WHERE username =%s AND password = %s"
    val = (username , password)
    res = selectone(qry,val)
    if res is None:
        return jsonify({'task':'invalid'})

    else:
        return jsonify({'task': 'success',"id":res[0]})
@app.route('/viewnotification', methods=['POST'])
def viewnotification():
    qry="SELECT * FROM `notification` "
    res=androidselectallnew(qry)
    return jsonify(res)

@app.route('/androidregistar', methods=['POST'])
def androidregistar():

    FirstName = request.form['firstname']
    Lastname = request.form['lastname']
    DOB = request.form['dates']
    Gender = request.form['gender']
    Place = request.form['place']
    Post = request.form['post']
    Pin = request.form['pin']
    Email = request.form['emails']
    Phone = request.form['phone']
    username =  request.form['username1']
    password =  request.form['password1']

    qry = "INSERT INTO `login`  VALUES (NULL,%s,%s,'user')"
    val = (username, password)
    id=iud(qry,val)

    qry="INSERT INTO `user` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(str(id),FirstName,Lastname,DOB,Gender,Place,Post,Pin,Email,Phone)
    iud(qry, val)
    return jsonify({'task':'success'})
@app.route('/viewandupdateprofile', methods=['POST'])
def viewandupdateprofile():
    id = request.form['userid']

    qry = "SELECT * FROM `user` WHERE `loginid` = %s"
    val = (str(id))
    res =androidselectall(qry,val)
    return jsonify(res)



@app.route('/viewandupdatingcode', methods=['POST'])
def viewandupdatingcode():
    id = request.form['id']
    FirstName = request.form['fname']
    Lastname = request.form['lname']
    DOB = request.form['DOB']
    Gender = request.form['Gen']
    Place = request.form['Place']
    Post = request.form['Post']
    Pin = request.form['Pin']
    Email = request.form['Email']
    Phone = request.form['phone']
    qry = "UPDATE `user` SET `firstname`=%s,`lastname`=%s,`dob`=%s,`gender`=%s,`place`=%s,`post`=%s,`pin`=%s,`email`=%s,`phone`=%s WHERE `loginid`=%s"
    val = (FirstName, Lastname, DOB, Gender, Place, Post, Pin, Email, Phone, str(id))
    iud(qry, val)
    return jsonify({'task': 'success'})


@app.route('/viewworkandsendcommentsandrate', methods=['POST'])
def viewworkandsendcommentsandrate():
    print(request.form)
    userid=request.form['userid']

    qry = "SELECT `complaint`.`id`,`complaint`.`complaint`,complaint.`photo`,complaint.`date`,`finished_work_report`.`image`,`description` FROM `complaint` JOIN `finished_work_report` ON `complaint`.`id`=`finished_work_report`.`complaint_id` WHERE `complaint`.`userid`=%s "
    res = androidselectall(qry,userid)
    print(res)
    return jsonify(res)

@app.route('/viewworkandsendcommentsandratemore', methods=['POST'])
def viewworkandsendcommentsandratemore():
    print(request.form)
    cid=request.form['cid']

    qry = "SELECT `complaint`.`complaint`,complaint.`photo`,complaint.`date`,`finished_work_report`.`image`,`description`,finished_work_report.id FROM `complaint` JOIN `finished_work_report` ON `complaint`.`id`=`finished_work_report`.`complaint_id` WHERE `complaint`.`id`=%s"
    res = androidselectall(qry,cid)
    print(res)
    return jsonify(res)





@app.route('/sendcomments', methods=['POST'])
def sendcomments():
    comment=request.form['comment']
    userid=request.form['userid']
    finishedworkreport=request.form['finishedworkreport']

    qry="INSERT INTO `comment` VALUES(NULL ,%s,%s,%s,CURDATE())"
    val=(userid,finishedworkreport,comment)
    iud(qry,val)
    return jsonify({'task':'success'})


@app.route('/sendrating', methods=['POST'])
def sendrating():
    rating=request.form['rate']
    userid=request.form['userid']
    finishedworkid=request.form['finishedworkid']
    qry="INSERT INTO `rating` VALUES (NULL ,%s,%s,%s,CURDATE())"
    val=(userid,finishedworkid,rating)
    iud(qry,val)
    return jsonify({'task':'success'})

@app.route('/viewcomplaintsreplay', methods=['POST'])
def viewcomplaintsreplay():
    userid=request.form['userid']
    qry="SELECT * FROM `complaint` WHERE `userid`=%s"

    res= androidselectall(qry,userid)
    return jsonify(res)

@app.route('/Sendcomplaint', methods=['POST'])
def Sendcomplaint():
    userid=request.form['lid']
    complaint= request.form['complaint']
    image = request.files['file']
    file = secure_filename(image.filename)
    image.save(os.path.join("static/uploads", file))
    qry="INSERT INTO `complaint` VALUES(NULL,%s,%s,%s,CURDATE(),'pending')"
    val=(userid,complaint,file)
    iud(qry,val)
    return jsonify({'task': 'success'})




@app.route('/Sendemergency', methods=['POST'])
def Sendemergency():
    userid=request.form['userid']
    langitude=request.form['langitude']
    longitude=request.form['longitude']
    qry="INSERT INTO `emergency` VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(userid,langitude,longitude)
    iud(qry,val)
    return jsonify({'task': 'success'})



@app.route('/frgtpswd',methods=['post'])
def frgtpswd():
    con = pymysql.Connect(host="localhost", port=3306, user='root', password='rootpassword123', db='know your road')
    cmd = con.cursor()
    email=request.form['email']
    cmd.execute("SELECT `login`.`password` FROM `login` JOIN `user` ON login.`id`=`user`.`loginid` WHERE `user`.`email`='"+email+"'")
    s1 = cmd.fetchone()
    print(s1)
    passwd = s1[0]
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('knowyourroad12@gmail.com', 'knowyourROAD#123')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your Password is : " + passwd)
    print(msg)
    msg['Subject'] = 'Password info'
    msg['To'] = email
    msg['From'] = 'knowyourroad12@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return jsonify({'task': 'success'})





app.run(host='0.0.0.0',port=5000)


