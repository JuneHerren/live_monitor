# detailed list:

- flask_backend.py
  - The source code for my entry task
- test_for_createorder.py
  - It is used to test the orderItems api
- test_for_livemonitor.py
  - it is used to test the getTop5 api
- Data_for_create_order.json
  - the test data for the file of test_for_createorder.py
- Data_for_livemonitor.json
  - the test data for the file of test_for_livemonitor.py
- create_report.py
  - it  is used to create a test report for my entry task 

- .html
  - the test report
- test_cases.xlsx
  - the test cases

- test_case.pdf

# flask_backend.py

it consists of two api -- getTop5 and live monitor

### getTop5 api

- Method: get

- Parameter name: shopid

- Parameter type: string

- Return: 

  - For example :  http://127.0.0.1:5000/livemonitor/?shopid=234

    ```json
    {
        "items": [
            {
                "itemid": 131,
                "sales": 28075606651415569016
            },
            {
                "itemid": 130,
                "sales": 13368
            },
            {
                "itemid": 128,
                "sales": 6684
            },
            {
                "itemid": 129,
                "sales": 6684
            },
            {
                "itemid": 125,
                "sales": 6684
            }
        ],
        "shopid": "234",
        "total_sales": 28075606651415619248
    }
    ```

    

### orderItems api

- method: post
- body
  - Type: json
  - parameters
    - Key: shopid,  value type: sting
    - Key: itemid, value type: string
    - Key:  amount , value type: int
    - key: sales, value type: int 
- return 
  - code
  - Msg
# to run 

## to start nginx
brew services start nginx

## to start backend server 

gunicorn -c config.py flask_backend:app 

## to do pressure measurement for apis with wrk

wrk -t 16 -c 200 -d 60s --latency  -s post.lua http://127.0.0.1:8181/createorder/ 
 wrk -t 16 -c 200 -d 60s --latency  -s get.lua http://127.0.0.1:8181/livemonitor/

# tools

- unittes
- htmlTestRunner
- flask
- requests
- Sqlite3
- logging
- gunicorn
- nginx
- wrk
- macOS

# others



- postman

- Pycharm

- python3+

  





