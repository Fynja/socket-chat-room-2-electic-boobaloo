def encode(key, string):
    encoded = ""
    for i in range(len(string)):
        key_ord = ord(key[i % len(key)])
        str_i_ord = ord(string[i])
        coded_ord = key_ord + str_i_ord
        encoded = encoded + str(chr(coded_ord))
    return encoded
def decode(key, string):
    decoded = ""
    for i in range(len(string)):
        key_ord = ord(key[i % len(key)])
        str_i_ord = ord(string[i])
        coded_ord = str_i_ord - key_ord
        decoded = decoded + str(chr(coded_ord))
    return decoded