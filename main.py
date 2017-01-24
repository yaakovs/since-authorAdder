import re
import sys
import os
import git
from DocComments.DocComment import DocComment
from DocComments.JavaDocComment import JavaDocComment

'''
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

'''

def get_commit_info(path, filePath):
    '''
    :param path: The absolute path to root
    :param filePath: the file path
    :return: Author, Date
    returns the Author and Date of the file - when was it created first and by who, according to the
    commit in which it was created
    note - we could have used the "popen" function of "subprocess" library, but we chose to use the git library and be
    dependent on it because using libraries in python is the pythonic way, as we have learned in the course
    '''
    repo = git.Repo(path)
    log = repo.git.log('--diff-filter=A', '--summary', filePath)
    author = ""
    since = ""
    print(filePath)
    foundAuth = False
    foundSince = False
    for line in log.split("\n"):
        if ("Date:" in line) and not foundSince:
            FullDate = line.split("Date:")[1].split(" ")
            foundSince = True
            #The date format we chose
            offset = 3
            since += FullDate[1 + offset] + " " + FullDate[2 + offset] + ", " + FullDate[4 + offset]
        if ("Author:" in line) and not foundAuth:
            author += line.split("Author:")[1]
            foundAuth = True
    print("modifying file:" + filePath + " author from first commit: " + author + ", date of first commit: " + since)
    return author, since


def get_suitable_doc_comment(filePath, fileLines):
    '''
    :param filePath: the abs path to the file
    :return: a DocComm
    the suitable DocComm for the code file if such exists
    '''
    fileEnding = filePath.split(".")[-1]
    if fileEnding and re.match("java", fileEnding, re.IGNORECASE):
        return JavaDocComment(fileLines)
    return DocComment(fileLines)

def change_file(path, filePath):
    '''
    :param path: The absolute path to root
    :param filePath: the file path
    :return: None
    calls the suitable DocComment according to the file ending (depends on the pl if it is a code file)
    changes the file if needed - if since,author or description needed (only if a supported code file)
    for a list of supported pl's check __this__ out
    '''
    with open(filePath, "r", encoding="latin-1") as f:
        contents = f.readlines()
    DocComm = get_suitable_doc_comment(filePath, contents)
    if not DocComm.needs_change():
        return
    Author, Date = get_commit_info(path, filePath)
    Contents = DocComm.return_edited_file(Author, Date)
    if not contents:
        return
    with open(filePath, "w", encoding="latin-1") as f:
        f.write("".join(contents))


def main():
    path = str(sys.argv[1])
    path = os.path.abspath(path)
    for root, subdirs, files in os.walk(path):
        #iiterate on files
        for filename in files:
            file_path = os.path.join(root, filename)
            change_file(path, file_path)

if __name__ == '__main__':
    main()
