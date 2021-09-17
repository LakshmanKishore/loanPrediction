from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html',hideresult="hidden")

@app.route('/predict',methods=['POST'])
def predict():
    data=dict(request.form)

    Gender = 1 if data["Gender"][0]=="male" else 0
    Married = 1 if data["Married"][0]=="yes" else 0
    if data["Dependents"][0]=="0":
        Dependents = 0
    elif data["Dependents"][0]=="1":
        Dependents = 1
    elif data["Dependents"][0]=="2":
        Dependents = 2
    else:
        Dependents = 3
    Education = 0 if data["Education"][0]=="Graduate" else 1
    Self_Employed = 1 if data["Self_Employed"][0]=="s_yes" else 0
    LoanAmount = np.log(int(data["LoanAmount"][0]))
    Loan_Amount_Term = np.log(int(data["Loan_Amount_Term"][0]))
    Credit_History = 1 if data["Credit_History"][0]=="c_yes" else 0
    if data["Property_Area"][0]=="Rural":
        Property_Area = 0
    elif data["Property_Area"][0]=="Semiurban":
        Property_Area = 1
    else:
        Property_Area = 2
    TotalIncome = np.log(int(data["ApplicantIncome"][0])+int(data["CoapplicantIncome"][0]))

    predictionData = [Gender,Married,Dependents,Education,Self_Employed,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,TotalIncome]
    result = model.predict([predictionData])
    if result[0]==1:
        result = "will"
    else:
        result = "will not"
    return render_template("index.html",hideform = "hidden",result=result)

if __name__=="__main__":
    app.run(debug=True)