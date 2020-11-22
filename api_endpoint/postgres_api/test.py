import requests

url = 'http://localhost:5000/voucher'
myobj = {
    "customer_id": 123,
    "country_code": "Peru",
    "last_order_ts": "2020-10-03 00:00:00",
    "segment_name": "recency_segment",
    "total_orders":3
}

x = requests.post(url, json=myobj)

print(x.text)
# print(x)
