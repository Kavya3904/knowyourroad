import os.path

from flask import *
from werkzeug.utils import secure_filename

from src.database import *

app = Flask(__name__)
app.secret_key = "fsfsg"




import functools

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('Admin/Loginpage.html')
        return func()

    return secure_function


# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect('/')


@app.route('/')
def startpage():
    return render_template('Admin/Loginpage.html')
    #Admin


@app.route('/Adminhome')
def adminhome():
    return render_template('Admin/Admin home.html')


@app.route('/replay')
@login_required
def replay():
    id=request.args.get('id')
    session['id']=id
    return render_template('Admin/Replay.html')

#replay code
@app.route('/replaycode', methods=['POST'])
@login_required
def replaycode():
    rid=session['id']
    reply=request.form['textarea']
    qry="update complaint set replay=%s where id=%s"
    val=(reply,rid)
    iud(qry,val)

    return '''<script>alert("Replay has sended"); window.location="viewcomplaintsandreplay" </script>'''


@app.route('/sendnnotification')
@login_required
def sendnotification():
    return render_template('Admin/send notification.html')

#sendnotificationcode

@app.route('/sendnnotificationcode', methods =['POST'])
@login_required


def sendnotificationcode():
    noti = request.form['textarea']

    qry = "INSERT INTO `notification` VALUES (NULL,%s,CURDATE())"
    iud(qry,noti)

    return '''<script>alert("Notification has been sended"); window.location="Adminhome" </script>'''

@app.route('/sendreport')
@login_required
def sendreport():
    qry = "SELECT `id`,`complaint`,`photo`,`date`FROM `complaint`"
    res=selecteall(qry)
    return render_template('Admin/Send report.html',val=res)





@app.route('/updatestatus')
@login_required
def updatestatus():
    id = request.args.get('id')
    session['cid']=id
    return render_template('Admin/update status.html')

@app.route('/adminsendreport',methods=['post'])
@login_required
def adminsendreport():


    id=session['cid']
    discreption = request.form['textarea']
    image = request.files['fileField']
    file = secure_filename(image.filename)
    image.save(os.path.join("static/uploads",file))
    qry="INSERT INTO `finished_work_report` VALUES(NULL,%s,%s,%s,CURDATE())"
    val=(str(id),file,discreption)
    iud(qry,val)


    return '''<script>alert("success"); window.location="Adminhome" </script>'''




@app.route('/verifytrafficpolice')
@login_required
def verifytraffic():
    qry = "SELECT * FROM `traffic_police`  JOIN `login` ON `login`.`id`=`traffic_police`.`loginid` WHERE `login`.`type`='pending'"
    res = selecteall(qry)
    return render_template('Admin/verify traffic police.html', val=res)

@app.route('/viewacceptedpolice', methods=['POST'])
@login_required
def viewacceptedpolice():
    qry = " SELECT * FROM `traffic_police`  JOIN `login` ON `login`.`id`=`traffic_police`.`loginid` WHERE `login`.`type`='Traffic police'"

    res = selecteall(qry)
    return render_template('Admin/view accepted police.html', val=res)
@app.route('/accepted')
@login_required
def accept():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `login`.type='Traffic police' WHERE `login`.`id` = %s"
    val = id
    iud(qry, val)


    return '''<script>alert("Accepted"); window.location="verifytrafficpolice" </script>'''
@app.route('/rejected')
@login_required
def reject():
    id = request.args.get('id')
    qry = "UPDATE `login` SET `login`.type='rejected' WHERE `login`.`id` = %s"
    val = id
    iud(qry, val)
    return '''<script>alert("Rejected"); window.location="verifytrafficpolice" </script>'''


@app.route('/viewcommentsandrate')
@login_required
def commentandrate():
    qry ="SELECT complaint.* ,user.`firstname`,`lastname`,`phone` ,`rating`.`rating`,`comment`.`comment` FROM complaint JOIN `user` ON `user`.`loginid`=`complaint`.`userid`  JOIN `finished_work_report` ON `finished_work_report`.`complaint_id`=`complaint`.`id`  JOIN `comment` ON `comment`.`finished_work_reportid`=`finished_work_report`.`id` JOIN `rating` ON `rating`.`finished_work_reportid`=`finished_work_report`.`id` "
    res = selecteall(qry)

    return render_template('Admin/view comments and rate.html',val  =res)


@app.route('/viewcomplaintsandreplay')
@login_required
def viewcomplaintsandreplay():
    qry ="SELECT complaint.* ,user.`firstname`,`lastname`,`phone` FROM complaint JOIN `user` ON `user`.`loginid`=`complaint`.`userid` WHERE `complaint`.`replay`='pending'"
    res = selecteall(qry)
    return render_template('Admin/View complaints & replay.html',val=res)


@app.route('/viewdetailsviolationreport')
@login_required
def violationandreport():
    qry="SELECT `violation_report`.*,`traffic_police`.`firstname`,`lastname`,`email`,`phone` FROM `violation_report` JOIN `traffic_police` ON `traffic_police`.`id`=`violation_report`.`traffic_police_id`  "
    res = selecteall(qry)
    return render_template('Admin/view details violation report.html',val = res)

@app.route('/viewuser')
@login_required
def viewuser():
    qry = "SELECT * FROM `user`"
    res = selecteall(qry)
    return render_template('Admin/view user.html',val =res)

#traffic Police

@app.route('/addmanagetrafficviolation')
@login_required
def addmanagetrafficviolation():
    qry = "SELECT * FROM `violation_report` "
    res = selecteall(qry)

    return render_template('Traffic Police/add and manage traffic voilation report.html',val=res)

