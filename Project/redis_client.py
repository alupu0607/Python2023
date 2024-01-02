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

    def lists_set_lpush(self, key, *values):
        command = f"*{2 + len(values)}\r\n$5\r\nLPUSH\r\n${len(key)}\r\n{key}\r\n"
        for value in values:
            command += f"${len(str(value))}\r\n{value}\r\n"
        return self._send_command(command)

    def lists_update_linsert(self, key, position, pivot, *values):
        options = {"BEFORE": "BEFORE", "AFTER": "AFTER"}
        if position.upper() not in options:
            raise ValueError("Invalid position. Use 'BEFORE' or 'AFTER'.")

        command = f"*{4 + len(values)}\r\n$7\r\nLINSERT\r\n${len(key)}\r\n{key}\r\n${len(options[position])}\r\n{options[position]}\r\n${len(pivot)}\r\n{pivot}\r\n"
        for value in values:
            command += f"${len(str(value))}\r\n{value}\r\n"
        return self._send_command(command)

    def lists_get_lrange(self, key, start, stop):
        command = f"*4\r\n$6\r\nLRANGE\r\n${len(key)}\r\n{key}\r\n${len(str(start))}\r\n{start}\r\n${len(str(stop))}\r\n{stop}\r\n"
        return self._send_command(command)

    def lists_del_lrem(self, key, count, element):
        command = f"*4\r\n$4\r\nLREM\r\n${len(key)}\r\n{key}\r\n${len(str(count))}\r\n{count}\r\n${len(str(element))}\r\n{element}\r\n"
        return self._send_command(command)

    def ping(self):
        try:
            response = self._send_command("*1\r\n$4\r\nPING\r\n")
            return response.strip() == "+PONG"
        except Exception as e:
            print(f"Error during PING: {e}")
            return False
    def close(self):
        self.socket.close()


redis_client = RedisClient()
# LPUSH
lpush_response = redis_client.lists_set_lpush("my_list2", "value1", "value2", "value3")
print("LPUSH Response:", lpush_response)

# LINSERT
#linsert_response = redis_client.lists_update_linsert("my_list", "AFTER", "value1", "new_value")
#print("LINSERT Response:", linsert_response)

# LRANGE
lrange_response = redis_client.lists_get_lrange("my_list2", 0, -1)
print("LRANGE Response:", lrange_response)

# LREM
lrem_response = redis_client.lists_del_lrem("my_list", 1, "value2")
print("LREM Response:", lrem_response)
redis_client.close()

