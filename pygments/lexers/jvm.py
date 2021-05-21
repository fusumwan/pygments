"""
    pygments.lexers.jvm
    ~~~~~~~~~~~~~~~~~~~

    Pygments lexers for JVM languages.

    :copyright: Copyright 2006-2021 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, include, bygroups, using, \
    this, combined, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation
from pygments.util import shebang_matches
from pygments import unistring as uni

__all__ = ['JavaLexer', 'ScalaLexer', 'GosuLexer', 'GosuTemplateLexer',
           'GroovyLexer', 'IokeLexer', 'ClojureLexer', 'ClojureScriptLexer',
           'KotlinLexer', 'XtendLexer', 'AspectJLexer', 'CeylonLexer',
           'PigLexer', 'GoloLexer', 'JasminLexer', 'SarlLexer']


class JavaLexer(RegexLexer):
    """
    For `Java <https://www.oracle.com/technetwork/java/>`_ source code.
    """

    name = 'Java'
    aliases = ['java']
    filenames = ['*.java']
    mimetypes = ['text/x-java']

    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    tokens = {
        'root': [
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            # keywords: go before method names to avoid lexing "throw new XYZ"
            # as a method signature
            (r'(assert|break|case|catch|continue|default|do|else|finally|for|'
             r'if|goto|instanceof|new|return|switch|this|throw|try|while)\b',
             Keyword),
            # method names
            (r'((?:(?:[^\W\d]|\$)[\w.\[\]$<>]*\s+)+?)'  # return arguments
             r'((?:[^\W\d]|\$)[\w$]*)'                  # method name
             r'(\s*)(\()',                              # signature start
             bygroups(using(this), Name.Function, Text, Punctuation)),
            (r'@[^\W\d][\w.]*', Name.Decorator),
            (r'(abstract|const|enum|extends|final|implements|native|private|'
             r'protected|public|static|strictfp|super|synchronized|throws|'
             r'transient|volatile)\b', Keyword.Declaration),
            (r'(boolean|byte|char|double|float|int|long|short|void)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(class|interface)(\s+)', bygroups(Keyword.Declaration, Text),
             'class'),
            (r'(var)(\s+)', bygroups(Keyword.Declaration, Text),
             'var'),
            (r'(import(?:\s+static)?)(\s+)', bygroups(Keyword.Namespace, Text),
             'import'),
            (r'"', String, 'string'),
            (r"'\\.'|'[^\\]'|'\\u[0-9a-fA-F]{4}'", String.Char),
            (r'(\.)((?:[^\W\d]|\$)[\w$]*)', bygroups(Punctuation,
                                                     Name.Attribute)),
            (r'^\s*([^\W\d]|\$)[\w$]*:', Name.Label),
            (r'([^\W\d]|\$)[\w$]*', Name),
            (r'([0-9][0-9_]*\.([0-9][0-9_]*)?|'
             r'\.[0-9][0-9_]*)'
             r'([eE][+\-]?[0-9][0-9_]*)?[fFdD]?|'
             r'[0-9][eE][+\-]?[0-9][0-9_]*[fFdD]?|'
             r'[0-9]([eE][+\-]?[0-9][0-9_]*)?[fFdD]|'
             r'0[xX]([0-9a-fA-F][0-9a-fA-F_]*\.?|'
             r'([0-9a-fA-F][0-9a-fA-F_]*)?\.[0-9a-fA-F][0-9a-fA-F_]*)'
             r'[pP][+\-]?[0-9][0-9_]*[fFdD]?', Number.Float),
            (r'0[xX][0-9a-fA-F][0-9a-fA-F_]*[lL]?', Number.Hex),
            (r'0[bB][01][01_]*[lL]?', Number.Bin),
            (r'0[0-7_]+[lL]?', Number.Oct),
            (r'0|[1-9][0-9_]*[lL]?', Number.Integer),
            (r'[~^*!%&\[\]<>|+=/?-]', Operator),
            (r'[{}();:.,]', Punctuation),
            (r'\n', Text)
        ],
        'class': [
            (r'([^\W\d]|\$)[\w$]*', Name.Class, '#pop')
        ],
        'var': [
            (r'([^\W\d]|\$)[\w$]*', Name, '#pop')
        ],
        'import': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
        'string': [
            (r'[^\\"]+', String),
            (r'\\\\', String),  # Escaped backslash
            (r'\\"', String),  # Escaped quote
            (r'\\', String),  # Bare backslash
            (r'"', String, '#pop'),  # Closing quote
        ],
    }


class AspectJLexer(JavaLexer):
    """
    For `AspectJ <http://www.eclipse.org/aspectj/>`_ source code.

    .. versionadded:: 1.6
    """

    name = 'AspectJ'
    aliases = ['aspectj']
    filenames = ['*.aj']
    mimetypes = ['text/x-aspectj']

    aj_keywords = {
        'aspect', 'pointcut', 'privileged', 'call', 'execution',
        'initialization', 'preinitialization', 'handler', 'get', 'set',
        'staticinitialization', 'target', 'args', 'within', 'withincode',
        'cflow', 'cflowbelow', 'annotation', 'before', 'after', 'around',
        'proceed', 'throwing', 'returning', 'adviceexecution', 'declare',
        'parents', 'warning', 'error', 'soft', 'precedence', 'thisJoinPoint',
        'thisJoinPointStaticPart', 'thisEnclosingJoinPointStaticPart',
        'issingleton', 'perthis', 'pertarget', 'percflow', 'percflowbelow',
        'pertypewithin', 'lock', 'unlock', 'thisAspectInstance'
    }
    aj_inter_type = {'parents:', 'warning:', 'error:', 'soft:', 'precedence:'}
    aj_inter_type_annotation = {'@type', '@method', '@constructor', '@field'}

    def get_tokens_unprocessed(self, text):
        for index, token, value in JavaLexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.aj_keywords:
                yield index, Keyword, value
            elif token is Name.Label and value in self.aj_inter_type:
                yield index, Keyword, value[:-1]
                yield index, Operator, value[-1]
            elif token is Name.Decorator and value in self.aj_inter_type_annotation:
                yield index, Keyword, value
            else:
                yield index, token, value


class ScalaLexer(RegexLexer):
    """
    For `Scala <http://www.scala-lang.org>`_ source code.
    """

    name = 'Scala'
    aliases = ['scala']
    filenames = ['*.scala']
    mimetypes = ['text/x-scala']

    flags = re.MULTILINE | re.DOTALL

    opchar = '[!#%&*\\-\\/:?@^' + uni.combine('Sm', 'So') + ']'
    letter = '[_\\$' + uni.combine('Ll', 'Lu', 'Lo', 'Nl', 'Lt') + ']'
    upperLetter = '[' + uni.combine('Lu', 'Lt') + ']'
    letterOrDigit = '(?:%s|[0-9])' % letter
    letterOrDigitNoDollarSign = '(?:%s|[0-9])' % letter.replace('\\$', '')
    alphaId = '%s+' % letter
    simpleInterpolatedVariable  = '%s%s*' % (letter, letterOrDigitNoDollarSign)
    idrest = '%s%s*(?:(?<=_)%s+)?' % (letter, letterOrDigit, opchar)
    idUpper = '%s%s*(?:(?<=_)%s+)?' % (upperLetter, letterOrDigit, opchar)
    plainid = '(?:%s|%s+)' % (idrest, opchar)
    backQuotedId = r'`[^`]+`'
    anyId = r'(?:%s|%s)' % (plainid, backQuotedId)
    notStartOfComment = r'(?!//|/\*)'
    endOfLineMaybeWithComment = r'(?=\s*(//|$))'

    keywords = (
        'new', 'return', 'throw', 'classOf', 'isInstanceOf', 'asInstanceOf',
        'else', 'if', 'then', 'do', 'while', 'for', 'yield', 'match', 'case',
        'catch', 'finally', 'try'
    )

    operators = (
        '<%', '=:=', '<:<', '<%<', '>:', '<:', '=', '==', '!=', '<=', '>=',
        '<>', '<', '>', '<-', '←', '->', '→', '=>', '⇒', '?', '@', '|', '-',
        '+', '*', '%', '~'
    )

    storage_modifiers = (
        'private', 'protected', 'synchronized', '@volatile', 'abstract',
        'final', 'lazy', 'sealed', 'implicit', 'override', '@transient',
        '@native'
    )

    tokens = {
        'root': [
            include('whitespace'),
            include('comments'),
            include('script-header'),
            include('imports'),
            include('exports'),
            include('storage-modifiers'),
            include('annotations'),
            include('using'),
            include('declarations'),
            include('inheritance'),
            include('extension'),
            include('end'),
            include('constants'),
            include('strings'),
            include('symbols'),
            include('singleton-type'),
            include('inline'),
            include('quoted'),
            include('keywords'),
            include('operators'),
            include('punctuation'),
            include('names'),
        ],

        # Includes:
        'whitespace': [
            (r'\s+', Text),
        ],
        'comments': [
            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
        ],
        'script-header': [
            (r'^#!([^\n]*)$', Comment.Hashbang),
        ],
        'imports': [
            (r'\b(import)(\s+)', bygroups(Keyword, Text), 'import-path'),
        ],
        'exports': [
            (r'\b(export)(\s+)(given)(\s+)',
                bygroups(Keyword, Text, Keyword, Text), 'export-path'),
            (r'\b(export)(\s+)', bygroups(Keyword, Text), 'export-path'),
        ],
        'storage-modifiers': [
            (words(storage_modifiers, prefix=r'\b', suffix=r'\b'), Keyword),
            # Only highlight soft modifiers if they are eventually followed by
            # the correct keyword. Note that soft modifiers can be followed by a
            # sequence of regular modifiers; [a-z\s]* skips those, and we just
            # check that the soft modifier is applied to a supported statement.
            (r'\b(transparent|opaque|infix|open|inline)\b(?=[a-z\s]*\b'
             r'(def|val|var|given|type|class|trait|object|enum)\b)', Keyword),
        ],
        'annotations': [
            (r'@%s' % idrest, Name.Decorator),
        ],
        'using': [
            # using is a soft keyword, can only be used in the first position of
            # a parameter or argument list.
            (r'(\()(\s*)(using)(\s)', bygroups(Punctuation, Text, Keyword, Text)),
        ],
        'declarations': [
            (r'\b(def)\b(\s*)%s(%s)?' % (notStartOfComment, anyId),
             bygroups(Keyword, Text, Name.Function)),
            (r'\b(trait)\b(\s*)%s(%s)?' % (notStartOfComment, anyId),
                bygroups(Keyword, Text, Name.Class)),
            (r'\b(?:(case)(\s+))?(class|object|enum)\b(\s*)%s(%s)?' %
                (notStartOfComment, anyId),
                bygroups(Keyword, Text, Keyword, Text, Name.Class)),
            (r'(?<!\.)\b(type)\b(\s*)%s(%s)?' % (notStartOfComment, anyId),
                bygroups(Keyword, Text, Name.Class)),
            (r'\b(val|var)\b', Keyword.Declaration),
            (r'\b(package)(\s+)(object)\b(\s*)%s(%s)?' %
                (notStartOfComment, anyId),
                bygroups(Keyword, Text, Keyword, Text, Name.Namespace)),
            (r'\b(package)(\s+)', bygroups(Keyword, Text), 'package'),
            (r'\b(given)\b(\s*)(%s)' % idUpper,
                bygroups(Keyword, Text, Name.Class)),
            (r'\b(given)\b(\s*)(%s)?' % anyId, 
                bygroups(Keyword, Text, Name)),
        ],
        'inheritance': [
            (r'\b(extends|with|derives)\b(\s*)'
             r'(%s|%s|(?=\([^\)]+=>)|(?=%s)|(?="))?' %
                (idUpper, backQuotedId, plainid),
                bygroups(Keyword, Text, Name.Class)),
        ],
        'extension': [
            (r'\b(extension)(\s+)(?=[\[\(])', bygroups(Keyword, Text)),
        ],
        'end': [
            # end is a soft keyword, should only be highlighted in certain cases
            (r'\b(end)(\s+)(if|while|for|match|new|extension|val|var)\b',
                bygroups(Keyword, Text, Keyword)),
            (r'\b(end)(\s+)(%s)%s' % (idUpper, endOfLineMaybeWithComment),
                bygroups(Keyword, Text, Name.Class)),
            (r'\b(end)(\s+)(%s|%s)?%s' %
                (backQuotedId, plainid, endOfLineMaybeWithComment),
                bygroups(Keyword, Text, Name.Namespace)),
        ],
        'punctuation': [
            (r'[{}()\[\];,.]', Punctuation),
            (r'(?<!:):(?!:)', Punctuation),  
        ],
        'keywords': [
            (words(keywords, prefix=r'\b', suffix=r'\b'), Keyword),
        ],
        'operators': [
            (r'(%s{2,})(\s+)' % opchar, bygroups(Operator, Text)),
            (r'/(?![/*])', Operator),
            (words(operators), Operator),
            (r'(?<!%s)(!|&&|\|\|)(?!%s)' % (opchar, opchar), Operator),
        ],
        'constants': [
            (r'\b(this|super)\b', Name.Builtin.Pseudo),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'0[xX][0-9a-fA-F_]*', Number.Hex),
            (r'([0-9][0-9_]*\.[0-9][0-9_]*|\.[0-9][0-9_]*)'
             r'([eE][+-]?[0-9][0-9_]*)?[fFdD]?', Number.Float),
            (r'[0-9]+([eE][+-]?[0-9]+)?[fFdD]', Number.Float),
            (r'[0-9]+([eE][+-]?[0-9]+)[fFdD]?', Number.Float),
            (r'[0-9]+[lL]', Number.Integer.Long),
            (r'[0-9]+', Number.Integer),
            (r'""".*?"""(?!")', String),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r"(')(\\.)(')", bygroups(String.Char, String.Escape, String.Char)),
            (r"'[^\\]'|'\\u[0-9a-fA-F]{4}'", String.Char),
        ],
        "strings": [
            (r'[fs]"""', String, 'interpolated-string-triple'),
            (r'[fs]"', String, 'interpolated-string'),
            (r'raw"(\\\\|\\"|[^"])*"', String),
        ],
        'symbols': [
            (r"('%s)(?!')" % plainid, String.Symbol),
        ],
        'singleton-type': [
            (r'(\.)(type)\b', bygroups(Punctuation, Keyword)),
        ],
        'inline': [
            # inline is a soft modifer, only highlighted if followed by if, 
            # match or parameters.
            (r'\b(inline)(?=\s+(%s|%s)\s*:)' % (plainid, backQuotedId),
                Keyword),
            (r'\b(inline)\b(?=(?:.(?!\b(?:val|def|given)\b))*\b(if|match)\b)',
                Keyword),
        ],
        'quoted': [
            # '{...} or ${...}
            (r"['$]\{(?!')", Punctuation),
            # '[...]
            (r"'\[(?!')", Punctuation),
        ],
        'names': [
            (idUpper, Name.Class),
            (anyId, Name),
        ],

        # States
        'comment': [
            (r'[^/*]+', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline),
        ],
        'import-path': [
            (r'(?<=[\n;:])', Text, '#pop'),
            include('comments'),
            (r'\b(given)\b', Keyword),
            include('qualified-name'),
            (r'\{', Punctuation, 'import-path-curly-brace'),
        ],
        'import-path-curly-brace': [
            include('whitespace'),
            include('comments'),
            (r'\b(given)\b', Keyword),
            (r'=>', Operator),
            (r'\}', Punctuation, '#pop'),
            (r',', Punctuation),
            (r'[\[\]]', Punctuation),
            include('qualified-name'),
        ],
        'export-path': [
            (r'(?<=[\n;:])', Text, '#pop'),
            include('comments'),
            include('qualified-name'),
            (r'\{', Punctuation, 'export-path-curly-brace'),
        ],
        'export-path-curly-brace': [
            include('whitespace'),
            include('comments'),
            (r'=>', Operator),
            (r'\}', Punctuation, '#pop'),
            (r',', Punctuation),
            include('qualified-name'),
        ],
        'package': [
            (r'(?<=[\n;])', Text, '#pop'),
            (r':', Punctuation, '#pop'),
            include('comments'),
            include('qualified-name'),
        ],
        'interpolated-string-triple': [
            (r'"""(?!")', String, '#pop'),
            (r'"', String),
            include('interpolated-string-common'),
        ],
        'interpolated-string': [
            (r'"', String, '#pop'),
            include('interpolated-string-common'),
        ],
        'interpolated-string-brace': [
            (r'\}', String.Interpol, '#pop'),
            (r'\{', Punctuation, 'interpolated-string-nested-brace'),
            include('root'),
        ],
        'interpolated-string-nested-brace': [
            (r'\{', Punctuation, '#push'),
            (r'\}', Punctuation, '#pop'),
            include('root'),
        ],

        # Helpers
        'qualified-name': [
            (idUpper, Name.Class),
            (r'(%s)(\.)' % anyId, bygroups(Name.Namespace, Punctuation)),
            (r'\.', Punctuation),
            (anyId, Name),
            (r'[^\S\n]+', Text),
        ],
        'interpolated-string-common': [
            (r'[^"$\\]+', String),
            (r'\$\$', String.Escape),
            (r'(\$)(%s)' % simpleInterpolatedVariable,
                bygroups(String.Interpol, Name)),
            (r'\$\{', String.Interpol, 'interpolated-string-brace'),
            (r'\\.', String),
        ],
    }


