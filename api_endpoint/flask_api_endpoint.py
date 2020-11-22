# # principles of REST API:
# # it is stateless! meaning the API doesn't remember if a certain command was fired unless you check (e.g. putting an entry can be validated by using get)
# # for example, a user has authentication executed every time with it
#
#
# # add authentication
# # implement correct error codes 202, 201, 404, 400
#
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"name":"david_test_shop"}' \
#   http://localhost:5000/store
#
#
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"name": "sextoy", "price": 15}' \
#   http://localhost:5000/store/first_store/item
#
#
#
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"price": "50"}' \
#   http://localhost:5000/item/ps5
#
#
#
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"username": "bob", "password":"asdf"}' \
#   http://localhost:5000/auth
#
# curl -H "Authorization:JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDYwNTQ1MDEsImlhdCI6MTYwNjA1NDIwMSwibmJmIjoxNjA2MDU0MjAxLCJpZGVudGl0eSI6MX0.TUFiKzbpiAH9ZQPZgfRoj7rgcjjglHxrnT535uAcRAM" http://localhost:5000/items
#
#
# token = eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MDYwNTM1MjMsImlhdCI6MTYwNjA1MzIyMywibmJmIjoxNjA2MDUzMjIzLCJpZGVudGl0eSI6MX0.xKY-DDpRCvOiUww7LS_75a8rX1vsLea7Tnn0q6YVh74
#
#
# curl --header "Content-Type: application/json" \
#   --request POST \
#   --data '{"segment_name": "recency_segment", "last_order_ts":"2018-05-03 00:00:00"}' \
#   http://localhost:5000/voucher
#
#
