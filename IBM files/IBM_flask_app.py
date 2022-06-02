import requests
from os import stat
import json
from flask import Flask, render_template, request, url_for, redirect
import pickle
from sklearn.preprocessing import StandardScaler
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
with open('API_KEY.json') as f:
    data = json.load(f)
API_KEY = data["API_KEY"]
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + mltoken}

# -----------------------

app = Flask(__name__)
myscaler = pickle.load(open("scaler.pkl", "rb"))


@app.route('/')  # url binding
def loadhome():
    return render_template("homepage.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template("prediction.html")


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return redirect(url_for('form'))


@app.route('/submit', methods=['POST'])  # url binding
def user():
    Education = request.form["Education"]
    ApplicantIncome = request.form["ApplicantIncome"]
    Coapplicant = request.form["Co-applicant"]
    LoanAmount = request.form["LoanAmount"]
    LoanAmountTerm = request.form["Loan-Amount-Term"]
    CreditHistory = request.form["Credit-History"]
    dependents = request.form["dependents"]
    property = request.form["property"]
    if Education == "Graduate":
        se = 0
    else:
        se = 1
    if dependents == "0":
        s1, s2, s3, s4 = 0, 0, 0, 1
    elif dependents == "1":
        s1, s2, s3, s4 = 0, 0, 1, 0
    elif dependents == "2":
        s1, s2, s3, s4 = 0, 1, 0, 0
    elif dependents == "3+":
        s1, s2, s3, s4 = 1, 0, 0, 0
    if property == "Rural":
        sp1, sp2, sp3 = 0, 0, 1
    elif property == "Semi-urban":
        sp1, sp2, sp3 = 0, 1, 0
    elif property == "Urban":
        sp1, sp2, sp3 = 1, 0, 0
    # Education, Applicant Income, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, dependents(4), property(3)

    arrayofinputs = [[float(se), float(ApplicantIncome), float(Coapplicant), float(
        LoanAmount), float(LoanAmountTerm), float(CreditHistory), float(s1), float(s2), float(s3), float(s4), float(sp1), float(sp2), float(sp3)]]
    t = myscaler.transform(arrayofinputs)
    print(t)
    print(type(t))
    payload_scoring = {"input_data": [{"values": t.tolist()}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/00b5287b-b674-435e-9403-da3cf0440196/predictions?version=2022-05-31', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    # predictions
    y = response_scoring.json()['predictions'][0]['values'][0][0]
    print(y)
    if str(y) == '1':
        status = 'approved'
    else:
        status = 'rejected'
    return render_template("result.html", output="The Loan status is "+status)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
