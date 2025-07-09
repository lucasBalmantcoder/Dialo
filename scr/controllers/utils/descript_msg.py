from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives import serialization

def carregar_chave_privada(pem_privada: str):
    return serialization.load_pem_private_key(
        pem_privada.encode(),
        password=None,
    )

def descriptografar_mensagem(mensagem_criptografada: bytes, chave_privada):
    return chave_privada.decrypt(
        mensagem_criptografada,
        rsa_padding.PKCS1v15()
    ).decode()
