
from prompts import sys_prompt,baseline_prompt
from utils import ask_gpt_4o, get_real_prompt
task_desc='给我把手电筒给开开'
baseline_prompt=get_real_prompt(baseline_prompt,task_desc)
print(baseline_prompt)
response=ask_gpt_4o(sys_prompt,baseline_prompt)
print(response)