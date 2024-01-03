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




    def zsets_zcard(self, key):
        command = [
            "*2\r\n",
            "$5\r\nZCARD\r\n",
            f"${len(key)}\r\n{key}\r\n"
        ]

        #print(''.join(command))
        return self._send_command(''.join(command))

    def zsets_zrem(self, key, *members):
        command = [
            f"*{2 + len(members)}\r\n",
            "$4\r\nZREM\r\n",
            f"${len(key)}\r\n{key}\r\n"
        ]

        for member in members:
            command.extend([
                f"${len(str(member))}\r\n{member}\r\n"
            ])

        print(''.join(command))
        return self._send_command(''.join(command))

    def zsets_zincrby(self, key, increment, member):
        command = [
            "*4\r\n",
            "$7\r\nZINCRBY\r\n",
            f"${len(key)}\r\n{key}\r\n",
            f"${len(str(increment))}\r\n{increment}\r\n",
            f"${len(str(member))}\r\n{member}\r\n"
        ]

        print(''.join(command))
        return self._send_command(''.join(command))

    def zsets_zadd(self, key, *args,nx=False, xx=False, gt=False, lt=False, ch=False, incr=False):
        if len(args) % 2 == 1:
            raise ValueError("Invalid number of arguments. Must provide score and member pairs.")

        command = ["*"]

        num_elements = 2 + len(args) + (1 if nx or xx else 0) + (1 if gt or lt else 0) + ch + incr
        command.append(str(num_elements) + "\r\n")

        command.append("$4\r\nZADD\r\n")
        command.append(f"${len(key)}\r\n{key}\r\n")

        if nx:
            command.extend(["$2\r\nNX\r\n"])
        elif xx:
            command.extend(["$2\r\nXX\r\n"])

        if lt:
            command.extend(["$2\r\nGT\r\n"])
        elif gt:
            command.extend(["$2\r\nLT\r\n"])

        if ch:
            command.extend(["$2\r\nCH\r\n"])

        if incr:
            command.extend(["$4\r\nINCR\r\n"])

        for i in range(0, len(args), 2):
            score, member = args[i], args[i + 1]
            command.extend([f"${len(str(score))}\r\n{score}\r\n", f"${len(str(member))}\r\n{member}\r\n"])

        command_str = ''.join(command)
        print(command_str)
        return self._send_command(command_str)


redis_client = RedisClient()

#ZCARD
#result1 = redis_client.zsets_zcard('my_zset')
#print(result1)

# ZADD
result = redis_client.zsets_zadd('my_zset',  1, 'one', 2, 'two', 3, 'three', 4, "twelve", nx=False, xx=False, lt=False,
                                 gt=False, ch=False, incr=False,)
print(result)
# ZREM
#result2 = redis_client.zsets_zrem('my_zset', 'member1', 'member2', 'member3')
#print(result2)
# ZINCRBY
#new_score = redis_client.zsets_zincrby('my_zset', 5.0, 'member2')
#print(f"New score of member2 in my_zset: {new_score}")

redis_client.close()

