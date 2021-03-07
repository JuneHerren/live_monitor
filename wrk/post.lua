wrk.method  = "POST"
wrk.body  = '{"shopid": "123", "itemid": "234", "amount": 12, "sales":2234.0}'
wrk.headers["Content-Type"] = "application/json"
wrk.path ="/createorder/"
