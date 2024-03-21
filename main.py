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
    delete_files(ALGS, FILES_DIR, algs_dir_dict, algs_file_sizes_dict)


main()
