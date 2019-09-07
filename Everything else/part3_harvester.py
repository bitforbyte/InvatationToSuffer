#!/usr/bin/env python3
import sys, signal, socket, time, datetime, threading

global_lock = threading.Lock()
file_buffer = []
thread_list = []

class MonThread (threading.Thread):
    def __init__(self, threadID, name, ip, port, wait_time):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.ip = ip
      self.port = port
      self.wait_time = wait_time
      self.stop = threading.Event()

    def stop_it(self):
        self.stop.set()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.ip, self.port))
            while True:
                data = self.recv_timeout(sock)
                self.print_to_arbiter(data)
                if self.stop.is_set():
                    sock.close()
                    return

        except Exception as e:
            sock.close()
            print("Hit error:")
            print(e);
            sys.exit(0)

    def recv_timeout(self, the_socket):
        the_socket.setblocking(0)
        total_data=[];data=b'';begin=time.time()
        while 1:
            #if you got some data, then break after wait sec
            if total_data and time.time()-begin>self.wait_time:
                break
            #if you got no data at all, wait a little longer
            #elif time.time()-begin>timeout*2:
            #    break
            try:
                if self.stop.is_set():
                    return ""

                data=the_socket.recv(1024)
                if data:
                    now = datetime.datetime.now()
                    tmp = data.decode().replace('\n', '|')
                    total_data.append(tmp)
                    begin=time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        return now.strftime("%Y-%m-%d %H:%M:%S") + '--' + self.name + '--' + ''.join(total_data)

    def print_to_arbiter(self, string):
        global global_lock
        global file_buffer

        global_lock.acquire()
        file_buffer.append(string)
        global_lock.release()

class arbiterThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.stop = threading.Event()

    def stop_it(self):
        self.stop.set()

    def run(self):
        global global_lock
        global file_buffer

        while True:
            time.sleep(5)
            global_lock.acquire()

            for line in file_buffer:
                print(line)

            file_buffer = []

            global_lock.release()
            
            if self.stop.is_set():
                return


arbiter = arbiterThread(0, "arbiter")

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    for i in thread_list:
        i.stop_it()
    arbiter.stop_it()

signal.signal(signal.SIGINT, signal_handler)



if __name__ == "__main__":
    tid = 1
    for line in sys.stdin:
        items = line.split(',')
        thread_list.append(MonThread(tid, items[0], items[1], int(items[2]), 7))
        tid += 1

    arbiter.start()
    for thread in thread_list:
        thread.start()


    arbiter.join()
    for thread in thread_list:
        thread.join()
