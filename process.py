from datetime import datetime
from multiprocessing import Process, cpu_count


def factorize(*number):
    list_nums = []
    for num in number:
        for numeric in range(1, num+1):
            if num % numeric:
                continue
            else:
                list_nums.append(numeric)
        yield list_nums
        list_nums = []


if __name__ == "__main__":

    time_before_process = datetime.now().timestamp()
    pr = Process(target=factorize, args=(128, 255, 99999, 10651060))
    pr.start()
    pr.join()
    time_after_process = datetime.now().timestamp()
    time_for_process = time_after_process - time_before_process
    print(f"Time for process: {time_for_process}")

    time_before_func = datetime.now().timestamp()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    time_after_func = datetime.now().timestamp()
    time_for_func = time_after_func - time_before_func
    print(f"Time for func: {time_for_func}")

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
