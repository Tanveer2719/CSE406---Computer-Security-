from BitVector import *
import time

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

fixed_mixer = [
    [BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03"), BitVector(hexstring="01")],
    [BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02"), BitVector(hexstring="03")],
    [BitVector(hexstring="03"), BitVector(hexstring="01"), BitVector(hexstring="01"), BitVector(hexstring="02")]
]

fixed_invMixer = [
    [BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09")],
    [BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B"), BitVector(hexstring="0D")],
    [BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E"), BitVector(hexstring="0B")],
    [BitVector(hexstring="0B"), BitVector(hexstring="0D"), BitVector(hexstring="09"), BitVector(hexstring="0E")]
]

ROW = 4
COL = 4

IV = ['1a','2b', '3c', '4d', '5e', '6f', '78', '90' , '12', '34','56','78','9a','bc','de','f0']

def pad_string(string, total_width,  x):
    return string.ljust(total_width, x)

def slice_string(string, width):
    return string[:-width]

# pads the string with space and returns a hex array
def modify_input(string):
    dif = 16 - (len(string)%16)
    hex_string = string2hex(string)
    hex_string.extend(['00']*dif) # make the hex array a multiple of 16
    return hex_string
    
def string2hex(string):
    list = []
    for x in string:
        list.append(hex(ord(x))[2:])
    return list

def int2hex(key):
    string = str(bin(key)[2:])
    string = string.ljust(16*8, '0')
    substring_length = 8
    substrings = [string[i:i+substring_length] for i in range(0, len(string), substring_length)]

    hex_key = []
    for sub in substrings:
        val = int(sub, 2)
        hex_key.append(hex(val)[2:])
        
    return hex_key

def row_based_array2matrix(key):
    """convert the list to a 4 x 4 matrix"""
    return_list = []
    for i in range(0, len(key), COL):
        return_list.append(list(key[i:i+ROW]))
    return return_list

def col_based_array2matrix(input):
    col_mat = []
    for _ in range(ROW):
        col_mat.append([0] * COL)
    
    for i, value in enumerate(input):
        col_mat[i % ROW][i // COL] = value
        
    return col_mat

def col_based_matrix2array(input):
    arr = []
    for i in range(0, ROW):
        for j in range(0, COL):
            arr.append(input[j][i])
                    
    return arr

def row_based_matrix2array(key):
    """convert the list to a 4 x 4 matrix"""
    return_list = []
    for i in range(0,ROW):
        return_list.append(key[i])
    return return_list

def circular_left_shift(input, pos):
    return input[pos:] + input[:pos]

def circular_right_shift(input, pos):
    return input[-pos:] + input[:-pos]

def xor_hex_values(hex1, hex2):
    int1 = int(hex1, 16)
    int2 = int(hex2, 16)
    return hex(int1^int2)[2:]

def xor_hex_arrays(arr1, arr2):
    return_list = []
    if len (arr1) == len(arr1):
        for i in range(0, len(arr1)):
            return_list.append(xor_hex_values(arr1[i], arr2[i]))
    return return_list

def xor_matrices(mat1, mat2):
    return_list = []
    for i in range (0, ROW):
        return_list.append(xor_hex_arrays(mat1[i], mat2[i]))
    return return_list
             
def gen_round_constant(old_constant, itr):
    if itr == 1:
        return ['01', '00', '00', '00']
    else:
        if int(old_constant[0], 16) < int('80', 16):
            x = hex(2 * int(old_constant[0], 16))[2:]
        else:
            x = xor_hex_values(hex(2 * int(old_constant[0], 16)), '11B')
        
        return [str(x), '00', '00', '00']
    
def byte_sub(hex_list, encrypt = True):
    return_list = []
    for x in hex_list:
        if encrypt:
            return_list.append(hex(s_box[int(x,16)])[2:])
        else:
            return_list.append(hex(inv_s_box[int(x,16)])[2:])
    return return_list

def sub_matrix(mat, encrypt = True):
    return_list = []
    for x in mat:
       return_list.append(byte_sub(x, encrypt))
    return return_list

def g_function(input, round_constant):
    input = circular_left_shift(input, 1)
    input = byte_sub(input)
    for i in range(0, ROW):
        input[i] = xor_hex_values(input[i], round_constant[i])
    return input

def shift_matrix(matrix, encrypt = True):
    return_list = []
    for i in range(0, ROW):
        if encrypt:
            return_list.append(circular_left_shift(matrix[i], i))
        else:
            return_list.append(circular_right_shift(matrix[i], i))
    return return_list

def mix_columns(state_matrix, encrypt = True):
    modulus = BitVector(bitstring='100011011') # AES modulus
    
    # convert the hex matrix to bitvector matrix
    for i in range(0, ROW):
        for j in range(0, COL):
            state_matrix[i][j] = BitVector(hexstring=state_matrix[i][j])
            
            
    return_matrix = []
    for _ in range(ROW):
        return_matrix.append([BitVector(intVal=0, size=8)] * COL)
    
    mixer = []
    if encrypt:
        mixer = fixed_mixer
    else:
        mixer = fixed_invMixer
            
    for i in range(ROW):
        for j in range(COL):
            for k in range(ROW):
                return_matrix[i][j] ^= mixer[i][k].gf_multiply_modular(state_matrix[k][j], modulus, 8)
    
    # convert hex value from bitvector
    for i in range(0, ROW):
        for j in range(0, COL):
            return_matrix[i][j] = return_matrix[i][j].getHexStringFromBitVector()

    return return_matrix
      
        
class AES:
    
    def decrypt_helper(self, hex_ciphertext):
        cipher_matrix = col_based_array2matrix(hex_ciphertext)
        mat_round10 = col_based_array2matrix(self.key_set[10])
        
        cipher_matrix = xor_matrices(cipher_matrix, mat_round10)
                
        for i in range (1, 10):
            cipher_matrix = shift_matrix(cipher_matrix, False)
            cipher_matrix = sub_matrix(cipher_matrix, False)
            cipher_matrix = xor_matrices(cipher_matrix, col_based_array2matrix(self.key_set[10 - i]))
            cipher_matrix = mix_columns(cipher_matrix, False)
                    
        cipher_matrix = shift_matrix(cipher_matrix, False)
        cipher_matrix = sub_matrix(cipher_matrix, False)
        cipher_matrix = xor_matrices(cipher_matrix, col_based_array2matrix(self.key_set[0]))
        
        return col_based_matrix2array(cipher_matrix)
        
    
    def encrypt_helper(self, hex_plaintext):
        mat_plaintext = col_based_array2matrix(hex_plaintext)
        mat_round0 = col_based_array2matrix(self.key_set[0])
        
        state_matrix = xor_matrices(mat_plaintext, mat_round0)
        
        for i in range(1, 10):
            state_matrix = sub_matrix(state_matrix) # substitute bytes
            state_matrix = shift_matrix(state_matrix)  #shift row
            state_matrix = mix_columns(state_matrix)    # mix columns
            state_matrix = xor_matrices(state_matrix, col_based_array2matrix(self.key_set[i]))  # add round key
        
        # last round - no mix columns
        state_matrix = sub_matrix(state_matrix)
        state_matrix = shift_matrix(state_matrix)
        state_matrix = xor_matrices(state_matrix, col_based_array2matrix(self.key_set[10]))
        
        return col_based_matrix2array(state_matrix)
            
    def key_expansion(self, hex_matrix):
        return_list = [hex_matrix]
        round_constant = self.round_constant
        for i in range (1, 11):
            round_constant = gen_round_constant(round_constant, i)
            temp_list = []
            temp_list.append(xor_hex_arrays(return_list[i-1][0], g_function(return_list[i-1][3], round_constant)))
            temp_list.append(xor_hex_arrays(return_list[i-1][1], temp_list[0]))
            temp_list.append(xor_hex_arrays(return_list[i-1][2], temp_list[1]))
            temp_list.append(xor_hex_arrays(return_list[i-1][3], temp_list[2]))
            return_list.append(temp_list)
        return return_list 
     
    """
        returns the encrypted hexadecimal array and the encryypted string
        [0] - hex array
        [1] - enc string
    """
    def encrypt(self, plaintext, socket = False):
        originalText = plaintext
        hex_plaintext = modify_input(plaintext) # add '00' at the end for making a multiple of 16
        
        # make slices of 16 hex values
        sliced_arrays = [hex_plaintext[i:i + 16] for i in range(0, len(hex_plaintext), 16)]
        
        ########## print ###########
        if not socket: 
            print('Plain text: ')
            print('In ASCII: ' + originalText)
            print('In HEX: ', ' '.join(str(value) for value in hex_plaintext))
            print('')
        
        
        #### CBC implementation ##########
        hex_encrypted = []
        initializtion_vector = IV
        for slice in sliced_arrays:
            input = xor_hex_arrays(slice, initializtion_vector)
            initializtion_vector = self.encrypt_helper(input)
            hex_encrypted += initializtion_vector
        
        encrypted_string = ''
        for val in hex_encrypted:
            encrypted_string += chr(int(val, 16))
            
        return [hex_encrypted, encrypted_string]
    
    """
        returns the encrypted hexadecimal array and the encryypted string
        [0] - hex array
        [1] - enc string
    """
    def decrypt(self, ciphertext):
        hex_ciphered = string2hex(ciphertext)
        sliced_arrays = [hex_ciphered[i:i + 16] for i in range(0, len(hex_ciphered), 16)]
        
        ###### CBC implementation #########
        hex_decrypted = []
        initializtion_vector = IV
        for slice in sliced_arrays:
            temp_decrypted = self.decrypt_helper(slice)
            hex_decrypted += xor_hex_arrays(temp_decrypted, initializtion_vector)
            initializtion_vector = slice
        
        decrypted_string = ''
        
        for val in hex_decrypted:
            decrypted_string += chr(int(val, 16))
            
        return [hex_decrypted, decrypted_string]
            
    def __init__(self, key, socket = False):
        self.round_constant = ['01', '00', '00', '00']
        
        hex_key = []
        if not socket:
            # the key should be 16 bytes always
            if len(key) > 16:
                self.key = slice_string(key, len(key) - 16)
            elif len(key) < 16:
                self.key = pad_string(key, 16 , "0")
            else:
                self.key = key
                
            hex_key = string2hex(key)
            
            ########### print ###########
            print('Key: ')
            print('In ASCII: ' + key)
            print('In HEX: ', ' '.join(str(value) for value in hex_key))
            print('')
        else:
            hex_key = key
        
        key_matrix = row_based_array2matrix(hex_key)
        
        # for calculation of key_expansion duration
        self.key_exp_st = time.time() 
        round_keys  = self.key_expansion(key_matrix)
        self.key_exp_et = time.time()
        
        self.key_set = []
        for x in round_keys:
            temp_list = []
            for y in x:
               temp_list =  temp_list + y
            self.key_set.append(temp_list)
            
  
        
if __name__ == '__main__':
    # aes = AES('Thats my Kung Fu')
    # plaintext = 'Two One Nine Two'
    
    key = input()
    aes = AES(key)
    
    plaintext = input()
    
    
    enc_st = time.time()
    [enc_hex,ciphertext] = aes.encrypt(plaintext)
    enc_et = time.time()
    
    print('Ciphered Text: ')
    print('In HEX: ', ' '.join(str(value) for value in enc_hex))
    print('In ASCII: ' + ciphertext + '\n')
    
    
    
    dec_st = time.time()
    [dec_hex,plaintext] = aes.decrypt(ciphertext)
    dec_et = time.time()
    
    print('Deciphered Text: ')
    print('In HEX: ', ' '.join(str(value) for value in dec_hex))
    print('In ASCII: ' + plaintext + '\n')
    
    
    print("Execution Time Details: ")
    print("Key Schedule time: " + str((aes.key_exp_et - aes.key_exp_st) * 1000) + ' ms' )
    print('Encryption time: ' + str((enc_et - enc_st) * 1000) + ' ms')
    print('Decryption Time: ' + str((dec_et - dec_st)*1000) + ' ms')
    

    
