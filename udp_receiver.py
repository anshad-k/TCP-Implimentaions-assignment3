# receiver.py - The receiver in the reliable data transer protocol
import packet
import socket
import sys
import time
import os
import seaborn as sns
import numpy as np

SERVER_ADDR = ('127.0.0.1', 5000)
RECEIVER_ADDR = ('127.0.0.1', 8081)
MAX_PACKETS = 4096
BUFFER_SIZE = 26 * 1024

# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        print('Unable to open', filename)
        return
    
    expected_num = 0
    received_packets = [False] * MAX_PACKETS
    sock.sendto(b"SYN", SERVER_ADDR)
    print('Connection request sent to', SERVER_ADDR)
    while True:
        # Get the next packet from the sender
        pkt, addr = sock.recvfrom(BUFFER_SIZE)
        if addr != SERVER_ADDR:
            continue
        if not pkt or pkt == b"FIN" or len(pkt) == 0:
            break
        seq_num, data = packet.extract(pkt)
        print('Got packet', seq_num)
        
        # Send back an ACK
        if seq_num == expected_num:
            print('Got expected packet:  Sending ACK', expected_num)
            received_packets[seq_num] = data
            while received_packets[expected_num]:
                expected_num += 1
            pkt = packet.make(expected_num - 1)
            sock.sendto(pkt, addr)
        elif seq_num > expected_num:
            print('Sending ACK', expected_num - 1)
            received_packets[seq_num] = data
            pkt = packet.make(expected_num - 1)
            sock.sendto(pkt, addr)
        else:
            print('Sending ACK', expected_num - 1)
            pkt = packet.make(expected_num - 1)
            sock.sendto(pkt, addr)
    for idx in range(expected_num):
        file.write(received_packets[idx])
    file.close()

# Main function
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Expected filename as command line argument')
        exit()
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR) 
    filename = sys.argv[2]
    interface = sys.argv[1]

    bandwidth = 100 * 1024 * 8 / 1000 #100 KBps to kbps
    packet_size = 25 * 1024 #25 KB
    losses = [.1, 0.5, 1, 1.5, 2, 5] # % loss
    delays = [50, 100, 150, 200, 250, 500] # ms
    delay_deviation = 10 # ms
    
    print("Changing bandwidth to %s kbps" % bandwidth)
    try:
        os.system("sudo tc qdisc add dev %s root netem rate %skbit" % (interface, bandwidth))
    except:
        os.system("sudo tc qdisc del dev %s root" % (interface))
        os.system("sudo tc qdisc add dev %s root netem rate %skbit" % (interface, bandwidth))
    
    download_times_sw = np.random.rand(6, 6) 
    for i, loss in enumerate(losses):
        for j, delay in enumerate(delays):
            print("Setting loss to %s%% and delay to %s ms" % (loss, delay))
            os.system("sudo tc qdisc change dev %s root netem loss %s%% delay %sms %sms distribution normal" % (interface, loss, delay, delay_deviation))
            start_time = time.time()
            receive(sock, filename)
            end_time = time.time()
            download_times_sw[i][j] = end_time - start_time
    # start_time = time.time()
    # receive(sock, filename)
    # end_time = time.time()
    # print('Time taken: %s ms' % (end_time - start_time))
    print("resetting the interface")
    os.system("sudo tc qdisc del dev %s root" % (interface))
    sock.close()