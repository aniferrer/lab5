import order_ops as order_ops

if __name__ == '__main__':
    orders = order_ops.query_user_status('aarchamb', 'Placed')
    dates = order_ops.query_user_date('aarchamb', '06/07/2021 10:29 PM')
    for order in orders:
        for date in dates:
            if order == date:
                items = order_ops.query_order_items(date['sk'][7:])
                for item in items:
                    print(item['sk'], item['product_name'], '(', item['quantity'], ')')
