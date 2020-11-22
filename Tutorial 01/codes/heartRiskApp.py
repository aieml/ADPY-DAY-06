from flask import Flask,render_template,request
import keras.models as models
import keras.layers as layers
import keras.optimizers as optimizers
from keras.layers import Dropout
import numpy as np
from keras import backend as K
import joblib

scalerX=joblib.load('scaler_x.sav')
scalerY=joblib.load('scaler_y.sav')

def loadModel():

	model = models.Sequential()
	model.add(layers.Dense(128, input_dim=8, kernel_initializer='normal', activation='relu'))
	model.add(Dropout(0.2))
	model.add(layers.Dense(128, activation='relu'))
	model.add(Dropout(0.2))
	model.add(layers.Dense(10, activation='relu'))
	model.add(layers.Dense(1, activation='linear'))

	model.compile(optimizer='adam',loss='mse',metrics=['mse','mae'])

	model.load_weights('Predictions.h5')

	return model

app=Flask(__name__) #application

@app.route('/')
def index():

	return render_template('patientdetails.html')

@app.route('/getresults',methods=['POST'])
def getresults():

	result=request.form 

	name=result['name']
	gender=result['gender']
	age=float(result['age'])
	tc=float(result['tc'])
	hdl=float(result['hdl'])
	sbp=float(result['sbp'])
	smoke=float(result['smoke'])
	bpm=float(result['bpm'])
	diab=float(result['diab'])

	test_data=[gender,age,tc,hdl,sbp,smoke,bpm,diab]

	K.clear_session()		#clearing the keras/tensorflow backend memory is mandotory before getting a new prediction(in Flask)
	
	model=loadModel()

	test_data=scalerX.transform([test_data])

	prediction=model.predict(test_data)

	prediction=scalerY.inverse_transform(prediction)

	resultDict={"name":name,"risk":round(prediction[0][0],2)}

	return render_template('results.html',results=resultDict)

app.run(debug=True)