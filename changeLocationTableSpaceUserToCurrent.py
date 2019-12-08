import getpass

def readFile(path):
    with open(path, 'r') as f:
        content = f.read()
    return content


def writeFile(path, content):
    try:
        with open(path, 'w+') as f:
            f.write(content)
        return True
    except:
        return False


def changeUser(content):
    user = content.split('/', 3)[2]
    return content.replace(user, getpass.getuser())


filesToChange = [
    'flyway-6.0.7/sql/V5__tablespace_livraria.sql',
    'flyway-6.0.7/sql/V6__tablespace_indice.sql',
]

for file in filesToChange:
    content = readFile(file)
    content = changeUser(content)
    if writeFile(file, content):
        print('{} foi alterado com sucesso.'.format(file))
    else:
        print('{} não pode ser alterado.'.format(file))