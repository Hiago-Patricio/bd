import csv
import sys
import datetime
import faker
import random
import psycopg2 as db


def validate_info(field_list: list):
    valid_list_field = []
    for field in field_list:
        field_info = field.split('-')
        field_name = field_info[0]
        if field_name == '':
            return False
        
        data_type = field_info[1]
        invalid_cond = [
            not(data_type in data_types_with_2_args),
            not(data_type in data_types_with_3_args),
            not(data_type in data_types_with_4_args)
        ]
        if all(invalid_cond):
            return False

        valid_sizes = [
            len(field_info) == 2,
            len(field_info) == 3,
            len(field_info) == 4
            ]
        if any(valid_sizes):
            valid_list_field.append(field_info)
        else:
            return False
    return valid_list_field


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


def execute_query(connection, query: str):
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            file_name = 'sql_insercao_dados.sql'
            write_in_file(file_name, query)
            return True
        except:
            connection.rollback()
            cursor.close()
            return False
    return False


def write_in_file(file_name: str, content: str):
	with open(file_name, 'a') as file:
		file.write(content + '\n')
		file.close()


def generate_data(field: str, connection = None):
    field_name = field.split('-')[0]
    data_type = field.split('-')[1]
    data_type_no_exist = [
        not(data_type in data_types_with_2_args),
        not(data_type in data_types_with_3_args),
        not(data_type in data_types_with_4_args)
    ]
    if all(data_type_no_exist):
        return False

    if data_type == 'ADDRESS':
        return faker.Faker().address()
    elif data_type == 'BOOLEAN':
        return bool(random.randrange(0,2))
    elif data_type == 'DATE':
        return random_date()
    elif data_type == 'FALSE':
        return False
    elif data_type == 'FK':
        table_name = field.split('-')[2]
        field_name = field.split('-')[3]
        return random_fk(connection, table_name, field_name)
    elif data_type == 'FLOAT':
        return round(random.uniform(20, 100), 2)
    elif data_type == 'INTEGER':
        return random.randrange(1, 100)
    elif data_type == 'MIDIA':
        tipoMidiaNome = field.split('-')[2]
        return random_fk_midia(connection, tipoMidiaNome)
    elif data_type == 'NAME':
        return faker.Faker().name()
    elif data_type == 'SEX':
        return random_sex()
    elif data_type == 'TEXT':
        return faker.Faker().text()
    elif data_type == 'TRUE':
        return True
    elif data_type in archives_csv:
        return random_info_csv(data_type)


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


def random_fk(connection, table_name: str, field_name: str):
    try:
        query = '''
        SELECT {} 
        FROM {} 
        ORDER BY RANDOM() 
        LIMIT 1;
        '''.format(field_name, table_name)
        cursor = connection.cursor()
        cursor.execute(query)
        info = cursor.fetchone()[0]
        cursor.close()
        return int(info)
    except:
        return None


def random_fk_midia(connection, tipoMidiaNome: str):
    try:
        query = '''
        SELECT M.midiaID 
        FROM Midia M
        JOIN TipoMidia TM
        ON M.fkTipoMidiaId = TM.tipoMidiaId
        WHERE TM.nome = '{}'
        ORDER BY RANDOM() 
        LIMIT 1;
        '''.format(tipoMidiaNome)
        cursor = connection.cursor()
        cursor.execute(query)
        info = cursor.fetchone()[0]
        cursor.close()
        return int(info)
    except:
        return None


def random_sex():
    sex = ['M', 'F']
    return sex[random.randrange(0,2)]


def random_info_csv(name_csv_file: str):
    with open('csv/' + name_csv_file + '.csv') as csv_file:
        reader = csv.reader(csv_file)
        content = next(reader)
        return content[random.randrange(0, len(content))]


def serial(field: str):
    last_to_insert = field.split('-')[2]
    return int(last_to_insert)


