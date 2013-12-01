from threading import Thread
from Queue import Queue, Empty


def parallel_map(fun, lst, num_threads=None):
    threads = []
    results = []
    resultqueue = Queue(len(lst))
    jobqueue = Queue()

    if num_threads is None:
        num_threads = len(lst)

    for i, el in enumerate(lst):
        jobqueue.put((i, el))

    for i in range(num_threads):
        thread = Thread(target=_queuefun, args=(fun, jobqueue, resultqueue))
        threads.append(thread)
        thread.start()

    jobqueue.join()

    for i in range(len(lst)):
        try:
            results.append(resultqueue.get())
        except Empty:
            break
    results = sorted(results, key=lambda index: index[0])
    return [res for index, res in results]


def _queuefun(fun, jobqueue, resultqueue):
    while not jobqueue.empty():
        try:
            index, job = jobqueue.get()
        except Empty:
            break
        result = (index, fun(job))
        resultqueue.put(result)
        jobqueue.task_done()
