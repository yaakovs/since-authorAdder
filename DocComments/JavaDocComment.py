'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017
'''

from DocComments.DocComment import DocComment
import re


class JavaDocComment(DocComment):
    def __init__(self, FileLines):
        self.FileLines = FileLines
        self.getDocComment()
    """
    a father class for getting the edited code file (with since, author and TODO)
    """
    #JavaDocRegex = r'/\*\*([^/\*]*?)\*/[^*/]* class'
    JavaDocRegex = r'(/\*\*([^*]|[\n]|(\*+([^*/]|[\n])))*\*+/)[^*/]* (class|interface|Interface|Class)+'

    def getDocComment2(self):
        '''
        @:returns the docComment as a string, or None if such doesnt exist
        '''
        regexPattern = re.compile(self.JavaDocRegex, re.DOTALL)
        try:
            return regexPattern.findall("".join(self.FileLines))[0][0]
        except:
            return None

    def getDocComment(self):
        '''
        @:returns the docComment as a string, or None if such doesnt exist
        we want to get the last jdoc comment that comes before the first class/interface:
        assuming each file has the word class or interface:
            - get all that comes before the first class/inrterface
            - get all that comes after the last '/**' from what we sliced earlier
            - get all that comes until the first '*/'
        '''
        self.docComment = None
        self.docLines = None
        TillClassInter = re.split("class|interface","".join(self.FileLines))[0]
        if (TillClassInter == "".join(self.FileLines)):
            # no class and interface
            return None
        FromComm = TillClassInter.split("/**")[-1]
        if(FromComm == TillClassInter):
            #no jdoc
            return None
        self.docComment = FromComm.split("*/")[0]
        if(self.docComment==FromComm):
            return None
        self.docLines = self.docComment.split("\n")
        self.docLines = list(map(lambda line: line + "\n", self.docLines))
        self.docComment = "/**" + self.docComment + "*/"
        return self.docComment

    def getDescFromComment(self):
        '''
        @:returns: the description of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@author" not in line and "@since" not in line and re.search('[a-zA-Z]', line),
                                 self.docLines))
            if not res:
                return None
            return res
        except:
            return None

    def getAuthorFromComment(self):
        '''
        @:returns: the author of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@author" in line, self.docLines))
            if not res:
                return None
            return res
        except:
            return None

    def getSinceFromComment(self):
        '''
        @:returns: the since of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@since" in line, self.docLines))
            if not res:
                return None
            return res
        except:
            return None

    def NeedsChange(self):
        '''
        :return: True if needs change and False else
        '''
        return not self.getAuthorFromComment() or not self.getSinceFromComment() or not self.getDescFromComment()


    def Rewrite(self, Author, Date):
        '''
        @:returns a List of a suitable docComment
        '''
        if(not self.NeedsChange()):
            return self.FileLines

        desc = self.getDescFromComment()
        author = self.getAuthorFromComment()
        since = self.getSinceFromComment()

        TODONote = "/** TODO: "
        TODONote += author.split("@author")[1] if author else Author
        TODONote += " please add a description to your class\n"

        if desc:
            newDocComment = "/** " + desc + "\n"
        else:
            newDocComment = TODONote
        if author:
            newDocComment += author
        else:
            newDocComment += " * @author " + str(Author) + "\n"
        if since:
            newDocComment += since
        else:
            newDocComment += " * @since " + str(Date) + "\n"
        newDocComment += " */\n"

        #if no java doc existed
        if not self.docComment:
            retList = []
            found = False
            for line in self.FileLines:
                if "class" in line and found == False:
                    retList.append(newDocComment)
                    found = True
                retList.append(line)
            return list(map(lambda line: line + "\n", "".join(retList).split("\n")))
        res = "".join(self.FileLines).replace(self.docComment, newDocComment).split("\n")
        return list(map(lambda line: line + "\n", res))
