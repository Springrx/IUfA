import os
import faiss
import pandas as pd
import numpy as np
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os

os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

client = OpenAI(api_key='yourkey')


# 加载预训练的Sentence Transformer模型
model = SentenceTransformer('lier007/xiaobu-embedding-v2')
def get_embedding(text):
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding

def get_sentences_embeddings(sentences):
    embeddings = []
    try:
        for sentence in sentences:
            embedding = get_embedding(sentence)
            embeddings.append(embedding)
            #print(f"Embedding for '{sentence}'")
    except Exception as e:
        print(f"An error occurred: {e}")
    return embeddings

def generate_prompt(index, target):
    topK = 5
    search = get_embedding(target)
    search = np.array([search])
    D, I = index.search(search, topK)
    res=df.iloc[I[0]]
    #print(res)
    if(len(res)==0):
        return ""
    prompt = "You are an assistant who helps the Chinese elderly use voice assistants on their smartphones. Your main function is to refine the natural language commands of users to written commands, enabling the voice assistant to better understand the user's commands. \
    Here are some examples, please study the following examples and convert query into written language instructions.The requirement is to return only the modified results of the query.\n"
    example = "Example: "+ res.iloc[4,0] + " convert to " + res.iloc[4,1]+"\n"+"Example: "+ res.iloc[3,0] + " convert to " + res.iloc[3,1]+"\n" \
    +"Example: "+ res.iloc[2,0] + " convert to " + res.iloc[2,1]+"\n"+"Example: "+ res.iloc[1,0] + " convert to " + res.iloc[1,1]+"\n" \
    +"Example: "+ res.iloc[0,0] + " convert to " + res.iloc[0,1]+"\n"
    query = "Query: "+target
    prompt+=example
    prompt+=query
    #print(prompt)
    return prompt

def ask_gpt_4(prompt):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


# 把RAG数据库搞到faiss里去
dataset_path = 'dataset.txt'
df = pd.read_csv(dataset_path, sep="\t", header=None, names=["sentence","label"])
sentences = df['sentence'].tolist()
embeddings = get_sentences_embeddings(sentences)
sentence_embeddings=np.array(embeddings)
dimension = sentence_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(sentence_embeddings)

# 对测试集进行逐条prompt和ask，并把返回的结果逐条写进新文件
testset_path = 'testset.txt'
df1 = pd.read_csv(testset_path,header=None, names=["sample"])
samples = df1['sample'].tolist()

result_path = 'result.txt'
with open(result_path, 'w',encoding="utf-8") as res_file:
    for sample in samples:
        print(sample)
        prompt = generate_prompt(index, sample)
        answer = ask_gpt_4(prompt)
        res_file.write(answer + '\n')
res_file.close()
print("已完成")
