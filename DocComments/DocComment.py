'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017

a father class for getting the edited code file (with since, author and TODO)
'''
class DocComment():
    '''
    @:param fileLines - list of lines of the code file
    '''
    def __init__(self, FileLines):
        self.FileLines = FileLines

    '''
    @:returns the docComment as a string, or None if such doesnt exist
    '''
    def getDocComment(self):
        return None

    '''
    @:returns if the file needs to be edited
    '''
    def NeedsChange(self):
        return False

    '''
    @:returns a List of edited code lines
    '''
    def Rewrite(self):
        return None

    '''
    @:returns List of edited code lines or None if no change is needed
    '''
    def returnEditedFile(self):
        if(not self.NeedsChange()):
            return None
        return self.Rewrite()

