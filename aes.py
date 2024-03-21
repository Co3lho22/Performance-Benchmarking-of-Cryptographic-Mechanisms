from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def aes_aux(data: bytes,
            encrypt: bool,
            decrypt: bool,
            key: bytes,
            nonce: bytes) -> bytes:

    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    # encryption + decryption
    if encrypt and decrypt:
        # key = os.urandom(32)  # 256 bits key
        # nonce = os.urandom(16)
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()

        encrypt_data = encryptor.update(data) + encryptor.finalize()
        decrypt_data = decryptor.update(encrypt_data) + decryptor.finalize()
        return decrypt_data

    # encryption
    elif encrypt:
        encryptor = cipher.encryptor()

        # Here the data passed as argument needs to be already encrypt
        encrypt_data = encryptor.update(data) + encryptor.finalize()
        return encrypt_data

    # decryption
    elif decrypt:
        decryptor = cipher.decryptor()

        decrypt_data = decryptor.update(data) + decryptor.finalize()
        return decrypt_data

    else:
        raise TypeError("No mode was passed for the AES algorithm")
