import time
import threading
import itertools

from custom_print_library import *

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
                print_info(f'{self.message} {next(self.spinner)} [{elapsed_time:.1f}s]', end='\r')
                time.sleep(0.1)
            print_info('\r')
        
        self.thread = threading.Thread(target=update_time)
        self.thread.start()
        
        return self

    def end_timing(self, end_message):
        self.stop_event.set()
        self.thread.join()
        elapsed_time = time.time() - self.start_time
        # # 手动添加该代码，避免出现 `xxxx [Use 2.0s][1.9s]` 这样的输出
        # time.sleep(0.2)
        print_info(f'\r{end_message} [Use {elapsed_time:.1f}s]')

# 示例使用
if __name__ == '__main__':
    t = Timer().start_timing('Loading Files ...')
    # 模拟一些耗时的操作
    time.sleep(10)
    t.end_timing('Loading Files Done')
