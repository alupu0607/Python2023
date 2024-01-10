import socket

class RedisClient:
    """This class provides methods to connect to a Redis server, encode and decode text, and perform
        various CRUD operations on Redis data types (Strings, Hashes, Sets, Sorted Sets, Lists).

        The Redis server expects commands in an array of strings format. Each command is represented
        by an array containing the number of elements, the length of each string, and the actual content
        of each string.

        Args:
            host (str): The Redis server host.
            port (int): The Redis server port.

        Attributes:
            host (str): The Redis server host.
            port (int): The Redis server port.
            socket (socket.socket): The socket object for communication with the Redis server.

        Methods:
        __init__(self, host='localhost', port=6379): Initializes a new instance of the RedisClient class.
        _send_data(self, data): Sends data to the Redis server.
        _receive_data(self, buffer_size=1024): Receives data from the Redis server.
        _send_command(self, command): Sends a Redis command and receives the server's response.
        ping(self): Sends a PING command to the Redis server and checks for a successful response.
        close(self): Closes the socket connection to the Redis server.
        strings_set(self, key, value): Sets the value of a key in the Redis database.
        strings_get(self, key): Retrieves the value of a key from the Redis database.
        strings_incrby(self, key, increment): Increments the value of a key in the Redis database.
        strings_del(self, *keys): Deletes one or more keys from the Redis database.
        lists_set_lpush(self, key, *values): Prepends one or more values to a list in the Redis database.
        lists_update_linsert(self, key, position, pivot, *values): Inserts one or more values either before or after a specified pivot element in a list.
        lists_get_lrange(self, key, start, stop): Retrieves a range of elements from a list in the Redis database.
        lists_del_lrem(self, key, count, element): Removes elements from a list in the Redis database.
        sets_sadd(self, key, *members): Adds one or more members to a set in the Redis database.
        sets_smembers(self, key): Retrieves all members of a set from the Redis database.
        sets_smove(self, source, destination, member): Moves a member from one set to another in the Redis database.
        zsets_zcard(self, key): Retrieves the number of elements in a sorted set in the Redis database.
        zsets_zrem(self, key, *members): Removes one or more members from a sorted set in the Redis database.
        zsets_zincrby(self, key, increment, member): Increments the score of a member in a sorted set in the Redis database.
        zsets_zadd(self, key, *args, nx=False, xx=False, gt=False, lt=False, ch=False, incr=False):
            Adds one or more members with scores to a sorted set in the Redis database. Supports various options.
        hashes_hset(self, key, *args): Sets the values of multiple fields in a hash in the Redis database.
        hashes_hget(self, key, field): Retrieves the value of a field from a hash in the Redis database.
        hashes_hdel(self, key, *fields): Deletes one or more fields from a hash in the Redis database.
        hashes_hincrby(self, key, field, increment): Increments the value of a field in a hash in the Redis database.

        """
    def __init__(self, host='localhost', port=6379):
        """Initializes a new instance of the RedisClient class.

        Args:
            host (str): The Redis server host.
            port (int): The Redis server port.
        """
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def _send_data(self, data):
        """Sends data to the Redis server.

        Args:
            data (str): The data to be sent.
        """
        self.socket.sendall(data.encode('utf-8'))

    def _receive_data(self, buffer_size=1024):
        """Receives data from the Redis server.

        Args:
            buffer_size (int): The buffer size for receiving data.

        Returns:
            str: The received data.
        """
        data = b""
        while True:
            chunk = self.socket.recv(buffer_size)
            data += chunk
            if not chunk or b"\r\n" in chunk:
                break
        return data.decode('utf-8') #convert strings into bytes

    def _send_command(self, command):
        """Sends a Redis command and receives the server's response.

        Args:
            command (str): The Redis command.

        Returns:
            str: The server's response to the command.
        """
        self._send_data(command)
        return self._receive_data()

    def ping(self):
        """Ping the Redis server to check if it's alive.

        Returns:
            bool: True if the server responds with "+PONG", False otherwise.
        """
        try:
            response = self._send_command("*1\r\n$4\r\nPING\r\n")
            return response.strip() == "+PONG"
        except Exception as e:
            print(f"Error during PING: {e}")
            return False

    def close(self):
        """
        Close the connection to the Redis server.
        """
        self.socket.close()

    def strings_set(self, key, value, nx=False, xx=False, get=False, ex=None, px=None, exat=None, pxat=None,
                    keepttl=False):
        """Set the value of a key in Redis.

        Args:
            key (str): The key to set.
            value (str): The value to associate with the key.
            nx (bool): Only set the key if it does not exist.
            xx (bool): Only set the key if it already exists.
            get (bool): Return the old value of the key if it exists.
            ex (int): Set the specified expire time in seconds.
            px (int): Set the specified expire time in milliseconds.
            exat (int): Set the expire time using the UNIX timestamp in seconds.
            pxat (int): Set the expire time using the UNIX timestamp in milliseconds.
            keepttl (bool): Retain the time to live associated with the key.

        Returns:
            str: The Redis server response.
        """
        command_parts = ["*"]

        num_elements = 3 + (1 if nx or xx else 0) + (1 if get else 0) + (2 if ex is not None else 0) + \
                       (2 if px is not None else 0) + (2 if exat is not None else 0) + (2 if pxat is not None else 0) + \
                       (1 if keepttl else 0)
        command_parts.append(str(num_elements) + "\r\n")

        command_parts.extend(["$3\r\nSET\r\n", f"${len(key)}\r\n{key}\r\n", f"${len(str(value))}\r\n{value}\r\n"])

        if nx:
            command_parts.extend(["$2\r\nNX\r\n"])
        elif xx:
            command_parts.extend(["$2\r\nXX\r\n"])

        if get:
            command_parts.extend(["$3\r\nGET\r\n"])

        if ex is not None:
            command_parts.extend(["$2\r\nEX\r\n", f"${len(str(ex))}\r\n{ex}\r\n"])
        elif px is not None:
            command_parts.extend(["$2\r\nPX\r\n", f"${len(str(px))}\r\n{px}\r\n"])
        elif exat is not None:
            command_parts.extend(["$4\r\nEXAT\r\n", f"${len(str(exat))}\r\n{exat}\r\n"])
        elif pxat is not None:
            command_parts.extend(["$4\r\nPXAT\r\n", f"${len(str(pxat))}\r\n{pxat}\r\n"])
        elif keepttl:
            command_parts.extend(["$7\r\nKEEPTTL\r\n"])

        command = ''.join(command_parts)
        print(command)
        return self._send_command(command)

    def strings_get(self, key):
        """Retrieves the value associated with a key from the Redis server.

        Args:
            key (str): The key to retrieve.

        Returns:
            str: The value associated with the key.
        """
        command = f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n"
        return self._send_command(command)

    def strings_incrby(self, key, increment):
        """Increments the integer value of a key in the Redis server by a specified amount.

        Args:
            key (str): The key to increment.
            increment (int): The amount by which to increment the value.

        Returns:
            str: The server's response after executing the INCRBY command.
        """
        command = f"*3\r\n$6\r\nINCRBY\r\n${len(key)}\r\n{key}\r\n${len(str(increment))}\r\n{increment}\r\n"
        return self._send_command(command)

    def strings_del(self, *keys):
        """Deletes one or more keys from the Redis server.

        Args:
            *keys (str): Variable number of keys to delete.

        Returns:
            str: The server's response after executing the DEL command.
        """
        command = f"*{len(keys) + 1}\r\n$3\r\nDEL\r\n"
        for key in keys:
            command += f"${len(key)}\r\n{key}\r\n"
        response = self._send_command(command)
        return response

    def lists_set_lpush(self, key, *values):
        """Inserts one or more values at the beginning of a list in the Redis server.

        Args:
            key (str): The key of the list.
            *values: Variable number of values to insert.

        Returns:
            str: The server's response after executing the LPUSH command.
        """
        command = f"*{2 + len(values)}\r\n$5\r\nLPUSH\r\n${len(key)}\r\n{key}\r\n"
        for value in values:
            command += f"${len(str(value))}\r\n{value}\r\n"
        return self._send_command(command)

    def lists_update_linsert(self, key, position, pivot, *values):
        """Inserts values before or after a specified pivot element in a list in the Redis server.

        Args:
            key (str): The key of the list.
            position (str): The position to insert values - 'BEFORE' or 'AFTER'.
            pivot (str): The pivot element before or after which values will be inserted.
            *values: Variable number of values to insert.

        Returns:
            str: The server's response after executing the LINSERT command.
        """
        options = {"BEFORE": "BEFORE", "AFTER": "AFTER"}
        if position.upper() not in options:
            raise ValueError("Invalid position. Use 'BEFORE' or 'AFTER'.")

        command = f"*{4 + len(values)}\r\n$7\r\nLINSERT\r\n${len(key)}\r\n{key}\r\n${len(options[position])}\r\n{options[position]}\r\n${len(pivot)}\r\n{pivot}\r\n"
        for value in values:
            command += f"${len(str(value))}\r\n{value}\r\n"
        return self._send_command(command)

    def lists_get_lrange(self, key, start, stop):
        """Returns a range of elements from a list in the Redis server.

        Args:
            key (str): The key of the list.
            start (int): The start index of the range.
            stop (int): The stop index of the range.

        Returns:
            str: The server's response after executing the LRANGE command.
        """
        command = f"*4\r\n$6\r\nLRANGE\r\n${len(key)}\r\n{key}\r\n${len(str(start))}\r\n{start}\r\n${len(str(stop))}\r\n{stop}\r\n"
        return self._send_command(command)

    def lists_del_lrem(self, key, count, element):
        """Removes elements from a list in the Redis server.

            Args:
                key (str): The key of the list.
                count (int): The number of occurrences to remove.
                element: The element to remove.

            Returns:
                str: The server's response after executing the LREM command.
        """
        command = f"*4\r\n$4\r\nLREM\r\n${len(key)}\r\n{key}\r\n${len(str(count))}\r\n{count}\r\n${len(str(element))}\r\n{element}\r\n"
        return self._send_command(command)

    def sets_srem(self, key, *members):
        """Removes one or more members from a set in the Redis server.

        Args:
            key (str): The key of the set.
            *members: Variable number of members to remove.

        Returns:
            str: The server's response after executing the SREM command.
        """
        command = f"*{2 + len(members)}\r\n$4\r\nSREM\r\n${len(key)}\r\n{key}\r\n"
        for member in members:
            command += f"${len(member)}\r\n{member}\r\n"
        return self._send_command(command)

    def sets_sadd(self, key, *members):
        """Adds one or more members to a set in the Redis server.

        Args:
            key (str): The key of the set.
            *members: Variable number of members to add.

        Returns:
            str: The server's response after executing the SADD command.
        """
        command = f"*{2 + len(members)}\r\n$4\r\nSADD\r\n${len(key)}\r\n{key}\r\n"
        for member in members:
            command += f"${len(member)}\r\n{member}\r\n"
        return self._send_command(command)

    def sets_smembers(self, key):
        """Returns all members of a set in the Redis server.

        Args:
            key (str): The key of the set.

        Returns:
            str: The server's response after executing the SMEMBERS command.
        """
        command = f"*2\r\n$8\r\nSMEMBERS\r\n${len(key)}\r\n{key}\r\n"
        return self._send_command(command)

    def sets_smove(self, source, destination, member):
        """Moves a member from one set to another in the Redis server.

        Args:
            source (str): The key of the source set.
            destination (str): The key of the destination set.
            member: The member to move.

        Returns:
            str: The server's response after executing the SMOVE command.
        """
        command = f"*4\r\n$5\r\nSMOVE\r\n${len(source)}\r\n{source}\r\n${len(destination)}\r\n{destination}\r\n${len(member)}\r\n{member}\r\n"
        return self._send_command(command)




    def zsets_zcard(self, key):
        """Returns the number of members in a sorted set in the Redis server.

        Args:
            key (str): The key of the sorted set.

        Returns:
            str: The server's response after executing the ZCARD command.
        """
        command = [
            "*2\r\n",
            "$5\r\nZCARD\r\n",
            f"${len(key)}\r\n{key}\r\n"
        ]

        #print(''.join(command))
        return self._send_command(''.join(command))

    def zsets_zrem(self, key, *members):
        """Removes one or more members from a sorted set in the Redis server.

        Args:
            key (str): The key of the sorted set.
            *members: Variable number of members to remove.

        Returns:
            str: The server's response after executing the ZREM command.
        """
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
        """Increments the score of a member in a sorted set in the Redis server.

        Args:
            key (str): The key of the sorted set.
            increment: The amount by which to increment the score.
            member: The member whose score should be incremented.

        Returns:
            str: The server's response after executing the ZINCRBY command.
        """
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
        """Adds one or more members to a sorted set in the Redis server.

        Args:
            key (str): The key of the sorted set.
            *args: Variable number of score and member pairs to add.
            nx (bool): Only add new elements if they do not already exist.
            xx (bool): Only update elements that already exist.
            gt (bool): Only add elements with a score greater than the given value.
            lt (bool): Only add elements with a score less than the given value.
            ch (bool): Modify the return value to include the number of elements added.
            incr (bool): Increment the score of existing elements.

        Returns:
            str: The server's response after executing the ZADD command.
        """
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

    def hashes_hset(self, key, *args):
        """Sets the specified fields to their respective values in the hash stored at key.

        Args:
            key (str): The key of the hash.
            *args: Variable number of field-value pairs to set.

        Returns:
            str: The server's response after executing the HSET command.
        """
        ### ONLY WORKS IF I HAVE 1 field-value pair
        if len(args) % 2 != 0:
            raise ValueError("Invalid number of arguments. Must provide field and value pairs.")

        command = ["*"]
        num_elements = 2 + len(args)
        command.append(str(num_elements) + "\r\n")

        command.append("$" + str(len("HSET")) + "\r\nHSET\r\n")
        command.append(f"${len(key)}\r\n{key}\r\n")

        for i in range(0, len(args), 2):
            field, value = args[i], args[i + 1]
            command.extend([f"${len(str(field))}\r\n{field}\r\n", f"${len(str(value))}\r\n{value}\r\n"])

        command_str = ''.join(command)
        print(command_str)
        return self._send_command(command_str)

    def hashes_hget(self, key, field):
        """Gets the value associated with the specified field in the hash stored at key.

        Args:
            key (str): The key of the hash.
            field (str): The field to retrieve.

        Returns:
            str: The server's response after executing the HGET command.
        """
        command = [
            "*3\r\n",
            "$4\r\nHGET\r\n",
            f"${len(key)}\r\n{key}\r\n",
            f"${len(field)}\r\n{field}\r\n"
        ]

        print(''.join(command))
        return self._send_command(''.join(command))

    def hashes_hdel(self, key, *fields):
        """Removes one or more specified fields from the hash stored at key.

        Args:
            key (str): The key of the hash.
            *fields: Variable number of fields to delete.

        Returns:
            str: The server's response after executing the HDEL command.
        """
        command = [
            f"*{2 + len(fields)}\r\n",
            "$4\r\nHDEL\r\n",
            f"${len(key)}\r\n{key}\r\n"
        ]

        for field in fields:
            command.extend([
                f"${len(str(field))}\r\n{field}\r\n"
            ])

        print(''.join(command))
        return self._send_command(''.join(command))

    def hashes_hincrby(self, key, field, increment):
        """Increments the integer value of the specified field in the hash stored at key by the given increment.

        Args:
            key (str): The key of the hash.
            field (str): The field to increment.
            increment: The amount by which to increment the field.

        Returns:
            str: The server's response after executing the HINCRBY command.
        """
        command = [
            "*4\r\n",
            "$7\r\nHINCRBY\r\n",
            f"${len(key)}\r\n{key}\r\n",
            f"${len(field)}\r\n{field}\r\n",
            f"${len(str(increment))}\r\n{increment}\r\n"
        ]

        print(''.join(command))
        return self._send_command(''.join(command))

# = RedisClient()
#redis_client.close()

