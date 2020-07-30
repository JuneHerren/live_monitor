import requests
import unittest
import json
session = requests.session()
PFB = {"SPC_XXX": "xxx"}
session.cookies.update(PFB)

URL = "http://127.0.0.1:5000/createorder/"
data_json = {}
with open("./data_for_create_order.json", "r") as file:
    data_json = json.load(file)
#params = {"shopid": "456", "itemid": "457",  "amount": 4, "sales": 4567}

class TESTCreateOrder(unittest.TestCase):

    def test_stateCode(self):

        resp = requests.get(URL, json=data_json["1"])
        self.assertEqual(resp.status_code, 405)
        resp = requests.post("http://127.0.0.1:5000/", json=data_json["1"])
        self.assertEqual(resp.status_code, 404)
        resp = requests.post(URL, json=data_json["13"])
        self.assertEqual(resp.status_code, 500)

    def test_parameters_amount(self):
        # the parameters is too short or long or empty
        resp = requests.post(URL, json=data_json["2"])
        data = resp.json()
        self.assertEqual(data['code'], 11)
        resp = requests.post(URL, json=data_json["3"])
        self.assertEqual(data['code'], 11)
        resp = requests.post(URL, json=data_json["8"])
        data = resp.json()
        self.assertEqual(data['code'], 11)
    def test_parameters_type(self):
        resp = requests.post(URL, json=data_json["4"])
        data = resp.json()
        self.assertEqual(data['code'], 12)
        resp = requests.post(URL, json=data_json["5"])
        data = resp.json()
        self.assertEqual(data['code'], 12)
        resp = requests.post(URL, json=data_json["6"])
        data = resp.json()
        self.assertEqual(data['code'], 12)
        resp = requests.post(URL, json=data_json["7"])
        data = resp.json()
        self.assertEqual(data['code'], 12)
    def test_parameters_values_empty(self):
        #the value  of shopid or itemid is empty
        resp = requests.post(URL, json=data_json["10"])
        data = resp.json()
        self.assertEqual(data['code'], 13)
        resp = requests.post(URL, json=data_json["11"])
        data = resp.json()
        self.assertEqual(data['code'], 13)
        resp = requests.post(URL, json=data_json["12"])
        data = resp.json()
        self.assertEqual(data['code'], 13)
    def test_illegal_values(self):
        resp = requests.post(URL, json=data_json["14"])
        data = resp.json()
        self.assertEqual(data['code'], 14)
        resp = requests.post(URL, json=data_json["15"])
        data = resp.json()
        self.assertEqual(data['code'], 14)


    def test_database_insert(self):
        resp = requests.post(URL, json=data_json["1"])
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['code'], 0)
        #resp = requests.post(URL, json=data_json["9"])
        #data = resp.json()
        #self.assertEqual(data['code'], 13)
    def test_edge_value(self):
        pass
        #resp = requests.post(URL, json=data_json["16"])
        #self.assertEqual(resp.status_code, 200)
        #resp = requests.post(URL, json=data_json["17"])
        #self.assertEqual(resp.status_code, 500)


if __name__ == '__main__':
    unittest.main()