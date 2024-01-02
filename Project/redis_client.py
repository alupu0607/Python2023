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

    def sets_srem(self, key, *members):
        command = f"*{2 + len(members)}\r\n$4\r\nSREM\r\n${len(key)}\r\n{key}\r\n"
        for member in members:
            command += f"${len(member)}\r\n{member}\r\n"
        return self._send_command(command)

    def sets_sadd(self, key, *members):
        command = f"*{2 + len(members)}\r\n$4\r\nSADD\r\n${len(key)}\r\n{key}\r\n"
        for member in members:
            command += f"${len(member)}\r\n{member}\r\n"
        return self._send_command(command)

    def sets_smembers(self, key):
        command = f"*2\r\n$8\r\nSMEMBERS\r\n${len(key)}\r\n{key}\r\n"
        return self._send_command(command)

    def sets_smove(self, source, destination, member):
        command = f"*4\r\n$5\r\nSMOVE\r\n${len(source)}\r\n{source}\r\n${len(destination)}\r\n{destination}\r\n${len(member)}\r\n{member}\r\n"
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
srem_response = redis_client.sets_srem("my_set", "member1", "member2")
print("SREM Response:", srem_response)

# SADD
sadd_response = redis_client.sets_sadd("my_set", "member3", "member4")
print("SADD Response:", sadd_response)


sadd_response2 = redis_client.sets_sadd("my_set2", "ala", "bala")
print("SADD Response:", sadd_response2)

# SMEMBERS
smembers_response = redis_client.sets_smembers("my_set")
print("SMEMBERS Response:", smembers_response)

# SMOVE
smove_response = redis_client.sets_smove("my_set2", "my_set1", "ala")
print("SMOVE Response:", smove_response)

redis_client.close()

