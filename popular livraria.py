import sys
import datetime
import faker
import random
import psycopg2 as db



'''
Input with 2 args: fieldName-DATA_TYPE
Input with 4 args: fieldName-DATA_TYPE-TableName-fieldName
'''
data_types_with_2_args = ['INTEGER', 'FLOAT', 'DATE', 'BOOLEAN', 'NAME', 'ADDRESS', 'TEXT', 'SEX', 'MIDIA']
data_types_with_4_args = ['FK']
def validate_info(field_list: list):
    valid_list_field = []
    for field in field_list:
        field_name = field[0]
        if field_name == '':
            return False, 1
        
        data_type = field[1]
        if not(data_type in data_types_with_2_args) and not(data_type in data_types_with_4_args):
            return False, 2

        if len(field) == 2 or len(field) == 4:
            valid_list_field.append(field)
        else:
            return False, 3
    return valid_list_field


def validate_date(day: int, mounth: int, year: int):
    try:
        datetime.date(year, mounth, day)
        return True
    except:
        return False


def random_date():
    day = random.randrange(1, 32)
    mounth = random.randrange(1, 13)
    year = random.randrange(1900, 2019)
    while (not (validate_date(day, mounth, year))):
        day = random.randrange(1, 32)
        mounth = random.randrange(1, 13)
        year = random.randrange(1900, 2019)
    date = '{}-{}-{}'.format(year, mounth, day)
    return date


def create_insert_query(table_name: str, field_name_list: list, field_data_list: list):
    len_valid_args = [
        len(field_name_list) == 0,
        len(field_data_list) == 0,
        len(field_name_list) != len(field_data_list)
    ]

    if any(len_valid_args):
        return None


    field_name_sql = ''
    field_data_sql = ''
    for field_name, field_data in zip(field_name_list, field_data_list):
        no_quotes = [
            type(field_data) is int,
            type(field_data) is float,
            field_data == 'NULL',
            field_data == False,
            field_data == True,
        ]
        
        field_name_sql += "{} ".format(field_name)
        if any(no_quotes):
            field_data_sql += str(field_data) + ' '
        else:
            field_data_sql += "'{}' ".format(field_data)
    field_name_sql = field_name_sql.strip().replace(' ', ',')
    field_data_sql = field_data_sql.strip().replace(' ', ',')

    query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table_name, field_name_sql, field_data_sql)
    return query


def insert_data_in_table(connection, query: str):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            return True
        except:
            connection.rollback()
            cursor.close()
            return False
    return False


midia = ['Revista', 'Livro', 'Volume']
def random_midia():
    return midia[random.randrange(0,3)]

def random_sex():
    sex = ['M', 'F']
    return sex[random.randrange(0,2)]


def random_fk(connection, table_name: str, field_name: str):
    try:
        query = "SELECT {} FROM {} ORDER BY RANDOM() LIMIT 1;".format(field_name, table_name)
        cursor = connection.cursor()
        cursor.execute(query)
        info = cursor.fetchone()[0]
        cursor.close()
        return int(info)
    except:
        return None


def generate_data(field: str, connection = None):
    field_name = field.split('-')[0]
    data_type = field.split('-')[1]
    data_type_no_exist = [
        not(data_type in data_types_with_2_args),
        not(data_type in data_types_with_4_args)
    ]
    if all(data_type_no_exist):
        print('*'*50)
        print(field)
        print('*'*50)
        return False

    if data_type == 'INTEGER':
        return random.randrange(1, 100)
    elif data_type == 'FLOAT':
        return random.uniform(1, 100)
    elif data_type == 'DATE':
        return random_date()
    elif data_type == 'BOOLEAN':
        return bool(random.randrange(0,2))
    elif data_type == 'NAME':
        return faker.Faker().name()
    elif data_type == 'ADDRESS':
        return faker.Faker().address()
    elif data_type == 'TEXT':
        return faker.Faker().text()
    elif data_type == 'SEX':
        return random_sex()
    elif data_type == 'MIDIA':
        return random_midia()
    elif data_type == 'FK':
        table_name = field.split('-')[2]
        field_name = field.split('-')[3]
        return random_fk(connection, table_name, field_name)
    

field_dict_list = {}
table_name_list = []

table_name = 'Genero'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'nome-NAME',
    'localizacao-ADDRESS'
]

table_name = 'Midia'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkGeneroId-FK-Genero-generoId',
    'tipo-MIDIA',
    'dataPublicacao-DATE',
    'editora-NAME',
    'nome-NAME',
    'idioma-NAME',
    'localPublicacao-ADDRESS',
    'precoMidia-FLOAT'
]

table_name = 'Livro'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkMidiaId-FK-Midia-midiaId',
    'sinopse-TEXT',
    'edicao-INTEGER',
    'paginas-INTEGER'
]

table_name = 'Manga'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'nome-NAME',
    'adaptacaoAnime-BOOLEAN',
    'finalizado-BOOLEAN'
]

table_name = 'Volume'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkMidiaId-FK-Midia-midiaId',
    'fkMangaId-FK-Manga-mangaId',
    'sinopse-TEXT',
    'numero-FLOAT',
    'quantidadeCapitulos-INTEGER'
]

table_name = 'Revista'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkMidiaId-FK-Midia-midiaId',
    'empresa-NAME',
    'edicao-INTEGER'
]

table_name = 'Autor'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'nacionalidade-NAME',
    'nome-NAME',
    'dataNascimento-DATE',
    'dataFalecimento-DATE'
]

table_name = 'AutorMidia'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkAutorId-FK-Autor-autorId',
    'fkMidiaId-FK-Midia-midiaId'
]

table_name = 'Funcionario'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'funcao-NAME',
    'nome-NAME',
    'salario-FLOAT',
    'dataAdmissao-DATE'
]

table_name = 'Cliente'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'quantidadeCompras-INTEGER',
    'endereco-ADDRESS',
    'sexo-SEX',
    'nome-NAME',
    'dataNascimento-DATE'
]

table_name = 'Compra'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkCLienteId-FK-Cliente-clienteId',
    'fkFuncionarioId-FK-Funcionario-funcionarioId',
    'data-DATE',
    'precoTotal-FLOAT',
    'precoFinal-FLOAT']

table_name = 'ProdutosComprados'
table_name_list.append(table_name)
field_dict_list[table_name] = [
    'fkCompraId-FK-Compra-compraId',
    'fkMidiaId-FK-Midia-midiaId',
    'quantidade-INTEGER',
    'precoUnidade-FLOAT'
]


for table_name, field_list in field_dict_list.items():
    stop = False
    if validate_info(field_list) == False:
        print('Erro nos campos de ', table_name)
        stop = True


if stop:
    sys.exit()


user:str = 'postgres'
password:str = '123'
host:str = '127.0.0.1'
port:str = '5432'
database:str = 'postgres'
connection = db.connect(user=user, password=password, host=host, port=port, database=database)
rows = 50

for table_name, field_list in field_dict_list.items():
    x = []
    field_name_list = []
    for field in field_list:
        field_name_list.append(field.split('-')[0]) 

    inserted_rows = 0
    for i in range(rows):
        field_data_list = []
        for field in field_list:
            field_data_list.append(generate_data(field, connection)) 

        query = create_insert_query(table_name, field_name_list, field_data_list)
        if insert_data_in_table(connection, query):
            inserted_rows += 1
    print('{} linhas inseridas na tabela {}.'.format(inserted_rows, table_name))