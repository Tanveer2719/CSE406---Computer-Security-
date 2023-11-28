import socket
import pickle

import Task1
import Task2



# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket options to reuse the address
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ip address, port
server.bind(('localhost', 8080))

print('server started at 8080')

# can connect at most 1 client
server.listen(1)

  
# socket address of the client and the address of the client
con, addr = server.accept()
print(f'client with ip {addr} connected')

serialized_params = con.recv(1024) #[prime, a, b, G, A]
params = pickle.loads(serialized_params)

print(f"params received from client")

[kb, B] = Task2.calculate_secret_key(params[1], params[3], params[0])
secret_R = Task2.scaler_multiplication(kb, params[1], params[0], params[4])


########### send Kb*G(mod p) ############
serialized_B = pickle.dumps(B)
con.sendall(serialized_B)
print('B sent from server')

msg = con.recv(1024)
msg = msg.decode( 'utf-8')
if msg == 'ready':
    con.sendall(bytes('ready',  'utf-8'))
    aes = Task1.AES(Task1.int2hex(secret_R[0]), True)
    ciphertext = (con.recv(1024))
    ciphertext = ciphertext.decode( 'utf-8')
    message = aes.decrypt(ciphertext)[1]
    print(f"The message received : {message}")
else:
    print('Client is not ready')

con.close()
server.close()

  

