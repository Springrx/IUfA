from rouge import Rouge
import jieba
# candidate = 'i am a student from xx school'  # 预测摘要
# reference = 'i am a student from school on china' #真实摘要
# why return rouge-l['r']? ref: https://blog.csdn.net/u013521274/article/details/89460322
def calculate_rouge_l(candidate, reference):
    candidate_tokens = " ".join(jieba.lcut(candidate))
    reference_tokens = " ".join(jieba.lcut(reference))
    candidate=[candidate_tokens]
    reference=[reference_tokens]
    rouge = Rouge()
    rouge_score = rouge.get_scores(hyps=candidate, refs=reference)
    return rouge_score[0]["rouge-l"]['r']