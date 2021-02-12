
# 회의록 공통 질문 및 agenda 내 첫번째 table용
def make_table_with_qa1(items=['Topic','Participants', 'Date'], queries=['','','']):

  html_string = '<table class="table table-bordered">'

  for item in items:
    temp='<tr><td><strong>'+item+'</strong></td>'
    html_string+=temp

    answer = '<td>'+''+'/td></tr>' # model 생성 후 query 내용 넣어 수정
    html_string+=answer

  html_string+='</table>'

  return html_string


# agenda의 두번째 table용
def make_table_with_qa2(items=['Action Items','Person Responsible', 'Deadline'], queries=['','','']):

  num_act_items = 2 #모델 학습 후 query로 몇개인지 찾기

  html_string = '<table class="table table-bordered"><tr>'

  for item in items:
    html_string += '<td><strong>'+item+'</strong></td>'

  html_string+='<tr>'

  for i in range(num_act_items):
    for query in queries:
      answer = '<td>'+''+'</td>' # 답 나오게 수정
      html_string += answer

  html_string+='</tr>'

  html_string+='</table><table class="table table-bordered"> <tr><td><strong>Additional Notes</strong></td></tr><tr><td></td></tr></table>'
  
  return html_string


# 각 Agenda table 생성용
def make_table_with_agenda():
  num_agenda = 3 #모델 학습 후 query로 몇개의 agenda 존재하는지 찾기

  html_string = ''
  for i in range(num_agenda):
    html_string += '<label><strong>Agenda '+str(i)+'</strong></label><table class="table table-bordered">'
    html_string+= make_table_with_qa1(items=['Presenter', 'Discussion topic', 'Conclusion'])# 이후 적절한 query로 수정
    html_string+=make_table_with_qa2() # 수정
  return html_string