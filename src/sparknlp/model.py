from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import shutil


MODEL_NAME = "ramonmedeiro1/bertimbau-products-reviews-pt-br"

def save_model():
    #Para carregar o modelo iremos utilizar a função `from_pretrained`:
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

    #O HuggingFace vem com uma função `save_pretrained` para modelos baseados no TensorFlow. Usaremos isso para salvar o vocabulário do modelo.
    tokenizer.save_pretrained('./{}_tokenizer/'.format(MODEL_NAME))

    #Iremos carregar o modelo usando o `TFBertForSequenceClassification` que é usado para classificação de sentenças:
    try:
      model = TFBertForSequenceClassification.from_pretrained(MODEL_NAME)
    except:
      model = TFBertForSequenceClassification.from_pretrained(MODEL_NAME, from_pt=True)

    @tf.function(
      input_signature=[
          {
              "input_ids": tf.TensorSpec((None, None), tf.int32, name="input_ids"),
              "attention_mask": tf.TensorSpec((None, None), tf.int32, name="attention_mask"),
              "token_type_ids": tf.TensorSpec((None, None), tf.int32, name="token_type_ids"),
          }
      ]
    )
    def serving_fn(input):
        return model(input)

    model.save_pretrained("./{}".format(MODEL_NAME), saved_model=True, signatures={"serving_default": serving_fn})

def copy_model(model):
    """A pasta de assets está vazia e iremos copiar o vocabulário para esta pasta. Agora o modelo estará completo:"""
    asset_path = '{}/saved_model/1/assets'.format(MODEL_NAME)

    shutil.copyfile(f"{MODEL_NAME}_tokenizer/vocab.txt", asset_path)

    # Carrega o dicionário label2id com os labels de sentimentos dos reviews:
    labels = model.config.label2id

    # Ordena o dicionário baseado no id
    labels = sorted(labels, key=labels.get)

    # Salva o dicionário com os labels de sentimentos na pasta de assets:
    with open(asset_path + '/labels.txt', 'w') as f:
        f.write('\n'.join(labels))