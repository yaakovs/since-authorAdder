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
    @:returns: the description of the class, if there isn't any returns None
    '''
    def getDescFromComment(self):

        return None
    '''
    @:returns: the author of the class, if there isn't any returns None
    '''
    def getAuthorFromComment(self):

        return None

    '''
    @:returns: the since of the class, if there isn't any returns None
    '''
    def getSinceFromComment(self):
        return None

    '''
    @:returns a List of edited code lines
    '''
    def Rewrite(self,Author,Date):
        return None

    '''
    @:returns List of edited code lines or None if no change is needed
    '''
    def ReturnEditedFile(self, Author, Date):
        if(not self.NeedsChange()):
            return None
        return self.Rewrite()

