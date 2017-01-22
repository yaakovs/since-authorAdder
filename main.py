import sys
import os
import subprocess

from DocComments.DocComment import DocComment
from DocComments.JavaDocComment import JavaDocComment

'''
For now - works only for java projects
adds @since and @author to projects

USAGE:
python main.py PATH_TO_GIT_PROJECT
--or--
python3 main.py PATH_TO_GIT_PROJECT


TODO:
make as plugin
make generic for more langs
do something with the TODO if missing

'''

##TODO: remove prints, maybe change to logs
def getCommitInfo(path,filePath):
    '''

    :param path: The absolute path to root
    :param filePath: the file path
    :return: Author, Date
    returns the Author and Date of the file - when was it created first and by who, according to the
    commit in which it was created
    '''
    PIPE = subprocess.PIPE
    process = subprocess.Popen(['git', 'log', '--diff-filter=A', '--summary', filePath], stdout=PIPE, stderr=PIPE, cwd=path)
    stdoutput, stderroutput = process.communicate()

    if ('fatal' in stdoutput) or (stderroutput != ''):
        # Handle error case
        print("Error")
    else:
        # Success
        author = ""
        since = ""
        for line in stdoutput.split("\n"):
            if ("Date:" in line):
                FullDate = line.split("Date:")[1].split(" ")
                #The date formatting we chose
                since += FullDate[1] + " " + FullDate[2] + ", " + FullDate[4]
            if ("Author:" in line):
                author += line.split("Author:")[1]
        print("NEED AUTH OR SINCE IN " + filePath + " AND DETAILS ARE - " + author + ", " + since)
        return author, since


def GetSuitableDocComm(filePath,fileLines):
    '''
    :param filePath: the abs path to the file
    :return: a DocComm
    the suitable DocComm for the code file if such exists
    '''
    fileEnding = filePath.split(".")[-1:]
    if "java" in fileEnding:
        return JavaDocComment(fileLines)
    if "JAVA" in fileEnding:
        return JavaDocComment(fileLines)
    if "Java" in fileEnding:
        return JavaDocComment(fileLines)
    return DocComment(fileLines)
    ##TODO: organize in nice switch or something like that

def ChangeFile(path, filePath):
    '''
    :param path: The absolute path to root
    :param filePath: the file path
    :return: None
    calls the suitable DocComment according to the file ending (depends on the pl if it is a code file)
    changes the file if needed - if since,author or description needed (only if a supported code file)
    for a list of supported pl's check __this__ out
    '''

    f = open(filePath, "r")
    contents = f.readlines()
    f.close()

    DocComm = GetSuitableDocComm(filePath,contents)
    if(not DocComm.NeedsChange()):
        return
    Author, Date = getCommitInfo(path,filePath)
    contents = DocComm.ReturnEditedFile(Author,Date)

    f = open(filePath, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()





def main():
    path = str(sys.argv[1])
    path = os.path.abspath(path)
    for root, subdirs, files in os.walk(path):
        #iiterate on files
        for filename in files:
            file_path = os.path.join(root, filename)
            ChangeFile(path, file_path)




if __name__ == '__main__':
    main()
