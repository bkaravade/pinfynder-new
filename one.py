from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import pandas as pd
import json


one = Flask(__name__) # one Init
mail = Mail(one) # Mail Init

# Mail Config
one.config['MAIL_SERVER']='mail.spellsys.tech'
one.config['MAIL_PORT'] = 465
one.config['MAIL_USERNAME'] = 'demo@spellsys.tech'
one.config['MAIL_PASSWORD'] = 'DemoMail@12'
one.config['MAIL_USE_TLS'] = False
one.config['MAIL_USE_SSL'] = True
mail = Mail(one)

# Read data convert into Json Format
rdata = pd.read_csv('PincodeData.csv', sep=",")
pindata = rdata.to_json(orient = 'records')
pindata = json.loads(pindata)

# Function will return Pincode json 
def fid_details(code):
   return_elements_list = []
   for i in pindata:
      if i['Pincode'] == int(code):
         return_elements_list.oneend(i)

   if len(return_elements_list) == 0:
      return_elements_list = [{
         'Message': 'Record Not Found',
         'Error': 'Custom Error',
         'Hint': 'Check Pincode'
      }]
   return return_elements_list

# Function will return Postoffice Json
def fid_PostName(PostName):
   return_elements_list = []
   # print(PostName)
   for i in pindata:
      if (PostName in i['Place / City / Area']):
         return_elements_list.oneend(i)
   
   if len(return_elements_list) == 0:
      return_elements_list = [{
         'Message': 'Record Not Found',
         'Error': 'Custom Error',
         'Hint': 'Check Post Office Name'
      }]
   return return_elements_list



@one.route('/api', methods = ['GET', 'POST'])
def api():
   return jsonify({ 'Pincode': pindata})

#  API Data From Pincode<int>
@one.route('/api/<int:pcode>', methods = ['GET', 'POST'])
def api_code(pcode):
      return jsonify({ 'Pincode': fid_details(pcode) })

# API Data From PostName<string>
@one.route('/api/<string:postName>', methods = ['GET', 'POST'])
def api_name(postName):
      return jsonify({ 'Pincode': fid_PostName(postName) })

@one.route('/')
def index():
   return render_template('index.html')

@one.route('/name')
def pname():
   return render_template('name.html')

@one.route('/code')
def hello_world():
   return render_template('code.html')

@one.route('/getCode', methods = ['POST'])
def getPincode():
   output = request.form.to_dict()
   code = output['code']
   if len(code) == 6 and code.isnumeric():
      return render_template('code.html', name = fid_details(code))
   else:
      return render_template('code.html', name1 = 'Pincode Length Should be 6 Numbers Not Characters!')

@one.route('/getPin',  methods = ['POST'])
def getPin():
   output = request.form.to_dict()
   name = output['name']
   if name.isnumeric():
      return render_template('name.html', name1 = 'PostName Should be String and case Sensitive!')
   else:
      # print(type(name)) 
      return render_template('name.html', name = fid_PostName(name))
      


@one.route('/send-mail', methods = ['GET','POST'])
def send():
   data = request.get_json()
   msg = Message(
                'Hello! Pinfynder Mail from ' + data['name'] ,
                sender = data['email'],
                recipients = ['karawadeballal@gmail.com' , 'raddibasket05@gmail.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'+ '\n' + data['msg'] + '\nPhoneNO: '+ data['pno'] + '\n'
   mail.send(msg)
   return 'Mail has been sent. Thank You!'


@one.route('/ballal', methods=['GET', 'POST'])
def hello_ballal():
   data = request.get_json()
   return data['name']




one.run(debug = True, port=5000)

# if __name__ == '__main__':

# 	one.run()
