# flask_backend2.py
from flask import Flask, request, jsonify
import json
import logging
import sqlite3
import time
app = Flask(__name__)

# the response for GET
@app.route('/livemonitor/', methods=['GET'])

def getTop5():
	#data = request.json
	size =len(request.args)
	if size != 1:
		logging.error('the parameter is too long or too short')
		return {'code': 11, 'msg': 'the parameter is too long or too short', 'data': {}}
	shopid = request.args.get("shopid")
	if not shopid :
		logging.error('the parameter is empty')
		return {'code': 13, 'msg': 'the parameter is empty', 'data': {}}
	if(type(shopid) != type(str())):
		logging.error('the parameters type is wrong')
		return {'code': 12, 'msg': 'the parameters type is wrong', 'data': {} }
	return_data ={"shopid": shopid, "total_sales": 0, "items": [] }
	total_sales = 0
	time_from = time.strftime("%Y-%m-%d", time.localtime())
	time_from = time_from + ' ' + '00:00'
	time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	paras = (shopid, time_from, time_now)
	items_set = set()
	conn = sqlite3.connect('./myDB.db')
	cursor = conn.cursor()
	cnt = 0
	for item in (cursor.execute('SELECT  * FROM s123 WHERE shopid = ? and orderdate between ? and ?', paras)):
		total_sales = total_sales + item[3]
		items_set.add(item[1])
		cnt = cnt + 1
	if cnt == 0:
		logging.info('there is no records for the shopid')
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
	logging.info('finished')
	return {'code': 0, 'msg': 'success', 'data': return_data}

#the response for POST
@app.route('/createorder/', methods=['POST'])
def orderItems():
	# read the request data
	data = request.json
	return_data = {'code': 0}
	# check the size of the request
	size = len(data)
	if size != 4:
		logging.error('parameters: parameters is too long or too short')
		return {'code': 11, 'msg': 'parameters is too long or too short' }
	if type(data["shopid"]) != type(str()) or type(data["itemid"]) != type(str()) or type(data["amount"]) != type(int()) or type(data["sales"]) != type(float()):
		logging.error('the parameter type is wrong')
		return {'code': 12, 'msg': 'the parameter type is wrong' }
	if data["shopid"] == "" or data["itemid"] == "":
		logging.error('there is  empty parameter(s) in the request')
		return {'code': 13, 'msg': 'there is  empty parameter in the request' }
	if data["amount"] < 0 or data["sales"] < 0:
		logging.error('the parameters is illegal')
		return {'code': 14, 'msg': 'the parameter value is illegal'}
	# data = request.get_json()
	#update the database
	conn = sqlite3.connect('./myDB.db')
	cursor = conn.cursor()
	# check whether there is the table s123 in the database or not
	cursor.execute('''CREATE TABLE IF NOT EXISTS s123 (shopid string NOT NULL, itemid string(128) NOT NULL, amount integer(128) NOT NULL, sales float(128) NOT NULL, orderdate datetime(128) PRIMARY KEY NOT NULL)''')

	t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	paras = (data["shopid"], data["itemid"], data["amount"], data["sales"], t)
	cursor.execute("INSERT INTO s123 VALUES (?, ?, ?, ?, ?)", paras)
	cursor.execute('select shopid from s123 where orderdate = ?', (t,))
	data = cursor.fetchall()
	conn.commit()
	conn.close()
	if data:
		logging.info("success!")
		return  {'code': 0, 'msg': 'success'}
	else:
		return {'code': 15, 'msg': 'the update for database has failed'}

if __name__ == "__main__":
	app.run(debug=True)
	
