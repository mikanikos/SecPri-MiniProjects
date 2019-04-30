from hashlib import sha256
from itertools import product

characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

to_crack = [    "019bb283c8c44d8a9b4b2ee4b312d71d1d0b1a82b2aefe7a03442a75193ce561", 
                "ed807b1b8c648887107eff0ccc2e4f2538ad7d679c42d94ae3490776ef68de8e",
                "5ee54ab72ffa9fabca1e1401801332d78fd29f3b9b6430192c95f552df4566e1",
                "49a8ea7869f8fd3bed53d2679e3603bf619e5238d9a670b767714aa2f99976a8",
                "fc06ce1d57520fe7d37ab7f5f5da7328029b534d33cc8160928d03c3925f504e",
                "c5b7af6cefdcf30f0353b521df0efbdb80b0d1da2b2d36da035ea8fd3115274d",
                "e216831e4c87deacf61890a63b036bb624f23e56852716aa1915f9c3978c6827",
                "e9177719568279f314e412bfa2f5aa1ee20a1f0f058e0d419f93e0ed35408993",
                "c6869f9cfc70599e31697e8cb447759106749dba7abcbc3f4ef371fa92929f51",
                "97511929b3ec2c4c36e5f645099a1da6fdf11f57c7f898a45bc4da72084ca220" ]

cracked = []
for length in range(4, 7):
    to_attempt = product(characters, repeat=length)
    for attempt in to_attempt:
        psw = ''.join(attempt)
        hash_psw = sha256(psw.encode()).hexdigest()
        if hash_psw in to_crack:
            print("Password Found: " + psw)
            cracked.append(psw)
            to_crack.remove(hash_psw)
        if to_crack == []:
            break
    if to_crack == []:
        break

with open('cracked_a', 'w') as f:
    for i in cracked:
        f.write("%s\n" % i)
