import sys
import os
import subprocess

'''
For now - works only for java projects
adds @since and @author to projects

TODO:
make as plugin
refactor
make generic for more langs
do something with the TODO if missing
beautify the writing of since and author:
    edit the files
    change date format to e.g Oct 19, 2016
'''


def checkFile(path,filePath):
    #Check if has since and author
    sinceFlag = False
    authorFlag = False
    with open(filePath, 'r') as f:
        f_content = f.read()
        if("@since" in f_content and "@author" in f_content):
            return
        #else
        if("@since" in f_content):
            sinceFlag = True
        if("@author" in f_content):
            authorFlag = True
    #check commit
    PIPE = subprocess.PIPE
    process = subprocess.Popen(['git', 'log', '--diff-filter=A', '--summary', filePath], stdout=PIPE, stderr=PIPE, cwd = path)
    stdoutput, stderroutput = process.communicate()

    if ('fatal' in stdoutput) or (stderroutput != ''):
        # Handle error case
        print("Error")
    else:
        # Success
        author = "//@author "
        since = "//@since "
        for line in stdoutput.split("\n"):
            if("Date:" in line):
                since += line.split("Date:")[1]
            if("Author:" in line):
                author += line.split("Author:")[1]
        print("===========")
        print("For the file - " + str(filePath) + " :")
        if(not sinceFlag):
            #add //since Date line
            print(since)
        if(not authorFlag):
            #add //author Author line
            print(author)
        print("===========")


def main():
    path = str(sys.argv[1])
    # If your current working directory may change during script execution, it's recommended to
    # immediately convert program arguments to an absolute path. Then the variable root below will
    # be an absolute path as well. Example:
    path = os.path.abspath(path)
    #print('path (absolute) = ' + os.path.abspath(path))
    for root, subdirs, files in os.walk(path):
        #print('--\nroot = ' + root)
        '''
        #iterate through sub directories
        for subdir in subdirs:
            print('\t- subdirectory ' + subdir)
        '''
        #iiterate on files
        for filename in files:
            file_path = os.path.join(root, filename)
            #print('\t- file %s (full path: %s)' % (filename, file_path))
            if(".java" in file_path):
                checkFile(path,file_path)




if __name__ == '__main__':
    main()
