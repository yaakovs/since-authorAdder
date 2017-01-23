'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017
'''

from DocComments.DocComment import DocComment
import re


class JavaDocComment(DocComment):
    """
    a father class for getting the edited code file (with since, author and TODO)
    """
    def __init__(self, FileLines):
        self.needsChange = False
        self.FileLines = FileLines
        self.docComment = None
        self.docLines = None
        self.initDocComment()



    def initDocComment(self):
        '''
        @:inits: the docComment variable as a string, or None if such doesnt exist
        we want to get the last jdoc comment that comes before the first class/interface:
        assuming each file has the word class or interface:
            - get all that comes before the first class/inrterface
            - get all that comes after the last '/**' from what we sliced earlier
            - get all that comes until the first '*/'
        '''
        TillClassInter = re.split("class|interface","".join(self.FileLines))[0]
        if TillClassInter == "".join(self.FileLines):
            # no class and interface and enum
            return
        FromComm = TillClassInter.split("/**")[-1]
        if FromComm == TillClassInter:
            #no jdoc
            self.needsChange = True
            return
        self.docComment = FromComm.split("*/")[0]
        if(self.docComment==FromComm):
            #an error case
            return
        self.docComment = "/**" + self.docComment + "*/"
        self.docLines = self.docComment.split("\n")
        self.docLines = list(map(lambda line: line + "\n", self.docLines))
        self.needsChange = not self.getDescFromComment() or not self.getAuthorFromComment() or not self.getSinceFromComment()

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

    def NeedsChange(self):
        return self.needsChange

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
        TODONote += " please add a description \n" ##TODO: to your class

        if desc:
            newDocComment = "/** " + desc + "\n" ##TODO: remove the \n
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
                if "class" in line or "interface" in line and not found: ##TODO: or enum
                    retList.append(newDocComment)
                    found = True
                retList.append(line)
            return list(map(lambda line: line + "\n", "".join(retList).split("\n")))
        res = "".join(self.FileLines).replace(self.docComment, newDocComment).split("\n")
        return list(map(lambda line: line + "\n", res))
