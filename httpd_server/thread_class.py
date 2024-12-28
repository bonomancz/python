import threading


class Thread:

    def __init__(self):
        self.__thread_pool = {}
        self.__thread_pool_lock = threading.Lock()

    def start_new_thread(self, func, data):
        new_thread = threading.Thread(target=func, args=data)
        new_thread.start()
        thread_id = new_thread.ident
        with self.__thread_pool_lock:
            new_thread_info = [new_thread, False]
            self.__thread_pool[thread_id] = new_thread_info

    def remove_finished_threads(self):
        with self.__thread_pool_lock:
            finished_threads = [thread_id for thread_id, thread_info in self.__thread_pool.items() if thread_info[1]]
            for thread_id in finished_threads:
                try:
                    self.__thread_pool[thread_id][0].join()
                    self.__thread_pool.pop(thread_id)
                except Exception as ex:
                    print("fThread::remove_finished_threads(): Exception: {ex}")

    def remove_all_threads(self):
        with self.__thread_pool_lock:
            for thread_info in self.__thread_pool.values():
                thread_info[0].join()
            self.__thread_pool.clear()

    def remove_thread(self, thread_id):
        with self.__thread_pool_lock:
            self.__thread_pool[thread_id][0].join()
            self.__thread_pool.pop(thread_id)

    def set_thread_finished(self, thread_id) -> None:
        with self.__thread_pool_lock:
            self.__thread_pool[thread_id][1] = True

    def get_thread_pool_statistics(self) -> str:
        statistics = ""
        for thread_id, thread_info in self.__thread_pool.items():
            statistics += f"{thread_id} - {str(thread_info[1])}\n"
        statistics += f"Threads in threadpool: {self.get_thread_pool_size()}\n"
        return statistics

    def get_thread_pool_size(self) -> int:
        with self.__thread_pool_lock:
            return len(self.__thread_pool)

    def get_current_thread_id(self) -> int:
        return threading.get_ident()
