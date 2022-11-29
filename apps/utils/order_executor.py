from .order import MyOrders


# 锁定订单后 获取、封装订单消息

def get_order_message(my_order: MyOrders):
    # my_order.get_order_phone()
    # mobile = my_order.mobile
    from_name = "".join(map(lambda x, y: my_order.one_match_order['from_location'][x][y],
                            ["province", "city", "county", "town"], ["name", "name", "name", "name"])) \
                + my_order.one_match_order['from_location']["address"]
    to_name = "".join(map(lambda x, y: my_order.one_match_order['to_location'][x][y],
                          ["province", "city", "county", "town"], ["name", "name", "name", "name"])) \
              + my_order.one_match_order['to_location']["address"]
    description = my_order.one_match_order['description']
    goods_time = my_order.one_match_order['time']
    price = my_order.one_match_order['price']['price']
    message = locals()
    message.pop("my_order")
    return message


def get_order_message_result(my_order: MyOrders):
    my_order.get_order_phone()
    mobile = my_order.mobile
    from_name = "".join(map(lambda x, y: my_order.one_match_order['from_location'][x][y],
                            ["province", "city", "county", "town"], ["name", "name", "name", "name"])) \
                + my_order.one_match_order['from_location']["address"]
    to_name = "".join(map(lambda x, y: my_order.one_match_order['to_location'][x][y],
                          ["province", "city", "county", "town"], ["name", "name", "name", "name"])) \
              + my_order.one_match_order['to_location']["address"]
    description = my_order.one_match_order['description']
    goods_time = my_order.one_match_order['time']
    price = my_order.one_match_order['price']['price']
    message = locals()
    message.pop("my_order")
    return message


