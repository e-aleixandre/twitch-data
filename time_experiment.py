import requests
import time
import threading


def lock_thread():
    r = requests.get("https://api.punkapi.com/v2/beers/random")
    b = r.json()[0]
    with lock:
        beverages[b["id"]] = b


def multi_thread():
    r = requests.get("https://api.punkapi.com/v2/beers/random")
    b = r.json()[0]
    beverages[b["id"]] = b


time_mono = time_multi = time_lock = 0
amount = 200
start_time = time.time()
beverages = {}

for i in range(amount):
    r = requests.get("https://api.punkapi.com/v2/beers/random")
    b = r.json()[0]
    beverages[b["id"]] = b

end_time = time.time()
time_mono = end_time - start_time

threads = []
beverages.clear()
start_time = time.time()

for i in range(amount):
    t = threading.Thread(target=multi_thread)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

end_time = time.time()
time_multi = end_time - start_time


threads.clear()
beverages.clear()
lock = threading.Lock()
start_time = time.time()

for i in range(amount):
    t = threading.Thread(target=lock_thread)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

end_time = time.time()
time_lock = end_time - start_time

end_time = time.time()

print("Results for requesting %d beverages from the API:" % amount)
print("\tTime for single threaded program: %f" % time_mono)
print("\tTime for multi threaded program: %f" % time_multi)
print("\tTime for multi threaded w/ lock: %f" % time_lock)

"""
Results for requesting 200 beverages from the API:
    Time for single threaded program: 74.816454
    Time for multi threaded program: 2.191067
    Time for multi threaded w/ lock: 1.698684
"""