class GosuLexer(RegexLexer):
    """
    For Gosu source code.

    .. versionadded:: 1.5
    """

    name = 'Gosu'
    aliases = ['gosu']
    filenames = ['*.gs', '*.gsx', '*.gsp', '*.vark']
    mimetypes = ['text/x-gosu']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w.\[\]]*\s+)+?)'  # modifiers etc.
             r'([a-zA-Z_]\w*)'                       # method name
             r'(\s*)(\()',                           # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'@[a-zA-Z_][\w.]*', Name.Decorator),
            (r'(in|as|typeof|statictypeof|typeis|typeas|if|else|foreach|for|'
             r'index|while|do|continue|break|return|try|catch|finally|this|'
             r'throw|new|switch|case|default|eval|super|outer|classpath|'
             r'using)\b', Keyword),
            (r'(var|delegate|construct|function|private|internal|protected|'
             r'public|abstract|override|final|static|extends|transient|'
             r'implements|represents|readonly)\b', Keyword.Declaration),
            (r'(property\s+)(get|set)?', Keyword.Declaration),
            (r'(boolean|byte|char|double|float|int|long|short|void|block)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(true|false|null|NaN|Infinity)\b', Keyword.Constant),
            (r'(class|interface|enhancement|enum)(\s+)([a-zA-Z_]\w*)',
             bygroups(Keyword.Declaration, Text, Name.Class)),
            (r'(uses)(\s+)([\w.]+\*?)',
             bygroups(Keyword.Namespace, Text, Name.Namespace)),
            (r'"', String, 'string'),
            (r'(\??[.#])([a-zA-Z_]\w*)',
             bygroups(Operator, Name.Attribute)),
            (r'(:)([a-zA-Z_]\w*)',
             bygroups(Operator, Name.Attribute)),
            (r'[a-zA-Z_$]\w*', Name),
            (r'and|or|not|[\\~^*!%&\[\](){}<>|+=:;,./?-]', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'[0-9]+', Number.Integer),
            (r'\n', Text)
        ],
        'templateText': [
            (r'(\\<)|(\\\$)', String),
            (r'(<%@\s+)(extends|params)',
             bygroups(Operator, Name.Decorator), 'stringTemplate'),
            (r'<%!--.*?--%>', Comment.Multiline),
            (r'(<%)|(<%=)', Operator, 'stringTemplate'),
            (r'\$\{', Operator, 'stringTemplateShorthand'),
            (r'.', String)
        ],
        'string': [
            (r'"', String, '#pop'),
            include('templateText')
        ],
        'stringTemplate': [
            (r'"', String, 'string'),
            (r'%>', Operator, '#pop'),
            include('root')
        ],
        'stringTemplateShorthand': [
            (r'"', String, 'string'),
            (r'\{', Operator, 'stringTemplateShorthand'),
            (r'\}', Operator, '#pop'),
            include('root')
        ],
    }


