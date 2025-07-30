'''
Simple script that performs an HTTP fetch/get operation for the Debian README page for mirror servers. The main lesson from this
example is how to receive data in chunks of 512 bytes at a time, ending when the length of data received is less than 1 (i.e. no
further data received.)

Based on code provided by the book "Python for Security and Networking" by Jose Manuel Ortega, Chapter 3 page 89.
'''
from socket import socket, AF_INET, SOCK_STREAM

sock = socket( AF_INET, SOCK_STREAM )
sock.connect( ('ftp.debian.org', 80) )

cmd = 'GET http://ftp.debian.org/debian/README.mirrors.txt HTTP/1.0\r\n\r\n'.encode()
sock.send( cmd )

while True:
    data = sock.recv( 512 )

    if len( data ) < 1:
        break

    print( data.decode(), end = '' )

sock.close()