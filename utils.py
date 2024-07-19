from openai import OpenAI
import csv
client = OpenAI(api_key='your key')
def ask_gpt_4o(sys_prompt,content):
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": sys_prompt},
      {"role": "user", "content":content}
    ],
    temperature=0,
    response_format={ "type": "json_object" }
  )
  return completion.choices[0].message.content

def get_real_prompt(prompt,task_desc):
  real_prompt=prompt.replace('<user_command>',task_desc)
  return real_prompt
def get_real_response(response):
  return response.replace("<task>", "").replace("<t_end>", "")

def get_task_desc_from_csv(file_path):
  task_desc=[]
  with open(file_path, 'r',encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
      task_desc.append( row[0])
  return task_desc

def write_to_csv(file_path, string_array):
  data = [[string] for string in string_array]
  with open(file_path, 'w',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)