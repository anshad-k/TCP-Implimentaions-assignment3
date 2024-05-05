import socket
import sys
import time
import _thread
import udt
from timer import Timer
import packet

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
        self.timer = Timer(RTO)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.mutex = _thread.allocate_lock()
        self.base = 0
    
    def run(self, tcp_algorithm):
        self.__sock.bind(("", self.port))
        file = open(self.file_name, "rb")
        if file is None:
            print("File not found")
            return
        while True:
            message, address = self.__sock.recvfrom(32)
            if message != b"SYN":
                continue
            if tcp_algorithm == UDPServer.SW:
                self.__stop_and_wait(address)
            elif tcp_algorithm == UDPServer.GBN:
                self.__go_back_n(address)
            elif tcp_algorithm == UDPServer.SR:
                self.__selective_repeat(address)
            else:
                print("Invalid TCP algorithm")
    def __stop_and_wait(self, client_address):
        packets = []
        seq_num = 0
        while True:
            data = self.file.read(self.packet_size)
            if not data:
                break
            packets.append(packet.make(seq_num, data))
            seq_num += 1
        
        num_packets = len(packets)
        self.current_packet = 0

        _thread.start_new_thread(self.__SW_receive, (client_address))

        while self.current_packet < num_packets:
            self.mutex.acquire()
            udt.send(packets[self.current_packet], self.__sock, client_address)
            print("Sent packet", self.current_packet)
            self.timer.stop()
            self.timer.start()
            sent_packet = self.current_packet
            self.mutex.release()

            while not self.timer.timeout():
                self.mutex.acquire()
                if self.current_packet > sent_packet:
                    break
                self.mutex.release()
            self.mutex.release()
        udt.send(packet.make_empty(), self.__sock, client_address)
        print("File sent")
    
    def __SW_receive(self, client_address):
        while True:
            pkt, address = udt.recv(self.__sock)
            ack, _ = packet.extract(pkt)
            if address != client_address:
                continue
            if ack == self.current_packet:
                self.mutex.acquire()
                print("Received ACK", ack)
                self.current_packet += 1
                self.mutex.release()


    def __go_back_n(self, client_address):
        pass
    def __selective_repeat(self, client_address):
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