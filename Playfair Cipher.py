def to_lower_case(text):
    return text.lower()


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


list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm',
         'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


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
        matrix.append(comp_elements[:5])
        comp_elements = comp_elements[5:]
    return matrix


def search(mat, element):
    for i in range(5):
        for j in range(5):
            if mat[i][j] == element:
                return i, j


def encrypt_row_rule(matr, e1r, e1c, e2r, e2c):
    if e1c == 4:
        char1 = matr[e1r][0]
    else:
        char1 = matr[e1r][e1c + 1]
    if e2c == 4:
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


def encrypt_by_playfair_cipher(matrix, plain_list):
    cipher_text = []
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
        cipher_text.append(cipher)
    return cipher_text


text_Plain = 'textbook'
text_Plain = remove_spaces(to_lower_case(text_Plain))
PlainTextList = digraph(filler_letter(text_Plain))
if len(PlainTextList[-1]) != 2:
    PlainTextList[-1] = PlainTextList[-1] + 'z'

key = "scientifix"
print("Key text:", key)
key = to_lower_case(key)
Matrix = generate_key_table(key, list1)

print("Plain Text:", text_Plain)
CipherList = encrypt_by_playfair_cipher(Matrix, PlainTextList)

CipherText = ""
for i in CipherList:
    CipherText += i
print("Cipher Text:", CipherText)
