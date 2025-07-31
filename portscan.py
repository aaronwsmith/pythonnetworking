'''
This script performs a port scan against the specified host, defaulting to the localhost. Based on code provided by the
book "Python for Security and Networking" by Jose Manuel Ortega, Chapter 3 page 88. 

TCP Sockets: SOCK_STREAM
UDP Sockets: SOCK_DGRAM

IPv4: AP_INET
IPv6: AP_INET6

errno: This module makes available standard errno system symbols. The value of each symbol is the corresponding integer value.
https://docs.python.org/3/library/errno.html

socket: This module provides access to the BSD socket interface. It is available on all modern Unix systems, Windows, MacOS,
and probably additional platforms.
https://docs.python.org/3/library/socket.html
'''

import errno
import os
import sys
from   socket import socket, getservbyport, AF_INET, SOCK_STREAM


if __name__ == '__main__':
    if len( sys.argv ) == 1:
        sys.argv.append( '127.0.0.1' )

    for ip in sys.argv[1:]:
        print( ip )
        portlist = [ 22, 80, 443 ]

        for port in portlist:
            sock    = socket( AF_INET, SOCK_STREAM )
            pstatus = sock.connect_ex( (ip,port) )

            if pstatus == 0:
                pstatus = 'OPEN: Connected'
            else:
                _pstatus = errno.errorcode.get( pstatus, 'Unknown error' )
                pstatus  = f'{_pstatus}: {os.strerror(pstatus)}'

            print( f'{ip}: port {port} ({getservbyport(port)}): {pstatus}' )

            sock.close()
