from lexer import lexer


def tokenize(s):
    lexer.input(s)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


print('Example 1:')
tokenize('imp --help')

print('Example 2:')
tokenize('imp crop --img="path/to/image.jpg" --x=100 --y=100 --w=200 --h=200')

print('Example 3:')
tokenize('imp compress --img="./path/to/folder/"')

print('Example 4:')
tokenize('imp convert --img="path/to/image.jpg" --format="png"')

print('Example 5:')
tokenize('imp blur --img="C:/path/to/image.webp" --lvl=50 && imp th --img="./path/to/image.png" --lvl=20')

print('Example 6:')
tokenize(
    'imp --img="path/to/image.png" -> resize --w=200 --h=200 -> crop --x=50 --y=50 --w=100 --h=100 -> convert --format="jpg"')

print('Example 7:')
tokenize('imp convert --img="path/to/image.tiff" --format="jpfg"')

print('Example 8:')
tokenize('imp convert --img="path/to/image.tiff" --formt="jpg"')

print('Example 9:')
tokenize('imp --img="path/to/image.png" | bw | blur --lvl=50')
