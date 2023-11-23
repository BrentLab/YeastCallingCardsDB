def get_file_content(filepath):
    """open a file and return its contents as a string"""
    with open(filepath, 'rb') as file:
        return file.read()