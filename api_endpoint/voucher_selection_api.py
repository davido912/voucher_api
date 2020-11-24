"""
This module represents the API. The API is built to use a Postgres Database in its background to query results from.
"""

from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from pg_connect import PgHook
from voucher_segments import SelectionCriteriaTable
from datetime import datetime

app = Flask(__name__)

args = ['voucher', 'voucher', 'password', 'localhost', 5433]


class SelectionCriteria(Resource):
    """
    This endpoint resource is created to give access and better understanding of what are the criteria for the segments
    and their relevant voucher amounts.
    """

    def get(self):
        headers = {'Content-Type': 'text/html'}  # display GET request as HTML via browser
        hook = PgHook(*args)  # create connection to Postgres database (containerised)
        data = hook.execute_query('SELECT * FROM model_staging.voucher_segments;')
        table = SelectionCriteriaTable(data)  # create table format
        table.border = True
        # when using flask_restful, make_response is required for applying jinja templating
        return make_response(render_template('voucher_segments.html', table=table), 200, headers)


class VoucherSelection(Resource):
    """
    Endpoint for a post request to the voucher_segments table, using different dimensions according to the segment chosen
    When using recency segment, date difference from last order is used.
    However, when using frequent segment, total orders are used.
    """

    def post(self):
        data = request.get_json()
        hook = PgHook(*args)
        query = """
                    SELECT * FROM model_staging.voucher_segments WHERE segment_type='{segment_name}' AND minimum <= {dimension}
                                                            AND (maximum >= {dimension} OR maximum IS NULL) ;
                    """

        segment_name = data['segment_name']
        if segment_name == 'recency_segment':
            last_order_ts = data['last_order_ts']
            datediff = abs(datetime.strptime(last_order_ts, '%Y-%m-%d %H:%M:%S') - datetime.now()).days
            query = query.format(segment_name=segment_name, dimension=datediff)

        # add exception for out of range
        elif data['segment_name'] == 'frequent_segment':
            total_orders = data['total_orders']
            query = query.format(segment_name=segment_name, dimension=total_orders)

        try:
            data = hook.execute_query(query)
            return {"voucher_amount": data[0]['voucher_amount']}, 200
        except:
            return {"invalid_request": "request format is incorrect, ensure request format adheres to documentation"}, 400


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(SelectionCriteria, '/selection_criteria')
    api.add_resource(VoucherSelection, '/voucher')
    app.run(port=5000, debug=True)
