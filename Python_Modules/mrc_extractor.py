import numpy as np
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class MRC_EXTRACTION:

	def __init__(self, queries, full_context, max_seq_len=512, \
              trained_model1="amberoad/bert-multilingual-passage-reranking-msmarco", \
              trained_model2="ahotrod/electra_large_discriminator_squad2_512"):
		self.queries = queries
		self.full_context = full_context
		self.max_seq_len =  max_seq_len
		self.trained_model1 = trained_model1
		self.trained_model2 = trained_model2
		self.tokenizer = AutoTokenizer.from_pretrained(self.trained_model1)
		self.model = AutoModelForSequenceClassification.from_pretrained(self.trained_model1)
		self.model_name = self.trained_model2
		self.nlp = pipeline('question-answering', model=self.model_name, tokenizer=self.model_name)


	def get_sep_passages(self):
		# <br> 처리 & ' 처리된 text
		context=[ x for x in self.full_context.split('<br>') if x]
		n_text=len(context)
		n_token_query = max([len(self.tokenizer(query)['input_ids']) for query in self.queries]) + 1

		i=0
		texts=[]
		while i<= n_text-1:
			index=i+1
			while index<=n_text-1:
				if len(self.tokenizer(" ".join(context[i:index+1]))['input_ids']) > self.max_seq_len-n_token_query:
					break;
				index += 1
			texts.append(" ".join(context[i: index]))
			i=index
		return texts

	# Model 1 
	def passage_reranking(self):

		texts = self.get_sep_passages()
		ranked_texts = {}

		for query in self.queries:
			scores = []
			for text in texts: 
				inputs = self.tokenizer.encode_plus(query, text, add_special_tokens=True, return_tensors="pt")
				input_ids = inputs["input_ids"].tolist()[0]
				score = self.model(**inputs)[0][0][1]
				scores.append(score)
			ranked_texts[query] = np.array(texts)[np.array(scores).argsort()[::-1]]

		return ranked_texts

	# Model 2 
	def get_answer(self, query, context):

		QA_input = {
		'question': query,
		'context': context
		}
		res = self.nlp(QA_input, model_max_length=self.max_seq_len) # max_question_len=64
		return query, res['answer'], res['score']

	def get_topN_answers(self, max_texts=3, n_answer=1):

		texts = self.passage_reranking()
		n_texts=len(texts[list(texts.keys())[0]])

		qa_result={}
		for query in self.queries:
			res={}
			for i in range(min(n_texts, max_texts)):
				result = self.get_answer(query=query, context=texts[query][i])
				res[i] = (result[1], result[2])
			res = sorted(res.items(), key=lambda x: x[1][1], reverse=True)
			answers = [x[1][0] for x in res[:n_answer]] #candidates
			if n_answer==1:
				answers=answers[0]
			qa_result[query]=answers
		return qa_result


if __name__ == "__main__":
	main()

