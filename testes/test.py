# --- IMPORTAÇÕES ---

import os
import sys
import json
import base64
import requests

from cryptography.hazmat.primitives import serialization, hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# --- CONFIGURAÇÕES GERAIS ---

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

BASE_URL = "http://127.0.0.1:5000"

# --- FUNÇÕES DE CRIPTOGRAFIA ---

def encrypt_rsa_public_key(data_bytes, public_key_pem):
    public_key = serialization.load_pem_public_key(public_key_pem.encode(), backend=default_backend())
    encrypted = public_key.encrypt(
        data_bytes,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()

def decrypt_rsa_private_key(encrypted_b64, private_key_pem):
    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None, backend=default_backend())
    decrypted = private_key.decrypt(
        base64.b64decode(encrypted_b64),
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted

def encrypt_aes_cbc(plaintext, key_b64):
    key = base64.b64decode(key_b64)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()

def decrypt_aes_cbc(ciphertext_iv_b64, key_bytes):
    full_data = base64.b64decode(ciphertext_iv_b64)
    iv = full_data[:16]
    ciphertext = full_data[16:]
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode('utf-8')

# --- INTERAÇÃO COM A API ---

def login_user(username, password):
    res = requests.post(f"{BASE_URL}/auth/login", json={"login": username, "password": password})
    res.raise_for_status()
    return res.json()

def get_room_details(room_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/rooms/{room_id}", headers=headers)
    res.raise_for_status()
    return res.json()

def send_encrypted_message(room_id, payload_str, token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    res = requests.post(f"{BASE_URL}/messages", json={"room_id": room_id, "message": payload_str}, headers=headers)
    res.raise_for_status()
    return res.json()

def get_messages(room_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/messages/{room_id}", headers=headers)
    res.raise_for_status()
    return res.json()

# --- EXECUÇÃO DO TESTE ---

def run_e2e_test():
    USERNAME = "lucas"
    PASSWORD = "lucas"
    ROOM_ID = 1
    PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2vNf54DH/Uyhn
VS0xUnK2YVSclN4U2ScBncLeNCeSbX65tym/T1S7TyYwysfnC1PiD4IVCvaj7t3o
eGG2sjachc+0pZrSLnI6et1y6iFY3lkq9VtlPo7URDWG3FPpL2HxxpGD9O/+MvyX
CascFPpO76SgVNaNfcAwIAVo5OqtA/H/yziujor2fX0Y9nMkUrEJCAe0xCuwHdAr
+oJChixP8UAtQoQg2EyqJqVhEE5S94Z2dJT3snv6mQyIEwWKC8UIopczrdpoFBXj
AA2Y9JhUCfBC2vTKbYrgykDQP0jWCm4jR91N+BVLrF/nmPc5I5pOc9BTPre6QL9B
6Uqxqve/AgMBAAECggEAA9K/+rXimz1xqcvMlhdsAqiBp9muKyXUnOzgkAaWUggh
b8rxwCjC6eerhwzPEY9D8jBcioqAA4kIB95GPmzMcLTqAL+66q0sbaXMGU87DbbF
NdK2q/pwQZJVw7G7aF8PP7WQWNWYlIBw7CC4fZjAw0MHS5AgLGCrqItwTDQHPEHA
9Ulf2OMi7oq04ta31PInLwJRd4Si1D5Auw3DH7byOoWhT1ByXYPWVSCCUkew/Vc8
tqvTh7OiR6Ctx2gQ/6jOcRNTbQ6YUeaMKN0amVmfQlZwUXoVcl2x3jKWJ4ABJ8tU
VN1Cr6W586hQjYjhu/OIWTNDg1C4Su0eM4m81gS19QKBgQDrd1AtPhext+ScF3iH
HyqWd1DXtVYSxthn4DTZCRT0VZzEQqI89jW19otMQwTy2P8FcA7NIv9fb7wVEUQz
k97O//0rf5yvYnwThu2ZyHrol30FNrRSIlBapRLFijIYyOol9Ec8gs5C8Ydj60U4
2/93eMGx8s073b/bTacDmMYeNQKBgQDGrGPObqGjITpb2PVBT/75VkgapqJHLHf6
PW2w6iSWhHQxTuZJ+Wa3gXHRBQYcRY7x316OEoedAczdjwu743rEFPMepfeU6fyR
e8sboyCr2rppzY/LThDidfH6Ztmw6deZpJuU5JoyrlwVn4RkP7eDQQ9OOFIw53ku
Q36LOhZMowKBgQDNECy4KhJSiNdEhUBHVQIu5hx2r4sVcSz4Ug9UUI96NrD/TxSh
yL6ACQXJVbiSkh6OqseJKYiDofiH1HC0BnyNg+0FG+7l4vwxuVlli25W789GYhzq
Rs36Ezbk6HS2lwssILCFZ1mgfV4uy6+OVDII5xaxFcZc88Lph5gDDuLDXQKBgBsx
OS/mAIWdZKlxlo/r7RAfeRr8t7VaJsm/YqYWRg+77VNaYza4xhBTzUo4j8+KzbfZ
RM3ZR2p79phUndyHlCQGYghN2wcsx376HKCZwT0EYQNeOVIwSytTzVzieuU1/GZx
G0JTz68kIkJrZOl7txhl7TxdhRJgfDuSzV0tBCRVAoGAXmk+1md5tAQc1sZgjVI6
spZ2RaLkT8fy5N49EL5J/PqFPbw+3wjxm0+/PdbP1Ri5E1U0uUpb2mWdyMTii2rG
wnak588XEAeYAxCDGTweq0W1Dezs8bfVPXDiy0ImKE04uw6KMGuC/j2gbAPOgZ7p
U3x4pqwsRMhAU4w0jymfBYc=
-----END PRIVATE KEY-----"""

    try:
        login_data = login_user(USERNAME, PASSWORD)
        token = login_data["access_token"]
        user_id = login_data["user"]["id"]

        room = get_room_details(ROOM_ID, token)
        room_users = room["users"]
        sender_pub_key = next((u["public_key"] for u in room_users if u["id"] == user_id), None)
        if not sender_pub_key:
            raise ValueError("Chave pública do remetente não encontrada.")

        test_msg = b"Teste RSA de integridade."
        encrypted = encrypt_rsa_public_key(test_msg, sender_pub_key)
        decrypted = decrypt_rsa_private_key(encrypted, PRIVATE_KEY)
        assert decrypted == test_msg, "Falha no teste de criptografia/descriptografia RSA."

        print("\nSUCESSO: Criptografia RSA funcional.")

        msg = "Olá, esta é uma mensagem de teste criptografada do Python!"
        sym_key_b64 = base64.b64encode(os.urandom(32)).decode()
        encrypted_content = encrypt_aes_cbc(msg, sym_key_b64)

        encrypted_keys = []
        for user in room_users:
            if not user["public_key"]:
                continue
            try:
                enc_key = encrypt_rsa_public_key(sym_key_b64.encode(), user["public_key"])
                encrypted_keys.append({"user_id": user["id"], "encrypted_key": enc_key})
            except Exception as e:
                print(f"Aviso: falha ao criptografar chave para {user['username']}: {e}")

        payload = {
            "encrypted_content": encrypted_content,
            "encrypted_symmetric_keys": encrypted_keys,
            "sender_id": user_id
        }

        send_encrypted_message(ROOM_ID, json.dumps(payload), token)

        messages = get_messages(ROOM_ID, token)
        for msg in messages:
            try:
                data = json.loads(msg["mensagem"])
                enc_key = next((k["encrypted_key"] for k in data["encrypted_symmetric_keys"] if k["user_id"] == user_id), None)
                if not enc_key:
                    continue
                dec_sym_key = decrypt_rsa_private_key(enc_key, PRIVATE_KEY)  # retorna bytes puros
                print(f"Chave simétrica descriptografada (bytes): {dec_sym_key} - Tamanho: {len(dec_sym_key)}")
                decrypted_msg = decrypt_aes_cbc(data["encrypted_content"], dec_sym_key)
            except Exception as e:
                print(f"Erro ao descriptografar mensagem {msg['id']}: {e}")

    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP {e.response.status_code}: {e.response.text}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# --- PONTO DE ENTRADA ---

if __name__ == "__main__":
    run_e2e_test()
