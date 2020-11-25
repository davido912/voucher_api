"""
This module represents the API. The API is built to use a Postgres Database in its background to query results from.
"""


from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from pg_connect import PgHook
from voucher_segments import SelectionCriteriaTable, MakeAPICall
from datetime import datetime
from os.path import expandvars

app = Flask(__name__)

args = [expandvars('$POSTGRES_DB'),
        expandvars('$POSTGRES_USER'),
        expandvars('$POSTGRES_PASSWORD'),
        expandvars('$POSTGRES_HOST'),
        expandvars('$POSTGRES_PORT')]


class SelectionCriteria(Resource):
    """
    This endpoint resource is created to give access and better understanding of what are the criteria for the segments
    and their relevant voucher amounts.
    """

    def get(self):
        headers = {'Content-Type': 'text/html'}  # display GET request as HTML via browser
        hook = PgHook(*args)  # create connection to Postgres database (containerised)
        data = hook.execute_query('SELECT * FROM model_production.voucher_segmentation;')
        table = SelectionCriteriaTable(data)  # create table format
        table.border = True
        # when using flask_restful, make_response is required for applying jinja templating
        return make_response(render_template('voucher_segments.html', table=table), 200, headers)


def api_query(request_data: request):
    """
    This function serves as basis for post requests and interacting with the Postgres Database. The input is the only
    difference (certain post requests are returned via form objects while others as JSON).
    """
    query = """
                    SELECT * FROM model_production.voucher_segmentation WHERE segment_type='{segment_name}' AND lower_floor <= {dimension}
                                                            AND (upper_floor >= {dimension} OR upper_floor IS NULL) ;
                    """
    segment_name = request_data.get('segment_name')
    if segment_name == 'recency_segment':
        last_order_ts = request_data.get('last_order_ts')
        # under the assumption that today is the 15th of September 2018
        datediff = abs((datetime.strptime(last_order_ts, '%Y-%m-%d %H:%M:%S') -
                        datetime.strptime(expandvars('$CUR_DATE'), '%Y-%m-%d %H:%M:%S')).days)
        query = query.format(segment_name=segment_name, dimension=datediff)

    # add exception for out of range
    elif segment_name == 'frequent_segment':
        total_orders = request_data.get('total_orders')
        query = query.format(segment_name=segment_name, dimension=total_orders)

    hook = PgHook(*args)

    try:
        data = hook.execute_query(query)
        return {"voucher_amount": data[0]['voucher_amount']}, 200
    except:
        return {"invalid_request": "request format is incorrect, ensure request format adheres to documentation"}, 400


class VoucherSelection(Resource):
    """
    Endpoint for a post request to the voucher_segments table, using different dimensions according to the segment chosen
    When using recency segment, date difference from last order is used.
    However, when using frequent segment, total orders are used.
    """
    def post(self):
        request_data = request.get_json()
        return api_query(request_data)


class CallAPIForm(Resource):
    """
    This endpoint resource to perform API calls via an interface instead of using external tools/frameworks.
    """

    def get(self):
        form = MakeAPICall(request.form)
        # when using flask_restful, make_response is required for applying jinja templating
        return make_response(render_template('api_request.html', form=form), 200)

    def post(self):
        return api_query(request.form)


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(SelectionCriteria, '/selection_criteria')
    api.add_resource(VoucherSelection, '/voucher')
    api.add_resource(CallAPIForm, '/search_voucher')
    app.run(host='0.0.0.0', port=5000, debug=True)
