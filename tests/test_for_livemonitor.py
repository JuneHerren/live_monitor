import requests
import unittest
import json
session = requests.session()
PFB = {"SPC_XXX": "xxx"}
session.cookies.update(PFB)

URL = "http://127.0.0.1:5000/livemonitor/"
headers = {'Content-Type': 'application/json'}
data_json = {}
with open("./../data/data_for_live_monitor.json", "r") as file:
    data_json = json.load(file)

#print(resp.json())
class TESTLiveMonitor(unittest.TestCase):
    def test_stateCode(self):
        resp = requests.get(URL, headers=headers, params=data_json["1"])
        self.assertEqual(resp.status_code, 200)
        resp = requests.post(URL, headers=headers, params=data_json["1"])
        self.assertEqual(resp.status_code, 405)
        resp = requests.get("http://127.0.0.1:5000/", headers=headers, params=data_json["1"])
        self.assertEqual(resp.status_code, 404)

    def test_parameter_type(self):
        resp = requests.get(URL, headers=headers, params=data_json["2"])
        data = resp.json()
        self.assertEqual(data['code'], 11)
        resp = requests.get(URL, headers=headers, params=data_json["3"])
        data = resp.json()
        self.assertEqual(data['code'], 11)
        resp = requests.get(URL, json=data_json["6"])
        data = resp.json()
        self.assertEqual(data['code'], 11)
    def test_parameter_value_empty(self):
        resp = requests.get(URL, headers=headers, params=data_json["5"])
        data = resp.json()
        self.assertEqual(data['code'], 13)
        resp = requests.get(URL, headers=headers, params=data_json["4"])
        data = resp.json()
        self.assertEqual(data['code'], 13)
    def test_shopid_records(self):
        resp = requests.get(URL, headers=headers, params=data_json["7"])
        data = resp.json()
        self.assertEqual(data['code'], 14)






if __name__ == '__main__':
    unittest.main()