class GosuTemplateLexer(Lexer):
    """
    For Gosu templates.

    .. versionadded:: 1.5
    """

    name = 'Gosu Template'
    aliases = ['gst']
    filenames = ['*.gst']
    mimetypes = ['text/x-gosu-template']

    def get_tokens_unprocessed(self, text):
        lexer = GosuLexer()
        stack = ['templateText']
        yield from lexer.get_tokens_unprocessed(text, stack)


class GroovyLexer(RegexLexer):
    """
    For `Groovy <http://groovy.codehaus.org/>`_ source code.

    .. versionadded:: 1.5
    """

    name = 'Groovy'
    aliases = ['groovy']
    filenames = ['*.groovy','*.gradle']
    mimetypes = ['text/x-groovy']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # Groovy allows a file to start with a shebang
            (r'#!(.*?)$', Comment.Preproc, 'base'),
            default('base'),
        ],
        'base': [
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            # keywords: go before method names to avoid lexing "throw new XYZ"
            # as a method signature
            (r'(assert|break|case|catch|continue|default|do|else|finally|for|'
             r'if|goto|instanceof|new|return|switch|this|throw|try|while|in|as)\b',
             Keyword),
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w.\[\]]*\s+)+?)'  # return arguments
             r'('
             r'[a-zA-Z_]\w*'                        # method name
             r'|"(?:\\\\|\\[^\\]|[^"\\])*"'         # or double-quoted method name
             r"|'(?:\\\\|\\[^\\]|[^'\\])*'"         # or single-quoted method name
             r')'
             r'(\s*)(\()',                          # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'@[a-zA-Z_][\w.]*', Name.Decorator),
            (r'(abstract|const|enum|extends|final|implements|native|private|'
             r'protected|public|static|strictfp|super|synchronized|throws|'
             r'transient|volatile)\b', Keyword.Declaration),
            (r'(def|boolean|byte|char|double|float|int|long|short|void)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(class|interface)(\s+)', bygroups(Keyword.Declaration, Text),
             'class'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'""".*?"""', String.Double),
            (r"'''.*?'''", String.Single),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'\$/((?!/\$).)*/\$', String),
            (r'/(\\\\|\\[^\\]|[^/\\])*/', String),
            (r"'\\.'|'[^\\]'|'\\u[0-9a-fA-F]{4}'", String.Char),
            (r'(\.)([a-zA-Z_]\w*)', bygroups(Operator, Name.Attribute)),
            (r'[a-zA-Z_]\w*:', Name.Label),
            (r'[a-zA-Z_$]\w*', Name),
            (r'[~^*!%&\[\](){}<>|+=:;,./?-]', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+L?', Number.Integer),
            (r'\n', Text)
        ],
        'class': [
            (r'[a-zA-Z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
    }

    def analyse_text(text):
        return shebang_matches(text, r'groovy')


class IokeLexer(RegexLexer):
    """
    For `Ioke <http://ioke.org/>`_ (a strongly typed, dynamic,
    prototype based programming language) source.

    .. versionadded:: 1.4
    """
    name = 'Ioke'
    filenames = ['*.ik']
    aliases = ['ioke', 'ik']
    mimetypes = ['text/x-iokesrc']
    tokens = {
        'interpolatableText': [
            (r'(\\b|\\e|\\t|\\n|\\f|\\r|\\"|\\\\|\\#|\\\Z|\\u[0-9a-fA-F]{1,4}'
             r'|\\[0-3]?[0-7]?[0-7])', String.Escape),
            (r'#\{', Punctuation, 'textInterpolationRoot')
        ],

        'text': [
            (r'(?<!\\)"', String, '#pop'),
            include('interpolatableText'),
            (r'[^"]', String)
        ],

        'documentation': [
            (r'(?<!\\)"', String.Doc, '#pop'),
            include('interpolatableText'),
            (r'[^"]', String.Doc)
        ],

        'textInterpolationRoot': [
            (r'\}', Punctuation, '#pop'),
            include('root')
        ],

        'slashRegexp': [
            (r'(?<!\\)/[im-psux]*', String.Regex, '#pop'),
            include('interpolatableText'),
            (r'\\/', String.Regex),
            (r'[^/]', String.Regex)
        ],

        'squareRegexp': [
            (r'(?<!\\)][im-psux]*', String.Regex, '#pop'),
            include('interpolatableText'),
            (r'\\]', String.Regex),
            (r'[^\]]', String.Regex)
        ],

        'squareText': [
            (r'(?<!\\)]', String, '#pop'),
            include('interpolatableText'),
            (r'[^\]]', String)
        ],

        'root': [
            (r'\n', Text),
            (r'\s+', Text),

            # Comments
            (r';(.*?)\n', Comment),
            (r'\A#!(.*?)\n', Comment),

            # Regexps
            (r'#/', String.Regex, 'slashRegexp'),
            (r'#r\[', String.Regex, 'squareRegexp'),

            # Symbols
            (r':[\w!:?]+', String.Symbol),
            (r'[\w!:?]+:(?![\w!?])', String.Other),
            (r':"(\\\\|\\[^\\]|[^"\\])*"', String.Symbol),

            # Documentation
            (r'((?<=fn\()|(?<=fnx\()|(?<=method\()|(?<=macro\()|(?<=lecro\()'
             r'|(?<=syntax\()|(?<=dmacro\()|(?<=dlecro\()|(?<=dlecrox\()'
             r'|(?<=dsyntax\())\s*"', String.Doc, 'documentation'),

            # Text
            (r'"', String, 'text'),
            (r'#\[', String, 'squareText'),

            # Mimic
            (r'\w[\w!:?]+(?=\s*=.*mimic\s)', Name.Entity),

            # Assignment
            (r'[a-zA-Z_][\w!:?]*(?=[\s]*[+*/-]?=[^=].*($|\.))',
             Name.Variable),

            # keywords
            (r'(break|cond|continue|do|ensure|for|for:dict|for:set|if|let|'
             r'loop|p:for|p:for:dict|p:for:set|return|unless|until|while|'
             r'with)(?![\w!:?])', Keyword.Reserved),

            # Origin
            (r'(eval|mimic|print|println)(?![\w!:?])', Keyword),

            # Base
            (r'(cell\?|cellNames|cellOwner\?|cellOwner|cells|cell|'
             r'documentation|hash|identity|mimic|removeCell\!|undefineCell\!)'
             r'(?![\w!:?])', Keyword),

            # Ground
            (r'(stackTraceAsText)(?![\w!:?])', Keyword),

            # DefaultBehaviour Literals
            (r'(dict|list|message|set)(?![\w!:?])', Keyword.Reserved),

            # DefaultBehaviour Case
            (r'(case|case:and|case:else|case:nand|case:nor|case:not|case:or|'
             r'case:otherwise|case:xor)(?![\w!:?])', Keyword.Reserved),

            # DefaultBehaviour Reflection
            (r'(asText|become\!|derive|freeze\!|frozen\?|in\?|is\?|kind\?|'
             r'mimic\!|mimics|mimics\?|prependMimic\!|removeAllMimics\!|'
             r'removeMimic\!|same\?|send|thaw\!|uniqueHexId)'
             r'(?![\w!:?])', Keyword),

            # DefaultBehaviour Aspects
            (r'(after|around|before)(?![\w!:?])', Keyword.Reserved),

            # DefaultBehaviour
            (r'(kind|cellDescriptionDict|cellSummary|genSym|inspect|notice)'
             r'(?![\w!:?])', Keyword),
            (r'(use|destructuring)', Keyword.Reserved),

            # DefaultBehavior BaseBehavior
            (r'(cell\?|cellOwner\?|cellOwner|cellNames|cells|cell|'
             r'documentation|identity|removeCell!|undefineCell)'
             r'(?![\w!:?])', Keyword),

            # DefaultBehavior Internal
            (r'(internal:compositeRegexp|internal:concatenateText|'
             r'internal:createDecimal|internal:createNumber|'
             r'internal:createRegexp|internal:createText)'
             r'(?![\w!:?])', Keyword.Reserved),

            # DefaultBehaviour Conditions
            (r'(availableRestarts|bind|error\!|findRestart|handle|'
             r'invokeRestart|rescue|restart|signal\!|warn\!)'
             r'(?![\w!:?])', Keyword.Reserved),

            # constants
            (r'(nil|false|true)(?![\w!:?])', Name.Constant),

            # names
            (r'(Arity|Base|Call|Condition|DateTime|Aspects|Pointcut|'
             r'Assignment|BaseBehavior|Boolean|Case|AndCombiner|Else|'
             r'NAndCombiner|NOrCombiner|NotCombiner|OrCombiner|XOrCombiner|'
             r'Conditions|Definitions|FlowControl|Internal|Literals|'
             r'Reflection|DefaultMacro|DefaultMethod|DefaultSyntax|Dict|'
             r'FileSystem|Ground|Handler|Hook|IO|IokeGround|Struct|'
             r'LexicalBlock|LexicalMacro|List|Message|Method|Mixins|'
             r'NativeMethod|Number|Origin|Pair|Range|Reflector|Regexp Match|'
             r'Regexp|Rescue|Restart|Runtime|Sequence|Set|Symbol|'
             r'System|Text|Tuple)(?![\w!:?])', Name.Builtin),

            # functions
            ('(generateMatchMethod|aliasMethod|\u03bb|\u028E|fnx|fn|method|'
             'dmacro|dlecro|syntax|macro|dlecrox|lecrox|lecro|syntax)'
             '(?![\\w!:?])', Name.Function),

            # Numbers
            (r'-?0[xX][0-9a-fA-F]+', Number.Hex),
            (r'-?(\d+\.?\d*|\d*\.\d+)([eE][+-]?[0-9]+)?', Number.Float),
            (r'-?\d+', Number.Integer),

            (r'#\(', Punctuation),

            # Operators
            (r'(&&>>|\|\|>>|\*\*>>|:::|::|\.\.\.|===|\*\*>|\*\*=|&&>|&&=|'
             r'\|\|>|\|\|=|\->>|\+>>|!>>|<>>>|<>>|&>>|%>>|#>>|@>>|/>>|\*>>|'
             r'\?>>|\|>>|\^>>|~>>|\$>>|=>>|<<=|>>=|<=>|<\->|=~|!~|=>|\+\+|'
             r'\-\-|<=|>=|==|!=|&&|\.\.|\+=|\-=|\*=|\/=|%=|&=|\^=|\|=|<\-|'
             r'\+>|!>|<>|&>|%>|#>|\@>|\/>|\*>|\?>|\|>|\^>|~>|\$>|<\->|\->|'
             r'<<|>>|\*\*|\?\||\?&|\|\||>|<|\*|\/|%|\+|\-|&|\^|\||=|\$|!|~|'
             r'\?|#|\u2260|\u2218|\u2208|\u2209)', Operator),
            (r'(and|nand|or|xor|nor|return|import)(?![\w!?])',
             Operator),

            # Punctuation
            (r'(\`\`|\`|\'\'|\'|\.|\,|@@|@|\[|\]|\(|\)|\{|\})', Punctuation),

            # kinds
            (r'[A-Z][\w!:?]*', Name.Class),

            # default cellnames
            (r'[a-z_][\w!:?]*', Name)
        ]
    }


class ClojureLexer(RegexLexer):
    """
    Lexer for `Clojure <http://clojure.org/>`_ source code.

    .. versionadded:: 0.11
    """
    name = 'Clojure'
    aliases = ['clojure', 'clj']
    filenames = ['*.clj']
    mimetypes = ['text/x-clojure', 'application/x-clojure']

    special_forms = (
        '.', 'def', 'do', 'fn', 'if', 'let', 'new', 'quote', 'var', 'loop'
    )

    # It's safe to consider 'ns' a declaration thing because it defines a new
    # namespace.
    declarations = (
        'def-', 'defn', 'defn-', 'defmacro', 'defmulti', 'defmethod',
        'defstruct', 'defonce', 'declare', 'definline', 'definterface',
        'defprotocol', 'defrecord', 'deftype', 'defproject', 'ns'
    )

    builtins = (
        '*', '+', '-', '->', '/', '<', '<=', '=', '==', '>', '>=', '..',
        'accessor', 'agent', 'agent-errors', 'aget', 'alength', 'all-ns',
        'alter', 'and', 'append-child', 'apply', 'array-map', 'aset',
        'aset-boolean', 'aset-byte', 'aset-char', 'aset-double', 'aset-float',
        'aset-int', 'aset-long', 'aset-short', 'assert', 'assoc', 'await',
        'await-for', 'bean', 'binding', 'bit-and', 'bit-not', 'bit-or',
        'bit-shift-left', 'bit-shift-right', 'bit-xor', 'boolean', 'branch?',
        'butlast', 'byte', 'cast', 'char', 'children', 'class',
        'clear-agent-errors', 'comment', 'commute', 'comp', 'comparator',
        'complement', 'concat', 'conj', 'cons', 'constantly', 'cond', 'if-not',
        'construct-proxy', 'contains?', 'count', 'create-ns', 'create-struct',
        'cycle', 'dec',  'deref', 'difference', 'disj', 'dissoc', 'distinct',
        'doall', 'doc', 'dorun', 'doseq', 'dosync', 'dotimes', 'doto',
        'double', 'down', 'drop', 'drop-while', 'edit', 'end?', 'ensure',
        'eval', 'every?', 'false?', 'ffirst', 'file-seq', 'filter', 'find',
        'find-doc', 'find-ns', 'find-var', 'first', 'float', 'flush', 'for',
        'fnseq', 'frest', 'gensym', 'get-proxy-class', 'get',
        'hash-map', 'hash-set', 'identical?', 'identity', 'if-let', 'import',
        'in-ns', 'inc', 'index', 'insert-child', 'insert-left', 'insert-right',
        'inspect-table', 'inspect-tree', 'instance?', 'int', 'interleave',
        'intersection', 'into', 'into-array', 'iterate', 'join', 'key', 'keys',
        'keyword', 'keyword?', 'last', 'lazy-cat', 'lazy-cons', 'left',
        'lefts', 'line-seq', 'list*', 'list', 'load', 'load-file',
        'locking', 'long', 'loop', 'macroexpand', 'macroexpand-1',
        'make-array', 'make-node', 'map', 'map-invert', 'map?', 'mapcat',
        'max', 'max-key', 'memfn', 'merge', 'merge-with', 'meta', 'min',
        'min-key', 'name', 'namespace', 'neg?', 'new', 'newline', 'next',
        'nil?', 'node', 'not', 'not-any?', 'not-every?', 'not=', 'ns-imports',
        'ns-interns', 'ns-map', 'ns-name', 'ns-publics', 'ns-refers',
        'ns-resolve', 'ns-unmap', 'nth', 'nthrest', 'or', 'parse', 'partial',
        'path', 'peek', 'pop', 'pos?', 'pr', 'pr-str', 'print', 'print-str',
        'println', 'println-str', 'prn', 'prn-str', 'project', 'proxy',
        'proxy-mappings', 'quot', 'rand', 'rand-int', 'range', 're-find',
        're-groups', 're-matcher', 're-matches', 're-pattern', 're-seq',
        'read', 'read-line', 'reduce', 'ref', 'ref-set', 'refer', 'rem',
        'remove', 'remove-method', 'remove-ns', 'rename', 'rename-keys',
        'repeat', 'replace', 'replicate', 'resolve', 'rest', 'resultset-seq',
        'reverse', 'rfirst', 'right', 'rights', 'root', 'rrest', 'rseq',
        'second', 'select', 'select-keys', 'send', 'send-off', 'seq',
        'seq-zip', 'seq?', 'set', 'short', 'slurp', 'some', 'sort',
        'sort-by', 'sorted-map', 'sorted-map-by', 'sorted-set',
        'special-symbol?', 'split-at', 'split-with', 'str', 'string?',
        'struct', 'struct-map', 'subs', 'subvec', 'symbol', 'symbol?',
        'sync', 'take', 'take-nth', 'take-while', 'test', 'time', 'to-array',
        'to-array-2d', 'tree-seq', 'true?', 'union', 'up', 'update-proxy',
        'val', 'vals', 'var-get', 'var-set', 'var?', 'vector', 'vector-zip',
        'vector?', 'when', 'when-first', 'when-let', 'when-not',
        'with-local-vars', 'with-meta', 'with-open', 'with-out-str',
        'xml-seq', 'xml-zip', 'zero?', 'zipmap', 'zipper')

    # valid names for identifiers
    # well, names can only not consist fully of numbers
    # but this should be good enough for now

    # TODO / should divide keywords/symbols into namespace/rest
    # but that's hard, so just pretend / is part of the name
    valid_name = r'(?!#)[\w!$%*+<=>?/.#|-]+'

    tokens = {
        'root': [
            # the comments - always starting with semicolon
            # and going to the end of the line
            (r';.*$', Comment.Single),

            # whitespaces - usually not relevant
            (r'[,\s]+', Text),

            # numbers
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            (r'0x-?[abcdef\d]+', Number.Hex),

            # strings, symbols and characters
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String),
            (r"'" + valid_name, String.Symbol),
            (r"\\(.|[a-z]+)", String.Char),

            # keywords
            (r'::?#?' + valid_name, String.Symbol),

            # special operators
            (r'~@|[`\'#^~&@]', Operator),

            # highlight the special forms
            (words(special_forms, suffix=' '), Keyword),

            # Technically, only the special forms are 'keywords'. The problem
            # is that only treating them as keywords means that things like
            # 'defn' and 'ns' need to be highlighted as builtins. This is ugly
            # and weird for most styles. So, as a compromise we're going to
            # highlight them as Keyword.Declarations.
            (words(declarations, suffix=' '), Keyword.Declaration),

            # highlight the builtins
            (words(builtins, suffix=' '), Name.Builtin),

            # the remaining functions
            (r'(?<=\()' + valid_name, Name.Function),

            # find the remaining variables
            (valid_name, Name.Variable),

            # Clojure accepts vector notation
            (r'(\[|\])', Punctuation),

            # Clojure accepts map notation
            (r'(\{|\})', Punctuation),

            # the famous parentheses!
            (r'(\(|\))', Punctuation),
        ],
    }


