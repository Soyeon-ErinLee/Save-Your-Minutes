#이후에 일괄적으로 class화 해두겠습니다
import numpy as np

!pip install transformer==3.3.0
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def get_sep_passages(query, full_context, max_seq_len=512):
	# <br> 처리 & ' 처리된 text
	context=[ x for x in full_context.split('<br>') if x]
	n_text=len(context)
	n_token_query = len(tokenizer(query)['input_ids']) + 1

	i=0
	texts=[]
	while i<= n_text-1:
	  index=i+1
	  while index<=n_text-1:
	    if len(tokenizer(" ".join(context[i:index+1]))['input_ids']) > max_seq_len-n_token_query:
	      break;
	    index += 1
	  texts.append(" ".join(context[i: index]))
	  i=index
	return texts

# Model 1 
def passage_reranking(query, full_context,max_seq_len=512, model_1="amberoad/bert-multilingual-passage-reranking-msmarco"):

	tokenizer = AutoTokenizer.from_pretrained(model_1)
	model = AutoModelForSequenceClassification.from_pretrained(model_1)

	texts = get_sep_passages(query, full_context, max_seq_len)
	scores = []

	for text in texts: 
	  inputs = tokenizer.encode_plus(query, text, add_special_tokens=True, return_tensors="pt")
	  input_ids = inputs["input_ids"].tolist()[0]
	  score = model(**inputs)[0][0][1]
	  scores.append(score)

	texts = np.array(texts)[np.array(scores).argsort()[::-1]]

	return texts


# arg 형태 및 에러 관련 수정사항 추가할 것
# Model 2 
def get_answer(query, context, model_2="ahotrod/electra_large_discriminator_squad2_512"):

	model_name = model_2
                #deepset/electra-base-squad2 
                #twmkn9/distilbert-base-uncased-squad2
	nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)
	QA_input = {
    'question': query,
    'context': context
	}
	res = nlp(QA_input, max_seq_len=512) # max_question_len=64
	return query, res['answer'], res['score']


def get_topN_answers(query, texts, n_text=3, n_answer=1):

	texts = passage_reranking(query, full_context, max_seq_len=512)
	res={}
	
	for i in range(n_texts):
	  result = get_answer(query, texts[i])
	  res[i] = (result[1], result[2])
	res = sorted(res.items(), key=lambda x: x[1][1], reverse=True)
	answers = [x[1][0] for x in res[:n]] #candidates
	if n==1:
		answers=answers[0]

	return answers





