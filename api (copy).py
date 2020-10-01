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
from datetime import datetime
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
UPLOAD_FOLDER='/var/www/html/ucracy/public/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
IMAGEPATH="/var/www/html/ucracy/public/uplods/"
DOCPATH="/var/www/html/ucracy/public/uplods/documents/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mail = Mail(app)
bcrypt = Bcrypt(app)
now = datetime.utcnow()
timestamp = int(datetime.timestamp(now))
#dynamodb = boto3.resource('dynamodb')
dynamodb = boto3.resource('dynamodb',region_name='us-east-2',aws_access_key_id='AKIASCYB3IX4GPRNBVXZ',
aws_secret_access_key= '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')

@app.route('/')
@app.route('/<name>')

def hello(name=None):
	return "naveen Kumar here write webservices"
	
@app.route("/api/signup", methods=['POST'])

def signup():
	data = {}
	result={}
	table = dynamodb.Table('user')
	
	username = request.json.get('username'),
	email = request.json.get('email'),
	password = request.json.get('password')
			
	response = table.get_item(
		Key={'email':request.json.get('email') }
		)
	item = response.get('Item')
	if (item):

		data = {
		'meggase':"this user is already exist",
			'responce':{}

		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		pw_hash = bcrypt.generate_password_hash(request.json.get('password'))
		table.put_item(
	Item={
		'id':uuid.uuid4().hex,
		'username': request.json.get('username'),
		'email': request.json.get('email'),
		'password': pw_hash,
		'utype':1,
		'status':True
		
		}
)

		msg = Message('Thanks for join with us', sender = 'naveenk@sourcesoftsolutions.com', recipients = ['naveenk@sourcesoftsolutions.com'])
		msg.body = "Thanks for join with us"
		mail.send(msg)
	
		data = {
		'meggase':"Recoard is save sucessfully",
			'responce':{}

		},
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
		Key={'email':request.json.get('email') }
		)
	item = response.get('Item')
	if not item:
		data = {
		'meggase':"Invalid user email which you have provide",
			'responce':{}

		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		# if bcrypt.check_password_hash(item.get('password'), request.json.get('password')):
			data = {
			'meggase':"Login has been sucessfully ",
			'responce':{
			'id':item.get('id') and item.get('id') or "",
			'username':item.get('username'),
			'email':item.get('email'),
			'status':item.get('status') and item.get('status') or False,
			'image':item.get('image') and IMAGEPATH+item.get('image') or "",
			'utype':int(item.get('utype')) and int(item.get('utype')) or "",
			'document':item.get('document') and DOCPATH+item.get('document') or "",
			'country':item.get('country') and item.get('country') or "",
			'uregion':item.get('uregion') and item.get('uregion') or "",
			'city':item.get('city') and item.get('city') or "",
			'area':item.get('area') and item.get('area') or "",
			
			}
			},
			resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
			
			return resp
		# else:
		# 	data = {'meggase':"Invalid password which you have provide",'responce':{}},
		# 	resp  = app.response_class(
		# 	response=json.dumps(data),
		# 	status=400,
		# 	mimetype='application/json'
		# 	)
		# return resp

		
@app.route("/api/countrylist", methods=['get'])
def countrylist():
	params = {"positions":[0,6,7,29]}
	r = requests.get("http://battuta.medunes.net/api/country/all/?key=4b23e6bb381c99fed8eeb061784cb09e")

	#print(r.status_code)
	#print(r.json())
	#return r.json()
	data = {
			'meggase':"Country list are",
			'responce':r.json()
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
			'meggase':"Region  list are",
			'responce':r.json()
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
			'meggase':"City list are",
			'responce':r.json()
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
		'meggase':"Invalid user email which you have provide",
			'responce':{}

		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:

		data = {'meggase':"User  Details are ",
		'responce':{
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
		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
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
		'meggase':"Invalid user email which you have provide",
			'responce':{}

		},
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
		':val2': request.json.get('country'),
		':val3': request.json.get('city'),
		':val4': request.json.get('area'),
		':val5': request.json.get('uregion'),
	}
)
		data = {'meggase':"User address update successfully",
		'responce':{}
		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
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
			'meggase':"dddd",
			'responce':[
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
		'meggase':"Invalid user which you have provide",
			'responce':{}

		},
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
			'meggase':"Image upload sucessfully ",
			'responce':{"profileimage":IMAGEPATH+filename}
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

			'meggase':"Image format not support",
			'responce':{}
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
		'meggase':"Invalid user which you have provide",
			'responce':{}

		},
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
			'meggase':"Doucments upload sucessfully ",
			'responce':{"profileimage":IMAGEPATH+filename}
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

			'meggase':"Doucments format not support",
			'responce':{}
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
		'meggase':"Invalid user email which you have provide",
			'responce':{}

		},
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
		'date':timestamp
		}
)
		data = {
		'meggase':"Recoard is save sucessfully",
			'responce':{}

		},
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
		'meggase':"Invalid user",
			'responce':{}

		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		data = {'meggase':"Deed  Details are ",
		'responce':{
			'feedid':item[0]['feedid'] and item[0]['feedid'] or "",
			'email':item[0]['email'] and item[0]['email'] or "",
			'message':item[0]['message'] and item[0]['message'] or "",
			'status':item[0]['fstatus'] and item[0]['fstatus'],
			'date': int(item[0]['date']) and int(item[0]['date']) ,
			
			}
		},
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
		'meggase':"Invalid user",
			'responce':{}

		},
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
	data = {'meggase':"User feeds update successfully",
		'responce':{}
		},
	resp  = app.response_class(
			response=json.dumps(data),
			status=400,
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
		'date':timestamp
		}
)
		data = {
		'meggase':"Recoard is save sucessfully",
			'responce':{}

		},
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
			resp  = app.response_class(
			response=json.dumps({'meggase':"You have already perform this action",
		'responce':{}
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
			
		resp  = app.response_class(
			response=json.dumps({'meggase':"User feeds update successfully",
		'responce':{}
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

	if (request.json.get('feedid')):
			table.put_item(
	Item={
		'feedid':request.json.get('feedid'),
		'commentid': uuid.uuid4().hex,
		'email': request.json.get('email'),
		'comment': request.json.get('comment'),
		'cstatus':True,
		'date':timestamp
		}
)
	data = {
		'meggase':"Comments is save sucessfully",
			'responce':{}

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
		'meggase':"Invalid details",
			'responce':{}

		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)
		return resp
	else:
		data = {'meggase':"comments  Details are ",
		'responce':{
			'id':item[0]['feedid'],
			'feedid':item[0]['feedid'] and item[0]['feedid'] or "",
			'email':item[0]['email'] and item[0]['email'] or "",
			'ucomment':item[0]['comment'] and item[0]['comment'] or "",
			'status':item[0]['cstatus'] and item[0]['cstatus'],
			'date': int(item[0]['date']) and int(item[0]['date']) ,
			
			}
		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
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
		'meggase':"Invalid details provide",
			'responce':{}

		},
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
	data = {'meggase':"User comment update successfully",
		'responce':{}
		},
	resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
	return resp		


	
		
		
		
		
		
	



app.run(host='192.168.0.11', port=5005, debug=True)
