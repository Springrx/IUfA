import pandas as pd
import json

# 读取CSV文件
origin_df = pd.read_csv('data/origin.csv', header=None)  # 假设数据在第一列，没有标题
text2_df = pd.read_csv('data/text2.csv', header=None)    # 假设数据在第一列，没有标题

# 确保CSV文件中有足够的行
n_rows = min(len(origin_df), len(text2_df))

# 打开一个文件以写入JSONL格式的数据
with open('output.jsonl', 'w', encoding='utf-8') as file:
    for i in range(n_rows):
        # 创建一个字典，包含id和两列数据
        data = {
            "id": i + 1,
            "origin_content": origin_df.iloc[i, 0],
            "formal_content": text2_df.iloc[i, 0]
        }
        # 将字典转换为JSON字符串
        json_str = json.dumps(data, ensure_ascii=False)
        # 写入文件，并添加换行符以符合JSONL格式
        file.write(json_str + '\n')

print("JSONL文件生成完毕。")
