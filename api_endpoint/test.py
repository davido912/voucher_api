import requests

url = 'http://localhost:5000/voucher'
myobj = {
    "customer_id": 123,
    "total_orders": 10,
    "country_code": "Peru",
    "last_order_ts": "2018-07-18 00:00:00",
    "segment_name": "frequent_segment"
}

x = requests.post(url, json=myobj)

print(x.text)
# print(x)
