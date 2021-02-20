import numpy as np
import warnings
warnings.filterwarnings("ignore")
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import mrc_extractor
from mrc_extractor import MRC_EXTRACTION
import pandas as pd
from word2number import w2n


#질문 부분 수정
class MAKE_TABLES:

	def __init__(self, queries_dict, full_context, types='Agenda'):
		self.date = full_context[:10] 
		self.full_context =  full_context[22:]
		self.types=types
		self.queries_dict=queries_dict
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

		html_string = '<table class="table addel table-bordered" id="addel'+str(n_agenda)+'"><tr>'

		for item in items:
			html_string += '<td><strong>'+item+'</strong></td>'

		html_string+='</tr><tr>'

		if self.types=='Agenda':
			for i in range(1,1+n_act_items):
				for item in items:
					answer = '<td>'+self.answers_dict[loc+'_'+str(i)][item]+'</td>' 
					html_string += answer
				if i!=n_act_items:
					html_string+='</tr><tr>'
				else:     
					html_string+='</tr>'

			html_string+='<input types="button" class="float" value="Add" id="addrow'+str(n_agenda)+'"></table>'

		else:
			html_string += '<td>'
			answer=''
			for item in self.queries_dict[loc+'_1'].keys():
				answer+='&#9642; '+self.answers_dict[loc+'_1'][item] +'<br>'
			html_string += answer[:-4]

			html_string += '</td></tr><tr><td><strong>Comments</strong></td></tr><tr><td></tr></table><br></div>'

		return html_string


	# 각 Agenda table 생성용

	def make_table_final(self):
		label = ''
		if self.types=='Agenda':  
			label = 'Agenda'
			html_string = self.make_table_top()
			for i in range(1, 1+self.num_agendas):
				loc='table_main'+str(i)
				html_string += '<label><strong>'+label+' '+str(i)+'</strong></label> <div class="form-group2">'
				html_string += self.make_table_top(items=['Presenter', 'Discussion Topic', 'Conclusion'], loc=loc)
				html_string += self.make_table_mid(self.num_act_items[i], n_agenda=i, loc=loc) 
				html_string += '<table class="table table-bordered"><tr><td><strong>Additional Notes</strong></td></tr><tr><td></td></tr></table></div>' 

		elif self.types=='Idea':
			label = 'Idea '
			html_string = self.make_table_top()
			html_string +='<label><strong>Idea Discussion Summary</strong></label>'
			for i in range(1, 1+self.num_agendas):
				loc='table_main'+str(i)
				html_string += '<div class="form-group2">'
				html_string += self.make_table_top(items=[label+str(i)], loc=loc)
				html_string += self.make_table_mid(n_act_items=1, n_agenda=i, items=['Details'], loc=loc) 

		elif self.types=='Interview':
			label = 'Subject '
			html_string = self.make_table_top(items=['Topic','Interviewer', 'Interviewee','Date'])
			html_string +='<label><strong>Interview Summary</strong></label>'

			for i in range(1, 1+self.num_agendas):
				loc='table_main'+str(i)
				html_string += '<div class="form-group2">'
				html_string += self.make_table_top(items=[label+str(i)], loc=loc)
				html_string += self.make_table_mid(num_act_items=1, n_agenda=i, items=['Details'], loc=loc) 

		return html_string

	def make_java(self):
		java_string=''
		for i in range(1, 1 + self.num_agendas):
			java_string += '<script>   $(document).ready(function () {var tbody = $("#addel'+str(i)+'").children("tbody"); var table = tbody.length ? tbody : $("#addel'+str(i)+'"); $("#addrow'+str(i)+'").click(function () {table.append("<tr><td></td><td></td><td></td></tr>");})});</script>'
		return java_string            


	def get_table(self):

		result_tb=self.make_table_final()
		result_jv=self.make_java()

		with open("Output.html", "w") as text_file:
			text_file.write(result_tb)

		if self.types=='Agenda':
			with open("javascript.txt", "w") as text_file:
				text_file.write(result_jv)
		
		return result_tb, result_jv




if __name__ == "__main__":
	main()

