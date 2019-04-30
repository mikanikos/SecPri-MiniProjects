from hashlib import sha256
from itertools import product
import os

to_crack = ["fe58be757c13306ddb0ae4b20e507a56b85cfd07cfe0451736c5e94f3ba1fdf0",
            "0da7602de41ba1814150f9aa9ffbbbc52c6acae4ac20fcc32ee9916ee26595b1",
            "2bd62cd949aa12f24dc1a2da1a019e3cfd58826697b4ede9a1c441e6a7a0872a",
            "e2ce040bc487499f593c3bafea22c0e8883fbe4d49e8ebfd26f985910ab3bcb7",
            "21b4c40e12a2e08c1d8f1e358a4acda93c5d170bf972e1192d3d5d637b057ddc",
            "221e16092c7c3d40b7b319365e65e1762f3e5e822894a4f3793ffa9acf90b42d",
            "0bb1f949af6aff3cbfed8310168685d22808722d1fb972023af7f550331c0fe3",
            "e999c8889409a2cbe7156bea63f122a115e0f80a9fcfee37c6adf408676e9313",
            "d7ac0c6339dd2bb5aea6c02d37c97b2a914fc13a1fde4ed88d75e790bd157469",
            "dcc5f8f4009f4957a151cd735c87800e7f0fd2fefbe872da986691acb168fc6b"]


options = {
    'e': ['e', '3'],
    'o': ['o', '0', ],
    'i': ["i", "1"]}


def filler(word):
    combos = [(c,) if c not in options else options[c] for c in word]
    return (''.join(o) for o in product(*combos))


cracked = []
for filename in os.listdir("data/"):
    dictionary = (list(line.strip() for line in open("data/" + filename, errors="ignore")))

    dictionary = filter(lambda x: str.isalnum(x) and len(x) <= 20, dictionary)
    
    for word in dictionary:
        psw_list = list(filler(word)) + list(filler(word.title()))
        for psw in psw_list:
            hash_psw = sha256(psw.encode()).hexdigest()
            if hash_psw in to_crack:
                print("Password Found: " + psw)
                cracked.append(psw)
                to_crack.remove(hash_psw)
            if to_crack == []:
                break
        if to_crack == []:
            break


with open('cracked_b', 'w') as f:
    for i in cracked:
        f.write("%s\n" % i)
