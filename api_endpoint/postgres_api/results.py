from flask_table import Table, Col

class SelectionCriteriaTable(Table):
    segment_type = Col('segment_type')
    segment_name = Col('segment_name')
    minimum = Col('minimum')
    maximum = Col('maximum')
    voucher_amount = Col('voucher_amount')