class ClojureScriptLexer(ClojureLexer):
    """
    Lexer for `ClojureScript <http://clojure.org/clojurescript>`_
    source code.

    .. versionadded:: 2.0
    """
    name = 'ClojureScript'
    aliases = ['clojurescript', 'cljs']
    filenames = ['*.cljs']
    mimetypes = ['text/x-clojurescript', 'application/x-clojurescript']


class TeaLangLexer(RegexLexer):
    """
    For `Tea <http://teatrove.org/>`_ source code. Only used within a
    TeaTemplateLexer.

    .. versionadded:: 1.5
    """

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w\.\[\]]*\s+)+?)'  # return arguments
             r'([a-zA-Z_]\w*)'                       # method name
             r'(\s*)(\()',                           # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'@[a-zA-Z_][\w\.]*', Name.Decorator),
            (r'(and|break|else|foreach|if|in|not|or|reverse)\b',
             Keyword),
            (r'(as|call|define)\b', Keyword.Declaration),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(template)(\s+)', bygroups(Keyword.Declaration, Text), 'template'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'(\.)([a-zA-Z_]\w*)', bygroups(Operator, Name.Attribute)),
            (r'[a-zA-Z_]\w*:', Name.Label),
            (r'[a-zA-Z_\$]\w*', Name),
            (r'(isa|[.]{3}|[.]{2}|[=#!<>+-/%&;,.\*\\\(\)\[\]\{\}])', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+L?', Number.Integer),
            (r'\n', Text)
        ],
        'template': [
            (r'[a-zA-Z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
    }


class CeylonLexer(RegexLexer):
    """
    For `Ceylon <http://ceylon-lang.org/>`_ source code.

    .. versionadded:: 1.6
    """

    name = 'Ceylon'
    aliases = ['ceylon']
    filenames = ['*.ceylon']
    mimetypes = ['text/x-ceylon']

    flags = re.MULTILINE | re.DOTALL

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w.\[\]]*\s+)+?)'  # return arguments
             r'([a-zA-Z_]\w*)'                      # method name
             r'(\s*)(\()',                          # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'comment'),
            (r'(shared|abstract|formal|default|actual|variable|deprecated|small|'
             r'late|literal|doc|by|see|throws|optional|license|tagged|final|native|'
             r'annotation|sealed)\b', Name.Decorator),
            (r'(break|case|catch|continue|else|finally|for|in|'
             r'if|return|switch|this|throw|try|while|is|exists|dynamic|'
             r'nonempty|then|outer|assert|let)\b', Keyword),
            (r'(abstracts|extends|satisfies|'
             r'super|given|of|out|assign)\b', Keyword.Declaration),
            (r'(function|value|void|new)\b',
             Keyword.Type),
            (r'(assembly|module|package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(class|interface|object|alias)(\s+)',
             bygroups(Keyword.Declaration, Text), 'class'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String),
            (r"'\\.'|'[^\\]'|'\\\{#[0-9a-fA-F]{4}\}'", String.Char),
            (r'(\.)([a-z_]\w*)',
             bygroups(Operator, Name.Attribute)),
            (r'[a-zA-Z_]\w*:', Name.Label),
            (r'[a-zA-Z_]\w*', Name),
            (r'[~^*!%&\[\](){}<>|+=:;,./?-]', Operator),
            (r'\d{1,3}(_\d{3})+\.\d{1,3}(_\d{3})+[kMGTPmunpf]?', Number.Float),
            (r'\d{1,3}(_\d{3})+\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?',
             Number.Float),
            (r'[0-9][0-9]*\.\d{1,3}(_\d{3})+[kMGTPmunpf]?', Number.Float),
            (r'[0-9][0-9]*\.[0-9]+([eE][+-]?[0-9]+)?[kMGTPmunpf]?',
             Number.Float),
            (r'#([0-9a-fA-F]{4})(_[0-9a-fA-F]{4})+', Number.Hex),
            (r'#[0-9a-fA-F]+', Number.Hex),
            (r'\$([01]{4})(_[01]{4})+', Number.Bin),
            (r'\$[01]+', Number.Bin),
            (r'\d{1,3}(_\d{3})+[kMGTP]?', Number.Integer),
            (r'[0-9]+[kMGTP]?', Number.Integer),
            (r'\n', Text)
        ],
        'class': [
            (r'[A-Za-z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'[a-z][\w.]*',
             Name.Namespace, '#pop')
        ],
        'comment': [
            (r'[^*/]', Comment.Multiline),
            (r'/\*', Comment.Multiline, '#push'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[*/]', Comment.Multiline)
        ],
    }


