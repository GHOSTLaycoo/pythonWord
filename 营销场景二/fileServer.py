import os
import pandas as pd


def sortByFileTime():
    old_name = ""
    dir_name = "H:/数为/DW/财务-场景八/"
    file_list = os.listdir(dir_name)
    new_file_list = sorted(file_list, key=lambda file: os.path.getmtime(os.path.join(dir_name, file)), reverse=True)
    for f in new_file_list:
        if f.startswith("数字化应付") and f.endswith(".xlsx"):
            old_name = os.path.join(dir_name, f)
            break

    data = pd.read_excel(old_name)

    new_name = os.path.join(dir_name, "-"+str(f))
    print(new_name)
    os.rename(old_name, new_name)
    print(data)


if __name__ == '__main__':
    sortByFileTime()