import base64
import hashlib
from Crypto.Cipher import AES
import json
import random

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(raw):
    with open('blood_bank/keys.json5', 'r') as file:
        data = json.load(file)
    pwd = data["password"]
    iv_d = data["iv"]
    password = pwd.encode("utf-8")
    private_key = hashlib.sha256(password).digest()
    raw = pad(raw).encode("utf-8")
    iv = pad(iv_d).encode("utf-8")
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw)).hex()


def decrypt(enc):
    with open('blood_bank/keys.json5', 'r') as file:
        data = json.load(file)
    pwd = data["password"]
    iv_d = data["iv"]
    password = pwd.encode("utf-8")
    private_key = hashlib.sha256(password).digest()
    enc = base64.b64decode(bytes.fromhex(enc))
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:])).decode()
ids = []
def generate_random_id(email, lic_no):
    left = email.split('@')[0]
    right = lic_no[4:]
    id = left+right
    if id not in ids:
        ids.append(id)
        return id
    else:
        return regenerate(id)
def regenerate(id):
    r1 = random.randint(0,len(id))
    r2 = r1
    while r2 == r1:
        r2 = random.randint(0, len(id))
    new_id = id
    new_id[r1], new_id[r2] = new_id[r2], new_id[r1]
    if new_id not in ids:
        ids.append(new_id)
        return new_id
    else:
        return regenerate(id)
def generate_random_no():
    return random.randint(1000000,9999999)