class KotlinLexer(RegexLexer):
    """
    For `Kotlin <http://kotlinlang.org/>`_
    source code.

    .. versionadded:: 1.5
    """

    name = 'Kotlin'
    aliases = ['kotlin']
    filenames = ['*.kt', '*.kts']
    mimetypes = ['text/x-kotlin']

    flags = re.MULTILINE | re.DOTALL | re.UNICODE

    kt_name = ('@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' +
               '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf',
                                 'Mn', 'Mc') + ']*')

    kt_space_name = ('@?[_' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl') + ']' +
               '[' + uni.combine('Lu', 'Ll', 'Lt', 'Lm', 'Nl', 'Nd', 'Pc', 'Cf',
                                 'Mn', 'Mc', 'Zs')
                + r'\'~!%^&*()+=|\[\]:;,.<>/\?-]*')

    kt_id = '(' + kt_name + '|`' + kt_space_name + '`)'

    modifiers = (r'actual|abstract|annotation|companion|const|crossinline|'
                r'data|enum|expect|external|final|infix|inline|inner|'
                r'internal|lateinit|noinline|open|operator|override|private|'
                r'protected|public|sealed|suspend|tailrec')

    tokens = {
        'root': [
            # Whitespaces
            (r'[^\S\n]+', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'\n', Text),
            # Comments
            (r'//.*?\n', Comment.Single),
            (r'^#!/.+?\n', Comment.Single),  # shebang for kotlin scripts
            (r'/[*].*?[*]/', Comment.Multiline),
            # Keywords
            (r'as\?', Keyword),
            (r'(as|break|by|catch|constructor|continue|do|dynamic|else|finally|'
             r'get|for|if|init|[!]*in|[!]*is|out|reified|return|set|super|this|'
             r'throw|try|typealias|typeof|vararg|when|where|while)\b', Keyword),
            (r'it\b', Name.Builtin),
            # Built-in types
            (words(('Boolean?', 'Byte?', 'Char?', 'Double?', 'Float?',
             'Int?', 'Long?', 'Short?', 'String?', 'Any?', 'Unit?')), Keyword.Type),
            (words(('Boolean', 'Byte', 'Char', 'Double', 'Float',
             'Int', 'Long', 'Short', 'String', 'Any', 'Unit'), suffix=r'\b'), Keyword.Type),
            # Constants
            (r'(true|false|null)\b', Keyword.Constant),
            # Imports
            (r'(package|import)(\s+)(\S+)', bygroups(Keyword, Text, Name.Namespace)),
            # Dot access
            (r'(\?\.)((?:[^\W\d]|\$)[\w$]*)', bygroups(Operator, Name.Attribute)),
            (r'(\.)((?:[^\W\d]|\$)[\w$]*)', bygroups(Punctuation, Name.Attribute)),
            # Annotations
            (r'@[^\W\d][\w.]*', Name.Decorator),
            # Labels
            (r'[^\W\d][\w.]+@', Name.Decorator),
            # Object expression
            (r'(object)(\s+)(:)(\s+)', bygroups(Keyword, Text, Punctuation, Text), 'class'),
            # Types
            (r'((?:(?:' + modifiers + r'|fun)\s+)*)(class|interface|object)(\s+)',
             bygroups(using(this, state='modifiers'), Keyword.Declaration, Text), 'class'),
            # Variables
            (r'(var|val)(\s+)(\()', bygroups(Keyword.Declaration, Text, Punctuation),
             'destructuring_assignment'),
            (r'((?:(?:' + modifiers + r')\s+)*)(var|val)(\s+)',
             bygroups(using(this, state='modifiers'), Keyword.Declaration, Text), 'variable'),
            # Functions
            (r'((?:(?:' + modifiers + r')\s+)*)(fun)(\s+)',
             bygroups(using(this, state='modifiers'), Keyword.Declaration, Text), 'function'),
            # Operators
            (r'::|!!|\?[:.]', Operator),
            (r'[~^*!%&\[\]<>|+=/?-]', Operator),
            # Punctuation
            (r'[{}();:.,]', Punctuation),
            # Strings
            (r'"""', String, 'multiline_string'),
            (r'"', String, 'string'),
            (r"'\\.'|'[^\\]'", String.Char),
            # Numbers
            (r"[0-9](\.[0-9]*)?([eE][+-][0-9]+)?[flFL]?|"
             r"0[xX][0-9a-fA-F]+[Ll]?", Number),
            # Identifiers
            (r'' + kt_id + r'((\?[^.])?)', Name) # additionally handle nullable types
        ],
        'class': [
            (kt_id, Name.Class, '#pop')
        ],
        'variable': [
            (kt_id, Name.Variable, '#pop')
        ],
        'destructuring_assignment': [
            (r',', Punctuation),
            (r'\s+', Text),
            (kt_id, Name.Variable),
            (r'(:)(\s+)(' + kt_id + ')', bygroups(Punctuation, Text, Name)),
            (r'<', Operator, 'generic'),
            (r'\)', Punctuation, '#pop')
        ],
        'function': [
            (r'<', Operator, 'generic'),
            (r'' + kt_id + r'(\.)' + kt_id, bygroups(Name, Punctuation, Name.Function), '#pop'),
            (kt_id, Name.Function, '#pop')
        ],
        'generic': [
            (r'(>)(\s*)', bygroups(Operator, Text), '#pop'),
            (r':', Punctuation),
            (r'(reified|out|in)\b', Keyword),
            (r',', Punctuation),
            (r'\s+', Text),
            (kt_id, Name)
        ],
        'modifiers': [
            (r'\w+', Keyword.Declaration),
            (r'\s+', Text),
            default('#pop')
        ],
        'string': [
            (r'"', String, '#pop'),
            include('string_common')
        ],
        'multiline_string': [
            (r'"""', String, '#pop'),
            (r'"', String),
            include('string_common')
        ],
        'string_common': [
            (r'\\\\', String),  # escaped backslash
            (r'\\"', String),  # escaped quote
            (r'\\', String),  # bare backslash 
            (r'\$\{', String.Interpol, 'interpolation'),
            (r'(\$)(\w+)', bygroups(String.Interpol, Name)),
            (r'[^\\"$]+', String)
        ],
        'interpolation': [
            (r'"', String),
            (r'\$\{', String.Interpol, 'interpolation'),
            (r'\{', Punctuation, 'scope'),
            (r'\}', String.Interpol, '#pop'),
            include('root')
        ],
        'scope': [
            (r'\{', Punctuation, 'scope'),
            (r'\}', Punctuation, '#pop'),
            include('root')
        ]
    }


