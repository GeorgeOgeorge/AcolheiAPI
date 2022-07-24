import socket

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        server_ip = s.getsockname()[0]
    except Exception:
        server_ip = '127.0.0.1'
    finally:
        s.close()
    return server_ip
