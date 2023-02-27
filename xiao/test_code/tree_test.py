from treelib import Tree, Node


tree = Tree(tree=None, deep=False, node_class=None, identifier=None)
# print(tree.identifier)
["SOUTH-EAST", "Abia", "Aba North", "Ariaria Market"]


tree.create_node(tag='0', identifier="node-0", data="SOUTH-EAST")
if not tree.contains("SOUTH-EAST"):
    tree.create_node(tag='Node-5', identifier="SOUTH-EAST", parent='node-0',
                     data="SOUTH-EAST")
tree.create_node(tag='Node-10', identifier='node-10', parent='node-0', data=10)
tree.create_node(tag='Node-15', identifier='node-15', parent='node-10', data=15)

node = Node(tag=None, identifier=None, expanded=True, data=50)
tree.add_node(node, parent='node-0')
node_a = Node(tag='Node-A', identifier='node-A', data='A')
tree.add_node(node_a, parent='node-0')
tree.show()
tree_depth = tree.depth(node=None)  # 返回节点的高度
print("tree_depth=%r" % tree_depth)
root_note = tree.get_node("node-0")
print("root_note=%r" % root_note)


for node_1 in tree.children("node-0"):
    if not node_1.is_leaf():
        for node_2 in tree.children(node_1.identifier):
            if not node_2.is_leaf():
                for node_3 in tree.children(node_2.identifier):
                    if not node_3.is_leaf():
                        for node_4 in tree.children(node_3.identifier):
                            print(node_4.data)

for it in tree.expand_tree():
    node = tree.get_node(it)
    print(node.identifier, node.tag, node.data, node.is_leaf())





