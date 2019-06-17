"""

For request-based servers (including socket-based):

- client address verification before further looking at the request
        (This is actually a hook for any processing that needs to look
         at the request before anything else, e.g. logging)
- how to handle multiple requests:
        - synchronous (one request is handled at a time)
        - forking (each request is handled by a new process)
        - threading (each request is handled by a new thread)

Another approach to handling multiple simultaneous requests in an
environment that supports neither threads nor fork (or where these are
too expensive or inappropriate for the service) is to maintain an
explicit table of partially finished requests and to use a selector to
decide which request to work on next (or whether to handle a new
incoming request).  This is particularly important for stream services
where each client can potentially be connected for a long time (if
threads or subprocesses cannot be used).

"""

# Author of the BaseServer patch which this is based off of: Luke Kenneth Casson Leighton

__version__ = "1.0"


import socket
import os
import sys
import threading
from modbus_handler import ModService
#from time import monotonic as time

__all__ = ["Server"]

class Server(ModService):
    """
    Methods for derived classes:

   Public Methods:

    - serve_forever()
    - stop_serve()

    """

    def __init__(self, host=None, port=None, handlerclass=None, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        self.server_address = (host, port) #convert to socket style address
        self.address_family = socket.AF_INET
        self.socket_type = socket.SOCK_STREAM

        self.handler = handlerclass()

        self.timeout = None
        self.request_queue_size = 100
        self.allow_reuse_address = False

        self.__is_not_serving = threading.Event()
        self.__is_not_serving.set()
        self.__shutdown_request = False

        #Values of 1 == True
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.settimeout(3)

        self.debug = True

        if bind_and_activate:
            try:
                self.socket.bind(self.server_address)
                self.socket.listen(self.request_queue_size)
            except:
                self.socket.close()
                raise
        if self.debug:
            print(self.socket.getsockname())


    def handle_timeout(self): pass #future for various things, don't want one task taknig up the whole chain


    def handle_error(self, conn, client_address): #Handle an error gracefully.  The default is to print a traceback and continue.
        print('-'*40, file=sys.stderr)
        print('Exception happened during processing of request from',
            client_address, file=sys.stderr)
        import traceback
        traceback.print_exc()
        print('-'*40, file=sys.stderr)

    def stop_serve(self): 
    # blocks until serve_forever loop is done. this lets
    # this lets requests finish being handled
        if not self.__is_not_serving.is_set():
            self.__shutdown_request = True
            self.__is_shut_down.wait()
        else:pass


    def shutdown_conn(self, conn):
        """Called to shutdown and close an individual request."""
        try:
            #explicitly shutdown.  socket.close() merely releases
            #the socket and waits for GC to perform the actual close.
            conn.shutdown(socket.SHUT_WR)
        except OSError:
            pass #some platforms may raise ENOTCONN here
        finally: conn.close()

    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.__is_not_serving.clear()
        try:
            while not self.__shutdown_request:
                try: #need selector pol for shutdown request
                    conn, addr = self.socket.accept()
                    none_if_return_msg_success = self.handle_request(conn, addr)
                    if not none_if_return_msg_success: print('return send successful')
                    if none_if_return_msg_success: print('no return send message')
                except socket.timeout:
                    if self.debug: print('blocking call: socket.accept() timeout, recycling accept call')
                #except: print('exception called')
        finally:
            self.__shutdown_request = False
            self.__is_not_serving.set()

    def handle_request(self, conn, addr):

        if self.debug:
            print('Connected by: ', addr)
            print('Servier Side Connection: ', conn.getsockname())

        data = bytes()

        data = conn.recv(1024)
        #if self.debug: print('chunk: {}'.format(chunk))
        if self.debug: print('data {}'.format(data))
        #handoff to modbus handler
        return_bytes = self.handler.handle(data)
        return conn.sendall(return_bytes) #sendall returns None if successful

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.server_close()

if __name__ == "__main__":

    def cmdlist():
        global s
        print('\n r        reset server')
        print(' stop     stop serve_forever')
        print(' start    start serve_forever')
        print(' setbit')
        print(' getbit')
        print('-------------------------------')
        x = input('Command: ')

        if x=='r': make_server()
        if x=='stop': s.stop_serve()
        if x=='start': s.serve_forever()
        if x=='setbit': s.handler.set_bits(0,[1])
        if x=='getbit': print(s.handler.get_bits(0))
        cmdlist()

    def make_server():
        global s
        s = Server(host='localhost', port=0, handlerclass=ModService)
        print('\nHost: {}'.format(s.host))
        print('Port: {}'.format(s.port))
        #th.Timer(5, function=test.stop).start()
        #t.serve_forever()

    #try:
    s = Server(host='localhost', port=0, handlerclass=ModService)
    s.serve_forever()

    #cmdlist()
    #finally: input('press enter to exit')