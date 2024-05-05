import socket
import time

class Timer(object):
    TIMER_STOP = -1

    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    # Starts the timer
    def start(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    # Stops the timer
    def stop(self):
        if self._start_time != self.TIMER_STOP:
            self._start_time = self.TIMER_STOP

    # Determines whether the timer is runnning
    def running(self):
        return self._start_time != self.TIMER_STOP

    # Determines whether the timer timed out
    def timeout(self):
        if not self.running():
            return False
        else:
            return time.time() - self._start_time >= self._duration
        

class UDPServer:
    SW = 0
    GBN = 1
    SR = 2
    def __init__(self, file_name, packet_size, window_size, RTO, port=5000):
        self.port = port
        self.file = open(file_name, "rb")
        if self.file is None:
            print("File not found")
            del self
            return
        self.packet_size = packet_size
        self.window_size = window_size
        self.RTO = RTO
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def run(self, tcp_algorithm):
        self.__sock.bind(("", self.port))
        file = open(self.file_name, "rb")
        if file is None:
            print("File not found")
            return
        if tcp_algorithm == UDPServer.SW:
            self.__stop_and_wait()
        elif tcp_algorithm == UDPServer.GBN:
            self.__go_back_n()
        elif tcp_algorithm == UDPServer.SR:
            self.__selective_repeat()
        else:
            print("Invalid TCP algorithm")
    def __stop_and_wait(self):
        pass
    def __go_back_n(self):
        pass
    def __selective_repeat(self):
        pass
    def __del__(self):
        if self.__sock is not None:
          self.__sock.close()
        if self.file is not None:
          self.file.close()

if __name__ == "__main__":
    # server = UDPServer()
    # server.run()
    pass