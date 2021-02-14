import numpy as np
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import mrc_extractor
from mrc_extractor import MRC_EXTRACTION
import pandas as pd

query_dict_ex={'table_top': {
	'Participants':'who are the attendees at the meeting?',
	'Topic':'what was the main topic of the meeting?'
	},
 'table_mid_1': {
	'Discussion Topic':'what was the topic of the first agenda?',
	'Presenter':'who was the presenter of the first agenda?',
	'Conclusion':'what was the conclusion of the first agenda?'
	},
 'table_mid_2': {
	'Action Items':'what was the first ?',
	'Person Responsible':'who was the presenter of the first agenda?',
	'Deadline':'what was the deadline of the first action item?'
	},
'num_tables':{
	'num_agendas':'How many agendas?',
	'num_act_items':'How many action items for the first agenda?'
	}
}


## number  처리할것 
#질문 부분 수정
class make_tables:

	def __init__(self, queries_dict, full_context, type='PPC'):
		self.date = full_context[:10] 
		self.full_context =  full_context[10:]
		# if type=='PPC':
		# 	self.num_act_items, self.num_agendas = list(MRC_EXTRACTION.get_topN_answers( \
		# 		['How many action items for the first agenda?','How many agendas?'], self.full_context).values())  #모델 학습 후 query로 몇개인지 찾기

		#질문 수정할 것
		queries=[list(x.values()) for x in  list(queries_dict.values())]
		queries = [item for sublist in queries for item in sublist]

		mrc = MRC_EXTRACTION(queries, self.full_context)
		
		answers_list=mrc.get_topN_answers()

		temp_df = pd.DataFrame(queries_dict)
		self.answers_dict=temp_df.replace(answers_list).to_dict()
		self.answers_dict['Date']=self.date
		self.num_agendas=self.answers_dict['num_tables']['num_agendas']
		self.num_act_items=self.answers_dict['num_tables']['num_act_items']


	# 회의록 공통 질문 및 agenda 내 첫번째 table용
	def make_table_top(self, items=['Topic','Participants', 'Date'], loc='table_top'):

	  html_string = '<table class="table table-bordered">'

	  for item in items:
	    temp='<tr><td><strong>'+item+'</strong></td>'
	    html_string+=temp
	    if item=='Date':
	    	answer_str = '<td>'+self.answers_dict[item]+'/td></tr>' # model 생성 후 query 내용 넣어 수정
	    else:
	    	answer_str = '<td>'+self.answers_dict[loc][item]+'/td></tr>' # model 생성 후 query 내용 넣어 수정


	    html_string+=answer_str

	  html_string+='</table>'

	  return html_string


	# agenda의 두번째 table용
	def make_table_mid_2(self, items=['Action Items','Person Responsible', 'Deadline'], loc='table_mid_2'):


	  html_string = '<table class="table addel table-bordered" id="addel"><tr>'

	  for item in items:
	    html_string += '<td><strong>'+item+'</strong></td>'

	  html_string+='<tr>'

	  for i in range(int(self.num_act_items)):
	    for item in items:
	      answer = '<td>'+self.answers_dict[loc][item]+'</td>' # 답 나오게 수정
	      html_string += answer

	  html_string+='</tr>'

	  html_string+='</table><table class="table table-bordered"> <tr><td><strong>Additional Notes</strong></td></tr><tr><td></td></tr></table>'
	  
	  return html_string


	# 각 Agenda table 생성용

	def make_table_final(self):

	  html_string = self.make_table_top()
	  print(1)
	  for i in range(int(self.num_agendas)):
	    html_string += '<label><strong>Agenda '+str(i)+'</strong></label><table class="table table-bordered">'
	    print(2)
	    html_string+= self.make_table_top(items=['Presenter', 'Discussion Topic', 'Conclusion'], loc='table_mid_1')# 이후 적절한 query로 수정
	    html_string+=self.make_table_mid_2() # 수정
	    print(3)
	  return html_string


