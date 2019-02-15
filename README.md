## Teste - SPARK - NASA Kennedy Log

HTTP requests to the NASA Kennedy Space Center WWW server

Dataset oficial: https://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html

## Requisitos:

É necessário instalar o Spark em um ambiente de sua preferência.
O teste foi criado e executado em um ambiente Linux (Mint 18).

Mais informações:
* [Install Spark on Ubuntu (PySpark)] (https://medium.com/@GalarnykMichael/install-spark-on-ubuntu-pyspark-231c45677de0)

* Caso faça o clone e queira rodar o script, é necessário baixar e extrair os seguintes datasets na pasta 'data' do projeto:
- [NASA_access_log_Jul95.gz] (ftp://ita.ee.lbl.gov/traces/NASA_access_log_Jul95.gz)
- [NASA_access_log_Aug95.gz] (ftp://ita.ee.lbl.gov/traces/NASA_access_log_Aug95.gz)

* Para rodar o script python no terminal:
```
$ ./spark-submit spark_nasa.py
```

## Análises
* Q1. Qual o objetivo do comando cache em Spark?
    - R1. O comando cache() do Spark tem como objetivo armazenar os RDDs - Resilient Distribuited Dataset em memória, aumentando o desempenho. Diferente do persist() que faz o cache em memória, no disco ou memória off-heap dependendo da estratégia de cache definida no comando.

* Q2. O mesmo código implementado em Spark é normalmente mais ráído que a implementação equivalente em MapReduce. Por quê?
    - R2. Algumas das razões pelo qual o Spark é mais rápido que o MapReduce:
    - O core do Spark é o RDD - Resilient Distribuited Dataset que nada mais é do que uma coleção distribuida de objetos mutáveis para processar os dados em diferentes nós com partições lógicas.
    - A melhor forma que o MapReduce processa os dados é no modo offline. O Spark tem vantagens distintas desde que não persista os dados no disco e, sim, em memória para leitura e gravação rápida.
    - O Spark provê cache em memória, o que é ideal para multiplas operações que necessitam acessar o mesmo dado de entrada.
    - O MapReduce inia uma JVM - Java Virtual Machine para cada tarefa enquanto o Spark tem um JVM próprio em cada nó, tornando simples a tarefa com RPC - Remote procedure Call e tornando, assim, o Spark extremamente rápido.
    - O Spark utiliza o DAG - Direct Acyclic Graph que ajuda na otimização e cálculos em um único estágio ao invés de multiplos estágios como no modelo MapReduce.

* Q3. Qual a função do SparkContext?
    - R3. SparkContext é o objeto central do Spark que tem como função coordenar diferentes aplicações e clusters, provendo acesso a funcionalidades e recursos do Spark.

* Q4. Explique com suas palavras o que é Resilient Distributed Datasets (RDD).
    - R4. RDD é a unidade fundamental de dados no Apache Spark, sendo uma coleção distribuida de objetos imutáveis nos nós e que podem realizar operações em paralelo. Uma obervação é que o Spark RDDs, apesar de imutáveis, podem gerar novos RDDs à partir dos RDDs existentes.

* Q5. GroupByKey é menos eficiente que reduceByKey em grandes dataset. Por quê?
    - R5. O reduceByKey agrupa as keys antes de realizar o processo shuffle e o groupBykey realize o processo shuffle em todos os pares de chaves para, somente após esse processo, agrupá-los.

* Q6. Explique o que o código Scala abaixo faz.
```
val textFile = sc.textFile("hdfs://...")
val counts = textFile.flatMap(line => line.split(" "))
        .map(word => (word, 1))
        .reduceByKey(_+_)
counts.saveAsTextFile("hdfs://...")
```

    - R6. Dado um input de um external storage de um sistema distribuído, os mesmos são separados (pelos espaços) e transformados em uma sequência de caracteres (método flatMap). Feito isso, com essa sequência de caracteres são criados uma nova coleção do tipo chave/valor (tupla) sendo atribuido um valor (1) para cada chave (método map). Em seguida, é realizado a somatória de ocorrências pelo Spark (método reduceByKey) e, ao final, essa coleção é armazenada em um sistema distribuído.

* Q7. Responda as seguintes questôes. Devem ser desenvolvidas em Spark utilizando a sua linguagem de preferência.

- Q7.1) Número de hosts únicos.
    - R7.1) 137978

- Q7.2) O total de erros 404.
    - R7.2) 20901

- Q7.3) Os 5 URLs que mais causaram erro 404.
    - R7.3)
```
ts8-1.westwood.ts.ucla.edu/images/Nasa-logo.gif 
nexus.mlckew.edu.au/images/nasa-logo.gif 
203.13.168.17/images/nasa-logo.gif 
203.13.168.24/images/nasa-logo.gif 
crl5.crl.com/images/nasa-logo.gif
```

* Q7.4) Quantidade de erros 404 por dia.
    - R7.4)
```
    01/Jul/1995: 316
    02/Jul/1995: 291
    03/Jul/1995: 474
    04/Jul/1995: 359
    05/Jul/1995: 497
    06/Jul/1995: 640
    07/Jul/1995: 570
    08/Jul/1995: 302
    09/Jul/1995: 348
    10/Jul/1995: 398
    11/Jul/1995: 471
    12/Jul/1995: 471
    13/Jul/1995: 532
    14/Jul/1995: 413
    15/Jul/1995: 254
    16/Jul/1995: 257
    17/Jul/1995: 406
    18/Jul/1995: 465
    19/Jul/1995: 639
    20/Jul/1995: 428
    21/Jul/1995: 334
    22/Jul/1995: 192
    23/Jul/1995: 233
    24/Jul/1995: 328
    25/Jul/1995: 461
    26/Jul/1995: 336
    27/Jul/1995: 336
    28/Jul/1995: 94
    01/Aug/1995: 243
    03/Aug/1995: 304
    04/Aug/1995: 346
    05/Aug/1995: 236
    06/Aug/1995: 373
    07/Aug/1995: 537
    08/Aug/1995: 391
    09/Aug/1995: 279
    10/Aug/1995: 315
    11/Aug/1995: 263
    12/Aug/1995: 196
    13/Aug/1995: 216
    14/Aug/1995: 287
    15/Aug/1995: 327
    16/Aug/1995: 259
    17/Aug/1995: 271
    18/Aug/1995: 256
    19/Aug/1995: 209
    20/Aug/1995: 312
    21/Aug/1995: 305
    22/Aug/1995: 288
    23/Aug/1995: 345
    24/Aug/1995: 420
    25/Aug/1995: 415
    26/Aug/1995: 366
    27/Aug/1995: 370
    28/Aug/1995: 410
    29/Aug/1995: 420
    30/Aug/1995: 571
    31/Aug/1995: 526
```

* Q7.5) O total de bytes retornados.
    - R7.5) 61.02 Gb
