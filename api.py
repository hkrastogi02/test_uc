import os
import boto3
import uuid
import random
import requests
from flask import Flask
from flask import Response, Request, request, json,jsonify,url_for
from flask_restful import Resource, Api
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from locale import str
from datetime import datetime,timezone
import pytz
from flask_bcrypt import Bcrypt
from flask import render_template
from flask_mail import Mail, Message
from boto3.dynamodb.conditions import Key, Attr


app = Flask(__name__)
api = Api(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sourcesoft.developer@gmail.com'
app.config['MAIL_PASSWORD'] = '!!#$124><RTTq1'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
UPLOAD_FOLDER='/var/www/html/htdoc/ucracy/public/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGEPATH="http://148.76.75.204/ucracy/public/uploads/"
NOIMAGEPATH="http://148.76.75.204/ucracy/public/uploads/noimage.png"
DOCPATH="http://148.76.75.204/ucracy/public/uploads/documents/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail = Mail(app)
bcrypt = Bcrypt(app)
now = datetime.utcnow()
timestamp = int(datetime.now(tz=pytz.utc).timestamp() * 1000) 
#int(datetime.now().timestamp())
#int(datetime.now().timestamp())
#int(datetime.now().strftime("%s")) * 1000 
#dynamodb = boto3.resource('dynamodb')
dynamodb = boto3.resource('dynamodb',region_name='us-east-2',aws_access_key_id='AKIASCYB3IX4GPRNBVXZ',
aws_secret_access_key= '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')

@app.route('/')
@app.route('/<name>')

def hello(name=None):
	return "naveen Kumar here write webservices"
	
@app.route("/api/signup", methods=['POST'])

def signup():
	
	table = dynamodb.Table('user')
	
	username = request.json.get('username'),
	email = request.json.get('email'),
	password = request.json.get('password')
			
	response = table.get_item(
		Key={'email':request.json.get('email').lower() }
		)
	item = response.get('Item')
	if (item):

		data = {
			'message':"This user is already exist",
			'response':{}
			}

		js = json.dumps(data)
		resp  = app.response_class(
		response=json.dumps(data),
		status=400,
		mimetype='application/json'
	)
		return resp

	else:
		#pw_hash = bcrypt.generate_password_hash(request.json.get('password'))
		pw_hash =request.json.get('password')
		table.put_item(
	Item={
		'id':uuid.uuid4().hex,
		'username': request.json.get('username'),
		'email': request.json.get('email').lower(),
		'password': pw_hash,
		'utype':1,
		'status':True,
		'date':int(datetime.now(tz=pytz.utc).timestamp() * 1000)
		
		}
)

		msg = Message('Thanks for join with us', sender = request.json.get('email'), recipients = [request.json.get('email')])
		msg.body = "Thanks for join with us"
		mail.send(msg)
		data = {
			'message':"User registered successfully",
			'response':""
			}

		js = json.dumps(data)
		resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
		return resp

# forgot password

@app.route("/api/recoverpassword", methods=["POST"])
def recoverpassword():
	table = dynamodb.Table('user')
	email = request.json.get('email'),
	response = table.get_item(
		Key={'email':request.json.get('email').lower() }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user email which you have provide",
			'response':{}

		}
		js = json.dumps(data)
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		msg = Message('Your password is ', sender = request.json.get('email'), recipients = ['naveenk@sourcesoftsolutions.com'])
		msg.body = "Hello "+item.get('username')+" n your password is  "+item.get('password')+" you can login now."
		mail.send(msg) 
		data = {
			'message':"Password has been send your email id ,Please check you email.",
			'response':{}
			}


		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp

@app.route("/api/login", methods=["POST"])
def login():
	table = dynamodb.Table('user')
	email = request.json.get('email'),
	password = request.json.get('password')
	response = table.get_item(
		Key={'email':request.json.get('email').lower() }
		)
	item = response.get('Item')
	if not item:
		data = {
			'message':"Invalid user email which you have provide",
			'response':{}
			}

		js = json.dumps(data)
		resp  = app.response_class(
		response=json.dumps(data),
		status=400,
		mimetype='application/json'
	)
		return resp
		
	else:
		# if bcrypt.check_password_hash(item.get('password'), request.json.get('password')):
		if item.get('password') == request.json.get('password'):
			data = {
			'message':"Login has been sucessfully ",
			'response':{
			'id':item.get('id') and item.get('id') or "",
			'username':item.get('username'),
			'email':item.get('email').lower(),
			'status':item.get('status') and item.get('status') or False,
			'image':item.get('image') and IMAGEPATH+item.get('image') or "",
			'utype':int(item.get('utype')) and int(item.get('utype')) or "",
			'document':item.get('document') and DOCPATH+item.get('document') or "",
			'docstatus':item.get('docstatus') and item.get('docstatus') or "false",
			'country':item.get('country') and item.get('country') or "",
			'uregion':item.get('uregion') and item.get('uregion') or "",
			'city':item.get('city') and item.get('city') or "",
			'area':item.get('area') and item.get('area') or "",
			
			}
			}


			js = json.dumps(data)
			resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
			return resp
			
		
		else:
			data = {
			'message':"Invalid user email which you have provide",
			'response':""
			}
			js = json.dumps(data)
			resp  = app.response_class(
				response=json.dumps(data),
				status=400,
				mimetype='application/json'
			  )
		return resp

		
@app.route("/api/countrylist", methods=['get'])
def countrylist():
	params = {"positions":[0,6,7,29]}
	r = requests.get("http://battuta.medunes.net/api/country/all/?key=4b23e6bb381c99fed8eeb061784cb09e")

	#print(r.status_code)
	#print(r.json())
	#return r.json()
	data = {
			'message':"Country list are",
			'response':r.json()
			}
	js = json.dumps(data)
	resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return resp

@app.route("/api/regionbycountry", methods=['POST'])
def regionbtcountrycode():
	countrycode = request.json.get('country_code'),
	r = requests.get("http://battuta.medunes.net/api/region/"+ request.json.get('country_code') +"/all/?key=4b23e6bb381c99fed8eeb061784cb09e")
	#print(r.status_code)
	#print(r.json())
	#return r.json()
	data = {
			'message':"Region  list are",
			'response':r.json()
			}
	js = json.dumps(data)
	resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return resp      
	
@app.route("/api/citybyregion", methods=['POST'])
def citybtregion():
	countrycode = request.json.get('regionname'),
	r = requests.get("http://battuta.medunes.net/api/city/in/search/?region="+ request.json.get('regionname')+"&key=4b23e6bb381c99fed8eeb061784cb09e")
	#print(r.status_code)
	#print(r.json())
	#return r.json()
	data = {
			'message':"City list are",
			'response':r.json()
			}
	js = json.dumps(data)
	resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	return resp 

#get user address details by using email
@app.route("/api/profile", methods=["POST"])
def address():
	table = dynamodb.Table('user')
	email = request.json.get('email'),
	response = table.get_item(
		Key={'email':request.json.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user email which you have provide",
			'response':{}

		}
		js = json.dumps(data)
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:

		data = {'message':"User  Details are ",
		'response':{
			'id':item.get('id') and item.get('id') or "",
			'username':item.get('username'),
			'email':item.get('email'),
			'utype':int(item.get('utype')) and int(item.get('utype')) or "",
			'image':item.get('image') and IMAGEPATH+item.get('image') or "",
			'document':item.get('document') and DOCPATH+item.get('document') or "",
			'country':item.get('country') and item.get('country') or "",
			'uregion':item.get('state') and item.get('uregion') or "",
			'city':item.get('city') and item.get('city') or "",
			'area':item.get('area') and item.get('area') or "",
			
			}
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
		
#uddate address by user email
@app.route("/api/updateaddress", methods=["POST"])
def updateaddress():
	table = dynamodb.Table('user')
	email = request.json.get('email'),
	utype = request.json.get('utype'),
	country = request.json.get('country'),
	uregion = request.json.get('uregion'),
	city = request.json.get('city'),
	area = request.json.get('area'),
	response = table.get_item(
		Key={'email':request.json.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user email which you have provide",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:

		res=table.update_item(
	Key={'email':request.json.get('email')},
	UpdateExpression='SET utype=:val1, country=:val2, city=:val3, area=:val4, uregion=:val5 ',
	ExpressionAttributeValues={
		':val1': request.json.get('utype'),
		':val2': request.json.get('country') and request.json.get('country') or "",
		':val3': request.json.get('city') and request.json.get('city') or " ",
		':val4': request.json.get('area') and request.json.get('area') or "",
		':val5': request.json.get('uregion') and request.json.get('uregion') or "",
	}
)

		newresponse = table.get_item(
		Key={'email':request.json.get('email') }
		)
		newitem = newresponse.get('Item')
		data = {'message':"User address update successfully",
		'response':{
			'id':newitem.get('id') and newitem.get('id') or "",
			'username':newitem.get('username'),
			'email':item.get('email'),
			'utype':int(newitem.get('utype')) and int(newitem.get('utype')) or "",
			'image':newitem.get('image') and IMAGEPATH+newitem.get('image') or "",
			'document':newitem.get('document') and DOCPATH+newitem.get('document') or "",
			'docstatus':item.get('docstatus') and item.get('docstatus') or "false",
			'country':newitem.get('country') and newitem.get('country') or "",
			'uregion':newitem.get('state') and newitem.get('uregion') or "",
			'city':newitem.get('city') and newitem.get('city') or "",
			'area':newitem.get('area') and newitem.get('area') or "",
			
			}
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp



@app.route("/api/signup_test", methods=['POST'])

def signup234():
	data = {}
	result={}
	table = dynamodb.Table('user')
	username = request.json.get('username'),
	email = request.json.get('email'),
	password = request.json.get('password')
	
	
	data = {
			'message':"dddd",
			'response':[
			{'name':'india',
					'abf':'ddd'
			},
			{'name':'pakistian'},
			{'name':'US'},
			{'name':'UK'},
			{'name':'NZ'}
			]


	}


	js = json.dumps(data)

	resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
	
	

	return resp
#allowed extension image and document    
def allowed_file(filename):

	return '.' in filename and \
	filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS    

@app.route('/api/uploadimage', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		table = dynamodb.Table('user')
		file = request.files['file']
		email=request.form.get('email')
		response = table.get_item(
		Key={'email':request.form.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user which you have provide",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		
		if file and allowed_file(file.filename):
			
			filename = str(random.randint(1,10000000))+secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			table.update_item(
	Key={'email': request.form.get('email')},
	UpdateExpression='SET image = :val1',
	ExpressionAttributeValues={
		':val1': filename
	}
)
			data = {
			'message':"Image upload successfully ",
			'response':{"profileimage":IMAGEPATH+filename}
			}

			js = json.dumps(data)
			resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
			return resp
		else:
			data = {

			'message':"Image format not support",
			'response':{}
			}

			js = json.dumps(data)
			resp  = app.response_class(
		response=json.dumps(data),
		status=400,
		mimetype='application/json'
	)
			return resp
					
#upload documents
@app.route('/api/documents', methods=['POST'])
def upload_documents():
	if request.method == 'POST':
		table = dynamodb.Table('user')
		file = request.files['file']
		email=request.form.get('email')
		response = table.get_item(
		Key={'email':request.form.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user which you have provide",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		
		if file and allowed_file(file.filename):
			
			filename = str(random.randint(1,10000000))+secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER']+"documents", filename))
			table.update_item(
	Key={'email': request.form.get('email')},
	UpdateExpression='SET document = :val1',
	ExpressionAttributeValues={
		':val1': filename
	}
)
			data = {
			'message':"Documents upload successfully ",
			'response':{"profileimage":IMAGEPATH+filename}
			}

			js = json.dumps(data)
			resp  = app.response_class(
		response=json.dumps(data),
		status=200,
		mimetype='application/json'
	)
			return resp
		else:
			data = {

			'message':"Doucments format not support",
			'response':{}
			}

			js = json.dumps(data)
			resp  = app.response_class(
		response=json.dumps(data),
		status=400,
		mimetype='application/json'
	)
			return resp

# Insert feeds by a user 
@app.route("/api/addfeeds", methods=["POST"])
def addfeed():
	table = dynamodb.Table('user')
	ftable= dynamodb.Table('feeds')
	email = request.json.get('email'),
	messase = request.json.get('message'),
   
	response = table.get_item(
		Key={'email':request.json.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'message':"Invalid user email which you have provide",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		if (request.json.get('message')):
			ftable.put_item(
	Item={
		'feedid':uuid.uuid4().hex,
		'message': request.json.get('message'),
		'email': request.json.get('email'),
		'fstatus':True,
		'date':int(datetime.now(tz=pytz.utc).timestamp() * 1000)
		}
)
		data = {
		'message':"Post has been create successfully",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
@app.route("/api/feeddetails",methods=["POST"])
def feeds_details():
	
	table= dynamodb.Table('feeds')
	email=request.json.get('email')
	feedid=request.json.get('feedid')
	response =table.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))& Key('email').eq(request.json.get('email'))
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"Invalid user",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		data = {'message':"Feed  Details are ",
		'response':{
			'feedid':item[0]['feedid'] and item[0]['feedid'] or "",
			'email':item[0]['email'] and item[0]['email'] or "",
			'message':item[0]['message'] and item[0]['message'] or "",
			'status':item[0]['fstatus'] and item[0]['fstatus'],
			'date': int(item[0]['date']) and int(item[0]['date']) ,
			
			}
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
#update feeds
# Insert feeds by a user 
@app.route("/api/updatefeed",methods=["POST"])
def updatefeeds():
	
	table= dynamodb.Table('feeds')
	email=request.json.get('email')
	feedid=request.json.get('feedid')
	message=request.json.get('message')
	response =table.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))& Key('email').eq(request.json.get('email'))
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"Invalid user",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		res=table.update_item(
		Key={'feedid':request.json.get('feedid')},
		UpdateExpression='SET message=:val1 ',
		ExpressionAttributeValues={
		':val1': request.json.get('message')
	}
)
	data = {'message':"User feeds update successfully",
		'response':{}
		}
	resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
	return resp
		
#Add like to feeds  by user 

@app.route("/api/addfavourite", methods=["POST"])
def addlike():
	table= dynamodb.Table('like')
	email = request.json.get('email')
	messase = request.json.get('feedid')
	status = request.json.get('status')
	response =table.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))& Key('email').eq(request.json.get('email'))
)
	item = response.get('Items')
	if not item:
		if (request.json.get('feedid')):
			table.put_item(
	Item={
		'feedid':request.json.get('feedid'),
		'id': uuid.uuid4().hex,
		'email': request.json.get('email'),
		'lstatus':request.json.get('status'),
		'date':int(datetime.now(tz=pytz.utc).timestamp() * 1000)
		}
)
			ltable = dynamodb.Table('like')
			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("true") & Key('feedid').eq(request.json.get('feedid'))
				)
			litem = response.get('Items')
			#print(len(litem))

			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("false") & Key('feedid').eq(request.json.get('feedid'))
				)
			Ulitem = response.get('Items')
			
			commtable = dynamodb.Table('comment')
			response =commtable.scan(
				FilterExpression= Key('feedid').eq(request.json.get('feedid'))
				)
			commitem = response.get('Items')
			response =ltable.scan(
				FilterExpression= Key('email').eq(request.json.get('email')) & Key('feedid').eq(request.json.get('feedid'))
				)
			myitem = response.get('Items')	
		data = {
		'message':"Record is save successfully",
			'response':{
			   "feedid":request.json.get('feedid'),
			   "feedstatus":True,
			   "feedmessage":"",
			   "date":int(datetime.now(tz=pytz.utc).timestamp() * 1000),
			   "email":request.json.get('email'),
			   "username":"",
			   "image":"",
			   "userid":"",
			   "usercountry":"",
			   "totallike":len(litem),
			   "totalunlike":len(Ulitem),
			   "totalcomments":len(commitem),
			   "userlikestatus":len(myitem)>0 and myitem[0]['lstatus'] or ""
			  }

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp	
		
	else:


		response =table.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))& Key('email').eq(request.json.get('email')) & Key('lstatus').eq(request.json.get('status'))
)

		aitem = response.get('Items')
		if len(aitem)>0:
			res=table.delete_item(
		Key={'feedid':request.json.get('feedid'),'email':request.json.get('email')}
)
			ltable = dynamodb.Table('like')
			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("true") & Key('feedid').eq(request.json.get('feedid'))
				)
			litem = response.get('Items')
			#print(len(litem))

			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("false") & Key('feedid').eq(request.json.get('feedid'))
				)
			Ulitem = response.get('Items')
			
			commtable = dynamodb.Table('comment')
			response =commtable.scan(
				FilterExpression= Key('feedid').eq(request.json.get('feedid'))
				)
			commitem = response.get('Items')
			response =ltable.scan(
				FilterExpression= Key('email').eq(request.json.get('email')) & Key('feedid').eq(request.json.get('feedid'))
				)
			myitem = response.get('Items') 


			resp  = app.response_class(
			response=json.dumps({'message':"User feeds like update successfully",
		'response':{
			   "feedid":request.json.get('feedid'),
			   "feedstatus":True,
			   "feedmessage":"",
			   "date":0,
			   "email":request.json.get('email'),
			   "username":"",
			   "image":"",
			   "userid":"",
			   "usercountry":"",
			   "totallike":len(litem),
			   "totalunlike":len(Ulitem),
			   "totalcomments":len(commitem),
			   "userlikestatus":len(myitem)>0 and myitem[0]['lstatus'] or ""
			  }
		}),
			status=200,
			mimetype='application/json'
			)
		#return resp

		else:
			res=table.update_item(
		Key={'feedid':request.json.get('feedid'),'email':request.json.get('email')},
		UpdateExpression='SET lstatus=:val1 ',
		ExpressionAttributeValues={
		':val1': request.json.get('status')
	}
)

			ltable = dynamodb.Table('like')
			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("true") & Key('feedid').eq(request.json.get('feedid'))
				)
			litem = response.get('Items')
			#print(len(litem))

			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("false") & Key('feedid').eq(request.json.get('feedid'))
				)
			Ulitem = response.get('Items')
			
			commtable = dynamodb.Table('comment')
			response =commtable.scan(
				FilterExpression= Key('feedid').eq(request.json.get('feedid'))
				)
			commitem = response.get('Items')
			response =ltable.scan(
				FilterExpression= Key('email').eq(request.json.get('email')) & Key('feedid').eq(request.json.get('feedid'))
				)
			myitem = response.get('Items')  
			
		resp  = app.response_class(
			response=json.dumps({'message':"User feeds update successfully",
		'response':{
			   "feedid":request.json.get('feedid'),
			   "feedstatus":True,
			   "feedmessage":"",
			   "date":0,
			   "email":request.json.get('email'),
			   "username":"",
			   "image":"",
			   "userid":"",
			   "usercountry":"",
			   "totallike":len(litem),
			   "totalunlike":len(Ulitem),
			   "totalcomments":len(commitem),
			   "userlikestatus":len(myitem)>0 and myitem[0]['lstatus'] or ""
			  }
		}),
			status=200,
			mimetype='application/json'
			)

		return resp
			
