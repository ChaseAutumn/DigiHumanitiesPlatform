# app/utils/search_entity_sentences.py

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


def search_entity_sentences(entity_name):
    kg = load_kg(KG_FILEPATH)
    if kg is None:
        return []

    sentences = set()

    # 如果实体在节点中，获取节点的 data
    if kg.has_node(entity_name):
        node_data = kg.nodes[entity_name]
        for obj in node_data.get('data', []):
            sent_text = obj.get('sentText', '')
            sentences.add(sent_text)

    # 遍历与该实体相关的边，获取关联的句子
    for u, v, edge_data in kg.edges(data=True):
        if u == entity_name or v == entity_name:
            for obj in edge_data.get('data', []):
                sent_text = obj.get('sentText', '')
                sentences.add(sent_text)

    return list(sentences)
