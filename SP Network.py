import numpy as np
import random


def digraph(text):
    digraph = []
    group = 0
    for i in range(2, len(text), 2):
        digraph.append(text[group:i])
        group = i
    digraph.append(text[group:])
    return digraph


list = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[{]}\\|;:'",<.>/?`~ '''


def generate_key_table(word, list):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)
    comp_elements = []
    for i in list:
        if i not in key_letters:
            comp_elements.append(i)
    matrix = []
    interval = 95 // len(key_letters)
    for i in range(2 * len(key_letters) + 1):
        if i % 2 != 0 and key_letters:
            matrix.extend(key_letters[:1])
            key_letters = key_letters[1:]
        else:
            matrix.extend(comp_elements[:interval - 1])
            comp_elements = comp_elements[interval - 1:]
    matrix = np.array(matrix)
    matrix = matrix.reshape(5, 19)
    return matrix


def scramble_key_table(word, length, matrix):
    seed = 0
    for i in range(len(word)):
        seed += ord(word[i]) * (i+1)
    seed*=length
    random.seed(seed)
    x0 = random.uniform(0.1, 0.9)
    u = random.uniform(0.1, 3.9)
    k = [x0, ]
    for i in range(1, matrix.size):
        if k[i - 1] < 0.5:
            next = u * k[i - 1] * (1 - k[i - 1]) + ((4 - u) * k[i - 1]) / 2
        else:
            next = u * k[i - 1] * (1 - k[i - 1]) + ((4 - u) * (1 - k[i - 1])) / 2
        k.append(next)
    x = k[:]
    k.sort()
    for i in range(matrix.size):
        x[i] = k.index(x[i])
    temp = matrix.flatten()
    m_scrambled = []
    for i in range(matrix.size):
        m_scrambled.append(temp[x[i]])
    m_scrambled = np.array(m_scrambled)
    m_scrambled = m_scrambled.reshape(5, 19)
    return m_scrambled


def generate_sequence(key, length):
    seed=0
    for i in range(len(key)):
        seed += ord(key[i]) * (i+1)
    seed*=length
    random.seed(seed)
    ratio = random.uniform(0.3, 0.7)
    sequence=[0]* round(ratio*length) + [1] * round((1-ratio)*length)
    random.shuffle(sequence)
    return sequence


def search(mat, element):
    for i in range(5):
        for j in range(19):
            if mat[i][j] == element:
                return i, j

def encrypt_twin_rule(matr, r, c):
    char = matr[4-r][18-c]
    return char, char


def encrypt_row_rule(matr, e1r, e1c, e2r, e2c):
    if e1c == 18:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c + 1]
    if e2c == 18:
        char2 = matr[e2r][0]
    else:
        char2 = matr[e2r][e2c + 1]
    return char1, char2


def encrypt_column_rule(matr, e1r, e1c, e2r, e2c):
    if e1r == 4:
        char1 = matr[0][e1c]
    else:
        char1 = matr[e1r + 1][e1c]
    if e2r == 4:
        char2 = matr[0][e2c]
    else:
        char2 = matr[e2r + 1][e2c]
    return char1, char2


def encrypt_rectangle_rule(matr, e1r, e1c, e2r, e2c):
    char1 = matr[e1r][e2c]
    char2 = matr[e2r][e1c]
    return char1, char2


def scramble_text(key, text):
    seed = 0
    sum=0
    for i in range(len(key)):
        seed += ord(key[i]) * (i+1)
    for i in range(len(text)):
        sum += ord(text[i])
    seed*=sum
    random.seed(seed)
    x0 = random.uniform(0.1, 0.9)
    u = random.uniform(0.1, 3.9)
    k = [x0, ]
    for i in range(1, len(text)):
        if k[i - 1] < 0.5:
            next = u * k[i - 1] * (1 - k[i - 1]) + ((4 - u) * k[i - 1]) / 2
        else:
            next = u * k[i - 1] * (1 - k[i - 1]) + ((4 - u) * (1 - k[i - 1])) / 2
        k.append(next)
    x = k[:]
    k.sort()
    for i in range(len(text)):
        x[i] = k.index(x[i])
    cipher_scrambled = ''''''
    for i in range(len(text)):
        cipher_scrambled += text[x[i]]
    return cipher_scrambled


def encrypt_by_playfair_cipher(key, plaintext):
    plain_list = digraph(plaintext)
    if len(plain_list[-1]) != 2:
        plain_list[-1] = plain_list[-1] + '|'
    matrix1 = generate_key_table(key, list)
    matrix2 = scramble_key_table(key, len(plain_list), matrix1)
    sequence = generate_sequence(key, len(plain_list))
    cipher_text = plain_list

    for i in range(0, len(plain_list)):
        if sequence[i]== 0:
            matrix=matrix1
        else:
            matrix=matrix2
        ele1_x, ele1_y = search(matrix, plain_list[i][0])
        ele2_x, ele2_y = search(matrix, plain_list[i][1])
        if ele1_x == ele2_x and ele1_y == ele2_y:
            c1, c2 =encrypt_twin_rule(matrix, ele1_x, ele1_y)
        elif ele1_x == ele2_x:
            c1, c2 = encrypt_row_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_column_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_rectangle_rule(
                matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        cipher = c1 + c2
        cipher_text[i] = cipher

    text = ''''''
    for d in cipher_text:
        text += d
    text = scramble_text(key, text)
    cipher_list = digraph(text)

    cipher_text = cipher_list
    for i in range(0, len(cipher_list)):
        if sequence[i] == 0:
            matrix=matrix2
        else:
            matrix=matrix1
        ele1_x, ele1_y = search(matrix, cipher_list[i][0])
        ele2_x, ele2_y = search(matrix, cipher_list[i][1])
        if ele1_x == ele2_x and ele1_y == ele2_y:
            c1, c2 = encrypt_twin_rule(matrix, ele1_x, ele1_y)
        elif ele1_x == ele2_x:
            c1, c2 = encrypt_row_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_column_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_rectangle_rule(
                matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        cipher = c1 + c2
        cipher_text[i] = cipher

    text = ''''''
    for d in cipher_text:
        text += d
    text = scramble_text(key, text)
    return text


key = "scientifi"
print("Key text:", key)

plaintext = '''textboox'''
print("Plain Text:", plaintext)
CipherList = encrypt_by_playfair_cipher(key, plaintext)

CipherText = ""
for i in CipherList:
    CipherText += i
print("Cipher Text:", CipherText)
