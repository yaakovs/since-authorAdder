"""
For now - works only for java projects
adds @since and @author to projects

USAGE:
first check that you have the git api by using "import git" in a python terminal
if you don't have it install, use pip3 install gitpython (or by manually installing)


python3 main.py PATH_TO_GIT_PROJECT


TODO:
make as plugin
make generic for more langs
do something with the TODO if missing
"""
import re
import sys
import os
import git
from DocComments.DocComment import DocComment
from DocComments.JavaDocComment import JavaDocComment


def get_commit_info(path, file_path):
    """
    :param path: The absolute path to root
    :param file_path: the file path
    :return: author, date
    returns the Author and Date of the file - when was it created first and by who, according to the
    commit in which it was created
    note - we could have used the "popen" function of "subprocess" library, but we chose to use the git library and be
    dependent on it because using libraries in python is the pythonic way, as we have learned in the course
    """
    repo = git.Repo(path)
    log = repo.git.log('--diff-filter=A', '--summary', file_path)
    author = ""
    date = ""
    found_author = False
    found_date = False
    for line in log.split("\n"):
        if ("Date:" in line) and not found_date:
            full_date = line.split("Date:")[1].split(" ")
            found_date = True
            # The date format we chose
            offset = 3
            date += full_date[1 + offset] + " " + full_date[2 + offset] + ", " + full_date[4 + offset]
        if ("Author:" in line) and not found_author:
            author += line.split("Author:")[1]
            found_author = True
    print("modifying file: " + file_path + "\nauthor from first commit:" + author + ", date of first commit: " + date + "\n")
    return author, date


def get_suitable_doc_comment(file_path, file_lines):
    """
    :param file_path: the abs path to the file
    :param file_lines: list of file lines
    :return: a DocComm
    the suitable DocComm for the code file if such exists
    """
    file_ending = file_path.split(".")[-1]
    if file_ending and re.match("java", file_ending, re.IGNORECASE):
        return JavaDocComment(file_lines)
    return DocComment(file_lines)


def change_file(path, file_path):
    """
    :param path: The absolute path to root
    :param file_path: the file path
    :return: None
    calls the suitable DocComment according to the file ending (depends on the pl if it is a code file)
    changes the file if needed - if since,author or description needed (only if a supported code file)
    for a list of supported pl's check __this__ out
    """
    with open(file_path, "r", encoding="latin-1") as f:
        file_content = f.readlines()
    file_DocComment = get_suitable_doc_comment(file_path, file_content)
    if not file_DocComment.needs_change():
        return
    author, date = get_commit_info(path, file_path)
    edited_content = file_DocComment.return_edited_file(author, date)
    if not edited_content:
        return
    with open(file_path, "w", encoding="latin-1") as f:
        f.write("".join(edited_content))


def main():
    path = str(sys.argv[1])
    path = os.path.abspath(path)
    for root, subdirs, files in os.walk(path):
        # iterate on files
        for filename in files:
            file_path = os.path.join(root, filename)
            change_file(path, file_path)

if __name__ == '__main__':
    main()