@app.route('/deletingviolation')
@login_required
def deletingviolation():
    id = request.args.get('id')
    qry="DELETE  FROM `violation_report`  WHERE id=%s "
    val=id
    iud(qry, val)

    return '''<script>alert("Deleted"); window.location="addmanagetrafficviolation" </script>'''







@app.route('/addviolation',methods=['post'])
@login_required
def addviolation():
    return render_template('Traffic Police/add violation.html')

@app.route('/addingviolationreport',methods=['post'])
@login_required
def addingviolationreport():
    id = session['lid']
    discreption = request.form['textarea']
    image = request.files['fileField']
    file = secure_filename(image.filename)
    image.save(os.path.join("static/report", file))
    qry = "INSERT INTO `violation_report` VALUES(NULL,%s,%s,%s,CURDATE())"
    val = (str(id), file, discreption)
    iud(qry, val)




    return '''<script>alert("Successfully Added"); window.location="addmanagetrafficviolation" </script>'''



@app.route('/editviolation')
@login_required
def editviolation():
    id=request.args.get('id')
    session['vid']=id
    qry="SELECT * FROM `violation_report` WHERE id=%s"
    res=selectone(qry,session['vid'])



    return render_template('Traffic Police/edit violation.html',val=res)


@app.route('/editedviolation',methods=['post'])
@login_required
def editedviolation():
    try:
        discreption = request.form['textarea']
        image = request.files['fileField']
        file = secure_filename(image.filename)
        image.save(os.path.join("static/report", file))
        qry = "UPDATE `violation_report` SET `report`=%s,`description`=%s WHERE id=%s"
        val = (file, discreption,session['vid'])
        iud(qry, val)

        return '''<script>alert("successfully edited"); window.location="addmanagetrafficviolation" </script>'''
    except Exception as e:
        discreption = request.form['textarea']

        qry = "UPDATE `violation_report` SET `description`=%s WHERE id=%s"
        val = (discreption, session['vid'])
        iud(qry, val)

        return '''<script>alert("successfully edited"); window.location="addmanagetrafficviolation" </script>'''


@app.route('/regestartion')

def regestration():
    return render_template('Traffic Police/regestration.html')

@app.route('/RegisteringTraficpolice',methods=['POST'])
@login_required
def RegisteringTraficpolice():

    FirstName = request.form['textfield']
    Lastname = request.form['textfield2']
    DOB = request.form['date']
    Gender = request.form['radio']
    Place = request.form['textarea']
    Post = request.form['textfield3']
    Pin = request.form['number']
    Email = request.form['email']
    Phone = request.form['number2']
    username =  request.form['textfield4']
    password =  request.form['password']

    qry = "INSERT INTO `login`  VALUES (NULL,%s,%s,'pending')"
    val = (username,password)
    id=iud(qry, val)

    qry = "INSERT INTO `traffic_police` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (str(id),FirstName, Lastname, DOB, Gender, Place, Post, Pin, Email, Phone)
    iud(qry, val)
    return '''<script>alert("Successfully Registerd"); window.location="trafficpolicehome" </script>'''







@app.route('/trafficpolicehome')

def Trafficpolicehome():
   return render_template('Traffic Police/traffic police home.html')

@app.route('/viewandupdate')
@login_required
def viewandupdate():
    id=session['lid']

    qry="SELECT * FROM `traffic_police` WHERE `loginid` = %s"
    val=(str(id))
    res=selectone(qry,val)

    return render_template('Traffic Police/view and update.html',val=res)


@app.route('/viewtrafficdata', methods=['POST'])
@login_required
def viewtrafficdata():
    id = session['lid']
    FirstName = request.form['textfield']
    Lastname = request.form['textfield2']
    DOB = request.form['date']
    Gender = request.form['radio']
    Place = request.form['textarea']
    Post = request.form['textfield3']
    Pin = request.form['number']
    Email = request.form['email']
    Phone = request.form['number2']
    qry="UPDATE `traffic_police` SET `firstname`=%s,`lastname`=%s,`dob`=%s,`gender`=%s,`place`=%s,`post`=%s,`pin`=%s,`email`=%s,`phone`=%s WHERE `loginid`=%s"
    val=(FirstName,Lastname,DOB,Gender,Place,Post,Pin,Email,Phone,str(id))
    iud(qry,val)

    return '''<script>alert("Success"); window.location="Traffic Police/trafficpolicehome" </script>'''




@app.route('/viewemergency')
@login_required
def viewemergency():
    qry="SELECT `user`.`firstname`,`lastname`,`phone`,`emergency`.`latitude`,`longitude` FROM `user` JOIN `emergency` ON `emergency`.`user_id`=`user`.`loginid`"
    res=selecteall(qry)

    return render_template('Traffic Police/view emergency.html',val=res )

# @app.route('/addingemergency')
# def addingemergency():
#
#     return




@app.route('/Logout')
def Logout():
    session.clear()
    return render_template('Admin/LoginPage.html')

#get login data
@app.route('/login', methods=['POST'])
def login():
    username = request.form['textfield']
    password = request.form['password']
    qry = "SELECT * FROM login WHERE username =%s AND password = %s"
    val = (username , password)
    res = selectone(qry,val)
    if res is None:
        return '''<script>alert("invalid"); window.location="/" </script>'''
    elif res[3] == "Admin":
        session['lid'] = res[0]
        return redirect('/Adminhome')
    elif res[3] == "Traffic police":
        session['lid']=res[0]
        return redirect('/trafficpolicehome')
    else:
        return '''<script>alert(invalid); window.location="/" </script>'''












#








app.run(debug = True)

