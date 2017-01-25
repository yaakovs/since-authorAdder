import sys
import os
import src.SinceAuthor

def main():
    if len(sys.argv) == 4:
        src.SinceAuthor.github_plugin(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 2:
        path = str(sys.argv[1])
        path = os.path.abspath(path)
        src.SinceAuthor.dir_walk(path)
    else:
        print("USAGE IS: python3 main.py <local_repo> OR python3 main.py <github_repo> <user.name> <user.mail>")

if __name__ == '__main__':
    main()