import errno
import os
from   socket import socket, AF_INET, SOCK_STREAM

ip       = '127.0.0.1'
portlist = [ 22, 80, 443 ]

for port in portlist:
    sock    = socket( AF_INET, SOCK_STREAM )
    pstatus = sock.connect_ex( (ip,port) )

    if pstatus == 0:
        pstatus = 'OPEN: Connected'
    else:
        _pstatus = errno.errorcode.get( pstatus, 'Unknown error' )
        pstatus  = f'{_pstatus}: {os.strerror(pstatus)}'

    print( f'{ip}: port {port}: {pstatus}' )

    sock.close()
