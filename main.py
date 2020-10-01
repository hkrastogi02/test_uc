import json

import boto3
import hashlib
from flask import Flask
from flask import Response, Request, request, jsonify
from flask_restful import Resource, Api
from botocore.exceptions import ClientError

from flask import render_template
app = Flask(__name__)
api = Api(app)
dynamodb = boto3.resource('dynamodb')


tasks = [
	{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
		'done': False
	},
	{
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web', 
		'done': False
	}
]


@app.route('/')
@app.route('/<name>')
def hello(name=None):
	return "navvvf"
	
@app.route('/api/createtable', methods=['GET'])
def get_tasks():
	table = dynamodb.create_table(
	TableName='user',
	KeySchema=[
		{
			'AttributeName': 'id',
			'KeyType': 'HASH'  #Partition key
		},
		{
			'AttributeName': 'username',
			'KeyType': 'RANGE'  #Sort key
		}
	],
	AttributeDefinitions=[
		{
			'AttributeName': 'id',
			'AttributeType': 'N'
		},
		{
			'AttributeName': 'username',
			'AttributeType': 'S'
		},

	],
	ProvisionedThroughput={
		'ReadCapacityUnits': 10,
		'WriteCapacityUnits': 10
	}
)

@app.route('/api/putiteam', methods=['GET'])
def get_task123():
	table = dynamodb.Table('user')
	table.put_item(
	Item={
		'id':2,
		'username': 'janedoe4',
		'email': 'jane4@gmail.com',
		'password': '123456',
		'role': 1,
		'country': 'IN',
		'city':'delhi',
		'state':'delhi',
		'area':'cp',
		'image':'abc.jpg',
		'status':1,
		'document':'abc.png'
		}
)
@app.route("/api/users/<string:username>", methods=['GET'])

def get_user(username):
	table = dynamodb.Table('user')
	
	response = table.get_item(

		

		

		Key={'id': 1, 'username': "janedoe"}

		

	)
	
	item = response.get('Item')

	if not item:

		return jsonify({'error': 'User does not exist'}), 404


	return jsonify({

		'email': item.get('email'),

		'username': item.get('username')

	})

@app.route("/api/updateusers/<string:username>", methods=['GET'])

def get_userupdate(username):
	table = dynamodb.Table('user')
	table.update_item(
    Key={'id': 1, 'username': "janedoe"},
    UpdateExpression='SET area = :val1, city= :val2',
    ExpressionAttributeValues={
        ':val1': "chandni ",
        ':val2': "noida ", 
    }
)

	response = table.get_item(

		

		

		Key={'id': 1, 'username': "janedoe"}

		

	)
	
	item = response.get('Item')

	if not item:

		return jsonify({'error': 'User does not exist'}), 404


	return jsonify({

		'email': item.get('email'),

		'username': item.get('username')

	})
	


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if len(task) == 0:
	 abort(404)
	return jsonify({'task': task[0]})
	
	
@app.route('/api/tasks/posttask', methods=['POST']) 
def create_task():
	print( request.json);
	return jsonify({'task': []})
	
	
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
		'status':request.json.get('status'),
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
	FilterExpression= Key('feedid').eq(request.json.get('feedid'))& Key('email').eq(request.json.get('email')) & Key('status').eq(request.json.get('status'))
)

		aitem = response.get('Items')
		if not aitem:
			res=table.update_item(
		Key={'feedid':request.json.get('feedid'),'email':request.json.get('email')},
		UpdateExpression='SET status=:val1 ',
		ExpressionAttributeValues={
		':val1': request.json.get('status')
	}
)
			data = {'meggase':"User feeds update successfully",
		'responce':{}
		},
		resp  = app.response_class(
			response=json.dumps(data),
			status=200,
			mimetype='application/json'
			)
		return resp
		else:
			data = {
		'meggase':"You have already like this feed.",
			'responce':{}

		},

		resp  = app.response_class(
			response=json.dumps(data),
			status=400,
			mimetype='application/json'
			)


		return resp
		
	
	
	
	
	

app.run(host='0.0.0.0', port=5001, debug=True)
