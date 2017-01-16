'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017
'''

import re

from DocComments.DocComment import DocComment


class JavaDocComment(DocComment):

    """
    a father class for getting the edited code file (with since, author and TODO)
    """

    def getDocComment(self):
        '''
            @:returns the docComment as a string, or None if such doesnt exist
        '''

        comment = re.compile(r'/\*\*(.*?)\*/', re.DOTALL)
        try:
            return comment.findall("\n".join(self.FileLines))[-1:][0]
        except:
            return None
        '''
        try:
            TillClass = "\n".join(self.FileLines).split("class")[0]
            print(TillClass)
            FromComm = TillClass.split("/**")[-1:]
            print(FromComm)
            return FromComm[0].split("*/")[0]
        except:
            return None
'''


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

