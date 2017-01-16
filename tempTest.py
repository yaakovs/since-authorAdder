import unittest

from DocComments.JavaDocComment import JavaDocComment


class JavaDocCommentTest(unittest.TestCase):
    def test_noDoc(self):
        self.assertEqual(None,JavaDocComment(["abc","efg","hoj"].getDocComment()))

    def getDocCommentNoDoc(self):
        self.assertEqual(None, JavaDocComment(["abc", "efg", "hoj"].getDocComment()))

    def getDocComment1Doc(self):
         self.assertEqual(None, JavaDocComment(["abc", "efg", "hoj"].getDocComment()))

    def getDocComment2Docs(self):
        self.assertEqual(None, JavaDocComment(["abc", "efg", "hoj"].getDocComment()))