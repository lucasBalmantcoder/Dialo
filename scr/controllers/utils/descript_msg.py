from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def carregar_chave_privada(pem_privada: str):
    return serialization.load_pem_private_key(
        pem_privada.encode(),
        password=None,
    )

def descriptografar_mensagem(mensagem_criptografada: bytes, chave_privada):
    return chave_privada.decrypt(
        mensagem_criptografada,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode()