class XtendLexer(RegexLexer):
    """
    For `Xtend <http://xtend-lang.org/>`_ source code.

    .. versionadded:: 1.6
    """

    name = 'Xtend'
    aliases = ['xtend']
    filenames = ['*.xtend']
    mimetypes = ['text/x-xtend']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w.\[\]]*\s+)+?)'  # return arguments
             r'([a-zA-Z_$][\w$]*)'                  # method name
             r'(\s*)(\()',                          # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'@[a-zA-Z_][\w.]*', Name.Decorator),
            (r'(assert|break|case|catch|continue|default|do|else|finally|for|'
             r'if|goto|instanceof|new|return|switch|this|throw|try|while|IF|'
             r'ELSE|ELSEIF|ENDIF|FOR|ENDFOR|SEPARATOR|BEFORE|AFTER)\b',
             Keyword),
            (r'(def|abstract|const|enum|extends|final|implements|native|private|'
             r'protected|public|static|strictfp|super|synchronized|throws|'
             r'transient|volatile)\b', Keyword.Declaration),
            (r'(boolean|byte|char|double|float|int|long|short|void)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(true|false|null)\b', Keyword.Constant),
            (r'(class|interface)(\s+)', bygroups(Keyword.Declaration, Text),
             'class'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r"(''')", String, 'template'),
            (r'(\u00BB)', String, 'template'),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'[a-zA-Z_]\w*:', Name.Label),
            (r'[a-zA-Z_$]\w*', Name),
            (r'[~^*!%&\[\](){}<>\|+=:;,./?-]', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+L?', Number.Integer),
            (r'\n', Text)
        ],
        'class': [
            (r'[a-zA-Z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
        'template': [
            (r"'''", String, '#pop'),
            (r'\u00AB', String, '#pop'),
            (r'.', String)
        ],
    }


class PigLexer(RegexLexer):
    """
    For `Pig Latin <https://pig.apache.org/>`_ source code.

    .. versionadded:: 2.0
    """

    name = 'Pig'
    aliases = ['pig']
    filenames = ['*.pig']
    mimetypes = ['text/x-pig']

    flags = re.MULTILINE | re.IGNORECASE

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*', Comment),
            (r'/\*[\w\W]*?\*/', Comment.Multiline),
            (r'\\\n', Text),
            (r'\\', Text),
            (r'\'(?:\\[ntbrf\\\']|\\u[0-9a-f]{4}|[^\'\\\n\r])*\'', String),
            include('keywords'),
            include('types'),
            include('builtins'),
            include('punct'),
            include('operators'),
            (r'[0-9]*\.[0-9]+(e[0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-f]+', Number.Hex),
            (r'[0-9]+L?', Number.Integer),
            (r'\n', Text),
            (r'([a-z_]\w*)(\s*)(\()',
             bygroups(Name.Function, Text, Punctuation)),
            (r'[()#:]', Text),
            (r'[^(:#\'")\s]+', Text),
            (r'\S+\s+', Text)   # TODO: make tests pass without \s+
        ],
        'keywords': [
            (r'(assert|and|any|all|arrange|as|asc|bag|by|cache|CASE|cat|cd|cp|'
             r'%declare|%default|define|dense|desc|describe|distinct|du|dump|'
             r'eval|exex|explain|filter|flatten|foreach|full|generate|group|'
             r'help|if|illustrate|import|inner|input|into|is|join|kill|left|'
             r'limit|load|ls|map|matches|mkdir|mv|not|null|onschema|or|order|'
             r'outer|output|parallel|pig|pwd|quit|register|returns|right|rm|'
             r'rmf|rollup|run|sample|set|ship|split|stderr|stdin|stdout|store|'
             r'stream|through|union|using|void)\b', Keyword)
        ],
        'builtins': [
            (r'(AVG|BinStorage|cogroup|CONCAT|copyFromLocal|copyToLocal|COUNT|'
             r'cross|DIFF|MAX|MIN|PigDump|PigStorage|SIZE|SUM|TextLoader|'
             r'TOKENIZE)\b', Name.Builtin)
        ],
        'types': [
            (r'(bytearray|BIGINTEGER|BIGDECIMAL|chararray|datetime|double|float|'
             r'int|long|tuple)\b', Keyword.Type)
        ],
        'punct': [
            (r'[;(){}\[\]]', Punctuation),
        ],
        'operators': [
            (r'[#=,./%+\-?]', Operator),
            (r'(eq|gt|lt|gte|lte|neq|matches)\b', Operator),
            (r'(==|<=|<|>=|>|!=)', Operator),
        ],
    }