def run_in_sequence(field_dic_list: dict, rows_list: list, connection):
    for dict_item, rows in zip(field_dict_list_to_run_in_sequence.items(), rows_list):
        table_name, field_list = dict_item
        field_name_list = []
        serial_value_list = []
        for field in field_list:
            name = field.split('-')[0]
            field_name_list.append(name)
            if field.split('-')[1] == 'SERIAL':
                serial_value_list.append(1)

        inserted_rows = 0
        for i in range(rows):
            field_data_list = []
            index = 0
            for field in field_list:
                data_type = field.split('-')[1]
                if data_type == 'SERIAL':
                    data = serial_value_list[index]
                    serial_value_list[index] += 1
                    index += 1
                else:
                    data = generate_data(field, connection)
                field_data_list.append(data) 

            query = create_insert_query(table_name, field_name_list, field_data_list)
            if execute_query(connection, query):
                inserted_rows += 1
            else:
                print('Query falha: ', query)
        print('{} linhas inseridas na tabela {}.'.format(inserted_rows, table_name))


def run_intervaled(field_dict_list: dict, rows_list: list, connection):
    try:
        max_row_value = max(rows_list)

        serial_value_list = []
        for dict_item in field_dict_list.items():
            field_list = dict_item[1]
            for field in field_list:
                if field.split('-')[1] == 'SERIAL':
                    serial_value_list.append(1)
                    

        for i in range(max_row_value):
            index = 0
            for dict_item, rows in zip(field_dict_list.items(), rows_list):
                table_name, field_list = dict_item
                field_name_list = []
                field_data_list = []
                for field in field_list:
                    name = field.split('-')[0]
                    field_name_list.append(name)
                    data_type = field.split('-')[1]
                    if data_type == 'SERIAL':
                        data = serial_value_list[index]
                        serial_value_list[index] += 1
                        index += 1
                    else:
                        data = generate_data(field, connection)
                    field_data_list.append(data)
                
                if rows > 0:
                    query = create_insert_query(table_name, field_name_list, field_data_list)
                    if not execute_query(connection, query):
                        print('Query falha: ', query)
            for i, j in zip(range(len(rows_list)), rows_list):
                rows_list[i] -= 1
    except:
        pass

user:str = 'postgres'
password:str = '123'
host:str = '127.0.0.1'
port:str = '5432'
database:str = 'postgres'
connection = db.connect(user=user, password=password, host=host, port=port, database=database)

'''
Input with 2 args: fieldName-DATA_TYPE
Input with 3 args: fieldName-DATA_TYPE-last_number_to_insert
Input with 4 args: fieldName-DATA_TYPE-TableName-fieldName
'''
archives_csv = [
    'Autor_nacionalidade',
    'Funcionario_funcao',
    'Genero_localizacao',
    'Genero_nome',
    'Manga_nome',
    'Midia_editora',
    'Midia_idioma',
    'Midia_nacionalidade',
    'Midia_nome',
    'Revista_empresa',
    'TipoMidia_nome'
]
data_types_with_2_args = [
    'ADDRESS',
    'BOOLEAN',
    'DATE',
    'FALSE',
    'FK',
    'FLOAT',
    'INTEGER',
    'NAME',
    'SEX',
    'TEXT',
    'TRUE'
    ] + archives_csv
data_types_with_3_args = ['SERIAL', 'MIDIA']
data_types_with_4_args = ['FK']


field_dict_list_to_run_in_sequence = {}
field_dict_list_to_run_intervaled = {}
table_name_list = []
rows_list_to_run_in_sequence = []
rows_list_to_run_intervaled = []

table_name = 'Genero'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'generoId-SERIAL-1',
    'nome-Genero_nome',
    'localizacao-Genero_localizacao'
]
rows_list_to_run_in_sequence.append(10)

table_name = 'TipoMidia'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'tipoMidiaId-SERIAL-1',
    'nome-TipoMidia_nome'
]
rows_list_to_run_in_sequence.append(100)


