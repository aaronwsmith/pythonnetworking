from socket import socket, AF_INET, SOCK_STREAM

ip       = '127.0.0.1'
portlist = [ 22, 80, 443 ]

for port in portlist:
    sock    = socket( AF_INET, SOCK_STREAM )
    pstatus = sock.connect_ex( (ip,port) )

    print( f'{ip}: port {port} status: {pstatus}' )

    sock.close()
