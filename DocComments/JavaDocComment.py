'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017
'''

from DocComment import DocComment
import re

class JavaDocComment(DocComment):

    """
    a father class for getting the edited code file (with since, author and TODO)
    """

    def getDocComment(self):
        '''
            @:returns the docComment as a string, or None if such doesnt exist
            TODO: do it better
        '''
        '''
        JavaDocPattern = r'/\*\*((?:.|\n)*?)\*/.*class'
        comment = re.compile(JavaDocPattern,re.MULTILINE)
        try:
            return comment.findall("\n".join(self.FileLines))[-1:][0]
        except:
            return None
        '''
        self.DocString = None
        try:
            TillClass = "\n".join(self.FileLines).split("class")[0]
            if(TillClass == "\n".join(self.FileLines)):
                return None
            FromComm = TillClass.split("/**")[-1:]
            if(FromComm[0] == TillClass):
                return None
            self.DocString = FromComm[0].split("*/")[0]
            return FromComm[0].split("*/")[0]
        except:
            return None


    def hasTODO(self):
        '''
        :returns: True if we have a description for class, else False
        for now - return true always
        '''
        return True

    def NeedsChange(self):
        """
        @:returns if the file needs to be edited
        """
        if(not self.DocString):
            return False
        if("@since" in self.DocString and "@author" in self.DocString and self.hasTODO()):
            return False
        return True


    def Rewrite(self,Author,Date):
        '''
        @:returns a List of edited code lines
        '''
        author = "@author "
        since = "@since "
        if(not self.NeedsChange()):
            return None
        if("@since" in self.DocString):
            return True



