import ply.lex as lex

# ---------- keywords -------------------------------------------------
commands = (
    'crop', 'convert', 'rotate', 'resize', 'flipX', 'flipY', 'bw', 'colorize',
    'contrast', 'brightness', 'negative', 'blur', 'sharpen', 'compress', 'ft', 'th'
)
flags = ('target', 'x', 'y', 'w', 'h', 'format', 'deg', 'lvl', 'help')

# ---------- token list ----------------------------------------------
tokens = (
    "START_COMMAND", "COMMAND",
    "FLAG", "NUMBER",
    "IMG_FORMAT", "IMAGE_PATH", "FOLDER_PATH",
    "EQUALS", "PIPELINE",
    "UNKNOWN_STRING",
)

# ---------- simple regex tokens -------------------------------------
t_START_COMMAND = r'imp'
t_NUMBER        = r'\d+'
t_EQUALS        = r'='
t_PIPELINE      = r'->'           # imp … -> next

t_ignore = ' \t\r\n'

# ---------- complex regex tokens ------------------------------------
def t_IMG_FORMAT(t):
    r'"(png|jpg|jpeg|gif|bmp|tiff|webp)"'
    t.value = t.value[1:-1]
    return t

def t_IMAGE_PATH(t):
    r'"(?:[a-zA-Z]:\\|/)?(?:[^"/\\]+[\\/])*[^"/\\]*\.(png|jpg|jpeg|gif|bmp|tiff|webp)"'
    t.value = t.value.strip('"')
    return t

def t_FOLDER_PATH(t):
    r'"(?:[a-zA-Z]:\\|/)?(?:[^"/\\]+[\\/])+[^"/\\]*/?"'
    t.value = t.value.strip('"')
    return t

def t_FLAG(t):
    r'--[a-zA-Z]+'                # raw text
    t.value = t.value[2:]         # drop "--"
    if t.value not in flags:
        print(f"⚠️  unknown flag '{t.value}' at position {t.lexpos}")
        t.type = "UNKNOWN_STRING" # let the parser reject it
    return t

def t_COMMAND(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == "imp":
        t.type = "START_COMMAND"
    elif t.value not in commands:
        print(f"⚠️  unknown command '{t.value}' at position {t.lexpos}")
        t.type = "UNKNOWN_STRING"
    return t

def t_UNKNOWN_STRING(t):
    r'"[^"]+"'
    t.value = t.value.strip('"')
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    return t

lexer = lex.lex()
