# essential Flask modules
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect
# for reading the config file
import yaml
# for generating SQL queries in pure Python
import sql
# for interfacing with the PostgreSQL database
import psycopg2
# for generating JSON to send to the client
import json

from StudentDatabase import StudentDatabase


# create the flask app
app = Flask( __name__ )

sdb = StudentDatabase( "host", "dbName", "user", "pass" )


# a simple hello world route
@app.route( '/' )
def hello():
	return( "<h1><marquee>Hello, world!</marquee></h1>" )


# another route demoing how to use the request parameters
# try "http://localhost:5555/args?1=2&three=four"
@app.route( '/args' )
def returnArgs():
	return( str( request.args ) )


#################
# Server routes #
#################


##########################
# Admin interface routes #
##########################

@app.route( '/login', methods=['GET', 'POST'] )
def login():
	"""
	Responds with a web form to login and grants a session on successful login.
	"""
	# hard-coded password for now, will migrate out later
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		session['login'] = True
		return redirect( '/users' )

	return render_template(
		"main.html",
		title="Login",
		head="head.html",
		header="header.html",
		body=request.path,
		footer="footer.html" )


@app.route( '/users', methods=['GET'] )
def users():
	"""
	This route will display the list of currently registered users, along with
	their authorizations, registration dates, and other info.
	"""
	return render_template(
		"main.html",
		title="Users",
		head="head.html",
		header="header.html",
		body=request.path,
		footer="footer.html" )


@app.route( '/users/add', methods=['POST'] )
def addUser():
	"""
	Accepts a request to add a user to the database.
	"""

	try:
		sdb.add_user(
			request.form['card_id'],
			request.form['uw_id'],
			request.form['uw_netid'],
			request.form['first_name'],
			request.form['last_name'] )
		return render_template( "main.html", body="OK" )
	except:
		return render_template( "main.html", body="Error adding user" ), 500


@app.route( '/users/delete', methods=['POST'] )
def deleteUser():
	"""
	Deletes a user from the database.
	"""
	return request.path


@app.route( '/users/authorize', methods=['POST'] )
def authorizeUser():
	"""
	Adds an authorization to a specified user.
	"""
	return request.path


#########################
# User interface routes #
#########################

@app.route( '/users/new', methods=['GET'] )
def newUser():
	"""
	Responds with a webform to add a new user.
	"""
	return render_template(
		"main.html",
		title="New User",
		head="head.html",
		header="header.html",
		body=request.path,
		footer="footer.html" )


##################################
# Card terminal interface routes #
##################################

@app.route( '/users/swipe', methods=['GET'] )
def checkUserAuthorization():
	return request.path


# run the app if the namespace is main
if __name__ == '__main__':
	with open( 'config.yaml' ) as f:
		config = yaml.load( f )

	# makes your life easier
	app.debug = True
	# lol using the flask default secret KEY
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	# and, run the app
	app.run( port=config['serverPort'] )
	# if you get errors, make sure to make a copy of `config_default.yaml` and
	# call it `config.yaml`
