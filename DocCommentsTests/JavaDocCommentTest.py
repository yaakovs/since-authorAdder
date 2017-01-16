import unittest

from DocComments.JavaDocComment import JavaDocComment


class JavaDocCommentTest(unittest.TestCase):
    def test_getDocCommentNoDoc(self):
        self.assertEqual(None, JavaDocComment(["abc", "efg", "hoj"]).getDocComment())

    def test_getDocComment1Doc(self):
        self.assertEqual(" hello\n world\n", JavaDocComment(["abc", "/** hello", " world","*/","public static class main()"]).getDocComment())

    def test_getDocComment2Docs(self):
        self.assertEqual(" hello2\n world2\n", JavaDocComment(["/** hello", " world","*/", "efg","/** hello2", " world2","*/", "hoj","public static class main()"]).getDocComment())

    def test_oneLineDoc(self):
        str = "/** hello world */ class"
        self.assertEqual(" hello world ", JavaDocComment([str]).getDocComment())

    def test_oneLine2Docs(self):
        str = "/** hello world */ "
        str2 = "/** hello2 world2 */ class"
        self.assertEqual(" hello2 world2 ", JavaDocComment([str,str2]).getDocComment())


    def test_hasClassNoDoc(self):
        str = "/* hello world */ "
        str2 = "public static class"
        self.assertEqual(None, JavaDocComment([str, str2]).getDocComment())


    def test_noClassHasDoc(self):
        str = "/** hello world */ "
        str2 = "public static"
        self.assertEqual(None, JavaDocComment([str, str2]).getDocComment())


if __name__ == '__main__':
    unittest.main()

    # /**
    #     hello world
    # */
    # fkmsdfds
    # /**
    #     hello2 world2
    # */
    # public static void main
