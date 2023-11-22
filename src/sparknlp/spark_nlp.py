# -*- coding: utf-8 -*-
"""Análise de Sentimento com Spark NLP.ipynb

Spark NLP é uma biblioteca de processamento de linguagem natural de última geração que foi construída sobre o Apache Spark. """


import sparknlp
from sparknlp.annotator import *
from sparknlp.base import *
from pyspark.sql.functions import when, col, lit
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def main():
    # Para iniciar um cluster Spark com suporte a NLP, basta importar a biblioteca e iniciar a sessão executando o
    # comando abaixo. O parâmetro gpu=True indica para o Spark NLP que irá usar a GPU no processamento dos textos,
    # caso tenha alguma disponível.
    spark = sparknlp.start(gpu=True)

    print("Spark NLP version: {}".format(sparknlp.version()))
    print("Apache Spark version: {}".format(spark.version))

def create_pipeline():
    document_assembler = DocumentAssembler() \
        .setInputCol('content') \
        .setOutputCol('document')

    # A classe Tokenizer irá gerar os tokens a partir do documento de entrada
    tokenizer = Tokenizer() \
        .setInputCols(['document']) \
        .setOutputCol('token')

    # Vamos usar a função `loadSavedModel` da classe `BertForSequenceClassification`, que nos permite carregar o modelo do TensorFlow no formato SavedModel
    sequenceClassifier = BertForSequenceClassification.loadSavedModel(
        '{}/saved_model/1'.format(MODEL_NAME),
        spark
    ) \
        .setInputCols(["document", 'token']) \
        .setOutputCol("class") \
        .setMaxSentenceLength(128)

    pipeline = Pipeline(stages=[
        document_assembler,
        tokenizer,
        sequenceClassifier
    ])

    return pipeline

def inference(reviews_df, pipeline):
    result = pipeline.fit(reviews_df).transform(reviews_df)

    result = result.withColumn("result", result["class.result"].getItem(0))

    result = result.withColumn("prediction",
                               when((col('result') == lit('Negativo')) | (col('result') == lit('Muito Negativo')), 0.0)
                               .when(col('result') == lit('Neutro'), 1.0)
                               .otherwise(2.0))

    result = result.withColumn("label",
                               when((col('score') == 1) | (col('score') == 2), 0.0)
                               .when(col('score') == 3, 1.0)
                               .otherwise(2.0))

    # A classe `MulticlassClassificationEvaluator` do Apache Spark ML faz o cálculo automático da acurácia do modelo
    # utilizando os rótulos esperados (reviews do usuário) e o resultado do modelo (análise de sentimento)."""
    evaluator = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(result)
    print(f"Accuray = {accuracy}")

    return result