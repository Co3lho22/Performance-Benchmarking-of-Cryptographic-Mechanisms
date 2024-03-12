import os

FILES_DIR = "./files"
AES_DIR = "./files/AES"
SHA_DIR = "./files/SHA"
RSA_DIR = "./files/RSA"

AES_FILE_SIZE = [8, 64, 512, 4096, 32768, 262144, 2097152]
SHA_FILE_SIZE = [8, 64, 512, 4096, 32768, 262144, 2097152]
RSA_FILE_SIZE = [2, 4, 8, 16, 32, 64, 128]

ALGS = ["AES", "SHA", "RSA"]


def generate_random_file(file: str, size: int):
    with open(file, "wb") as f:
        # Create a file with the correct size
        f.write(os.urandom(size))


def main():
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

        for file_size in alg_file_sizes:
            filename = os.path.join(alg_dir, f"{alg.lower()}_{file_size}.bin")
            generate_random_file(filename, file_size)


main()
