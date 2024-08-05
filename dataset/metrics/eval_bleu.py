import jieba
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
# reference_sentence='人工标注'
# hypothesis_sentence='机器生成'
def calculate_bleu_scores(reference_sentence, hypothesis_sentence):
    """
    Calculate BLEU-1, BLEU-2, BLEU-3, and BLEU-4 scores.

    :param reference: String of reference sentences
    :param hypothesis: String of hypothesis words
    :return: Dictionary with BLEU scores
    """
    reference_words = list(jieba.cut(reference_sentence))
    hypothesis_words = list(jieba.cut(hypothesis_sentence))
    reference_list = [reference_words]
    smoothing_function = SmoothingFunction().method1
    bleu_scores = {
        'BLEU-1': sentence_bleu(reference_list, hypothesis_words, weights=(1, 0, 0, 0), smoothing_function=smoothing_function),
        'BLEU-2': sentence_bleu(reference_list, hypothesis_words, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothing_function),
        'BLEU-3': sentence_bleu(reference_list, hypothesis_words, weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothing_function),
        'BLEU-4': sentence_bleu(reference_list, hypothesis_words, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothing_function)
    }
    return bleu_scores
