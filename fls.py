#!/usr/bin/env python

# @author Robley Adrian < robleyadrian@gmail.com > <  +254 722 161 224 >
# @copyright 2015
# @license

# requires python 2.7.5+

## to install flask
# pip install flask  

## to install MySQLdb
# apt-get install python-mysqldb

from flask import Flask, render_template, request, redirect, json, session
from flask.ext.mysql import MySQL
import MySQLdb, time

fls = Flask(__name__)

fls.secret_key = 'secret'

my = MySQL()

# Database configuration

fls.config['MYSQL_DATABASE_USER'] = 'root'
fls.config['MYSQL_DATABASE_PASSWORD'] = 'toor'
fls.config['MYSQL_DATABASE_DB'] = 'flsk'
fls.config['MYSQL_DATABASE_HOST'] = 'localhost'

# initialize app

my.init_app(fls)



# index.html, 1st page to load

@fls.route('/')
def main_page():
	return render_template("index.html")

# after clicking register button
# the info submitted to the form is received by this fucntion

@fls.route('/reg', methods=['POST'])
def reg():


	# receive data from HTML form
	name = request.form['username']
	password = request.form['password']
	gender = request.form['gender']
	fname = request.form['fname']
	lname = request.form['lname']

	# connect to database
	conn = my.connect()

	# create cursor
	cur = conn.cursor()

	#check if the user exists first

	# insert into database
	cur.execute("""INSERT INTO users(u_fname, u_lname, u_name, u_passwd, u_gender) VALUES(%s,%s,%s,%s,%s)""",(fname,lname,name, password, gender))

	# commit changes
	conn.commit()

	# close connection
	conn.close()

	# write the details to a file, optional
	# f = open('dets.txt','a+')
	# f.write('First Name: %s\n'%(fname))
	# f.write('Last Name: %s\n'%(lname))
	# f.write('Username: %s\n'%(name))
	# f.write('Password: %s\n\n'%(password))
	# f.write('Gender: %s\n\n'%(gender))
	# f.close()

	msg="Your details have been submitted successfully. You can now login below"

	return render_template('lgnpg.html',msg=msg)

# direct user to login page

@fls.route('/login')
def logn():
	return render_template('lgnpg.html')

# the actual login page where user will enter login credentials

@fls.route('/login-page', methods=['POST'])
def lgnpg():
	username=request.form['username']
	password=request.form['password']

	curr=my.connect().cursor()

	curr.execute("""SELECT * FROM users WHERE u_name=%s AND u_passwd=%s""",(username, password))

	data=curr.fetchall()

	if len(data)>0:
		nme=data[0][1]
		nme2=data[0][2]

		# set the session as the user ID
		session['user'] = data[0][0]

		# stor the user session ID in a variable
		x = session.get('user')
		return render_template('hme.html', usr=nme+" "+nme2)
	else:
		res="Wrong username or password. Try again."
		return render_template('lgnpg.html',msg=res)	

# the home page

@fls.route('/home')
def home():

	# check if there is a user logged in, i.e if session variable has been set
	if session.get('user'):
		return render_template('hme.html')
	else:
		err = "You are not authorised to see this"
		return render_template('err.html', err = err)

# show add wish page

@fls.route('/add')
def add():
	# check if there is a user logged in, i.e if session variable has been set
	if session.get('user'):
		return render_template('add.html')
	else:
		err = "You are not authorised to see this"
		return render_template('err.html', err = err)
	
# add wish into database

@fls.route('/addwish', methods=['POST'])
def addwish():
	u_id = session.get('user')
	title = request.form['title']
	content = request.form['content']

	connadd = my.connect()
	curradd = connadd.cursor()

	curradd.execute("""INSERT INTO wish (u_id, w_title, w_content) VALUES (%s,%s,%s)""",(u_id,title, content))

	connadd.commit()

	connadd.close()

	return render_template('add.html',msg="You wish has been received")


# view wishes page

@fls.route('/view')
def view():
	# check if there is a user logged in, i.e if session variable has been set
	if session.get('user'):

		u_id = session.get('user')
		# u_ids = str(u_id)
		connview = my.connect()
		currview = connview.cursor()

		currview.execute("""SELECT * FROM wish WHERE u_id = %s """,(u_id))

		ws = currview.fetchall()

		if len(ws)>0:
	
			t=ws[0][1]
			d=ws[0][2]


			return render_template('view.html',ti=t,de=d)
		else:
			return render_template('view.html',ti='Sorry', de='No wishes available for you')
	else:
		err = "You are not authorised to see this"
		return render_template('err.html', err = err)

# log out

@fls.route('/logout')
def logout():

	# delete session
	session.pop('user',None)
	msg = 'You have successfully logged out'
	return render_template('lgnpg.html', msg = msg)

if __name__ == '__main__':
	fls.run()
