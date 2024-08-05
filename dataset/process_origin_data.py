import json
from utils import ask_gpt_4o, ask_llama_70b,get_config 
from prompts import model_sys_prompt, model_user_prompt
from metrics.eval_bleu import calculate_bleu_scores
from metrics.eval_rouge_l import calculate_rouge_l
import pandas as pd
def get_machine_tag(origin_content,model_name):
    user_prompt = model_user_prompt.replace("<spoken language>", origin_content)
    if model_name=='gpt4o':    
        result = ask_gpt_4o(model_sys_prompt, user_prompt)
    if model_name=='llama3.1:70b':
        result=ask_llama_70b(model_sys_prompt, user_prompt)
    # result = result.replace("<formal_start>", "").replace("</formal_end>", "")
    return result

def evaluate(formal_content, machine_tag):
    metric_results = calculate_bleu_scores(formal_content, machine_tag)
    metric_results['rouge_l']=calculate_rouge_l(formal_content, machine_tag)
    return metric_results

def process_jsonl_file(file_path,model_name):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            machine_tag = get_machine_tag(data['origin_content'], model_name)
            data['machine_tag'] = machine_tag            
            evaluation = evaluate(data['formal_content'], machine_tag)            
            data.update(evaluation)    
            print('---process ok---')       
            results.append(data)
    
    return results

jsonl_file_path = 'test_data/1_test.jsonl'
config=get_config()
processed_results = process_jsonl_file(jsonl_file_path, config['model_name'])

# Specify the path to the new JSONL file where the results will be saved
output_file_path = 'test_data/processed_results.jsonl'

# Save the processed results to a new JSONL file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for result in processed_results:
        output_file.write(json.dumps(result, ensure_ascii=False) + '\n')
# Specify the path to the Excel file where the results will be saved
excel_output_file_path = 'test_data/processed_results.xlsx'

# Save the processed results to a new Excel file
df = pd.DataFrame(processed_results)
df.to_excel(excel_output_file_path, index=False, engine='openpyxl')
# Calculate the average of BLEU-1, BLEU-2, BLEU-3, BLEU-4, rouge_l
bleu1_total = bleu2_total = bleu3_total = bleu4_total = rouge_l_total = 0
count = len(processed_results)

for result in processed_results:
    bleu1_total += result.get('BLEU-1', 0)
    bleu2_total += result.get('BLEU-2', 0)
    bleu3_total += result.get('BLEU-3', 0)
    bleu4_total += result.get('BLEU-4', 0)
    rouge_l_total += result.get('rouge_l', 0)

bleu1_avg = bleu1_total / count
bleu2_avg = bleu2_total / count
bleu3_avg = bleu3_total / count
bleu4_avg = bleu4_total / count
rouge_l_avg = rouge_l_total / count

# Print the average values
print(f"Average BLEU-1: {bleu1_avg:.4f}")
print(f"Average BLEU-2: {bleu2_avg:.4f}")
print(f"Average BLEU-3: {bleu3_avg:.4f}")
print(f"Average BLEU-4: {bleu4_avg:.4f}")
print(f"Average ROUGE-L: {rouge_l_avg:.4f}")

print(f"Processed results saved to {output_file_path}")
