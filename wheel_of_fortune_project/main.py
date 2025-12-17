import time

def calculate_median_time(arr):
    start_time = time.time()

    arr.sort()

    n = len(arr)
    median_value = 0

    if n % 2 != 0:
        median_value = arr[n // 2]
    else:
        middle1 = arr[n // 2 - 1]
        middle2 = arr[n // 2]
        median_value = (middle1 + middle2) / 2.0

    end_time = time.time()
    time_taken = end_time - start_time

    return time_taken

massiv = [i for i in range(10 ** 6)]

print(round(calculate_median_time(massiv), 4))