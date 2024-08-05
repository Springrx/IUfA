from openai import OpenAI
import yaml
client = OpenAI(api_key='sk-xxxxxxxxxx')
import requests

def ask_gpt_4o(sys_prompt,content):
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": sys_prompt},
      {"role": "user", "content":content}
    ],
    temperature=0,
  )
  return completion.choices[0].message.content

def ask_llama_70b(sys_prompt,content):
   # 定义URL和请求数据
  url = "http://localhost:11434/api/generate"
  data = {
      "model": "llama3.1:70b",
      "prompt": sys_prompt+content,
      "stream": False
  }
  response = requests.post(url, json=data)
  if response.done:
    print('request llama3.1:70b successfully')     
    return response.response
  else:
    print('request llama3.1:70b successfully')
    return 'something wrong while request llama3.1:70b'

def get_config():
  with open("config.yaml") as f:
      cfg = yaml.load(f, Loader=yaml.FullLoader)
  return cfg



