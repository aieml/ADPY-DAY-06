from flask import Flask,render_template

app=Flask(__name__) #application

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/page1')
def page1():

	return render_template('testpage1.html')

app.run(debug=True)