table_name = 'Midia'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'MidiaId-SERIAL-1',
    'fkGeneroId-FK-Genero-generoId',
    'fkTipoMidiaId-FK-TipoMidia-tipoMidiaId',
    'dataPublicacao-DATE',
    'editora-Midia_editora',
    'nome-Midia_nome',
    'idioma-Midia_idioma',
    'localPublicacao-Midia_nacionalidade',
    'precoMidia-FLOAT'
]
rows_list_to_run_in_sequence.append(30)

table_name = 'Livro'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'LivroId-SERIAL-1',
    'fkMidiaId-MIDIA-Livro',
    'sinopse-TEXT',
    'edicao-INTEGER',
    'paginas-INTEGER'
]
rows_list_to_run_in_sequence.append(100)

table_name = 'Manga'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'MangaId-SERIAL-1',
    'nome-Manga_nome',
    'adaptacaoAnime-BOOLEAN',
    'finalizado-BOOLEAN'
]
rows_list_to_run_in_sequence.append(5)

table_name = 'Volume'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'VolumeId-SERIAL-1',
    'fkMidiaId-MIDIA-Volume',
    'fkMangaId-FK-Manga-mangaID',
    'sinopse-TEXT',
    'numero-FLOAT',
    'quantidadeCapitulos-INTEGER'
]
rows_list_to_run_in_sequence.append(100)

table_name = 'Revista'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'RevistaId-SERIAL-1',
    'fkMidiaId-MIDIA-Revista',
    'empresa-Revista_empresa',
    'edicao-INTEGER'
]
rows_list_to_run_in_sequence.append(100)

table_name = 'Autor'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'AutorId-SERIAL-1',
    'nacionalidade-Autor_nacionalidade',
    'nome-NAME',
    'dataNascimento-DATE',
    'dataFalecimento-DATE'
]
rows_list_to_run_in_sequence.append(100)

table_name = 'AutorMidia'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'AutorMidiaId-SERIAL-1',
    'fkAutorId-FK-Autor-autorId',
    'fkMidiaId-FK-Midia-midiaId'
]
rows_list_to_run_in_sequence.append(100)

table_name = 'Funcionario'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'FuncionarioId-SERIAL-1',
    'funcao-Funcionario_funcao',
    'nome-NAME',
    'salario-FLOAT',
    'dataAdmissao-DATE'
]
rows_list_to_run_in_sequence.append(5)

table_name = 'Cliente'
table_name_list.append(table_name)
field_dict_list_to_run_in_sequence[table_name] = [
    'ClienteId-SERIAL-1',
    'endereco-ADDRESS',
    'sexo-SEX',
    'nome-NAME',
    'dataNascimento-DATE'
]
rows_list_to_run_in_sequence.append(3)

table_name = 'Compra'
table_name_list.append(table_name)
field_dict_list_to_run_intervaled[table_name] = [
    'CompraId-SERIAL-1',
    'fkCLienteId-FK-Cliente-clienteId',
    'fkFuncionarioId-FK-Funcionario-funcionarioId',
    'data-DATE'
]
rows_list_to_run_intervaled.append(600)

table_name = 'ProdutosComprados'
table_name_list.append(table_name)
field_dict_list_to_run_intervaled[table_name] = [
    'ProdutosCompradosId-SERIAL-1',
    'fkCompraId-FK-Compra-compraId',
    # 'fkMidiaId-FK-Midia-midiaId',
    'fkMidiaId-SERIAL-1',
    'quantidade-INTEGER'
]
rows_list_to_run_intervaled.append(1000)

for table_name, field_list in list(field_dict_list_to_run_in_sequence.items()) + list(field_dict_list_to_run_intervaled.items()):
    stop = False
    if validate_info(field_list) == False:
        print('Erro nos campos de', table_name)
        stop = True

if stop:
    print('Nenhum dado foi inserido.')
    sys.exit()

run_in_sequence(field_dict_list_to_run_in_sequence, rows_list_to_run_in_sequence, connection)
run_intervaled(field_dict_list_to_run_intervaled, rows_list_to_run_intervaled, connection)