import order_ops as order_ops

if __name__ == '__main__':
    orders = order_ops.query_status_orders('Pending')
    for order in orders:
        print(order['sk'], order['product_name'], '(', order['quantity'], ')')
