import os
import hashlib
import timeit
from typing import Dict, List
from aes import aes_aux
from rsa import generate_rsa_keys, rsa_aux


def measure_performance(alg: str,
                        file_path: str,
                        encrypt=False,
                        decrypt=False) -> float:
    with open(file_path, "rb") as f:
        data = f.read()

    match alg:
        case "aes":
            key = os.urandom(32)  # 256 bits key
            nonce = os.urandom(16)
            if decrypt and not encrypt:  # If only for decryption
                encrypt_data: bytes = aes_aux(data, True, False, key, nonce)
                stmt = lambda: aes_aux(encrypt_data,
                                       encrypt,
                                       decrypt,
                                       key,
                                       nonce)
            else:
                stmt = lambda: aes_aux(data, encrypt, decrypt, key, nonce)
        case "rsa":
            private_key, public_key = generate_rsa_keys()
            if decrypt and not encrypt:  # If only for decryption
                encrypt_data: bytes = rsa_aux(data,
                                              True,
                                              False,
                                              public_key,
                                              private_key)
                stmt = lambda: rsa_aux(encrypt_data,
                                       encrypt,
                                       decrypt,
                                       public_key,
                                       private_key)
            else:
                stmt = lambda: rsa_aux(data,
                                       encrypt,
                                       decrypt,
                                       public_key,
                                       private_key)
        case "sha":
            stmt = lambda: hashlib.sha256(data).hexdigest()

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
def create_files(algs: List[str],
                 files_dir: str,
                 algs_dir_dict: Dict[str, str],
                 algs_file_sizes_dict: Dict[str, [int]]) -> Dict[str, List[str]]:
    all_files_dic: Dict[str, List[str]] = {}

    # Create dir to store the files
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    # Create the random Files
    for alg in algs:
        alg_dir = algs_dir_dict[alg]
        if not os.path.exists(alg_dir):
            os.makedirs(alg_dir)

        alg_file_sizes = algs_file_sizes_dict[alg]

        file_names_list: List[str] = []
        for file_size in alg_file_sizes:
            filename = os.path.join(alg_dir, f"{alg.lower()}_{file_size}.bin")
            file_names_list.append(filename)

            generate_random_file(filename, file_size)

        all_files_dic[alg.lower()] = file_names_list

    return all_files_dic


# algs_dir: key-> alg (e.g. AES); str -> agl dir (e.g. ./files/AES)
# algs_file_sizes_dict: key-> alg (e.g. AES); [int] -> alg file size (8,64,512,4096,32768,262144,2097152)
def delete_files(algs: List[str],
                 files_dir: str,
                 algs_dir_dict: Dict[str, str],
                 algs_file_sizes_dict: Dict[str, [int]]):
    for alg in algs:
        alg_dir: str = algs_dir_dict[alg]
        alg_file_sizes: List[int] = algs_file_sizes_dict[alg]

        # Remove .bin files
        for file_size in alg_file_sizes:
            filename = os.path.join(alg_dir, f"{alg.lower()}_{file_size}.bin")
            os.remove(filename)

        # Removes the dir for each alg
        if os.path.exists(alg_dir):
            os.removedirs(alg_dir)

    # ".files/"
    if os.path.exists(files_dir):
        os.removedirs(files_dir)


def print_performance_results(performance_results_dic: Dict[str, float]):
    for file_path, time in performance_results_dic.items():
        print(f"{file_path}: {time} seconds")

    print("\n")