class GoloLexer(RegexLexer):
    """
    For `Golo <http://golo-lang.org/>`_ source code.

    .. versionadded:: 2.0
    """

    name = 'Golo'
    filenames = ['*.golo']
    aliases = ['golo']

    tokens = {
        'root': [
            (r'[^\S\n]+', Text),

            (r'#.*$', Comment),

            (r'(\^|\.\.\.|:|\?:|->|==|!=|=|\+|\*|%|/|<=|<|>=|>|=|\.)',
                Operator),
            (r'(?<=[^-])(-)(?=[^-])', Operator),

            (r'(?<=[^`])(is|isnt|and|or|not|oftype|in|orIfNull)\b', Operator.Word),
            (r'[]{}|(),[]', Punctuation),

            (r'(module|import)(\s+)',
                bygroups(Keyword.Namespace, Text),
                'modname'),
            (r'\b([a-zA-Z_][\w$.]*)(::)',  bygroups(Name.Namespace, Punctuation)),
            (r'\b([a-zA-Z_][\w$]*(?:\.[a-zA-Z_][\w$]*)+)\b', Name.Namespace),

            (r'(let|var)(\s+)',
                bygroups(Keyword.Declaration, Text),
                'varname'),
            (r'(struct)(\s+)',
                bygroups(Keyword.Declaration, Text),
                'structname'),
            (r'(function)(\s+)',
                bygroups(Keyword.Declaration, Text),
                'funcname'),

            (r'(null|true|false)\b', Keyword.Constant),
            (r'(augment|pimp'
             r'|if|else|case|match|return'
             r'|case|when|then|otherwise'
             r'|while|for|foreach'
             r'|try|catch|finally|throw'
             r'|local'
             r'|continue|break)\b', Keyword),

            (r'(map|array|list|set|vector|tuple)(\[)',
                bygroups(Name.Builtin, Punctuation)),
            (r'(print|println|readln|raise|fun'
             r'|asInterfaceInstance)\b', Name.Builtin),
            (r'(`?[a-zA-Z_][\w$]*)(\()',
                bygroups(Name.Function, Punctuation)),

            (r'-?[\d_]*\.[\d_]*([eE][+-]?\d[\d_]*)?F?', Number.Float),
            (r'0[0-7]+j?', Number.Oct),
            (r'0[xX][a-fA-F0-9]+', Number.Hex),
            (r'-?\d[\d_]*L', Number.Integer.Long),
            (r'-?\d[\d_]*', Number.Integer),

            (r'`?[a-zA-Z_][\w$]*', Name),
            (r'@[a-zA-Z_][\w$.]*', Name.Decorator),

            (r'"""', String, combined('stringescape', 'triplestring')),
            (r'"', String, combined('stringescape', 'doublestring')),
            (r"'", String, combined('stringescape', 'singlestring')),
            (r'----((.|\n)*?)----', String.Doc)

        ],

        'funcname': [
            (r'`?[a-zA-Z_][\w$]*', Name.Function, '#pop'),
        ],
        'modname': [
            (r'[a-zA-Z_][\w$.]*\*?', Name.Namespace, '#pop')
        ],
        'structname': [
            (r'`?[\w.]+\*?', Name.Class, '#pop')
        ],
        'varname': [
            (r'`?[a-zA-Z_][\w$]*', Name.Variable, '#pop'),
        ],
        'string': [
            (r'[^\\\'"\n]+', String),
            (r'[\'"\\]', String)
        ],
        'stringescape': [
            (r'\\([\\abfnrtv"\']|\n|N\{.*?\}|u[a-fA-F0-9]{4}|'
             r'U[a-fA-F0-9]{8}|x[a-fA-F0-9]{2}|[0-7]{1,3})', String.Escape)
        ],
        'triplestring': [
            (r'"""', String, '#pop'),
            include('string'),
            (r'\n', String),
        ],
        'doublestring': [
            (r'"', String.Double, '#pop'),
            include('string'),
        ],
        'singlestring': [
            (r"'", String, '#pop'),
            include('string'),
        ],
        'operators': [
            (r'[#=,./%+\-?]', Operator),
            (r'(eq|gt|lt|gte|lte|neq|matches)\b', Operator),
            (r'(==|<=|<|>=|>|!=)', Operator),
        ],
    }


class JasminLexer(RegexLexer):
    """
    For `Jasmin <http://jasmin.sourceforge.net/>`_ assembly code.

    .. versionadded:: 2.0
    """

    name = 'Jasmin'
    aliases = ['jasmin', 'jasminxt']
    filenames = ['*.j']

    _whitespace = r' \n\t\r'
    _ws = r'(?:[%s]+)' % _whitespace
    _separator = r'%s:=' % _whitespace
    _break = r'(?=[%s]|$)' % _separator
    _name = r'[^%s]+' % _separator
    _unqualified_name = r'(?:[^%s.;\[/]+)' % _separator

    tokens = {
        'default': [
            (r'\n', Text, '#pop'),
            (r"'", String.Single, ('#pop', 'quote')),
            (r'"', String.Double, 'string'),
            (r'=', Punctuation),
            (r':', Punctuation, 'label'),
            (_ws, Text),
            (r';.*', Comment.Single),
            (r'(\$[-+])?0x-?[\da-fA-F]+%s' % _break, Number.Hex),
            (r'(\$[-+]|\+)?-?\d+%s' % _break, Number.Integer),
            (r'-?(\d+\.\d*|\.\d+)([eE][-+]?\d+)?[fFdD]?'
             r'[\x00-\x08\x0b\x0c\x0e-\x1f]*%s' % _break, Number.Float),
            (r'\$%s' % _name, Name.Variable),

            # Directives
            (r'\.annotation%s' % _break, Keyword.Reserved, 'annotation'),
            (r'(\.attribute|\.bytecode|\.debug|\.deprecated|\.enclosing|'
             r'\.interface|\.line|\.signature|\.source|\.stack|\.var|abstract|'
             r'annotation|bridge|class|default|enum|field|final|fpstrict|'
             r'interface|native|private|protected|public|signature|static|'
             r'synchronized|synthetic|transient|varargs|volatile)%s' % _break,
             Keyword.Reserved),
            (r'\.catch%s' % _break, Keyword.Reserved, 'caught-exception'),
            (r'(\.class|\.implements|\.inner|\.super|inner|invisible|'
             r'invisibleparam|outer|visible|visibleparam)%s' % _break,
             Keyword.Reserved, 'class/convert-dots'),
            (r'\.field%s' % _break, Keyword.Reserved,
             ('descriptor/convert-dots', 'field')),
            (r'(\.end|\.limit|use)%s' % _break, Keyword.Reserved,
             'no-verification'),
            (r'\.method%s' % _break, Keyword.Reserved, 'method'),
            (r'\.set%s' % _break, Keyword.Reserved, 'var'),
            (r'\.throws%s' % _break, Keyword.Reserved, 'exception'),
            (r'(from|offset|to|using)%s' % _break, Keyword.Reserved, 'label'),
            (r'is%s' % _break, Keyword.Reserved,
             ('descriptor/convert-dots', 'var')),
            (r'(locals|stack)%s' % _break, Keyword.Reserved, 'verification'),
            (r'method%s' % _break, Keyword.Reserved, 'enclosing-method'),

            # Instructions
            (words((
                'aaload', 'aastore', 'aconst_null', 'aload', 'aload_0', 'aload_1', 'aload_2',
                'aload_3', 'aload_w', 'areturn', 'arraylength', 'astore', 'astore_0', 'astore_1',
                'astore_2', 'astore_3', 'astore_w', 'athrow', 'baload', 'bastore', 'bipush',
                'breakpoint', 'caload', 'castore', 'd2f', 'd2i', 'd2l', 'dadd', 'daload', 'dastore',
                'dcmpg', 'dcmpl', 'dconst_0', 'dconst_1', 'ddiv', 'dload', 'dload_0', 'dload_1',
                'dload_2', 'dload_3', 'dload_w', 'dmul', 'dneg', 'drem', 'dreturn', 'dstore', 'dstore_0',
                'dstore_1', 'dstore_2', 'dstore_3', 'dstore_w', 'dsub', 'dup', 'dup2', 'dup2_x1',
                'dup2_x2', 'dup_x1', 'dup_x2', 'f2d', 'f2i', 'f2l', 'fadd', 'faload', 'fastore', 'fcmpg',
                'fcmpl', 'fconst_0', 'fconst_1', 'fconst_2', 'fdiv', 'fload', 'fload_0', 'fload_1',
                'fload_2', 'fload_3', 'fload_w', 'fmul', 'fneg', 'frem', 'freturn', 'fstore', 'fstore_0',
                'fstore_1', 'fstore_2', 'fstore_3', 'fstore_w', 'fsub', 'i2b', 'i2c', 'i2d', 'i2f', 'i2l',
                'i2s', 'iadd', 'iaload', 'iand', 'iastore', 'iconst_0', 'iconst_1', 'iconst_2',
                'iconst_3', 'iconst_4', 'iconst_5', 'iconst_m1', 'idiv', 'iinc', 'iinc_w', 'iload',
                'iload_0', 'iload_1', 'iload_2', 'iload_3', 'iload_w', 'imul', 'ineg', 'int2byte',
                'int2char', 'int2short', 'ior', 'irem', 'ireturn', 'ishl', 'ishr', 'istore', 'istore_0',
                'istore_1', 'istore_2', 'istore_3', 'istore_w', 'isub', 'iushr', 'ixor', 'l2d', 'l2f',
                'l2i', 'ladd', 'laload', 'land', 'lastore', 'lcmp', 'lconst_0', 'lconst_1', 'ldc2_w',
                'ldiv', 'lload', 'lload_0', 'lload_1', 'lload_2', 'lload_3', 'lload_w', 'lmul', 'lneg',
                'lookupswitch', 'lor', 'lrem', 'lreturn', 'lshl', 'lshr', 'lstore', 'lstore_0',
                'lstore_1', 'lstore_2', 'lstore_3', 'lstore_w', 'lsub', 'lushr', 'lxor',
                'monitorenter', 'monitorexit', 'nop', 'pop', 'pop2', 'ret', 'ret_w', 'return', 'saload',
                'sastore', 'sipush', 'swap'), suffix=_break), Keyword.Reserved),
            (r'(anewarray|checkcast|instanceof|ldc|ldc_w|new)%s' % _break,
             Keyword.Reserved, 'class/no-dots'),
            (r'invoke(dynamic|interface|nonvirtual|special|'
             r'static|virtual)%s' % _break, Keyword.Reserved,
             'invocation'),
            (r'(getfield|putfield)%s' % _break, Keyword.Reserved,
             ('descriptor/no-dots', 'field')),
            (r'(getstatic|putstatic)%s' % _break, Keyword.Reserved,
             ('descriptor/no-dots', 'static')),
            (words((
                'goto', 'goto_w', 'if_acmpeq', 'if_acmpne', 'if_icmpeq',
                'if_icmpge', 'if_icmpgt', 'if_icmple', 'if_icmplt', 'if_icmpne',
                'ifeq', 'ifge', 'ifgt', 'ifle', 'iflt', 'ifne', 'ifnonnull',
                'ifnull', 'jsr', 'jsr_w'), suffix=_break),
             Keyword.Reserved, 'label'),
            (r'(multianewarray|newarray)%s' % _break, Keyword.Reserved,
             'descriptor/convert-dots'),
            (r'tableswitch%s' % _break, Keyword.Reserved, 'table')
        ],
        'quote': [
            (r"'", String.Single, '#pop'),
            (r'\\u[\da-fA-F]{4}', String.Escape),
            (r"[^'\\]+", String.Single)
        ],
        'string': [
            (r'"', String.Double, '#pop'),
            (r'\\([nrtfb"\'\\]|u[\da-fA-F]{4}|[0-3]?[0-7]{1,2})',
             String.Escape),
            (r'[^"\\]+', String.Double)
        ],
        'root': [
            (r'\n+', Text),
            (r"'", String.Single, 'quote'),
            include('default'),
            (r'(%s)([ \t\r]*)(:)' % _name,
             bygroups(Name.Label, Text, Punctuation)),
            (_name, String.Other)
        ],
        'annotation': [
            (r'\n', Text, ('#pop', 'annotation-body')),
            (r'default%s' % _break, Keyword.Reserved,
             ('#pop', 'annotation-default')),
            include('default')
        ],
        'annotation-body': [
            (r'\n+', Text),
            (r'\.end%s' % _break, Keyword.Reserved, '#pop'),
            include('default'),
            (_name, String.Other, ('annotation-items', 'descriptor/no-dots'))
        ],
        'annotation-default': [
            (r'\n+', Text),
            (r'\.end%s' % _break, Keyword.Reserved, '#pop'),
            include('default'),
            default(('annotation-items', 'descriptor/no-dots'))
        ],
        'annotation-items': [
            (r"'", String.Single, 'quote'),
            include('default'),
            (_name, String.Other)
        ],
        'caught-exception': [
            (r'all%s' % _break, Keyword, '#pop'),
            include('exception')
        ],
        'class/convert-dots': [
            include('default'),
            (r'(L)((?:%s[/.])*)(%s)(;)' % (_unqualified_name, _name),
             bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
             '#pop'),
            (r'((?:%s[/.])*)(%s)' % (_unqualified_name, _name),
             bygroups(Name.Namespace, Name.Class), '#pop')
        ],
        'class/no-dots': [
            include('default'),
            (r'\[+', Punctuation, ('#pop', 'descriptor/no-dots')),
            (r'(L)((?:%s/)*)(%s)(;)' % (_unqualified_name, _name),
             bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
             '#pop'),
            (r'((?:%s/)*)(%s)' % (_unqualified_name, _name),
             bygroups(Name.Namespace, Name.Class), '#pop')
        ],
        'descriptor/convert-dots': [
            include('default'),
            (r'\[+', Punctuation),
            (r'(L)((?:%s[/.])*)(%s?)(;)' % (_unqualified_name, _name),
             bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
             '#pop'),
            (r'[^%s\[)L]+' % _separator, Keyword.Type, '#pop'),
            default('#pop')
        ],
        'descriptor/no-dots': [
            include('default'),
            (r'\[+', Punctuation),
            (r'(L)((?:%s/)*)(%s)(;)' % (_unqualified_name, _name),
             bygroups(Keyword.Type, Name.Namespace, Name.Class, Punctuation),
             '#pop'),
            (r'[^%s\[)L]+' % _separator, Keyword.Type, '#pop'),
            default('#pop')
        ],
        'descriptors/convert-dots': [
            (r'\)', Punctuation, '#pop'),
            default('descriptor/convert-dots')
        ],
        'enclosing-method': [
            (_ws, Text),
            (r'(?=[^%s]*\()' % _separator, Text, ('#pop', 'invocation')),
            default(('#pop', 'class/convert-dots'))
        ],
        'exception': [
            include('default'),
            (r'((?:%s[/.])*)(%s)' % (_unqualified_name, _name),
             bygroups(Name.Namespace, Name.Exception), '#pop')
        ],
        'field': [
            (r'static%s' % _break, Keyword.Reserved, ('#pop', 'static')),
            include('default'),
            (r'((?:%s[/.](?=[^%s]*[/.]))*)(%s[/.])?(%s)' %
             (_unqualified_name, _separator, _unqualified_name, _name),
             bygroups(Name.Namespace, Name.Class, Name.Variable.Instance),
             '#pop')
        ],
        'invocation': [
            include('default'),
            (r'((?:%s[/.](?=[^%s(]*[/.]))*)(%s[/.])?(%s)(\()' %
             (_unqualified_name, _separator, _unqualified_name, _name),
             bygroups(Name.Namespace, Name.Class, Name.Function, Punctuation),
             ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots',
              'descriptor/convert-dots'))
        ],
        'label': [
            include('default'),
            (_name, Name.Label, '#pop')
        ],
        'method': [
            include('default'),
            (r'(%s)(\()' % _name, bygroups(Name.Function, Punctuation),
             ('#pop', 'descriptor/convert-dots', 'descriptors/convert-dots',
              'descriptor/convert-dots'))
        ],
        'no-verification': [
            (r'(locals|method|stack)%s' % _break, Keyword.Reserved, '#pop'),
            include('default')
        ],
        'static': [
            include('default'),
            (r'((?:%s[/.](?=[^%s]*[/.]))*)(%s[/.])?(%s)' %
             (_unqualified_name, _separator, _unqualified_name, _name),
             bygroups(Name.Namespace, Name.Class, Name.Variable.Class), '#pop')
        ],
        'table': [
            (r'\n+', Text),
            (r'default%s' % _break, Keyword.Reserved, '#pop'),
            include('default'),
            (_name, Name.Label)
        ],
        'var': [
            include('default'),
            (_name, Name.Variable, '#pop')
        ],
        'verification': [
            include('default'),
            (r'(Double|Float|Integer|Long|Null|Top|UninitializedThis)%s' %
             _break, Keyword, '#pop'),
            (r'Object%s' % _break, Keyword, ('#pop', 'class/no-dots')),
            (r'Uninitialized%s' % _break, Keyword, ('#pop', 'label'))
        ]
    }

    def analyse_text(text):
        score = 0
        if re.search(r'^\s*\.class\s', text, re.MULTILINE):
            score += 0.5
            if re.search(r'^\s*[a-z]+_[a-z]+\b', text, re.MULTILINE):
                score += 0.3
        if re.search(r'^\s*\.(attribute|bytecode|debug|deprecated|enclosing|'
                     r'inner|interface|limit|set|signature|stack)\b', text,
                     re.MULTILINE):
            score += 0.6
        return score


