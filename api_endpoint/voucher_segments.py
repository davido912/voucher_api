from flask_table import Table, Col
from wtforms import Form, StringField, validators


class SelectionCriteriaTable(Table):
    """
    This object is part of the flask_table module that creates a jinja rendered table when accessing the API on
    designated endpoints
    """
    segment_type = Col('segment_type')
    segment_name = Col('segment_name')
    lower_floor = Col('lower_floor')
    upper_floor = Col('upper_floor')
    voucher_amount = Col('voucher_amount')


class MakeAPICall(Form):
    customer_id = StringField('customer_id', [validators.DataRequired()])
    country_code = StringField('country_code', [validators.DataRequired()])
    last_order_ts = StringField('last_order_ts', [validators.DataRequired()])
    first_order_ts = StringField('first_order_ts', [validators.DataRequired()])
    total_orders = StringField('total_orders', [validators.DataRequired()])
    segment_name = StringField('segment_name', [validators.DataRequired()])
