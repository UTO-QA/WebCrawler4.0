from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, Response
from ASUCrawler import Crawler
from sqliteDB import sqliteDB;

app=Flask(__name__);

@app.route('/home')
@app.route('/')
def loginToCrawler():
	db=sqliteDB();
	rows=sqliteDB.getRuns(db);
	return render_template('index.html',rows=rows);
	
@app.route('/submit',methods=['POST'])	
def formDetails():
	
	print "In submit";
	#Get the username from the index page
	global username;
	username=request.form['username'];
	
	#Get the password
	global password;
	password=request.form['password'];
	
	#Get the website name
	global website
	website = request.form['website']
	
	return "Done"

@app.after_request
def	startCrawl(response):
	
	if request.endpoint=='formDetails':
		x=Crawler();
		rows=Crawler.performCrawl(x,website);
		x=render_template("Results.html",rows=rows);
		response.set_data(x);
	return response;

@app.route('/getResults')	
def getResults():
	db=sqliteDB();
	rows=sqliteDB.getRuns(db);
	return render_template("showResults.html",rows=rows);

@app.route('/displayResults',methods=["POST"])	
def displayResults():
	db=sqliteDB();
	run_id=request.form['run_id'];
	rows=sqliteDB.getResults(db,run_id);
	return render_template("Results.html",rows=rows,run_id=run_id);	

@app.route('/writeResults',methods=["POST"])
def writeResults():
	x=Crawler();
	run_id=request.form['run_id'];
	message=Crawler.writeResults(x,run_id);
	return render_template("WriteToFile.html",message=message);
	
	
if __name__=="__main__":	
	app.run();