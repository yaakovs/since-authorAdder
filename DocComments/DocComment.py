'''
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017

a father class for getting the edited code file (with since, author and TODO)
will be inherited by any PL doc Comment
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
    def init_doc_comment(self):
        return None

    def needs_change(self):
        '''
        @:returns: True if needs change, else false
        '''
        return False

    '''
    @:returns: the description of the class, if there isn't any returns None
    '''
    def get_desc_from_comment(self):

        return None
    '''
    @:returns: the author of the class, if there isn't any returns None
    '''
    def get_author_from_comment(self):

        return None

    '''
    @:returns: the since of the class, if there isn't any returns None
    '''
    def get_since_from_comment(self):
        return None

    '''
    @:returns a List of edited code lines
    '''
    def rewrite(self, author, date):
        return None

    '''
    @:returns List of edited code lines or None if no change is needed
    '''
    def return_edited_file(self, author, date):
        if not self.needs_change():
            return None
        return self.rewrite(author, date)

