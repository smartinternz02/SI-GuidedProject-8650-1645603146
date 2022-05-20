
from flask import Flask, render_template, request
# used to run/serve our application
# render_template is used for rendering the html pages
#import load from joblib to load the saved model file
from joblib import load


import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MJhw-Om3qDR-sME9fVwqf2_6c0vqPN2C_7f2-ye_9-v9"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/09100084-e9c0-4ddd-844b-d3ce69c83efa/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())




app=Flask(__name__) # our flask app
#load model file
model =load('floods.save')
sc=load('transform.save')


@app.route('/') # rendering the html template
def home():
    return render_template('home.html')
@app.route('/predict') # rendering the html template
def index() :
    return render_template("index.html")


@app.route('/data_predict', methods=['POST']) # route for our prediction
def predict():
    temp = request.form['temp']
    Hum = request.form['Hum']
    db = request.form['db']
    ap = request.form['ap']
    aa1 = request.form['aa1']

    data = [[float(temp),float(Hum),float(db),float(ap),float(aa1)]]
    #prediction = model.predict(sc.transform(data))
    #output=prediction[0]
    
    
    payload_scoring = {"input_data": [{"field": ['temp','hum','db','ap','aa1'], "values":data }]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/53b92894-458e-412c-8f3c-7c2424b545e3/predictions?version=2022-03-07', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions=response_scoring.json()
    print(predictions)
    print(response_scoring.json())


    output= predictions['predictions'][0]['values'][0][0]
    
    
    if(output==0):
        return render_template('noChance.html', prediction='No possibility of severe flood')
    else:
        return render_template('chance.html', prediction='possibility of severe flood')

if __name__ == '__main__':
    app.run(port=5000,debug=True,use_reloader=False)
