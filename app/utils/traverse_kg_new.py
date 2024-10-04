# app/utils/traverse_kg_new.py

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

def traverse_kg_depth_new(G, head_node, depth):
    """
    从指定的头节点开始，遍历指定深度的知识图谱。
    返回包含节点和边的列表，适用于前端展示。

    参数：
    - G: networkx 图对象
    - head_node: 起始节点名称（字符串）
    - depth: 遍历深度（整数）

    返回：
    - result: 包含 'nodes' 和 'edges' 的字典
    """
    from collections import deque

    if head_node not in G:
        print(f"节点 '{head_node}' 不在知识图谱中。")
        return {'nodes': [], 'edges': []}

    visited_nodes = set()
    result_nodes = []
    result_edges = []

    queue = deque()
    queue.append((head_node, 0))
    visited_nodes.add(head_node)

    while queue:
        current_node, current_level = queue.popleft()

        # 添加节点到结果
        node_data = {
            'data': {
                'id': current_node,
                'label': current_node
            }
        }
        result_nodes.append(node_data)

        if current_level < depth:
            for neighbor in G.successors(current_node):
                for key, edge_attr in G[current_node][neighbor].items():
                    edge_id = f"{current_node}_{neighbor}_{key}"
                    edge_data = {
                        'data': {
                            'id': edge_id,
                            'source': current_node,
                            'target': neighbor,
                            'label': edge_attr.get('relation', '')
                        }
                    }
                    result_edges.append(edge_data)

                if neighbor not in visited_nodes:
                    visited_nodes.add(neighbor)
                    queue.append((neighbor, current_level + 1))

    return {'nodes': result_nodes, 'edges': result_edges}