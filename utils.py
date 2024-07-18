from openai import OpenAI
client = OpenAI(api_key='you own key')
def ask_gpt_4o(sys_prompt,content):
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": sys_prompt},
      {"role": "user", "content":content}
    ],
  )
  return completion.choices[0].message.content

def get_real_prompt(prompt,task_desc):
  return prompt.replace('<user_command>',task_desc)