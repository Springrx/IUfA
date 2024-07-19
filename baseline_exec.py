
from prompts import sys_prompt,baseline_prompt
from utils import ask_gpt_4o, get_real_prompt, get_task_desc_from_csv,write_to_csv
import json
task_desc_file_path='test.csv'
task_after_format_file_path='test_after_format.csv'

task_desc=get_task_desc_from_csv(task_desc_file_path)
task_after_format=[]
def get_real_response(response):
  response=json.loads(response)
  return response['command']
for task in task_desc:
  real_prompt=get_real_prompt(baseline_prompt,task)
  response=ask_gpt_4o(sys_prompt,real_prompt)
  response=get_real_response(response)
  print('response:',response) 
  # task_after_format.append(response)
# write_to_csv(task_after_format_file_path,response)
