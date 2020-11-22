from flask import Flask, render_template, make_response, request
from flask_restful import Resource, Api
from pg_connect import PgHook
from results import SelectionCriteriaTable
from datetime import datetime

app = Flask(__name__)

args = ['airflow', 'airflow', 'airflow', 'localhost']


class SelectionCriteria(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}  # display GET request as HTML via browser
        hook = PgHook(*args)  # create connection to Postgres database (containerised)
        data = hook.execute_query('select * from model_staging.segments')
        table = SelectionCriteriaTable(data)  # create table format
        table.border = True
        # when using flask_restful, make_response is required for applying jinja templating
        return make_response(render_template('results.html', table=table), 200, headers)


class VoucherSelection(Resource):
    def post(self):
        """

        dimension is the measure we are measuring against (total orders or last order)
        """
        data = request.get_json()
        hook = PgHook(*args)
        query = """
                    SELECT * FROM model_staging.segments WHERE segment_type='{segment_name}' AND minimum <= {dimension}
                                                            AND (maximum >= {dimension} OR maximum IS NULL) ;
                    """

        segment_name = data['segment_name']
        if segment_name == 'recency_segment':
            last_order_ts = data['last_order_ts']
            # difference between last order time stamp and now
            datediff = abs(datetime.strptime(last_order_ts, '%Y-%m-%d %H:%M:%S') - datetime.now()).days
            # null maximum for cases where recency above 180
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
    # api.add_resource(Item, '/item/<string:name>')
    # api.add_resource(ItemList, '/items')
    app.run(port=5000, debug=True)
