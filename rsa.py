from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keys() -> (str, str):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Generate public key
    public_key = private_key.public_key()
    return private_key, public_key


def rsa_aux(data: bytes,
            encrypt: bool,
            decrypt: bool,
            public_key: str,
            private_key: str) -> bytes:

    if encrypt and decrypt:
        # RSA encryption
        encrypted_data = public_key.encrypt(
                         data,
                         padding.OAEP(
                             mgf=padding.MGF1(algorithm=hashes.SHA256,
                                              label=None)))

        # RSA decryption
        decrypted_data = private_key.decrypt(
             encrypted_data,
             padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                          algorithm=hashes.SHA256(),
                          label=None)
            )

        return decrypted_data
    elif encrypt:
        encrypted_data = public_key.encrypt(
                         data,
                         padding.OAEP(
                             mgf=padding.MGF1(algorithm=hashes.SHA256,
                                              label=None)))

        return encrypted_data
    elif decrypt:
        # Here the data passed as argument needs to be already encrypt
        decrypted_data = private_key.decrypt(
             data,
             padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                          algorithm=hashes.SHA256(),
                          label=None)
            )

        return decrypted_data
    else:
        raise TypeError("No mode was passed for the RSA algorithm")
