import os


def a(comment):
    os.system("git add .")
    os.system(f"git commit -a -m {comment}")
    os.system("git push")


a("808")
