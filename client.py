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

def exchange_numbers():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the host and port to connect
    host = 'localhost'
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    # parameters
    num = 997
    gen = 5

    # Private key for client
    private_key = generateRandom(2, num - 2)

    # public key generation
    number = computeSharedSecret(gen, private_key, num)
    print("public key sent to server:", number)
    client_socket.send(str(number).encode())

    # Receive the result from the server
    data = client_socket.recv(1024)
    result = int(data.decode())
    print("public key received from server is:", result)

    #calculating secret key
    secret_key = computeSharedSecret(result,private_key,num)
    print("Secret key of client is: ",secret_key)

    # Close the connection
    client_socket.close() 

exchange_numbers()
