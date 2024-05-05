# receiver.py - The receiver in the reliable data transer protocol
import packet
import socket
import sys
import os
import getpass

SERVER_ADDR = ('localhost', 8080)
RECEIVER_ADDR = ('localhost', 8081)
MAX_PACKET_SIZE = 4096

# Receive packets from the sender
def receive(sock, filename):
    # Open the file for writing
    try:
        file = open(filename, 'wb')
    except IOError:
        os.system('touch ' + filename)
        os.system('echo %s | sudo -S chmod +x %s' % (getpass.getpass(), filename))
        file = open(filename, 'wb')
    
    sock.sendto(b"SYN", SERVER_ADDR)
    
    expected_num = 0
    received_packets = [False] * MAX_PACKET_SIZE
    while True:
        # Get the next packet from the sender
        pkt, addr = sock.recvfrom(1024)
        if addr != SERVER_ADDR:
            continue
        if not pkt or pkt == b"FIN" or len(pkt) == 0:
            break
        seq_num, data = packet.extract(pkt)
        print('Got packet', seq_num)
        
        # Send back an ACK
        if seq_num == expected_num:
            print('Got expected packet')
            print('Sending ACK', expected_num)
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
    for data in received_packets:
        file.write(data)
    file.close()

# Main function
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Expected filename as command line argument')
        exit()
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(RECEIVER_ADDR) 
    filename = sys.argv[1]
    receive(sock, filename)
    sock.close()