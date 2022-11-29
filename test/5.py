# import os, time
# from multiprocessing import Process, Pool
#
# def run_a_sub_proc(name):
#     print(f'子进程：{name}（{os.getpid()}）开始！')
#     for i in range(2):
#         print(f'子进程：{name}（{os.getpid()}）运行中...')
#         time.sleep(1)
#     print(f'子进程：{name}（{os.getpid()}）结束！')
#
# if __name__ == '__main__':
#     print(f'主进程（{os.getpid()}）开始...')
#     p = Pool(4)
#     for i in range(1, 5):
#         p.apply_async(run_a_sub_proc, args=(f"进程-{i}",))
#     p.close()
#     p.join()
import time


def yield_def():
    for num in range(5):
        yield num


y = yield_def()
print(next(y))
print(next(y))
print(next(y))
print(next(y))
print(next(y))

result = (i for i in [1, 2, 3])
result1 = (i for i in range(1, 4))

print(type(result1))

str1 = {"ke": "123"}
list1 = [1, 2, 3, 4, 5]


def change_list(ls):
    ls.update({"ke2": "123123"})


change_list(str1)
print(str1)

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(type(myit))


def applee(*args):
    print(args)


class Cat:
    """定义一个猫类"""

    # def __init__(self, new_name, new_age):
    #     """在创建完对象之后 会自动调用, 它完成对象的初始化的功能"""
    #     # self.name = "汤姆"
    #     # self.age = 20
    #     self.name = new_name
    #     self.age = new_age  # 它是一个对象中的属性,在对象中存储,即只要这个对象还存在,那么这个变量就可以使用
    # num = 100  # 它是一个局部变量,当这个函数执行完之后,这个变量的空间就没有了,因此其他方法不能使用这个变量

    # def __str__(self):
    #     """返回一个对象的描述信息"""
    #     # print(num)
    #     return "名字是:%s , 年龄是:%d" % (self.name, self.age)

    def __get__(self):
        return "__get__调用"


# class B:
#     name = Cat().__get__()


# b = B()
# print(b.name)

print(Cat().__get__())


def timeit(run_nums):
    def inner(f):
        def wrap(x, y):
            return_num = None
            start_time = time.perf_counter()
            for _ in range(run_nums):
                return_num = f(x, y)
            print(time.perf_counter() - start_time)
            return return_num

        return wrap

    return inner


@timeit(100000000)
def add_num(x, y):
    return x + y


add_num(2, 3)
