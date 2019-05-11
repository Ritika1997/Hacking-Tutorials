from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from flask_mail import Mail, Message
app = Flask(__name__) 
mail = Mail(app)

from sqlalchemy import create_engine, asc, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from database_setup import Base, Logindata, Verify, Bankdata

from flask import session as login_session
import random, string

from hackernews import HackerNews
hn = HackerNews()

#Connect to Database and create database session
engine = create_engine('sqlite:///login.db',poolclass=SingletonThreadPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    if 'user' in login_session:
        show = "display: none;"
        hide = "display: inline-block;"
        user = login_session['user']
        return render_template('index.html', show = show, hide = hide, user = user)
    else:
        show = "display: inline-block;"
        hide = "display: none;"
        return render_template('index.html', show = show, hide = hide, user = "")

@app.route('/courses', methods=['GET','POST'])
def showCourses():
    if request.method == 'POST':
        show = "display: none;"
        hide = "display: inline-block;"
        user = login_session['user']
        trans_id = ''.join(random.choice(string.ascii_uppercase+string.digits)for x in xrange(32))
        if 'cardno' in request.form:
            ctype = request.form['coursetype2']
            cardname = request.form['cardname']
            cardno = request.form['cardno']
            exm = request.form['mm']
            exy = request.form['yyyy']
            cvv = request.form['cvv']
            trans_type = 'credit card'
            amt = courseAmt(ctype)
            newTrans = Bankdata(trans_id=trans_id,user=user,name=cardname,cardno=cardno,expirym=exm,expiryy=exy,cvv=cvv,trans_type=trans_type,coursetype=ctype,amount=amt)
        else:
            ctype = request.form['coursetype1']
            trans_type = 'net banking'
            bank = request.form['bank']
            amt = courseAmt(ctype)
            newTrans = Bankdata(trans_id=trans_id,user=user,bank=bank,trans_type=trans_type,coursetype=ctype,amount=amt)
        session.add(newTrans)
        session.commit()
        login_session['coursetype'] = ctype
        return render_template('courses.html', msg = "Purchase Successfull", show = show, hide = hide, user = user)
    else:
        if 'user' in login_session:
            show = "display: none;"
            hide = "display: inline-block;"
            user = login_session['user']
            return render_template('courses.html', msg = "", show = show, hide = hide, user = user)
        else:
            show = "display: inline-block;"
            hide = "display: none;"
            return render_template('courses.html', msg = "", show = show, hide = hide, user = "")
        


def courseAmt(ctype):
    if(ctype == 'STARTER'):
        return '19'
    elif(ctype == 'STANDARD'):
        return '23'
    else:
        return '39'

@app.route('/login', methods=['GET','POST'])
def showLogin():
    if request.method == 'POST':
        if 'email' in request.form:
            user = request.form['username']
            passwd = request.form['pass']
            email = request.form['email']
            newUser = Logindata(user=user,email_id=email,passwd=passwd)
            session.add(newUser)
            token = ''.join(random.choice(string.ascii_uppercase+string.digits)for x in xrange(32))
            newToken = Verify(email_id=email,token=token,verified='n')
            session.add(newToken)
            session.commit()
            login_session['user'] = user
            login_session['email'] = email
            login_session['token'] = token
            return redirect(url_for('home'))
        else:
            user = request.form['user']
            passwd = request.form['password']
            logindata = session.query(Logindata).filter_by(user=user).filter_by(passwd=passwd).first()
            if logindata is not None:
                bankdata = session.query(Bankdata).filter_by(user=user).first()
                login_session['coursetype'] = bankdata.coursetype
                login_session['user'] = logindata.user
                login_session['email'] = logindata.email_id
                return redirect(url_for('home'))
            else:
                return render_template('login.html',errormsg = "Username/Password is incorrect.")    
    else:
        return render_template('login.html',errormsg = "")


@app.route('/news')
def showNews():
    top = hn.top_stories()
    data = {}
    for i in top[0:10]:
        data[hn.get_item(i).title] = hn.get_item(i).url
    return render_template('news.html', data = data)

@app.route('/profile', methods=['GET','POST'])
def showProfile():
    user = login_session['user']
    if 'coursetype' in login_session:
        ctype = "Opted for "+str(login_session['coursetype'])+" Course"
    else:
        ctype = "No Course Opted"
    editedUser = session.query(Logindata).filter_by(user=user).first()
    if request.method == 'POST':
        if 'olduser' in request.form:
            olduser = request.form['olduser']
            newuser = request.form['newuser']
            editedUser.user = newuser
            login_session['user'] = newuser
            user = newuser
        else:
            oldpass = request.form['oldpass']
            editedUser.passwd = request.form['newpass']
        flash('Updated Successfully.')
        session.add(editedUser)
        session.commit()
        return render_template('profile.html', user = user, show="block", ctype = ctype)
    else:
        return render_template('profile.html', user = user, show="none", ctype = ctype)

@app.route('/logout')
def logout():
    login_session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 2999)
