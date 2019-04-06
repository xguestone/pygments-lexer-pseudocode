import re

from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Error, Punctuation, Text, Comment, Operator, Keyword, Name, String, Number


class PseudocodeLexer(RegexLexer):
    '''
    A Pseudo code (es) lexer
    '''
    name = 'Pseudocode'
    aliases = ['pseudocode', 'pseudo', 'algorithm', 'algo']
    filenames = ['*.algo', '*.pseudocode']
    mimetypes = []
    flags = re.IGNORECASE

    def op_replace(lexer, match):
        op = match.group(0)
        
        S = ('<=', '>=', '<>', '<-', '^')
        R = ('≤',  '≥',  '≠',  '←',  '↑')

        if op in S:
            op = R[S.index(op)]

        yield match.start(), Operator, op

    def scomment(lexer, match):
        s = match.group(1).lower().strip()
        c = Comment

        directives = ['passage par copie', 'passage par valeur', 'passage par référence', 'passage par reference', 'passage par adresse', 've', 'vs', 've/s']

        if s in directives:
            c = Comment.Special
        
        yield match.start(), c, match.group(0)
     
    tokens = {
        'root': [
                 (r'\/\*.*\*\/', Comment),
                 (r'(\/\/|#).*\n', Comment),
                 (r'\|', Comment),
                 (r'\{(.*)\}', scomment),
                 include('strings'),
                 include('core'),
                 (r'[a-zéàùçèÉÀÙÇÈ][a-z0-9éàùçèÉÀÙÇÈ_]*', Name.Variable),
                 include('nums'),
                 (r'[\s]+', Text)
        ],
        'core':[ # Statements
                 (r'\b(inicio|fin|si|entonces|sino|fin[_ ]si|tant[ _]que|mietras|fin[ _]mientras|hacer|repetir'
                  r'repeter|type|structure|fin[ _]structure|fonction|procédure|procedure|retourner|renvoyer|'
                  r'para|fin[ _]para|hasta|déclarations?|juqsque|spécialise|specialise|comporte|super|public|D.V.|privé|protégé|'
                  r'classe'
                  r')\s*\b', Keyword),

                 # Data Types
                 (r'\b(entero?|caracter?|real?|caracteres?|booleano?|'
                  r'booleens?|tableaux?|rien)\s*\b', 
                  Keyword.Type),

                  (r'\b(verdadero|falso|nil|acción)\s*\b',
                   Name.Constant),
                  
                 # Operators
                 (r'(<=|>=|<>|<-|\^|\*|\+|-|\/|<|>|=|\\\\|mod|←|↑|≤|≥|≠|÷|×|\.\.|\[|\]|\.|no|xou|and|or)',
                  op_replace),
                  
                 (r'(\(|\)|\,|\;|:)',
                  Punctuation),
                  
                 #(r'\b(\[(VE|VS|VE/S)\])\s*\b',
                 # Keyword.Declaration),

                  # Intrinsics
                 (r'\b(sqrt|pow|cos|sen|tan|arccos|arcsen|arctan|arctan2|lectura|escritura|écrire|'
                  r'exp|ln|log|détruire|detruire'
                  r')\s*\b', Name.Builtin)
                ],

        'strings': [
                 (r'"([^"])*"', String.Double),
                 (r"'([^'])*'", String.Single),
                ],

        'nums': [
                 (r'\d+(?![.Ee])', Number.Integer),
                 (r'[+-]?\d*\.\d+([eE][-+]?\d+)?', Number.Float),
                 (r'[+-]?\d+\.\d*([eE][-+]?\d+)?', Number.Float)
                ],
        }
        
