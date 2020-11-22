from flask import Flask

app=Flask(__name__) #application

@app.route('/')
def index():

	return("This is my First App in Flask")

@app.route('/testpage')
def testpage():

	return("This is the test page")


app.run(debug=True)