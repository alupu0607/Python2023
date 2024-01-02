import socket

class RedisClient:
    def __init__(self, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send_data(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def _receive_data(self, buffer_size=1024):
        data = b""
        while True:
            chunk = self.socket.recv(buffer_size)
            data += chunk
            if not chunk or b"\r\n" in chunk:
                break
        return data.decode('utf-8')

    def _send_command(self, command):
        self._send_data(command)
        return self._receive_data()

    def ping(self):
        try:
            response = self._send_command("*1\r\n$4\r\nPING\r\n")
            return response.strip() == "+PONG"
        except Exception as e:
            print(f"Error during PING: {e}")
            return False
    def close(self):
        self.socket.close()

# Example usage:
#redis_client = RedisClient()

#ping_success = redis_client.ping()
#print("Ping success:", ping_success)

#redis_client.close()
