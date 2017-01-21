import unittest

from DocComments.JavaDocComment import JavaDocComment


class JavaDocCommentTest(unittest.TestCase):
    def test_getDocCommentNoDoc(self):
        self.assertEqual(None, JavaDocComment(["abc", "efg", "hoj"]).getDocComment())

    def test_getDocComment1Doc(self):
        self.assertEqual("/** hello\n world\n*/", JavaDocComment(["abc", "/** hello", " world","*/","public static class main()"]).getDocComment())

    def test_getDocComment2Docs(self):
        self.assertEqual("/** hello2\n world2\n*/", JavaDocComment(["/** hello", " world","*/", "efg","/** hello2", " world2","*/", "hoj","public static class main()"]).getDocComment())

    def test_oneLineDoc(self):
        str = "/** hello world */ class"
        self.assertEqual("/** hello world */", JavaDocComment([str]).getDocComment())

    def test_oneLine2Docs(self):
        str = "/** hello world */ "
        str2 = "/** hello2 world2 */ class"
        self.assertEqual("/** hello2 world2 */", JavaDocComment([str,str2]).getDocComment())


    def test_hasClassNoDoc(self):
        str = "/* hello world */ "
        str2 = "public static class"
        self.assertEqual(None, JavaDocComment([str, str2]).getDocComment())


    def test_noClassHasDoc(self):
        str = "/** hello world */ "
        str2 = "public static"
        self.assertEqual(None, JavaDocComment([str, str2]).getDocComment())

    def test_realCode(self):
        str = "/** Expands terms of * or / expressions without reordering. "
        str2 = " * <p>"
        str3 = " * Functions named {@link #base} are non-recursive"
        str4 = " * @author Yossi Gil"
        str5 = " * @author Niv Shalmon"
        str6 = " * @since 2016-08 */"
        str7 = "public static class"
        self.assertEqual("/** Expands terms of * or / expressions without reordering. \n"
                         " * <p>\n"
                         " * Functions named {@link #base} are non-recursive\n"
                         " * @author Yossi Gil\n"
                         " * @author Niv Shalmon\n"
                         " * @since 2016-08 */", JavaDocComment([str, str2, str3, str4, str5, str6, str7]).getDocComment())

if __name__ == '__main__':
    unittest.main()