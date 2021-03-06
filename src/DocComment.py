"""
author Raviv Rachmiel
author Yaakov Sokolik
since Jan 16, 2017

a father class for getting the edited code file (with since, author and TODO)
will be inherited by any PL doc Comment
"""


class DocComment():

    def __init__(self, file_lines):
        """
        :param file_lines - list of lines of the code file
        """
        self.FileLines = file_lines

    def init_doc_comment(self):
        """
        :returns the docComment as a string, or None if such doesnt exist
        """
        return None

    def needs_change(self):
        """
        :returns: True if needs change, else false
        """
        return False

    def get_desc_from_comment(self):
        """
        :returns: the description of the class, if there isn't any returns None
        """
        return None
    
    def get_author_from_comment(self):
        """
        :returns: the author of the class, if there isn't any returns None
        """
        return None

    def get_since_from_comment(self):
        """
        :returns: the since of the class, if there isn't any returns None
        """
        return None

    def rewrite(self, author, date):
        """
        :param author: the author to add to doc comment
        :param date: the date to add to doc comment
        :returns a string of edited code file
        """
        return None

    def return_edited_file(self, author, date):
        """
        :param author: the author to add to doc comment
        :param date: the date to add to doc comment
        :returns List of edited code lines or None if no change is needed
        """
        if not self.needs_change():
            return None
        return self.rewrite(author, date)

