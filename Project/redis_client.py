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

    def strings_set(self, key, value):
        command = f"*3\r\n$3\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(str(value))}\r\n{value}\r\n"
        return self._send_command(command)

    def strings_get(self, key):
        command = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
        return self._send_command(command)

    def strings_incrby(self, key, increment):
        command = f"*3\r\n$6\r\nINCRBY\r\n${len(key)}\r\n{key}\r\n${len(str(increment))}\r\n{increment}\r\n"
        return self._send_command(command)

    def strings_del(self, *keys):
        command = f"*{len(keys) + 1}\r\n$3\r\nDEL\r\n"
        for key in keys:
            command += f"${len(key)}\r\n{key}\r\n"
        response = self._send_command(command)
        return response

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
redis_client = RedisClient()

# Set a string
set_response = redis_client.strings_set("my_key4", "my_value")
print("SET Response:", set_response)

# Get a string
get_response = redis_client.strings_get("my_key")
print("GET Response:", get_response)

# Increment a string by a certain value
incrby_response = redis_client.strings_incrby("counter", 5)
print("INCRBY Response:", incrby_response)

# Delete multiple keys
del_response = redis_client.strings_del("my_key4", "key2", "key3")
print("DEL Response:", del_response)


redis_client.close()

