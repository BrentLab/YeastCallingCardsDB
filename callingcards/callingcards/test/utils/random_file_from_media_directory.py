import os
import random


def random_file_from_media_directory(dir_name: str) -> str:
    # Assuming 'factories.py' is in the root of your test
    # directory and 'data' is a subdirectory of 'test'.
    test_data_directory = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        dir_name)

    # Ensuring the directory exists
    if not os.path.exists(test_data_directory):
        raise FileNotFoundError(
            f"Directory does not exist: {test_data_directory}")

    # List files in the specified directory within 'test/data'
    files = [f for f in os.listdir(test_data_directory)
             if os.path.isfile(os.path.join(test_data_directory, f))]

    # Return a random file path from the directory
    return os.path.join(test_data_directory, random.choice(files))
