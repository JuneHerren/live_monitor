# flask_backend2.py
from flask import Flask, request, jsonify
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import SchemaError, ValidationError
import sys
sys.path.append("..")
from common.logger import get_logger
logger = get_logger(__name__)
import sqlite3
import json
import time
app = Flask(__name__)
# the response for GET
@app.route('/livemonitor/', methods=['GET'])

def getTop5():
	#data = request.json
	schema = {
		"type" : "object",
		"properties": {
			"shopid": {
				"type": "string",
				"minLength": 1
			},
		},
		"required": [
			"shopid"
		],
		"additionalProperties": False,
	}
	shopid = request.args.get("shopid")
	data = {"shopid": shopid}
	try:
		validate(instance=data, schema=schema, format_checker=draft7_format_checker)
	except SchemaError as e:
		logger.error("验证模式schema出错!出错位置：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
		return {'code': 11, 'msg': "验证模式schema出错! 出错位置：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message), 'data': {}}
	except ValidationError as e:
		logger.error("json数据不符合schema规定! 出错字段：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
		return {'code': 12, 'msg': "json数据不符合schema规定! 出错字段：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message), 'data': {} }
	else:
		logger.info("验证成功！")
	
	# size =len(request.args)
	# if size != 1:
	# 	logger.error('the parameter is too long or too short')
	# 	return {'code': 11, 'msgmk': 'the parameter is too long or too short', 'data': {}}
	# shopid = request.args.get("shopid")
	# if not shopid :
	# 	logger.error('the parameter is empty')
	# 	return {'code': 13, 'msg': 'the parameter is empty', 'data': {}}
	# if(type(shopid) != type(str())):
	# 	logger.error('the parameters type is wrong')
	# 	return {'code': 12, 'msg': 'the parameters type is wrong', 'data': {} }
	return_data ={"shopid": shopid, "total_sales": 0, "items": [] }
	total_sales = 0
	time_from = time.strftime("%Y-%m-%d", time.localtime())
	time_from = time_from + ' ' + '00:00'
	time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	paras = (shopid, time_from, time_now)
	items_set = set()
	conn = sqlite3.connect('./../database/myDB.db')
	cursor = conn.cursor()
	cnt = 0
	for item in (cursor.execute('SELECT  * FROM s123 WHERE shopid = ? and orderdate between ? and ?', paras)):
		total_sales = total_sales + item[3]
		items_set.add(item[1])
		cnt = cnt + 1
	if cnt == 0:
		logger.info('there is no records for the shopid')
		conn.commit()
		conn.close()
		return {'code': 14, 'msg': 'there is no records for the shopid', 'data': {}}
	items_arry = []
	for item in items_set:
		paras = (shopid, item, time_from, time_now)
		cursor.execute('SELECT sales FROM s123 WHERE shopid = ? and itemid = ? and orderdate between ? and ?', paras)
		sales_list = cursor.fetchall()
		isales = 0
		for sales in sales_list:
			isales = isales + sales[0]
		items_dict = dict()
		items_dict["itemid"] = item
		items_dict["sales"]  = isales
		items_arry.append(items_dict)
	conn.commit()
	conn.close()
	items_arry.sort(key=lambda k: (k.get('sales',0)), reverse=True)
	count = 0
	for i in items_arry:
		count = count + 1
		if count == 6:
			break
		return_data["items"].append(i)

	return_data["total_sales"] = total_sales
	logger.info('finished')

	return {'code': 0, 'msg': 'success', 'data': return_data}

#the response for POST
@app.route('/createorder/', methods=['POST'])
def orderItems():
	# read the request data
	data = request.json
	#return_data = {'code': 0}
	# check the size of the request
	schema = {
		"type" : "object",
		"properties": {
			"shopid": {
				"type": "string",
				"minLength": 1
			},
			"itemid":{
				"type": "string",
				"minLength": 1
			},
			"amount":{
				"type": "number",
				"minimum": 0
			},
			"sales":{
				"type": "number",
				"minimum": 0

			}
		},
		"additionalProperties": False,
		"required": [
			"shopid", 
			"itemid",
			"amount",
			"sales"
		]
	}
	try:
		validate(instance=data, schema=schema, format_checker=draft7_format_checker)
	except SchemaError as e:
		logger.error("验证模式schema出错!出错位置：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
		return {'code': 11, 'msg': "验证模式schema出错! 出错位置：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message), 'data': {}}
	except ValidationError as e:
		logger.error("json数据不符合schema规定! 出错字段：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message))
		return {'code': 12, 'msg': "json数据不符合schema规定! 出错字段：{}; 提示信息：{}".format(" --> ".join([i for i in e.path]), e.message), 'data': {} }
	else:
		logger.info("验证成功！")
	# size = len(data)
	# if size != 4:
	# 	logger.error('parameters: parameters is too long or too short')
	# 	return {'code': 11, 'msg': 'parameters is too long or too short' }
	# if type(data["shopid"]) != type(str()) or type(data["itemid"]) != type(str()) or type(data["amount"]) != type(int()) or type(data["sales"]) != type(float()):
	# 	logger.error('the parameter type is wrong')
	# 	return {'code': 12, 'msg': 'the parameter type is wrong' }
	# if data["shopid"] == "" or data["itemid"] == "":
	# 	logger.error('there is  empty parameter(s) in the request')
	# 	return {'code': 13, 'msg': 'there is  empty parameter in the request' }
	# if data["amount"] < 0 or data["sales"] < 0:
	# 	logger.error('the parameters is illegal')
	# 	return {'code': 14, 'msg': 'the parameter value is illegal'}

	conn = sqlite3.connect('./../database/myDB.db')
	cursor = conn.cursor()
	# check whether there is the table s123 in the database or not
	cursor.execute('''CREATE TABLE IF NOT EXISTS s123 ( shopid string NOT NULL, itemid string(128) NOT NULL, amount integer(128) NOT NULL, sales float(128) NOT NULL, orderdate datetime(128)  NOT NULL, orderid integer primary key  autoincrement)''')

	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	paras = ( data["shopid"], data["itemid"], data["amount"], data["sales"], t, None)
	cursor.execute("INSERT INTO s123 VALUES (?, ?, ?, ?, ?, ?)", paras)
	cnt = cursor.rowcount

	conn.commit()
	conn.close()
	if cnt == 1:
		logger.info("success!")
		return  {'code': 0, 'msg': 'success'}
	else:
		logger.error("create order falied!")
		return {'code': 15, 'msg': 'the update for database has failed'}

if __name__ == "__main__":

	app.run()

	
