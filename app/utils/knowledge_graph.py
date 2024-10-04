# app/utils/knowledge_graph.py

import networkx as nx
import os
import json
import pickle  # 导入 pickle 模块

# 获取当前文件的上级目录，即 app/
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义数据目录
DATA_DIR = os.path.join(APP_DIR, 'data')
JSON_FILES_DIR = os.path.join(DATA_DIR, 'json_files')
KG_DATA_DIR = os.path.join(DATA_DIR, 'kg_data')

# 定义文件路径
JSON_FILEPATH = os.path.join(JSON_FILES_DIR, 'KG标注示例.json')
KG_FILEPATH = os.path.join(KG_DATA_DIR, 'knowledge_graph.gpickle')

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

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        fixed_json_str = fix_json_missing_commas(content)
        data = json.loads(fixed_json_str)

    return data

def build_kg(data):
    G = nx.MultiDiGraph()
    for obj in data:
        for relation in obj.get('relationMentions', []):
            head = relation['em1Text']
            tail = relation['em2Text']
            label = relation['label']
            
            # 初始化节点的 Data 为列表
            G.add_node(head, data=[obj])
            G.add_node(tail, data=[obj])
            
            # 初始化边的 Data 为列表
            G.add_edge(head, tail, relation=label, data=[obj])
    return G

def update_kg(G, new_data):
    for obj in new_data:
        for relation in obj.get('relationMentions', []):
            head = relation['em1Text']
            tail = relation['em2Text']
            label = relation['label']
            
            # 更新或添加节点
            for node in [head, tail]:
                if G.has_node(node):
                    # 节点已存在，更新 Data 列表
                    if 'data' in G.nodes[node]:
                        if obj not in G.nodes[node]['data']:
                            G.nodes[node]['data'].append(obj)
                    else:
                        G.nodes[node]['data'] = [obj]
                else:
                    # 节点不存在，添加节点并初始化 Data 列表
                    G.add_node(node, data=[obj])
            
            # 更新或添加边
            exists = False
            if G.has_edge(head, tail):
                for key, edge_attr in G[head][tail].items():
                    if edge_attr['relation'] == label:
                        exists = True
                        # 更新边的 Data 列表
                        if obj not in edge_attr['data']:
                            edge_attr['data'].append(obj)
                        break
            if not exists:
                # 添加新的关系类型的边
                G.add_edge(head, tail, relation=label, data=[obj])

def save_kg(G, filepath):
    with open(filepath, 'wb') as f:
        pickle.dump(G, f)

def load_kg(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    else:
        return nx.MultiDiGraph()

def query_kg(G, head=None, tail=None, relation=None):
    results = []
    for u, v, key, edge_data in G.edges(data=True, keys=True):
        if ((head is None or u == head) and
            (tail is None or v == tail) and
            (relation is None or edge_data['relation'] == relation)):
            results.append({
                'head': u,
                'tail': v,
                'relation': edge_data['relation'],
                'data': edge_data['data']
            })
    return results

def main():
    # 加载或初始化知识图谱
    kg = load_kg(KG_FILEPATH)
    
    # 加载新的 JSON 数据
    new_data = load_json(JSON_FILEPATH)
    
    if len(kg) == 0:
        # 如果 KG 为空，构建新的 KG
        kg = build_kg(new_data)
    else:
        # 更新已有的 KG
        update_kg(kg, new_data)
    
    # 保存更新后的 KG
    save_kg(kg, KG_FILEPATH)
    
    # 示例查询
    results = query_kg(kg, head='拉爹')
    for res in results:
        print(f"{res['head']} -[{res['relation']}]-> {res['tail']}")

if __name__ == '__main__':
    main()