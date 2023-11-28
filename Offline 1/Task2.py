# The secrets module in Python is designed for 
# generating cryptographically secure random numbers.
import secrets
import time
from sympy import nextprime

# if <n is a square modulo p> then < n^(p-1)/2 ≡ 1 (mod p) >
def is_square(n, p):
    return pow(n, (p - 1) // 2, p) == 1

# n ^ ((p – 1) / 2) (mod p), it must be 1 or p-1, 
# if it is p-1, then modular square root is not possible.

# n^(p+1)/4 * n^(p+1)/4 = n^(p+1)/2 = n^(p-1)/2 * n = n (mod p)
# since,  n ^ ((p – 1) / 2) (mod p), it must be 1
def sqrt_mod(n, p):
    return pow(n, (p + 1) // 4, p)
    
    
# generate prime
def gen_prime(bits):
    return nextprime(secrets.randbits(bits))

# generate a and b
def gen_ab(prime):
    a = secrets.randbelow(prime)
    b = secrets.randbelow(prime)
    # ensure nonsingularity
    while (4 * a**3 + 27* b**2) % prime == 0:
        a = secrets.randbelow(prime)
        b = secrets.randbelow(prime)
    
    return a, b

# generate the random point
def gen_G(a, b, prime):
    x = secrets.randbelow(prime)
    y_sq = (x**3 + a*x + b) % prime
    while not is_square(y_sq, prime):
        x = secrets.randbelow(prime)
        y_sq = (x**3 + a*x + b) % prime
    y = sqrt_mod(y_sq, prime)
    return x, y


def gen_parameters(bits):
    p = gen_prime(bits)
    a, b = gen_ab(p)
    G = gen_G(a, b, p)
    
    return p, a, b, G

def point_double(point, a, p):
    x1, y1 = point
    s = ((3 * x1**2 + a ) * pow(2*y1, p-2, p)) % p
    x3 = (s**2 - x1 - x1) % p
    y3 = (s*(x1-x3) - y1 ) % p
    return x3, y3


def point_add(point1, point2, a, p ):
    x1, y1 = point1
    x2, y2 = point2
    
    s = ((y2 - y1) * pow((x2-x1), p-2, p)) % p
    x3 = (s**2 - x1 - x2) % p
    y3 = (s*(x1-x3) - y1 ) % p
    return x3, y3
        
def scaler_multiplication(k, a, prime, point):
    result = point
    k_bin = bin(k)[2:]
    for i in range(1, len(k_bin)):
        result = point_double(result, a, prime)
        if k_bin[i] == '1':
            
            result = point_add(result, point, a, prime)
                   
    return result

def calculate_secret_key(a, G, prime):
    k = secrets.randbelow(prime)
    return k, scaler_multiplication(k, a, prime, G)


if __name__ == '__main__':
    
    bits = [128, 192, 256]
    total_time_A = 0.0
    total_time_B = 0.0
    total_time_R = 0.0
    print(f"K\tA(ms)\t\tB(ms)\t\tR(ms)")
    for bit_size in bits:
        # [prime, a, b, G]
        for _ in range(0,5):           
            params = gen_parameters(bit_size)
            
            st = time.time()
            [ka, A] = calculate_secret_key(params[1], params[3], params[0])
            et = time.time()
            total_time_A += (et - st)
            
            st = time.time()
            [kb, B] = calculate_secret_key(params[1], params[3], params[0])
            et = time.time()
            total_time_B += (et - st)
            
            st = time.time()
            shared_R = scaler_multiplication(ka*kb, params[1], params[0], params[3])
            et = time.time()
            total_time_R += (et - st)
        print(f"{bit_size}\t {round(total_time_A*1000 / 5, 4)}\t {round(total_time_B*1000 / 5, 4)}\t {round(total_time_R*1000 / 5, 4)}")
