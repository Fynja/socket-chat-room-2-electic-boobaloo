def encode(key, string):
    encoded = ""
    try:
        for i in range(len(string)):
            key_ord = ord(key[i % len(key)])
            str_i_ord = ord(string[i])
            coded_ord = key_ord + str_i_ord
            encoded = encoded + str(chr(coded_ord))
    except:
        encoded = "ERROR_COULD_NOT_BE_ENCODED"
    return encoded

def decode(key, string):
    decoded = ""
    try:
        for i in range(len(string)):
            key_ord = ord(key[i % len(key)])
            str_i_ord = ord(string[i])
            coded_ord = str_i_ord - key_ord
            decoded = decoded + str(chr(coded_ord))
    except:
        decoded = "ERROR_COULD_NOT_BE_DECODED"
    return decoded