import select
import socket
import logging
import threading

class CommunicationsInterface:
    @classmethod
    def listen(cls, event_manager, listen_port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(0)
        server_socket.bind((socket.gethostname(), listen_port))
        server_socket.listen(5)

        logging.debug("Bound socket on port %s" % listen_port)        

        while True:

            # Check if there is input
            readable, writable, exceptional = select.select(
                [server_socket], [], [], 0)

            for s in readable:
                (client_socket, address) = s.accept()
                data_received = ''
            
                # Read all the data the client sends
                while True:
                    data = client_socket.recv(1024)
                    data_received += data
                    if not data:
                        break
                logging.debug("Received data: \"%s\"" % data_received)

        server_socket.close()
        logging.debug("Listener thread finished")


    #
    # Broadcast data to all peers
    #
        
    @classmethod
    def broadcast_data(cls, data, peers):
        logging.debug("Broadcasting data: %s" % data)

        for peer in peers:
            try:

                # Connect to peer
                s = socket.create_connection(peer)
                logging.debug("Connected to peer %s:%s" % (peer[0], peer[1]))
                s.sendall(data)
                s.shutdown(socket.SHUT_RDWR)
                s.close()

            except socket.error, e:
                logging.error("Socket error with peer \"%s:%s\": %s" % (
                        peer[0], peer[1], e))

        logging.debug("Broadcast complete")
