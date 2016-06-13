import os
from flask import Flask, render_template, json, request, session, redirect
from flask.ext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ow31051995it'
app.config['MYSQL_DATABASE_DB'] = 'crm'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = 'why would I tell you my secret key?'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

from werkzeug import generate_password_hash, check_password_hash



@app.route('/showSignUp')
def showSignUp():
    if session.get('user') == "master":
        return render_template('signup.html')
    else:
        return render_template('error.html',error = "Unauthorised Access")

@app.route('/')
@app.route('/showSignin')
def showSignin():
    session.pop('user',None)
    return render_template('signin.html')

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        if session.get('user') == "master":
        # read the posted values from the UI
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            _hashed_password = generate_password_hash(_password)

            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

            data = cursor.fetchall()
         
            if len(data) is 0:
                conn.commit()
                return "User Created Successfully !"
            else:
                return str(data[0])
        else:
            render_template('error.html',error = "Unauthorised Access")

    except Exception as e:
        return render_template('error.html',error = str(e))
    
     
    # validate the received values
    

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
 
        _hashed_password = generate_password_hash("redrose123")
 
 
        if len(data) > 0:
            if check_password_hash(str(data[0][2]),_password):
                session['user'] = data[0][1]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()

@app.route('/userHome')
def userHome():
    if session.get('user') == 'master':
        return render_template('userHome-master.html')
    elif session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorised Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/searchID', methods = ['POST'])
def searchID():
    try:
        if session.get('user'):
            _ID = request.form['acc_id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_searchID',(_ID,))
            data = cursor.fetchall()
            if session.get('user')=="master":
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2],
                            'phone': account[3],
                            'email': account[7]}
                    accounts_dict.append(account_dict)
            else:
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2]}
                    accounts_dict.append(account_dict)

            return json.dumps(accounts_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    


@app.route('/searchPhone', methods = ['POST'])
def searchPhone():
    try:
        if session.get('user'):
            _Phone = request.form['phone']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_searchPhone',(_Phone,))
            data = cursor.fetchall()

            if session.get('user')=="master":
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2],
                            'phone': account[3],
                            'email': account[7]}
                    accounts_dict.append(account_dict)
            else:
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2]}
                    accounts_dict.append(account_dict)
 
            return json.dumps(accounts_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
   

@app.route('/searchEmail', methods = ['POST'])
def searchEmail():
    try:
        if session.get('user'):
            _Email = request.form['inputEmail']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_searchEmail',(_Email,))
            data = cursor.fetchall()

            if session.get('user')=="master":
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2],
                            'phone': account[3],
                            'email': account[7]}
                    accounts_dict.append(account_dict)
            else:
                accounts_dict = []
                for account in data:
                    account_dict = {
                            'id': account[0],
                            'fname': account[1],
                            'lname': account[2]}
                    accounts_dict.append(account_dict)
 
            return json.dumps(accounts_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/showAccount', methods = ['GET'])
def showAccount():
    try:
        if session.get('user'):
            _ID = request.args.get('acc_id')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_searchID',(_ID,))
            data = cursor.fetchall()
            for account in data:
                if session.get('user')=='master':
                    return render_template("showAccount.html",id=account[0],fname = account[1],lname = account[2],phone =account[3],aphone=account[4],cc=account[5],acc = account[6],email = account[7],subscription = account[8], address = account[9], source = account[10], timezone = account[11],notes = account[12], suspended = account[13], reason = account[14], user = account[15],creditcard = account[16])
                else:
                    return render_template("showAccount1.html",id=account[0],fname = account[1],lname = account[2],phone =account[3],aphone=account[4],cc=account[5],acc = account[6],email = account[7],subscription = account[8], address = account[9], source = account[10], timezone = account[11],notes = account[12], suspended = account[13], reason = account[14], user = account[15])
                    
        else:
            return render_template('error.html', error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/showAddAccount')
def showAddAccount():
    try:
        if session.get('user'):
            return render_template('addAccount.html')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template("error.html", error = str(e))


@app.route('/addAccount', methods = ['POST'])
def addAccount():
    try:
        if session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addAccount',(request.form['fname'],request.form['lname'],request.form['phone'],request.form['cc'],request.form['aphone'],request.form['acc'],request.form['email'],request.form['subscription'],request.form['address'],request.form['source'],request.form['timezone'],request.form['notes'],request.form['suspended'],request.form['reason'],session.get('user'),request.form['creditcard']))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return render_template("blank.html",title ="Account added Successfully")
            else:
                return render_template("blank.html", title="Database error")
            
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route("/showEditAccount")
def showEditAccount():
    try:
        if session.get('user')=='master':
            _ID = request.args.get('acc_id')
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_searchID',(_ID,))
            data = cursor.fetchall()
            for account in data:
                return render_template("editAccount.html",id=account[0],fname = account[1],lname = account[2],phone =account[3],aphone=account[4],cc=account[5],acc = account[6],email = account[7],subscription = account[8], address = account[9], source = account[10], timezone = account[11],notes = account[12], suspended = account[13], reason = account[14], user = account[15],creditcard=account[16])
                    
        else:
            return render_template('error.html', error = 'Unauthorized Access')

    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/editAccount', methods = ['POST'])
def editAccount():
    try:
        if session.get('user')=='master':
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_editAccount',(request.form['id'],request.form['fname'],request.form['lname'],request.form['phone'],request.form['cc'],request.form['aphone'],request.form['acc'],request.form['email'],request.form['subscription'],request.form['address'],request.form['source'],request.form['timezone'],request.form['notes'],request.form['suspended'],request.form['reason'],session.get('user'),request.form['creditcard']))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return render_template("blank.html",title ="Account added updated")
            else:
                return render_template("blank.html", title="Database error")
            
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/getNotes',methods=['POST'])
def getNotes():
    try:
        if session.get('user'):
            _ID = request.form['acc_id']
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getNotes',(_ID,))
            data = cursor.fetchall()
            accounts_dict = []
            for account in data:
                account_dict = {
                        'id': account[0],
                        'notes': account[1],
                        'createdby': account[2],
                        'status': account[3],
                        'createdon': account[4]}
                accounts_dict.append(account_dict)
            
            return json.dumps(accounts_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    
        
@app.route('/showAddNote',methods=['GET'])
def showAddNote():
    if session.get('user'):
        return render_template('addNote.html',id=request.args.get('acc_id'))

@app.route('/addNote',methods=['POST'])
def addNote():
    try:
        if session.get('user'):
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addNotes',(request.form['id'],request.form['note'],session.get('user'),request.form['status']))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/showAccount?acc_id='+request.form['id'])
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/getReport')
def getReport():
    try:
        if session.get('user') == 'master':
            os.system("rm /tmp/table.csv")
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getReport')
            data = cursor.fetchall()
            conn.commit()
            os.system("mv /tmp/table.csv /var/www/FlaskApp/FlaskApp/static/")
            return redirect('/static/table.csv')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/getCaseReport')
def getCaseReport():
    try:
        if session.get('user') == 'master':
            os.system("rm /tmp/case.csv")
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_getCaseReport')
            data = cursor.fetchall()
            conn.commit()
            os.system("mv /tmp/case.csv /var/www/FlaskApp/FlaskApp/static/")
            return redirect('/static/case.csv')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/showAddWish')
def showAddWish():
    if session.get('user'):
        return render_template('addWish.html')
    else:
        return render_template('error.html',error = 'Unauthorised Access')

@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()

@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
 
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
 
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
 
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


if __name__ == '__main__':
    app.run(debug = True)