#comments section 
@app.route("/api/addComment", methods=["POST"])
def addComments():
	table= dynamodb.Table('comment')
	email = request.json.get('email')
	feedid = request.json.get('feedid')
	comment = request.json.get('comment')
	utable = dynamodb.Table('user')
	
	response = utable.get_item(
	
		Key={'email':request.json.get('email') }
		)
	uitem = response.get('Item')
	if (request.json.get('feedid')):
			table.put_item(
	Item={
		'feedid':request.json.get('feedid'),
		'commentid': uuid.uuid4().hex,
		'email': request.json.get('email'),
		'comment': request.json.get('comment'),
		'cstatus':True,
		'date':int(datetime.now(tz=pytz.utc).timestamp() * 1000)
		}
)
	data = {
		'message':"Comments is save successfully",
			'response':{
		'feedid':request.json.get('feedid'),
		'commentid': uuid.uuid4().hex,
		'email': request.json.get('email'),
		'comment': request.json.get('comment'),
		"username":uitem.get('username') and uitem.get('username') or "",
	    "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
	    "userid":uitem.get('id') and uitem.get('id') or "",
	    "usercountry":uitem.get('country')and uitem.get('country') or "",
	    "usercity":uitem.get('city') and uitem.get('city') or "",
	    "userarea":uitem.get('area') and uitem.get('area') or "",
		'cstatus':True,
		'date':int(datetime.now(tz=pytz.utc).timestamp() * 1000)
		}

		}
	resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
	return resp	

