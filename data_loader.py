def load_data(file_path):               #This parameter represents the path to the file you want to read
    with open(file_path, 'r') as file:    # The with statement ensures that the file is automatically closed when the block of code is exited, even if an error occurs
        return file.read()
