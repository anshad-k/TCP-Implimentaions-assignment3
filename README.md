CS3205: ASSIGNMENT 3

AE20B035 Mohammed Anshad K
MM20B021 Golla Lalith Shiva Sai

## Run the Server
Sending file loco.jpg
`python udp_server.py <tcp_algorithm>`

Stop and Wait: `python udp_server.py 0`
Go Back n: `python udp_server.py 1`
Selective repeat(cumulative ack): `python udp_server.py 2`

## Run the Receiver/Experiment
`python udp_receiver.py <interface> <downloaded_file> <tcp_algorithm>`

interface: lo, wlan0, eth0
downloaded_file: existing file name to which the data is downloaded (eg: loco_dw.jpg)
tcp_algorithm: 0 -> SW, 1 -> GBN, 2 -> SR

## Outputs
Stop_and_Wait.png
Go_Back_n.png
Selective_Repeat.png

### Helper funcions in timer.py and packet.py
