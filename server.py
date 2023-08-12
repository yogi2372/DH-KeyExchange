import socket
import random

def generateRandom(min_value, max_value):
    return random.randint(min_value, max_value)

# modular exponentiation
def modExp(base, exponent, modulus):
    if modulus == 1:
        return 0

    result = 1
    base = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

def computeSharedSecret(base, private_key, modulus):
    return modExp(base, private_key, modulus)


def exchange_numbers(conn):
    # Receive public key from client
    data = conn.recv(1024)
    number = int(data.decode())
    print("public key received from client is:", number)
    # parameters
    num = 997
    gen = 5

    # Private key for server
    private_key = generateRandom(2, num - 2)
    
    # computing public key
    result = computeSharedSecret(gen, private_key, num)
    #print("public key of server:", result)

    # Send the result back to the client
    conn.send(str(result).encode())
    
    #calculating secret key
    secret_key = computeSharedSecret(number,private_key,num)
    print("Secret key of server is: ",secret_key)

    # Close the connection
    conn.close()

def run_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and port
    host = 'localhost'
    port = 12345

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print("Server listening on {}:{}".format(host, port))

    while True:
        # Accept a connection from a client
        conn, addr = server_socket.accept()
        print("Connected to client:", addr)

        # Exchange numbers with the client
        exchange_numbers(conn)

run_server()
