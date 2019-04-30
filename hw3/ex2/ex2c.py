from hashlib import sha256
from itertools import product
import os


characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

to_crack = [
    ("d0", "19c6eea5583e8e21cbb1e64c44569706efecc7a5658cf950eb17a862eb889276"),
    ("52", "828fb27be9202a29331b0f6cd3dea44e68136e533e49a1996e3ce99f88ef535f"),
    ("10", "3fd22fb527a0ce7111eadd7b5d4faa894b12d6da537b3aad4968e3f26757e2ec"),
    ("b2", "2dfc9c4e1183904822f245086f623a7eea809dda7f29c1e1f5bfa99e5354c40e"),
    ("36", "081594c6b1b430040967a0af0e81ad95e6a05cc0ec3833c4fe85993ff5c89174"),
    ("fd", "3cdf12026432df71c4ec5c2c1b524f1b6a898973f606551d80507aece9c88f5f"),
    ("3c", "a4e6fa7f5cf873e9f980456a789d69114e4fc3aa291cc68b6d5358579fda19f2"),
    ("64", "79c577a7dfb6653450f856128fa99103558488be3d7d7e7437fffab903b1dfe5"),
    ("45", "cd2198c5a5411b35fc1877f7bac082f732e5af3a7f75c702ea6e08f08510a9fa"),
    ("22", "06542c70370786159697786285aec4ffb9fc0367dc252de835c9de1dfd399cfa") ]


salts = [x[0] for x in to_crack]

cracked = []
for filename in os.listdir("data/"):
    dictionary = (list(line.strip() for line in open("data/" + filename, errors="ignore")))

    for s, enc_psw in to_crack:
        for word in dictionary:
            tot = word + s
            hash_psw = sha256(tot.encode()).hexdigest()
            if hash_psw == enc_psw:
                print("Password Found: " + word)
                cracked.append(word)
                break


with open('cracked_c', 'w') as f:
    for i in cracked:
        f.write("%s\n" % i)
