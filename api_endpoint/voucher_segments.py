from flask_table import Table, Col


class SelectionCriteriaTable(Table):
    """
    This object is part of the flask_table module that creates a jinja rendered table when accessing the API on
    designated endpoints
    """
    segment_type = Col('segment_type')
    segment_name = Col('segment_name')
    minimum = Col('minimum')
    maximum = Col('maximum')
    voucher_amount = Col('voucher_amount')

