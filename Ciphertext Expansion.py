#Implementation of modified Playfair cipher from:
#M. Anshari, A. Mujahidah et al., “Expending technique cryptography for
#plaintext messages by modifying playfair cipher algorithm with matrix
#5 x 19,” in 2019 International Conference on Electrical Engineering
#and Computer Science (ICECOS). IEEE, 2019, pp. 10–13.

def remove_spaces(text):
    new_text = ""
    for c in text:
        if c == " ":
            continue
        else:
            new_text = new_text + c
    return new_text


def digraph(text):
    digraph = []
    group = 0
    for i in range(2, len(text), 2):
        digraph.append(text[group:i])

        group = i
    digraph.append(text[group:])
    return digraph


def filler_letter(text):
    k = len(text)
    new_word = ''
    if k % 2 == 0:
        for i in range(0, k, 2):
            if text[i] == text[i + 1]:
                new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = filler_letter(new_word)
                break
            else:
                new_word = text
    else:
        for i in range(0, k - 1, 2):
            if text[i] == text[i + 1]:
                new_word = text[0:i + 1] + str('x') + text[i + 1:]
                new_word = filler_letter(new_word)
                break
            else:
                new_word = text
    return new_word


list = '''ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+[{]}\\|;:'",<.>/?`~ '''


def generate_key_table(word, list1):
    key_letters = []
    for i in word:
        if i not in key_letters:
            key_letters.append(i)
    comp_elements = []
    for i in key_letters:
        if i not in comp_elements:
            comp_elements.append(i)
    for i in list1:
        if i not in comp_elements:
            comp_elements.append(i)
    matrix = []
    while comp_elements:
        matrix.append(comp_elements[:19])
        comp_elements = comp_elements[19:]
    return matrix


def search(mat, element):
    for i in range(5):
        for j in range(19):
            if mat[i][j] == element:
                return i, j


def encrypt_row_rule(matr, e1r, e1c, e2r, e2c):
    if e1c == 18:
        bigram1 = matr[e1r][0] + matr[e1r][1]
    elif e1c == 17:
        bigram1 = matr[e1r][e1c + 1] + matr[e1r][0]
    else:
        bigram1 = matr[e1r][e1c + 1] + matr[e1r][e1c + 2]
    if e2c == 18:
        bigram2 = matr[e2r][0] + matr[e2r][1]
    elif e2c == 17:
        bigram2 = matr[e2r][e2c + 1] + matr[e2r][0]
    else:
        bigram2 = matr[e2r][e2c + 1] + matr[e2r][e2c + 2]
    return bigram1, bigram2


def encrypt_column_rule(matr, e1r, e1c, e2r, e2c):
    if e1r == 4:
        bigram1 = matr[0][e1c] + matr[1][e1c]
    elif e1r == 3:
        bigram1 = matr[e1r + 1][e1c] + matr[0][e1c]
    else:
        bigram1 = matr[e1r + 1][e1c] + matr[e1r + 2][e1c]
    if e2r == 4:
        bigram2 = matr[0][e2c] + matr[1][e2c]
    elif e2r == 3:
        bigram2 = matr[e2r + 1][e2c] + matr[0][e2c]
    else:
        bigram2 = matr[e2r + 1][e2c] + matr[e2r + 2][e2c]
    return bigram1, bigram2


def encrypt_rectangle_rule(matr, e1r, e1c, e2r, e2c):
    if e1r == 4:
        bigram1 = matr[e1r][e2c] + matr[0][e2c]
    else:
        bigram1 = matr[e1r][e2c] + matr[e1r + 1][e2c]
    if e2r == 0:
        bigram2 = matr[e2r][e1c] + matr[4][e1c]
    else:
        bigram2 = matr[e2r][e1c] + matr[e2r - 1][e1c]
    return bigram1, bigram2


def encrypt_by_playfair_cipher(matrix, plain_list):
    cipher_text = plain_list
    for i in range(0, len(plain_list)):
        ele1_x, ele1_y = search(matrix, plain_list[i][0])
        ele2_x, ele2_y = search(matrix, plain_list[i][1])
        if ele1_x == ele2_x:
            c1, c2 = encrypt_row_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        elif ele1_y == ele2_y:
            c1, c2 = encrypt_column_rule(matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        else:
            c1, c2 = encrypt_rectangle_rule(
                matrix, ele1_x, ele1_y, ele2_x, ele2_y)
        cipher = c1 + c2
        cipher_text[i] = cipher
    return cipher_text


text_Plain = '''SUNAN KALIJAGA'''
PlainTextList = digraph(filler_letter(text_Plain))
if len(PlainTextList[-1]) != 2:
    PlainTextList[-1] = PlainTextList[-1] + 'z'

key = "TEKNIK INFORMATIKACLBDGPQHSJ"
print("Key text:", key)
key = remove_spaces(key)
Matrix = generate_key_table(key, list)

print("Plain Text:", text_Plain)
CipherList = encrypt_by_playfair_cipher(Matrix, PlainTextList)

CipherText = ""
for i in CipherList:
    CipherText += i
print("Cipher Text:", CipherText)
