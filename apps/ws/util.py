import inspect

import ctypes
from geopy.distance import geodesic


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""

    tid = ctypes.c_long(tid)

    if not inspect.isclass(exctype):
        exctype = type(exctype)

    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

    if res == 0:

        raise ValueError("invalid thread id")

    elif res != 1:

        # """if it returns a number greater than one, you're in trouble,

        # and you should call it again with exc=NULL to revert the effect"""

        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def filter_distance(one_match_order_data: dict, min_distance: int, max_distance: int):
    try:
        if "from_location" in one_match_order_data.keys():
            if min_distance <= geodesic((one_match_order_data['from_location']['latitude'],
                                         one_match_order_data['from_location']['longitude']),
                                        (one_match_order_data['to_location']['latitude'],
                                         one_match_order_data['to_location']['longitude'])) <= max_distance:
                return True
        return False
    except Exception as e:
        print(e)
        return False
