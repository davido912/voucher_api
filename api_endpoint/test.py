import requests

url = 'http://localhost:5000/voucher'
myobj = {
    "customer_id": 123,
    "total_orders": 3,
    "country_code": "Peru",
    "last_order_ts": "2018-05-03 00:00:00",
    "segment_name": "recency_segment"
}

x = requests.post(url, json=myobj)

print(x.text)
# print(x)
