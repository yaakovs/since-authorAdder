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
        '''
        try:
            TillClass = "\n".join(self.FileLines).split("class")[0]
            if (TillClass == "\n".join(self.FileLines)):
                #no class
                TillInterface = "\n".join(self.FileLines).split("interface")[0]
                if (TillInterface == "\n".join(self.FileLines)):
                    #also no interface
                    return None
                FromComm = TillInterface.split("/**")[-1:]
            else:
                FromComm = TillClass.split("/**")[-1:]
            if (FromComm[0] == TillClass):
                return None
            return "/**" + FromComm[0].split("*/")[0] + "*/"
        except:
            return None

    def getDescFromComment(self):
        '''
        @:returns: the description of the class, if there isn't any returns None
        '''
        try:
            docBlock = self.getDocComment().split("\n")
            docBlock = map(lambda line: re.sub(r'/\*\*|\*/', "", line), docBlock)
            res =  "".join(filter(lambda line: "@author" not in line and "@since" not in line and re.search('[a-zA-Z]', line),
                                 docBlock))
            if(res== '' or res == ' ' or res == '\n'): #TODO: do it better
                return None
            return res
        except:
            return None

    def getAuthorFromComment(self):
        '''
        @:returns: the author of the class, if there isn't any returns None
        '''
        try:
            docBlock = self.getDocComment().split("\n")
            docBlock = map(lambda line: re.sub(r'/\*\*|\*/', "", line), docBlock)
            res = "".join(filter(lambda line: "@author" in line, docBlock))
            if (res == '' or res == ' ' or res == '\n'):  # TODO: do it better
                return None
            return res
        except:
            return None

    def getSinceFromComment(self):
        '''
        @:returns: the since of the class, if there isn't any returns None
        '''
        try:
            docBlock = self.getDocComment().split("\n")
            docBlock = map(lambda line: re.sub(r'/\*\*|\*/', "", line), docBlock)
            res = "".join(filter(lambda line: "@since" in line, docBlock))
            if (res == '' or res == ' ' or res == '\n'):  # TODO: do it better
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
        TODONote = "/** TODO: " + str(Author) + " please add a description to your class\n"

        desc = self.getDescFromComment()
        author = self.getAuthorFromComment()
        since = self.getSinceFromComment()

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
        if(not self.getDocComment()):
            retList = []
            found = False
            for line in self.FileLines:
                if "class" in line and found == False:
                    retList.append(newDocComment)
                    found = True
                retList.append(line)
            return map(lambda line: line + "\n", "".join(retList).split("\n"))
        res = "".join(self.FileLines).replace(self.getDocComment(), newDocComment).split("\n")
        return map(lambda line: line + "\n", res)
