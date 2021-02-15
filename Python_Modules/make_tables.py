import numpy as np
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import mrc_extractor
from mrc_extractor import MRC_EXTRACTION
import pandas as pd
from word2number import w2n

query_dict_ex={'table_top': {
	'Participants':'who are the attendees at the meeting?',
	'Topic':'what was the main topic of the meeting?',
    'num_agendas':'How many agendas?',
    'num_act_items_1':'How many action items for the first agenda?', # 이후 일괄 처리 --> 질문 생성 함수 만들기
    'num_act_items_2':'How many action items for the second agenda?' # 이후 일괄 처리 --> 질문 생성 함수 만들기
	},
 'table_main1': {
    'Discussion Topic':'what was the topic of the first agenda?',
	'Presenter':'who was the presenter of the first agenda?',
	'Conclusion':'what was the conclusion of the first agenda?'
 },
  'table_main1_1':{
	'Action Item':'what was the first task for the first agenda ?',
	'Person Responsible':'who was responsible for the first task  of the first agenda?',
	'Deadline':'when is the deadline of the first task of the first agenda?'
  },
    'table_main1_2':{
	'Action Item':'what was the second task for the first agenda ?',
	'Person Responsible':'who was responsible for the second task  of the first agenda?',
	'Deadline':'when is the deadline of the second task of the first agenda?'
  },
 'table_main2': {
    'Discussion Topic':'what was the topic of the second agenda?',
	'Presenter':'who was the presenter of the second agenda?',
	'Conclusion':'what was the conclusion of the second agenda?'
 },
  'table_main2_1':{
	'Action Item':'what was the first task for the second agenda?',
	'Person Responsible':'who was responsible for the first task  of the second agenda?',
	'Deadline':'when is the deadline of the first task of the second agenda?'
  },
    'table_main2_2':{
	'Action Item':'what was the second task for the second agenda ?',
	'Person Responsible':'who was responsible for the second task  of the second agenda?',
	'Deadline':'when is the deadline of the second task of the second agenda?'
  }
}


#질문 부분 수정
class make_tables:

	def __init__(self, queries_dict, full_context, type='PPC'):
		self.date = full_context[:10] 
		self.full_context =  full_context[22:]
		self.type=type
		queries=[list(x.values()) for x in  list(queries_dict.values())]
		queries = [item for sublist in queries for item in sublist]

		mrc = MRC_EXTRACTION(queries, self.full_context)
		
		answers_list=mrc.get_topN_answers()

		temp_df = pd.DataFrame(queries_dict)
		self.answers_dict=temp_df.replace(answers_list).to_dict()
		self.answers_dict['Date']=self.date
		#print(answers_list)
		try: 
			self.num_agendas=w2n.word_to_num(self.answers_dict['table_top']['num_agendas'])
			self.num_act_items={}
			for i in range(1, 1+self.num_agendas):
				try: 
					self.num_act_items[i]=w2n.word_to_num(self.answers_dict['table_top']['num_act_items_'+str(i)])
				except:
					self.num_act_items[i]=0
		except:
			self.num_agendas=0



	# 회의록 공통 질문 및 agenda 내 첫번째 table용
	def make_table_top(self, items=['Topic','Participants', 'Date'], loc='table_top'):

		html_string = '<table class="table table-bordered">'

		for item in items:
			temp='<tr><td><strong>'+item+'</strong></td>'
			html_string+=temp
			if item=='Date':
				answer_str = '<td>'+self.answers_dict[item]+'</td></tr>' 
			else:
				answer_str = '<td>'+self.answers_dict[loc][item]+'</td></tr>' 

			html_string+=answer_str

		html_string+='</table>'

		return html_string


	# agenda의 두번째 table용
	def make_table_mid(self, n_act_items=0,items=['Action Item','Person Responsible', 'Deadline'], n_agenda=1 ,loc='table_main1'):

		if n_act_items==0:
			return ''
		html_string = '<table class="table addel table-bordered" id="adde'+str(n_agenda)+'"><tr>'

		for item in items:
			html_string += '<td><strong>'+item+'</strong></td>'

		html_string+='</tr><tr>'

		for i in range(1,1+n_act_items):
			for item in items:
				answer = '<td>'+self.answers_dict[loc+'_'+str(i)][item]+'</td>' 
				html_string += answer
			if i==n_act_items:
				html_string+='</tr><tr>'
			else:     
				html_string+='</tr>'

		html_string+='<input type="button" class="float" value="Add" id="addrow'+str(n_agenda)+'"></table>'

		return html_string


	# 각 Agenda table 생성용

	def make_table_final(self):

		html_string = self.make_table_top()
		label = ''
		if type=='PPC':  
			label = 'Agenda'
		for i in range(1, 1+self.num_agendas):
			loc='table_main'+str(i)
			html_string += '<label><strong>'+label+' '+str(i)+'</strong></label>'
			html_string += self.make_table_top(items=['Presenter', 'Discussion Topic', 'Conclusion'], loc=loc)
			html_string += self.make_table_mid(self.num_act_items[i], n_agenda=i, loc=loc) 
		html_string += '<table class="table table-bordered"><tr><td><strong>Additional Notes</strong></td></tr><tr><td></td></tr></table>' 
		return html_string

	def make_java(self):
		java_string=''
		for i in range(1, 1 + self.num_agendas):
			java_string += '<script>   $(document).ready(function () {var tbody = $("#addel'+str(i)+'").children("tbody"); var table = tbody.length ? tbody : $("#addel'+str(i)+'"); $("#addrow'+str(i)+'").click(function () {table.append("<tr><td></td><td></td><td></td></tr>");})});</script>'
		return java_string            


	def get_table():
		result_tb=self.make_table_final()
		result_jv=self.make_java()
		with open("Output.txt", "w") as text_file:
			text_file.write(result_tb)
		with open("javascript.txt", "w") as text_file:
			text_file.write(result_jv)
		return result_tb, result_jv

