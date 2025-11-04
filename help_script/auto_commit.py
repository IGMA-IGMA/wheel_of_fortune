import os


def auto_commit(comment: str):
    os.system("git add .")
    os.system(f"git commit -a -m {comment}")
    os.system("git push")


if __name__ == "__main__":
    auto_commit(input("Коментарий к комиту: "))
