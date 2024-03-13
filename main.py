import os
import timeit
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from typing import Dict, List
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


FILES_DIR = "./files"
AES_DIR = "./files/AES"
SHA_DIR = "./files/SHA"
RSA_DIR = "./files/RSA"

AES_FILE_SIZE = [8, 64, 512, 4096, 32768, 262144, 2097152]
SHA_FILE_SIZE = [8, 64, 512, 4096, 32768, 262144, 2097152]
RSA_FILE_SIZE = [2, 4, 8, 16, 32, 64, 128]

ALGS = ["AES", "SHA", "RSA"]


def generate_rsa_keys() -> (str, str):
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Generate public key
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_decrypt(alg: str, data: bytes, private_key: str, public_key: str):
    if alg == "aes":
        # I will use the CTR mode
        key = os.urandom(32)  # 256 bits key
        nonce = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        decryptor = cipher.decryptor()

        encrypt_data = encryptor.update(data) + encryptor.finalize()
        _ = decryptor.update(encrypt_data) + decryptor.finalize()
    elif alg == "rsa":

        # RSA encryption
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # RSA decryption
        _ = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    elif alg == "sha":
        _ = hashlib.sha256(data).hexdigest()


def measure_performance(alg: str, file_path: str) -> float:
    with open(file_path, "rb") as f:
        data = f.read()

    private_key, public_key = generate_rsa_keys()
    stmt = lambda: encrypt_decrypt(alg, data, private_key, public_key)
    number_of_executions = 100

    execution_time = timeit.timeit(stmt,
                                   number=number_of_executions)

    return execution_time / number_of_executions


def generate_random_file(file: str, size: int):
    with open(file, "wb") as f:
        # Create a file with the correct size
        f.write(os.urandom(size))


# key - algorithms
# value - list of all file path to that algorithm
def create_files() -> Dict[str, List[str]]:
    all_files_dic: Dict[str, List[str]] = {}

    # Create dir to store the files
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    # Create the random Files
    for alg in ALGS:
        alg_dir = f"{alg}_DIR"
        alg_dir = globals()[alg_dir]
        if not os.path.exists(alg_dir):
            os.makedirs(alg_dir)

        alg_file_sizes = f"{alg}_FILE_SIZE"
        alg_file_sizes = globals()[alg_file_sizes]

        file_names_list: List[str] = []
        for file_size in alg_file_sizes:
            filename = os.path.join(alg_dir, f"{alg.lower()}_{file_size}.bin")
            file_names_list.append(filename)

            generate_random_file(filename, file_size)

        all_files_dic[alg.lower()] = file_names_list

    return all_files_dic


def delete_files():
    for alg in ALGS:
        alg_dir = f"{alg}_DIR"
        alg_dir = globals()[alg_dir]
        alg_file_sizes = f"{alg}_FILE_SIZE"
        alg_file_sizes = globals()[alg_file_sizes]

        # Remove .bin files
        for file_size in alg_file_sizes:
            filename = os.path.join(alg_dir, f"{alg.lower()}_{file_size}.bin")
            os.remove(filename)

        # Removes the dir for each alg
        if os.path.exists(alg_dir):
            os.removedirs(alg_dir)

    # ".files/"
    if os.path.exists(FILES_DIR):
        os.removedirs(FILES_DIR)


def print_performance_results(performance_results_dic: Dict[str, Dict[str, float]]):
    for alg, files_result_perform_dic in performance_results_dic.items():
        print(f"Performance Results for {alg}\n")
        for file_path, time in files_result_perform_dic.items():
            print(f"{file_path}: {time} seconds")
        print("\n")


def main():
    all_files_dic: Dict[str, List[str]] = create_files()

    # key = algorithm name
    # value:  str -> file_path | float -> time result preformance
    performance_results_dic: Dict[str, Dict[str, float]] = {}
    for alg, files_path_list in all_files_dic.items():
        alg_performance_results_dic: Dict[str, float] = {}

        for file_path in files_path_list:
            time = measure_performance(alg, file_path)
            alg_performance_results_dic[file_path] = time

        performance_results_dic[alg] = alg_performance_results_dic

    print_performance_results(performance_results_dic)

    # Delete files created
    delete_files()


main()
