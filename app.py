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
    data=request.form.to_dict()

    Gender = 1 if data["Gender"]=="male" else 0
    Married = 1 if data["Married"]=="yes" else 0
    if data["Dependents"]=="0":
        Dependents = 0
    elif data["Dependents"]=="1":
        Dependents = 1
    elif data["Dependents"]=="2":
        Dependents = 2
    else:
        Dependents = 3
    Education = 0 if data["Education"]=="Graduate" else 1
    Self_Employed = 1 if data["Self_Employed"]=="s_yes" else 0
    LoanAmount = np.log(int(data["LoanAmount"]))
    Loan_Amount_Term = np.log(int(data["Loan_Amount_Term"]))
    Credit_History = 1 if data["Credit_History"]=="c_yes" else 0
    if data["Property_Area"]=="Rural":
        Property_Area = 0
    elif data["Property_Area"]=="Semiurban":
        Property_Area = 1
    else:
        Property_Area = 2
    TotalIncome = np.log(int(data["ApplicantIncome"])+int(data["CoapplicantIncome"]))

    predictionData = [Gender,Married,Dependents,Education,Self_Employed,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,TotalIncome]
    result = model.predict([predictionData])
    if result[0]==1:
        result = "will"
    else:
        result = "will not"
    return render_template("index.html",hideform = "hidden",result=result)

if __name__=="__main__":
    app.run(debug=True)