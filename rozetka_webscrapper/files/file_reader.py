import os



def get_all_filenames(path, file_should_start_with = ""):
    passed = []
    all = os.listdir(path)
    dir_prefix = (path + "/").replace("/+", "/")
    for filename in all:
        if filename.startswith(file_should_start_with):
            passed.append(dir_prefix + filename)
    return passed



def read_file(path):
    with open(path, "r",encoding="utf-8") as f:
        return f.read()



def read_file_as(path, as_lambda = lambda file_data : file_data) :
    return as_lambda(read_file(path))
