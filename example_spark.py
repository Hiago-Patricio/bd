import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext, functions as F, types as T
from dateutil.relativedelta import relativedelta
from datetime import datetime

def getAgeYears(date: str) -> datetime:
    date = str(date)
    d1 = datetime.strptime(date, '%Y-%m-%d')
    d2 = datetime.now()
    diff = relativedelta(d2, d1)
    return diff.years


getAge = F.udf(getAgeYears, T.StringType())

sc =SparkContext()
sc.setLogLevel("Error")

sqlContext = SQLContext(sc)

# Seleciona quem tem John no nome ou sobrenome
df = sqlContext.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:test") \
    .option("query", "SELECT * FROM public.cliente WHERE nome like '%John %' or nome like '%John' ORDER BY quantidadecompras DESC") \
    .option("user", "postgres") \
    .option("password", "123") \
    .option("driver", "org.postgresql.Driver") \
    .load()

df.show()

# Troca John por João, m por masculino e f por Feminino
df = df.withColumn("nome", F.regexp_replace("nome", "John", "João"))
df = df.withColumn("sexo", F.regexp_replace("sexo", "^M$", "Masculino"))
df = df.withColumn("sexo", F.regexp_replace("sexo", "^F$", "Feminino"))
df = df.withColumn("vip", F.regexp_replace("vip", "false", "Não"))
df = df.withColumn("vip", F.regexp_replace("vip", "true", "Sim"))


df = df.select(F.col("clienteid").alias('Id'), F.col('quantidadecompras') \
    .alias("Quantidade de compras"), F.col('endereco').alias('Endereço'), F.col('sexo') \
    .alias('Sexo'), F.col('nome').alias('Nome'), F.col('datanascimento') \
    .alias("Data de Nascimento"), F.col('vip').alias('Vip'))

df = df.select('Id', 'Quantidade de compras', 'Endereço', 'Sexo', 'Nome', getAge('Data de Nascimento').alias('Idade'), 'Vip')

df.show()

# Salva no banco
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql:test") \
    .option("dbtable", "resumo") \
    .option("user", "postgres") \
    .option("password", "123") \
    .option("driver", "org.postgresql.Driver") \
    .save()

# Salva em json
df.coalesce(1).write.format('json').save('format_json')