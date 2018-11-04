#!/usr/bin/python3

from collections import Counter
import operator
import re
import string

def ic(ctext):
    num = 0.0
    den = 0.0
    for val in Counter(ctext).values():
        i = val
        num += i * (i - 1)
        den += i
    if den == 0.0:
        return 0.0
    else:
        return num / (den * (den - 1))

def partition(text, num):
    cols = [""] * num
    for i, c in enumerate(text):
        cols[i % num] += c
    return cols

def find_keylen_ics(ctext, low=3, high=10, rows=5):
    if high > len(ctext) / 2:
        high = len(ctext) / 2

    results = {}
    for length in range(low, high + 1):
        ics = [ic(col) for col in partition(ctext, length)]
        results[length] = sum(ics) / len(ics)

    best = sorted(results.items(), key=lambda kv: -kv[1])

    print("%8s %8s" % ("keylen", "ic"))
    for k, v in best[:rows]:
        print("%8d %8.3f" % (k, v))

    return best

def freq_score(text):
    freqs = {
        'a': 8167,
        'b': 1492,
        'c': 2782,
        'd': 4253,
        'e': 12702,
        'f': 2228,
        'g': 2015,
        'h': 6094,
        'i': 6966,
        'j': 153,
        'k': 772,
        'l': 4025,
        'm': 2406,
        'n': 6749,
        'o': 7507,
        'p': 1929,
        'q': 95,
        'r': 5987,
        's': 6327,
        't': 9056,
        'u': 2758,
        'v': 978,
        'w': 2360,
        'x': 150,
        'y': 1974,
        'z': 74
    }

    score = 0
    for c in text:
        if c == ' ':
            score += 10000
        elif c.lower() in freqs:
            score += freqs[c.lower()]
        elif ord(c) >= 128:
            score -= 5000
        else:
            score -= 1000

    return score

def find_key(ctext, keylen, alph=string.ascii_lowercase):
    key = ""
    for col in partition(ctext, keylen):
        scores = {}
        for i, letter in enumerate(alph):
            transposed = [alph[(alph.index(c.lower()) - i) %
                               len(alph)] for c in col]
            scores[letter] = freq_score(transposed)
        key += max(scores.items(), key=operator.itemgetter(1))[0]

    return key

def find_key_letter(col, op):
    best_score = 0
    best_char = 0
    for i in range(256):
        decoded = ''.join(chr(op(ord(a), i) % 256) for a in col)
        if freq_score(decoded) > best_score:
            best_score = freq_score(decoded)
            best_char = i

    return best_char

def decrypt(ctext, key, alph=string.ascii_lowercase):
    return ''.join(alph[(alph.index(c.lower()) - alph.index(key[i % len(key)])) % len(alph)] for i, c in enumerate(ctext))

def modvigenere_find_key(ctext, keylen):
    key = []
    for i, col in enumerate(partition(ctext, keylen)):
        if i % 8 == 0: key.append(find_key_letter(col, operator.xor))
        if i % 8 == 1: key.append(find_key_letter(col, operator.sub))
        if i % 8 == 2: key.append(find_key_letter(col, operator.xor))
        if i % 8 == 3: key.append(find_key_letter(col, operator.add))
        if i % 8 == 4: key.append(find_key_letter(col, operator.xor))
        if i % 8 == 5: key.append(find_key_letter(col, operator.xor))
        if i % 8 == 6: key.append(find_key_letter(col, operator.sub))
        if i % 8 == 7: key.append(find_key_letter(col, operator.add))

    return key

def decrypt_or_default(c, op, k, default='.'):
    p = chr(op(c, k) % 256)
    if p in string.printable:
        return p
    else:
        return default

def modvigenere_decrypt(ctext, key):
    plaintext = ""
    for i, c in enumerate(ctext):
        i %= len(key)
        c = ord(c)
        k = key[i]
        if i % 8 == 0: plaintext += decrypt_or_default(c, operator.xor, k)
        if i % 8 == 1: plaintext += decrypt_or_default(c, operator.sub, k)
        if i % 8 == 2: plaintext += decrypt_or_default(c, operator.xor, k)
        if i % 8 == 3: plaintext += decrypt_or_default(c, operator.add, k)
        if i % 8 == 4: plaintext += decrypt_or_default(c, operator.xor, k)
        if i % 8 == 5: plaintext += decrypt_or_default(c, operator.xor, k)
        if i % 8 == 6: plaintext += decrypt_or_default(c, operator.sub, k)
        if i % 8 == 7: plaintext += decrypt_or_default(c, operator.add, k)

    return plaintext

if __name__ == "__main__":
    ciphertext = "VIAYISBEQOWPKMQYRQAYCVEPKMQYRLOGMXRYSXNYMLDSLVIQORRORKSPJOGFYWCC"
    find_keylen_ics(ciphertext)
    key = find_key(ciphertext, 3)
    print(key)
    print(decrypt(ciphertext, key))

    print("")

    with open('modvigenere.cipher') as f:
        ciphertext = [chr(int(a, 16))
                      for a in re.findall('.{2}', f.read().strip())]

    find_keylen_ics(ciphertext, high=30)
    key = modvigenere_find_key(ciphertext, 13)
    print(key)
    print(modvigenere_decrypt(ciphertext, key))