class SarlLexer(RegexLexer):
    """
    For `SARL <http://www.sarl.io>`_ source code.

    .. versionadded:: 2.4
    """

    name = 'SARL'
    aliases = ['sarl']
    filenames = ['*.sarl']
    mimetypes = ['text/x-sarl']

    flags = re.MULTILINE | re.DOTALL

    tokens = {
        'root': [
            # method names
            (r'^(\s*(?:[a-zA-Z_][\w.\[\]]*\s+)+?)'  # return arguments
             r'([a-zA-Z_$][\w$]*)'                      # method name
             r'(\s*)(\()',                             # signature start
             bygroups(using(this), Name.Function, Text, Operator)),
            (r'[^\S\n]+', Text),
            (r'//.*?\n', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'@[a-zA-Z_][\w.]*', Name.Decorator),
            (r'(as|break|case|catch|default|do|else|extends|extension|finally|'
             r'fires|for|if|implements|instanceof|new|on|requires|return|super|'
             r'switch|throw|throws|try|typeof|uses|while|with)\b',
             Keyword),
            (r'(abstract|def|dispatch|final|native|override|private|protected|'
             r'public|static|strictfp|synchronized|transient|val|var|volatile)\b',
             Keyword.Declaration),
            (r'(boolean|byte|char|double|float|int|long|short|void)\b',
             Keyword.Type),
            (r'(package)(\s+)', bygroups(Keyword.Namespace, Text)),
            (r'(false|it|null|occurrence|this|true|void)\b', Keyword.Constant),
            (r'(agent|annotation|artifact|behavior|capacity|class|enum|event|'
             r'interface|skill|space)(\s+)', bygroups(Keyword.Declaration, Text),
             'class'),
            (r'(import)(\s+)', bygroups(Keyword.Namespace, Text), 'import'),
            (r'"(\\\\|\\[^\\]|[^"\\])*"', String.Double),
            (r"'(\\\\|\\[^\\]|[^'\\])*'", String.Single),
            (r'[a-zA-Z_]\w*:', Name.Label),
            (r'[a-zA-Z_$]\w*', Name),
            (r'[~^*!%&\[\](){}<>\|+=:;,./?-]', Operator),
            (r'[0-9][0-9]*\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float),
            (r'0x[0-9a-fA-F]+', Number.Hex),
            (r'[0-9]+L?', Number.Integer),
            (r'\n', Text)
        ],
        'class': [
            (r'[a-zA-Z_]\w*', Name.Class, '#pop')
        ],
        'import': [
            (r'[\w.]+\*?', Name.Namespace, '#pop')
        ],
    }
