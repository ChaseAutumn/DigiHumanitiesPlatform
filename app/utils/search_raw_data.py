import os
import re

def search_raw_txt(key_word):
    # 定义文件路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, 'data', 'raw_texts', '原文示例.txt')

    # 读取文件内容
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 去除每行的换行符和空行
    lines = [line.strip() for line in lines if line.strip() != '']

    # 获取标题（假设标题是第一行）
    title = lines[0]

    # 查找包含关键词的行的索引
    indices = [i for i, line in enumerate(lines) if key_word in line]

    # 如果没有找到，返回空结果
    if not indices:
        return {'title': title, 'results': []}

    search_results = []

    # 编译正则表达式，忽略大小写
    pattern = re.compile(re.escape(key_word), re.IGNORECASE)

    for idx in indices:
        # 获取前后5个句子的索引范围
        start = max(1, idx - 5)  # 从1开始，避免包括标题
        end = min(len(lines), idx + 6)  # 包含当前句子，所以+6

        # 获取上下文句子
        context = lines[start:end]

        # 对当前句子和上下文进行关键词高亮处理
        highlighted_sentence = pattern.sub(
            r'<span class="highlight">\g<0></span>', lines[idx])

        highlighted_context = [pattern.sub(
            r'<span class="highlight">\g<0></span>', line) for line in context]

        # 构建结果
        result = {
            'sentence': lines[idx],
            'highlighted_sentence': highlighted_sentence,
            'context': context,
            'highlighted_context': highlighted_context
        }
        search_results.append(result)

    return {'title': title, 'results': search_results}