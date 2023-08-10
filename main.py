import multiprocessing
import time
import redis
from redis import Redis
from rq.worker import Worker
from rq import Queue
from users import users
from worker import gomain

num_processes = 2 # how many chromedrivers are open at the same time

link_for_liking_post = 'https://www.instagram.com/kiamariax/tagged/' # link for like



def run_worker(queue):
    redis_conn = Redis(host='localhost', port=6379)
    worker = Worker(queue, connection=redis_conn)
    worker.work(burst=True)


def main():
    try:
        redis_conn = redis.Redis(host='localhost', port=6379)
        redis_conn.ping()
        print("Redis server - ok")
    except redis.ConnectionError:
        print("No connection to Redis.")


    start_time = time.time()

    queue = Queue(connection=redis_conn)

    for key, val in users.items():
        logpass = []
        logpass.append(key)
        logpass.append(val)
        logpass.append(link_for_liking_post)
        queue.enqueue(gomain, logpass, job_timeout=3600)

    num_workers = num_processes
    processes = []
    for _ in range(num_workers):
        proces = multiprocessing.Process(target=run_worker, args=(queue,))
        processes.append(proces)
        proces.start()

    for process in processes:
        process.join()

    queue.empty()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"parsng done: {execution_time}sec")


main()

