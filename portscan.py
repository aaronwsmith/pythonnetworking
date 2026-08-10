'''
This script performs a port scan against the specified host, defaulting to the localhost. Based on code provided by the
book "Python for Security and Networking" (3rd edition) by Jose Manuel Ortega, Chapter 3 page 88. 

TCP Sockets: SOCK_STREAM
UDP Sockets: SOCK_DGRAM

IPv4: AP_INET
IPv6: AP_INET6

errno: Makes available standard errno system symbols. The value of each symbol is the corresponding integer value.
https://docs.python.org/3/library/errno.html

ipaddress: Provides the capabilities to create, manipulate and operate on IPv4 and IPv6 addresses and networks.
https://docs.python.org/3/library/ipaddress.html

socket: Provides access to the BSD socket interface. It is available on all modern Unix systems, Windows, MacOS, and probably
additional platforms.
https://docs.python.org/3/library/socket.html

socket.connect_ex(): This is like connect(address), but returns an error code (the errno value) instead of raising an exception.
'''

from argparse  import ArgumentParser
from errno     import errorcode
from ipaddress import ip_address, ip_network
from os        import strerror
from socket    import socket, getservbyport, AF_INET, SOCK_STREAM

if __name__ == '__main__':
    try:
        argparser = ArgumentParser( description = 'Port scanner' )

        argparser.add_argument( '-ho', '--host'  , type   = str             , default = '127.0.0.1'        , help = 'IP or CIDR to scan (default: 127.0.0.1)' )
        argparser.add_argument( '-p', '--ports'  , type   = str, nargs = '+', default = ['22', '80', '443'], help = 'List of ports to scan (default: 22, 80, 443). You can '
                                                                                                                    'specify a range of ports using a hyphen (e.g., 1-1000)' )
        argparser.add_argument( '-t', '--timeout', type   = float           , default = 0.01               , help = 'Timeout in seconds for each port scan (default: 0.01)' )
        argparser.add_argument( '-v', '--verbose', action = 'store_true'    , default = False              , help = 'Enable verbose output' )

        args  = argparser.parse_args()
        ports = set()

        for p in args.ports:
            if '-' in p:
                start, end = p.split( '-' )
                ports.update( range( int(start), int(end) + 1 ) )
            else:
                ports.add( int(p) )

        if '/' in args.host:
            hosts = ip_network( args.host ).hosts()
        else:
            hosts = [ ip_address(args.host) ]

        for ip in hosts:
            ip = ip.exploded

            for port in ports:
                with socket( AF_INET, SOCK_STREAM ) as sock:    
                    sock.settimeout( args.timeout )
                    pstatus = sock.connect_ex( (ip,port) )

                    if pstatus == 0:
                        pstatusdisplay = 'OPEN'
                    elif args.verbose:
                        errstr = errorcode.get( pstatus, 'Unknown error' )
                        stderr = strerror( pstatus )

                        if stderr != 'Unknown error':
                            pstatusdisplay = f'{errstr}: {stderr}'
                        else:
                            pstatusdisplay = f'{errstr} ({pstatus})'

                    try:
                        service = f' ({getservbyport(port)})'
                    except OSError:
                        service = ''

                    if args.verbose or pstatus == 0:
                        print( f'{ip}: port {port:>5}{service}: {pstatusdisplay}' )
    except KeyboardInterrupt:
        pass
