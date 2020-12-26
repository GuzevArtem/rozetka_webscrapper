import os


def create_parent_dirs(file_path) :
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)



def write_plain(file_path, data, encoding='utf-8', mode = 'w') :
    create_parent_dirs(file_path)
    with open(file_path, mode, encoding='utf-8') as f:
        f.write(data)



def write_plain_iterable(file_path, data_iterable, operation_on_each = lambda o : o , encoding = 'utf-8', separator_between = ",\n\r", before_all = "[", after_all = "]") :
    create_parent_dirs(file_path)
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(before_all)
        count = 0
        for data in data_iterable:
            if count > 0 :
                f.write(separator_between)
            f.write(operation_on_each(data))
            count += 1
        f.write(after_all)

