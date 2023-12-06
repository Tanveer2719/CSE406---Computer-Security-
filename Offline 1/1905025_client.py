import socket
import pickle
import importlib


Task2 = importlib.import_module('1905025_Task2')
Task1 = importlib.import_module('1905025_Task1')

message = input()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.connect(('localhost', 8080))

print('client connected to server')

# the bit size 128
params = list(Task2.gen_parameters(128))
[ka, A] = Task2.calculate_secret_key(params[1], params[3], params[0])
params.append(A) #[prime, a, b, G, A]

serialized_params = pickle.dumps(params)
client.sendall(serialized_params)
print('params sent to server')

########### receive Kb*G(mod p) ##########
serialized_B = client.recv(2048)
B = pickle.loads(serialized_B)

# B = client.recv(1024)

print(f'B recieved from server')

#k, a, prime, point
secret_R = Task2.scaler_multiplication(ka, params[1], params[0], B)

client.sendall(bytes('ready', 'utf-8'))
print('ready sent from client')

##### receive confirmation #########
msg = client.recv(1024)
msg = msg.decode('utf-8')
if msg == 'ready':
    aes = Task1.AES(Task1.int2hex(secret_R[0]), True)
    cipherText = aes.encrypt(message, True)[1]
    client.sendall(bytes(str(cipherText), 'utf-8'))
    print(f'cipherText sent to server')
else:
    print('Server is not ready')
    client.close()
    


    





