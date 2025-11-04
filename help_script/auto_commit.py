import os


def auto_commit():
    os.system("git add .")
    os.system(f"git commit -a -m {input("Коментарий к комиту: ")}")
    os.system("git push")


if __name__ == "__main__":
    auto_commit()
