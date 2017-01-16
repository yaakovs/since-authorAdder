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
        '''
        JavaDocPattern = r'///*/*(.*)/*// .* class'
        matchObject = re.match(JavaDocPattern,self.FileLines.join("\n"))
        if matchObject:
            return matchObject.group(1) 
        return None


    def NeedsChange(self):
        """
        @:returns if the file needs to be edited
        """
        return False


    def Rewrite(self):
        '''
        @:returns a List of edited code lines
        '''
        return None


    def returnEditedFile(self):
        '''
        @:returns List of edited code lines or None if no change is needed
        '''
        if(not self.NeedsChange()):
            return None
        return self.Rewrite()

