import time
import threading
import itertools

class Timer:
    def __init__(self):
        self.start_time = None
        self.stop_event = threading.Event()
        self.thread = None

    def start_timing(self, message):
        self.start_time = time.time()
        self.message = message
        self.spinner = itertools.cycle(['\\', '|', '/', '-'])
        self.stop_event.clear()
        
        def update_time():
            while not self.stop_event.is_set():
                elapsed_time = time.time() - self.start_time
                print(f'\r{self.message} {next(self.spinner)} [{elapsed_time:.1f}s]', end='')
                time.sleep(0.1)
        
        self.thread = threading.Thread(target=update_time)
        self.thread.start()
        
        return self

    def end_timing(self, end_message):
        self.stop_event.set()
        self.thread.join()
        elapsed_time = time.time() - self.start_time
        print(f'\r{end_message} [Use {elapsed_time:.1f}s]')

# 示例使用
if __name__ == '__main__':
    t = Timer().start_timing('Loading Files ...')
    # 模拟一些耗时的操作
    time.sleep(2)
    t.end_timing('Loading Files Done')