# comments details 
@app.route("/api/commentdetails",methods=["POST"])
def comment_details():
	
	table= dynamodb.Table('comment')
	email=request.json.get('email')
	commentid=request.json.get('commentid')
	response =table.scan(
	FilterExpression= Key('commentid').eq(request.json.get('commentid'))& Key('email').eq(request.json.get('email'))
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"Invalid details",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		data = {'message':"comments  Details are ",
		'response':{
			'id':item[0]['feedid'],
			'feedid':item[0]['feedid'] and item[0]['feedid'] or "",
			'email':item[0]['email'] and item[0]['email'] or "",
			'ucomment':item[0]['comment'] and item[0]['comment'] or "",
			'status':item[0]['cstatus'] and item[0]['cstatus'],
			'date': int(item[0]['date']) and int(item[0]['date']) ,
			
			}
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp	
#update comments
@app.route("/api/updatecomment",methods=["POST"])
def updatecomment():
	
	table= dynamodb.Table('comment')
	email=request.json.get('email')
	commentid=request.json.get('commentid')
	comment=request.json.get('comment')
	response =table.scan(
	FilterExpression= Key('commentid').eq(request.json.get('commentid'))& Key('email').eq(request.json.get('email'))
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"Invalid details provide",
			'response':{}

		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:


	    res=table.update_item(
		Key={'commentid':request.json.get('commentid'),'email':request.json.get('email')},
		UpdateExpression='SET lstatus=:val1 ',
		ExpressionAttributeValues={
		':val1': request.json.get('comment')
	}
)
	data = {'message':"User comment update successfully",
		'response':{}
		}
	resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
	return resp		

@app.route("/api/feedslist",methods=['POST'])
def feedlist():
	table= dynamodb.Table('feeds')
	email=request.json.get('email')
	response =table.scan(
	FilterExpression= Key('fstatus').eq(True)
	
	
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"No records found",
			'response':{}


		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		newdat=[]
		for x in range(len(item)): 
			newemail=item[x]["email"]
			newfeedid=item[x]["feedid"]
			utable = dynamodb.Table('user')
			response = utable.get_item(
				Key={'email':newemail }
				)
			uitem = response.get('Item')
			#print(uitem.get('username'))
			ltable = dynamodb.Table('like')
			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("true") & Key('feedid').eq(newfeedid)
				)
			litem = response.get('Items')
			#print(len(litem))

			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("false") & Key('feedid').eq(newfeedid)
				)
			Ulitem = response.get('Items')
			#print(len(Ulitem))

			response =ltable.scan(
				FilterExpression= Key('email').eq(request.json.get('email')) & Key('feedid').eq(newfeedid)
				)
			myitem = response.get('Items')
			#print(len(myitem))

			commtable = dynamodb.Table('comment')
			response =commtable.scan(
				FilterExpression= Key('feedid').eq(newfeedid)
				)
			commitem = response.get('Items')
			#print(len(commitem))
			nwelist={
			   "feedid":item[x]["feedid"],
			   "feedstatus":item[x]["fstatus"],
			   "feedmessage":item[x]["message"],
			   "date":int(item[x]["date"]),
			   "email":item[x]["email"],
			   "username":uitem.get('username') and uitem.get('username') or "",
			   "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
			   "userid":uitem.get('id') and uitem.get('id') or "",
			   "usercountry":uitem.get('country') and uitem.get('country') or "",
			   "totallike":len(litem),
			   "totalunlike":len(Ulitem),
			   "totalcomments":len(commitem)>0 and len(commitem) or 0,
			   "userlikestatus":len(myitem)>0 and myitem[0]['lstatus'] or ""
			   
			  }
			newdat.append(nwelist)
			#print(newdat)
		
		data = {'message':"Deed  Details are ",
		'response':newdat
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp




	# Function for get user feed 
@app.route("/api/getfeedsbyuser",methods=["POST"])
def getfeed():
	table= dynamodb.Table('feeds')
	email=request.json.get('email')
	response =table.scan(
	FilterExpression= Key('fstatus').eq(True) & Key('email').eq(request.json.get('email')) 
	
	
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"No records found",
			'response':{}


		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		newdat=[]
		for x in range(len(item)): 
			newemail=item[x]["email"]
			newfeedid=item[x]["feedid"]
			utable = dynamodb.Table('user')
			response = utable.get_item(
				Key={'email':newemail }
				)
			uitem = response.get('Item')
			#print(uitem.get('username'))
			ltable = dynamodb.Table('like')
			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("true") & Key('feedid').eq(newfeedid)
				)
			litem = response.get('Items')
			#print(len(litem))

			response =ltable.scan(
				FilterExpression= Key('lstatus').eq("false") & Key('feedid').eq(newfeedid)
				)
			Ulitem = response.get('Items')
			#print(len(Ulitem))

			response =ltable.scan(
				FilterExpression= Key('email').eq(request.json.get('email')) & Key('feedid').eq(newfeedid)
				)
			myitem = response.get('Items')
			#print(len(myitem))

			commtable = dynamodb.Table('comment')
			response =commtable.scan(
				FilterExpression= Key('feedid').eq(newfeedid)
				)
			commitem = response.get('Items')
			#print(len(commitem))
			nwelist={
			   "feedid":item[x]["feedid"],
			   "feedstatus":item[x]["fstatus"],
			   "feedmessage":item[x]["message"],
			   "date":int(item[x]["date"]),
			   "email":item[x]["email"],
			   "username":uitem.get('username'),
			   "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
			   "userid":uitem.get('id'),
			   "usercountry":uitem.get('country'),
			   "totallike":len(litem),
			   "totalunlike":len(Ulitem),
			   "totalcomments":len(commitem)>0 and len(commitem) or 0,
			   "userlikestatus":len(myitem)>0 and myitem[0]['lstatus'] or ""
			   
             }
			newdat.append(nwelist)
			#print(newdat)
		
		data = {'message':"Feeds  Details are ",
		'response':newdat
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
	

	# Function for get user feed end

# Get like list  of a feed 
@app.route("/api/likelistbyfeed",methods=["POST"])
def likelistbyfeed():
	table= dynamodb.Table('feeds')
	ltable= dynamodb.Table('like')
	email=request.json.get('email')
	email=request.json.get('feedid')
	response =ltable.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid')) & Key('lstatus').eq("true") 
	
	
)
	item = response.get('Items')
	#print(item)
	if not item:
		data = {
		'message':"No records found ",
			'response':{}


		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		
		newdat=[]
		for x in range(len(item)): 
			newemail=item[x]["email"]
			
			utable = dynamodb.Table('user')
			response = utable.get_item(
				Key={'email':newemail }
				)
			uitem = response.get('Item')
			if uitem.get('image'):
				uimage =IMAGEPATH+(uitem.get('image') and uitem.get('image') or ""),
			else:
				uimage = NOIMAGEPATH
				
			nwelist={
			   "feedid":request.json.get('feedid'),
			   "email":item[x]["email"],
			   "username":uitem.get('username'),
			   "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
			 
			   "userid":uitem.get('id'),
			   "usercountry":uitem.get('country'),
			   "usercity":uitem.get('city'),
			   "userarea":uitem.get('city')
			   
			  }
			newdat.append(nwelist)
			#print(newdat)
		
		data = {'message':"likes  list are ",
		'response':newdat
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp

# Get dislike list  of a feed 
@app.route("/api/dislikelistbyfeed",methods=["POST"])
def dislikelistbyfeed():
	table= dynamodb.Table('feeds')
	ltable= dynamodb.Table('like')
	email=request.json.get('email')
	email=request.json.get('feedid')
	response =ltable.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid')) & Key('lstatus').eq("false")
	
	
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"No records found ",
			'response':{}


		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		newdat=[]
		for x in range(len(item)): 
			newemail=item[x]["email"]
			
			utable = dynamodb.Table('user')
			response = utable.get_item(
				Key={'email':newemail }
				)
			uitem = response.get('Item')
			
			nwelist={
			   "feedid":request.json.get('feedid'),
			   "email":item[x]["email"],
			   "username":uitem.get('username'),
			   "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
			   "userid":uitem.get('id'),
			   "usercountry":uitem.get('country'),
			   "usercity":uitem.get('city'),
			   "userarea":uitem.get('city')
			   
			  }
			newdat.append(nwelist)
			#print(newdat)
		
		data = {'message':"likes  list are ",
		'response':newdat
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
#get comments list by feeds	
@app.route("/api/commentbyfeed",methods=["POST"])
def commentlistbyfeed():
	table= dynamodb.Table('feeds')
	ctable= dynamodb.Table('comment')
	email=request.json.get('email')
	email=request.json.get('feedid')
	response =ctable.scan(
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))
	
	
)
	item = response.get('Items')
	if not item:
		data = {
		'message':"No records found ",
			'response':{}


		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		newdat=[]
		for x in range(len(item)): 
			newemail=item[x]["email"]
			
			utable = dynamodb.Table('user')
			response = utable.get_item(
				Key={'email':newemail }
				)
			uitem = response.get('Item')
			
			nwelist={
			   "feedid":request.json.get('feedid'),
			   "commentid":item[x]["commentid"],
			   "comment":item[x]["comment"],
			   "date": int(item[x]["date"]),
			   "email":item[x]["email"],
			   "username":uitem.get('username') and uitem.get('username') or "",
			   "image":uitem.get('image') and IMAGEPATH+uitem.get('image') or "",
			   "userid":uitem.get('id'),
			   "usercountry":uitem.get('country') and uitem.get('country') or "",
			   "usercity":uitem.get('city') and uitem.get('city') or "",
			   "userarea":uitem.get('area') and uitem.get('area') or ""
			   
			  }
			newdat.append(nwelist)
			#print(newdat)
		
		data = {'message':"Comments  list are ",
		'response':newdat
		}
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
	
		
		
		
		
		
	



app.run(host='192.168.0.11', port=5005, debug=True)
