import unittest

from DocComments.JavaDocComment import JavaDocComment


class JavaDocCommentTest(unittest.TestCase):
    def test_getDocCommentNoDoc(self):
        self.assertEqual(None, JavaDocComment(["abc\n", "efg\n", "hoj\n"]).initDocComment())

    def test_getDocComment1Doc(self):
        self.assertEqual("/** hello\n world\n*/", JavaDocComment(["abc\n", "/** hello\n", " world\n","*/\n","public static class main()\n"]).initDocComment())

    def test_getDocComment2Docs(self):
        self.assertEqual("/** hello2\n world2\n*/", JavaDocComment(["/** hello\n", " world\n","*/\n", "efg\n","/** hello2\n", " world2\n","*/\n", "hoj\n","public static class main()\n"]).initDocComment())

    def test_oneLineDoc(self):
        str = "/** hello world */ class"
        self.assertEqual("/** hello world */", JavaDocComment([str]).initDocComment())

    def test_oneLine2Docs(self):
        str = "/** hello world */ \n"
        str2 = "/** hello2 world2 */ class\n"
        self.assertEqual("/** hello2 world2 */", JavaDocComment([str,str2]).initDocComment())


    def test_hasClassNoDoc(self):
        str = "/* hello world */ \n"
        str2 = "public static class\n"
        self.assertEqual(None, JavaDocComment([str, str2]).initDocComment())


    def test_noClassHasDoc(self):
        str = "/** hello world */ "
        str2 = "public static"
        self.assertEqual(None, JavaDocComment([str, str2]).initDocComment())

    def test_realCode(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class\n"
        self.assertEqual("/** Expands terms of * or / expressions without reordering. \n"
                         " * <p>\n"
                         " * Functions named {@link #base} are non-recursive\n"
                         " * @author Yossi Gil\n"
                         " * @author Niv Shalmon\n"
                         " * @since 2016-08 */", JavaDocComment([str, str2, str3, str4, str5, str6, str7]).initDocComment())

    def test_realCode_getDesc(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class"
        self.assertEqual(" Expands terms of * or / expressions without reordering. \n"
                         " * <p>\n"
                         " * Functions named {@link #base} are non-recursive\n",
                         JavaDocComment([str, str2, str3, str4, str5, str6, str7]).getDescFromComment())

    def test_realCode_getDesc_None(self):
        str = "/** "
        str4 = " * @author Yossi Gil"
        str5 = " * @author Niv Shalmon"
        str6 = " * @since 2016-08 */"
        str7 = "public static class"
        self.assertEqual(None,
                         JavaDocComment([str, str4, str5, str6, str7]).getDescFromComment())

    def test_realCode_getAuth(self):
        str = "/** Expands terms of * or / expressions without reordering.\n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class\n"
        self.assertEqual(" * @author Yossi Gil\n"
                         " * @author Niv Shalmon\n",
                         JavaDocComment([str, str2, str3, str4, str5, str6, str7]).getAuthorFromComment())

    def test_realCode_getAuth_None(self):
        str = "/** Expands terms of * or / expressions without reordering. "
        str2 = " * <p>"
        str3 = " * Functions named {@link #base} are non-recursive"
        str6 = " * @since 2016-08 */"
        str7 = "public static class"
        self.assertEqual(None,
                         JavaDocComment([str, str2, str3, str6, str7]).getAuthorFromComment())

    def test_realCode_getAuth_SameLine(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil @author Niv Shalmon */ \n"
        str7 = "public static class\n"
        self.assertEqual(" * @author Yossi Gil "
                         "@author Niv Shalmon \n",
                         JavaDocComment([str, str2, str3, str4, str7]).getAuthorFromComment())

    def test_realCode_getSince(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class"
        self.assertEqual(" * @since 2016-08 \n",
                         JavaDocComment([str, str2, str3, str4, str5, str6, str7]).getSinceFromComment())

    ##TODO: fix this
    '''
    def test_realCode_getSince_SameLine(self):
        str = "/** Expands terms of * or / expressions without reordering. "
        str2 = " * <p>"
        str3 = " * Functions named {@link #base} are non-recursive"
        str4 = " * @author Yossi Gil @since 2016-08 */ "
        str7 = "public static class"
        self.assertEqual(" @since 2016-08 ",
                         JavaDocComment([str, str2, str3, str4, str7]).getSinceFromComment())
    '''

    def test_realCode_getSince_None(self):
        str = "/** Expands terms of * or / expressions without reordering. "
        str2 = " * <p>"
        str3 = " * Functions named {@link #base} are non-recursive"
        str4 = " * @author Yossi Gil */ "
        str7 = "public static class"
        self.assertEqual(None,
                         JavaDocComment([str, str2, str3, str4, str7]).getSinceFromComment())

    def test_doesnt_need_change(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class\n"
        self.assertEqual(False,
                         JavaDocComment([str, str2, str3, str4, str5, str6, str7]).NeedsChange())

    def test_need_change_since(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str7 = "public static class\n"
        self.assertEqual(True,
                         JavaDocComment([str, str2, str3, str4, str5, str7]).NeedsChange())

    def test_realCode_rewrite_no_change(self):
        str = "/** Expands terms of * or / expressions without reordering. \n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str4 = " * @author Yossi Gil\n"
        str5 = " * @author Niv Shalmon\n"
        str6 = " * @since 2016-08 */\n"
        str7 = "public static class\n"
        self.assertEqual([str, str2, str3, str4, str5, str6, str7], JavaDocComment([str, str2, str3, str4, str5, str6, str7]).Rewrite("Yossi Gil","2016-08"))


    def test_realCode_rewrite_change(self):
        str = "/** Expands terms of * or / expressions without reordering.\n"
        str2 = " * <p>\n"
        str3 = " * Functions named {@link #base} are non-recursive\n"
        str6 = " */\n"
        str7 = "public static class\n"
        self.assertEqual(["/**  Expands terms of * or / expressions without reordering.\n",
                         " * <p>\n",
                         " * Functions named {@link #base} are non-recursive\n",
                         "\n",
                         " * @author Yossi Gil\n",
                         " * @since 2016-08\n",
                          " */\n",
                          "\n",
                          "public static class\n","\n"], JavaDocComment([str, str2, str3, str6, str7]).Rewrite("Yossi Gil","2016-08"))


    def test_docComment_real_rav(self):
        str4 = "/** An expander to rename short or unnecessarily understandable variable names\n"
        str = "* in a method dec to more common or intuitive names (s.e i for an integer\n"
        str2 = "* variable and ret for a return variable) : <code>\n"
        str3 = "* Important - the $ will always change to ret by convention\n"
        str5 = "* @author Raviv Rachmiel <tt> raviv.rachmiel@gmail.com </tt>\n"
        str6 = "* @since 2017-01-10 Issue #979, {@link Issue0979} */\n"
        str7 = "// TODO: take care of single var decleration, tests\n"
        str8 = "public class RenameShortNamesMethodDec extends EagerTipper<MethodDeclaration>\n"
        self.assertEqual(False,
                         JavaDocComment([str4,str, str2, str3, str5, str6,str7,str8]).NeedsChange())
        #print( JavaDocComment([str4,str, str2, str3, str5, str6,str7,str8]).Rewrite("Yossi Gil","2016-08"))


if __name__ == '__main__':
    unittest.main()
