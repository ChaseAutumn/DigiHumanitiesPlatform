# app/utils/search_relation_sentences.py

import os
import pickle

# 获取当前文件的上级目录，即 app/
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义数据目录
DATA_DIR = os.path.join(APP_DIR, 'data')
KG_DATA_DIR = os.path.join(DATA_DIR, 'kg_data')

# 定义知识图谱文件路径
KG_FILEPATH = os.path.join(KG_DATA_DIR, 'knowledge_graph.gpickle')

def load_kg(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    else:
        return None

def search_relation_sentences(relation_name):
    kg = load_kg(KG_FILEPATH)
    if kg is None:
        return []

    results = []

    # 遍历所有的边，查找关系匹配的边
    for u, v, key, edge_data in kg.edges(data=True, keys=True):
        if edge_data.get('relation') == relation_name:
            # 获取关联的原始句子和实体
            for obj in edge_data.get('data', []):
                sent_text = obj.get('sentText', '')
                head_entity = u
                tail_entity = v

                # 将结果添加到列表
                results.append({
                    'sentence': sent_text,
                    'head_entity': head_entity,
                    'tail_entity': tail_entity,
                    'relation': relation_name
                })

    return results