import os
import json
import re

def fix_json_missing_commas(content):
    # 去除所有空白字符，以便检测 '}{' 的出现
    compact_content = ''.join(content.split())
    if '}{' in compact_content:
        # 如果发现 '}{'，说明缺失逗号，需要修复
        objects = []
        current_obj = ''
        brace_counter = 0

        for c in content:
            current_obj += c
            if c == '{':
                brace_counter += 1
            elif c == '}':
                brace_counter -= 1

            if brace_counter == 0 and current_obj.strip():
                objects.append(current_obj.strip())
                current_obj = ''

        fixed_json = '[\n' + ',\n'.join(objects) + '\n]'
        return fixed_json
    else:
        # 尝试直接解析内容
        try:
            data = json.loads(content)
            print("JSON 格式正确，无需修复。")
            return content  # 无需修改
        except json.JSONDecodeError as e:
            print("JSON 解析错误：", e)
            # 如果解析失败但不存在 '}{'，可能是其他问题
            # 可以在此添加其他修复逻辑
            return content

def search_corrupt_sentence(query):
    # 检查查询关键词是否包含 [MASK]
    if '[MASK]' not in query:
        return {'error': '查询关键词必须包含 [MASK]！'}

    # 预处理查询关键词，将多个 [MASK] 视为一个
    query_processed = query.replace('[MASK]', '[MASK]').replace(' ', '')

    # 构建正则表达式，忽略空格和大小写
    pattern = re.compile(re.escape(query_processed), re.IGNORECASE)

    # 定义文件路径
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, 'data', 'json_files', '修复标注示例.json')

    # 读取 JSON 数据
    with open(data_file, 'r', encoding='utf-8') as f:
        content = f.read()
        fixed_json_str = fix_json_missing_commas(content)
        data = json.loads(fixed_json_str)

    # 查找匹配的记录
    for index, record in enumerate(data):
        corrupt_sentence_processed = record['corrupt_sentence'].replace(
            '[MASK]', '[MASK]').replace(' ', '')
        if pattern.search(corrupt_sentence_processed):
            # 高亮处理
            highlighted_sentence = pattern.sub(
                r'<span class="highlight">\g<0></span>', record['corrupt_sentence'].replace(' ', ''))
            record['highlighted_corrupt_sentence'] = highlighted_sentence

            # 获取上下文记录
            up_context = []
            down_context = []

            # 追溯上文
            up_sentence = record.get('up_sentence')
            steps = 0
            while up_sentence and steps < 10:
                found = False
                for rec in data:
                    if rec.get('sentence') == up_sentence:
                        up_context.append(rec['sentence'])
                        up_sentence = rec.get('up_sentence')
                        found = True
                        break
                if not found:
                    break
                steps += 1

            # 追溯下文
            down_sentence = record.get('down_sentence')
            steps = 0
            while down_sentence and steps < 10:
                found = False
                for rec in data:
                    if rec.get('sentence') == down_sentence:
                        down_context.append(rec['sentence'])
                        down_sentence = rec.get('down_sentence')
                        found = True
                        break
                if not found:
                    break
                steps += 1

            # 返回结果
            return {
                'record': record,
                'up_context': up_context[::-1],  # 反转列表，使顺序从远到近
                'down_context': down_context
            }

    return {'error': '未找到匹配的记录！'}