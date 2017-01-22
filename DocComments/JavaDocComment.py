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
    JavaDocRegex = r'(/\*\*([^*]|[\n]|(\*+([^*/]|[\n])))*\*+/)[^*/]* class'

    def getDocComment(self):
        '''
        @:returns the docComment as a string, or None if such doesnt exist
        '''
        regexPattern = re.compile(self.JavaDocRegex, re.DOTALL)
        try:
            return regexPattern.findall("\n".join(self.FileLines))[0][0]
        except:
            return None


    def getDescFromComment(self):
        '''
        @:returns: the description of the class, if there isn't any returns None
        '''
        try:
            docBlock = self.getDocComment().split("\n")
            docBlock = map(lambda line: re.sub(r'/\*\*|\*/', "", line), docBlock)
            res =  "\n".join(filter(lambda line: "@author" not in line and "@since" not in line and re.search('[a-zA-Z]', line),
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
            res = "\n".join(filter(lambda line: "@author" in line, docBlock))
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
            res = "\n".join(filter(lambda line: "@since" in line, docBlock))
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
        TODONote = "/** TODO: " + str(Author) + " please add a description to your class\n */"

        desc = self.getDescFromComment()
        author = self.getAuthorFromComment()
        since = self.getSinceFromComment()

        if desc:
            newDocComment = "/** " + desc
        else:
            newDocComment = TODONote
        if author:
            newDocComment += author
        else:
            newDocComment += "* @author " + str(Author) + "\n"
        if since:
            newDocComment += since
        else:
            newDocComment += "* @since " + str(Date) + "\n"

        return "\n".join(self.FileLines).replace(self.getDocComment(), newDocComment).split("\n")
