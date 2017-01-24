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
    def __init__(self, FileLines):
        self.NeedsChange = False
        self.FileLines = FileLines
        self.DocComment = None
        self.DocLines = None
        self.init_doc_comment()

    JavaDefines = " class | interface | enum | annotation "

    def init_doc_comment(self):
        '''
        @:inits the DocComment variable as a string, or None if such doesnt exist
        we want to get the last jdoc comment that comes before the first class/interface:
        assuming each file has the word class or interface:
            - get all that comes before the first class/inrterface
            - get all that comes after the last '/**' from what we sliced earlier
            - get all that comes until the first '*/'
        '''
        TillClassInter = re.split(self.JavaDefines, "".join(self.FileLines))[0]
        if TillClassInter == "".join(self.FileLines):
            # no class and interface and enum
            return
        FromComment = TillClassInter.split("/**")[-1]
        if FromComment == TillClassInter:
            #no java doc
            self.NeedsChange = True
            return
        self.DocComment = FromComment.split("*/")[0]
        if self.DocComment == FromComment:
            #some error case
            return
        self.DocComment = "/**" + self.DocComment + "*/"
        self.DocLines = self.DocComment.split("\n")
        self.DocLines = list(map(lambda line: line + "\n", self.DocLines))
        self.DocLines = list(map(lambda line: re.sub(r'/\*\*|\*/', "", line), self.DocLines))
        self.NeedsChange = not self.get_desc_from_comment() or not self.get_author_from_comment() or not self.get_since_from_comment()

    def get_desc_from_comment(self):
        '''
        @:returns: the description of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@author" not in line and "@since" not in line and re.search('[a-zA-Z]', line),
                                 self.DocLines))
            return res if res else None
        except:
            return None


    def get_author_from_comment(self):
        '''
        @:returns: the author of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@author" in line, self.DocLines))
            return res if res else None
        except:
            return None

    def get_since_from_comment(self):
        '''
        @:returns: the since of the class, if there isn't any returns None
        '''
        try:
            res = "".join(filter(lambda line: "@since" in line, self.DocLines))
            return res if res else None
        except:
            return None

    def needs_change(self):
        return self.NeedsChange

    def rewrite(self, AuthorFormGit, DateFormGit):
        '''
        @:returns a List of a modified file lines with a suitable java doc comment
        '''
        if not self.needs_change():
            return self.FileLines

        Desc = self.get_desc_from_comment()
        AuthorFromComment = self.get_author_from_comment()
        SinceFromComment = self.get_since_from_comment()

        TODONote = "/** TODO: "
        TODONote += AuthorFromComment.split("@author")[1] if AuthorFromComment else AuthorFormGit
        TODONote += " please add a description\n"

        #build the new java doc ocmment
        newDocComment = "/** " + Desc if Desc else TODONote
        newDocComment += AuthorFromComment if AuthorFromComment else " * @author " + AuthorFormGit + "\n"
        newDocComment += SinceFromComment if SinceFromComment else " * @since " + DateFormGit + "\n"
        newDocComment += " */\n"

        #if no java doc existed
        if not self.DocComment:
            LinesToRet = []
            found = False
            for line in self.FileLines:
                if (re.match(self.JavaDefines, line)) and not found:
                    LinesToRet.append(newDocComment)
                    found = True
                LinesToRet.append(line)
            return list(map(lambda line: line + "\n", "".join(LinesToRet).split("\n")))

        res = "".join(self.FileLines).replace(self.DocComment, newDocComment).split("\n")
        return list(map(lambda line: line + "\n", res))
