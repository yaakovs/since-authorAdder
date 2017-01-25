"""
@author Raviv Rachmiel
@author Yaakov Sokolik
@since Jan 16, 2017
"""

from DocComments.DocComment import DocComment
import re


class JavaDocComment(DocComment):
    """
    a class for getting java code file (with since, author and TODO)
    """
    def __init__(self, file_lines):
        self.NeedsChange = False
        self.FileLines = file_lines
        self.DocComment = None
        self.DocLines = None
        self.init_doc_comment()

    JavaDefines = " class | interface | enum | annotation "

    def init_doc_comment(self):
        """
        :inits the DocComment variable as a string, or None if such doesnt exist
        we want to get the last jdoc comment that comes before the first class/interface:
        assuming each file has the word class or interface:
            - get all that comes before the first class/inrterface
            - get all that comes after the last '/**' from what we sliced earlier
            - get all that comes until the first '*/'
        """
        before_define = re.split(self.JavaDefines, "".join(self.FileLines))[0]
        if before_define == "".join(self.FileLines):
            # no class and interface and enum
            return
        from_comment = before_define.split("/**")[-1]
        if from_comment == before_define:
            # no java doc
            self.NeedsChange = True
            return
        self.DocComment = from_comment.split("*/")[0]
        if self.DocComment == from_comment:
            # some error case
            return
        self.DocComment = "/**" + self.DocComment + "*/"
        self.DocLines = map(lambda line: line + "\n", self.DocComment.split("\n"))
        self.DocLines = list(map(lambda line: re.sub(r'/\*\*|\*/', "", line), self.DocLines))
        self.NeedsChange = not self.get_desc_from_comment() or not self.get_author_from_comment() \
                           or not self.get_since_from_comment()

    def get_desc_from_comment(self):
        """
        :returns: the description of the class, if there isn't any returns None
        """
        try:
            res = "".join(filter(lambda line: "@author" not in line and "@since" not in line and
                                              re.search('[a-zA-Z]', line), self.DocLines))
            return res if res else None
        except:
            return None

    def get_author_from_comment(self):
        """
        :returns: the author of the class, if there isn't any returns None
        """
        try:
            res = "".join(filter(lambda line: "@author" in line, self.DocLines))
            return res if res else None
        except:
            return None

    def get_since_from_comment(self):
        """
        :returns: the since of the class, if there isn't any returns None
        """
        try:
            res = "".join(filter(lambda line: "@since" in line, self.DocLines))
            return res if res else None
        except:
            return None

    def needs_change(self):
        return self.NeedsChange

    def rewrite(self, author_form_git, date_form_git):
        """
        :param author_form_git: the author to add to doc comment
        :param date_form_git: the date to add to doc comment
        :returns a string of the modified file with a suitable java doc comment
        """
        if not self.needs_change():
            return self.FileLines

        desc = self.get_desc_from_comment()
        author_from_comment = self.get_author_from_comment()
        since_from_comment = self.get_since_from_comment()

        todo_note = "/** TODO: "
        todo_note += author_from_comment.split("@author")[1] if author_from_comment else author_form_git
        todo_note += " please add a description\n"

        # build the new java doc comment
        new_doc_comment = "/** " + desc if desc else todo_note
        new_doc_comment += author_from_comment if author_from_comment else " * @author " + author_form_git + "\n"
        new_doc_comment += since_from_comment if since_from_comment else " * @since " + date_form_git + "\n"
        new_doc_comment += " */"

        # if no java doc existed
        if not self.DocComment:
            lines_to_return = []
            found = False
            for line in self.FileLines:
                if (re.match(".*[" + self.JavaDefines + "]", line)) and not found:
                    lines_to_return.extend(list(map(lambda line: line + "\n", new_doc_comment.split("\n"))))
                    found = True
                lines_to_return.append(line)
            return "".join(lines_to_return)
        else:
            return "".join(self.FileLines).replace(self.DocComment, new_doc_comment, 1)
