import os

from dotenv import load_dotenv
from typing import Dict, List
from utils import delete_files, create_files, print_performance_results, measure_performance

load_dotenv()

FILES_DIR = os.getenv('FILES_DIR')
AES_DIR = os.getenv('AES_DIR')
SHA_DIR = os.getenv('SHA_DIR')
RSA_DIR = os.getenv('RSA_DIR')

AES_FILE_SIZE = [int(size) for size in os.getenv('AES_FILE_SIZE').split(",")]
SHA_FILE_SIZE = [int(size) for size in os.getenv('SHA_FILE_SIZE').split(",")]
RSA_FILE_SIZE = [int(size) for size in os.getenv('RSA_FILE_SIZE').split(",")]

ALGS = os.getenv('ALGS').split(",")


# Preate data for the creation and removal of the files
def main_aux() -> (Dict[str, str], Dict[str, [int]]):
    algs_dir_dict: Dict[str, str] = {}
    algs_file_sizes_dict: Dict[str, [int]] = {}
    for alg in ALGS:
        alg_dir = f"{alg}_DIR"
        alg_dir = globals()[alg_dir]
        alg_file_sizes = f"{alg}_FILE_SIZE"
        alg_file_sizes = globals()[alg_file_sizes]

        algs_dir_dict[alg] = alg_dir
        algs_file_sizes_dict[alg] = alg_file_sizes

    return (algs_dir_dict, algs_file_sizes_dict)


def main():
    algs_dir_dict, algs_file_sizes_dict = main_aux()
    all_files_dic: Dict[str, List[str]] = create_files(ALGS,
                                                       FILES_DIR,
                                                       algs_dir_dict,
                                                       algs_file_sizes_dict)

    # AES
    aes_alg: str = ALGS[0].lower()
    print(f"{aes_alg} encryp+decrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[aes_alg]:
        time: float = measure_performance(aes_alg, file_path, True, True)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    print(f"{aes_alg} encrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[aes_alg]:
        time: float = measure_performance(aes_alg, file_path, True, False)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    print(f"{aes_alg} decrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[aes_alg]:
        time: float = measure_performance(aes_alg, file_path, False, True)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    # RSA
    rsa_alg: str = ALGS[1].lower()
    print(f"{rsa_alg} encryp+decrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[rsa_alg]:
        time: float = measure_performance(rsa_alg, file_path, True, True)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    print(f"{rsa_alg} encrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[rsa_alg]:
        time: float = measure_performance(rsa_alg, file_path, True, False)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    print(f"{rsa_alg} decrypt:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[rsa_alg]:
        time: float = measure_performance(rsa_alg, file_path, False, True)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    # SHA
    sha_alg: str = ALGS[2].lower()
    print(f"{sha_alg} hashing:")
    performance_results_dic: Dict[str, float] = {}
    for file_path in all_files_dic[sha_alg]:
        time: float = measure_performance(sha_alg, file_path)
        performance_results_dic[file_path] = time

    print_performance_results(performance_results_dic)

    # Delete files created
    delete_files(ALGS, FILES_DIR, algs_dir_dict, algs_file_sizes_dict)


main()
