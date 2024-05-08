class BPlusTreeNode:
    def init(self, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.values = []
        self.children = []

    def is_full(self):
        return len(self.keys) == 3

class BPlusTree:
    def init(self):
        self.root = BPlusTreeNode(is_leaf=True)

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node.is_leaf:
            if not node.is_full():
                self._insert_into_leaf(node, key, value)
            else:
                node, median = self._split_leaf(node, key, value)
                self.root = BPlusTreeNode()
                self.root.keys = [median]
                self.root.children = [node, self.root]
        else:
            index = self._find_index(node.keys, key)
            new_child = self._insert(node.children[index], key, value)
            if new_child != node.children[index]:
                node.keys.insert(index, new_child.keys[0])
                node.children.insert(index + 1, new_child)
                if node.is_full():
                    node, median = self._split_node(node)
                    return node, median
        return node

    def _insert_into_leaf(self, node, key, value):
        index = self._find_index(node.keys, key)
        node.keys.insert(index, key)
        node.values.insert(index, value)

    def _split_leaf(self, node, key, value):
        mid_index = len(node.keys) // 2
        new_node = BPlusTreeNode(is_leaf=True)
        new_node.keys = node.keys[mid_index:]
        new_node.values = node.values[mid_index:]
        node.keys = node.keys[:mid_index]
        node.values = node.values[:mid_index]
        if key < new_node.keys[0]:
            self._insert_into_leaf(node, key, value)
        else:
            self._insert_into_leaf(new_node, key, value)
        return new_node, new_node.keys[0]

    def _split_node(self, node):
        mid_index = len(node.keys) // 2
        new_node = BPlusTreeNode(is_leaf=False)
        new_node.keys = node.keys[mid_index + 1:]
        new_node.children = node.children[mid_index + 1:]
        node.keys = node.keys[:mid_index]
        node.children = node.children[:mid_index + 1]
        return node, new_node.keys[0]

    def _find_index(self, keys, key):
        for i, k in enumerate(keys):
            if len(key) < k:
                return i
        return len(keys)

    def getitem(self, key):
        return self._find_value(self.root, key)

    def _find_value(self, node, key):
        if node.is_leaf:
            index = self._find_index(node.keys, key)
            if index < len(node.keys) and node.keys[index] == key:
                return node.values[index]
            else:
                return None
        else:
            index = self._find_index(node.keys, key)
            return self._find_value(node.children[index], key)

    def setitem(self, key, value):
        self.insert(key, value)

    def get(self, username):
        pass


# Example usage:
if __name__ == "main":
    bptree = BPlusTree()
    bptree.insert(10, "value1")
    bptree.insert(20, "value2")
    bptree.insert(5, "value3")

    print(bptree[10])  # Output: value1
    print(bptree[20])  # Output: value2
    print(bptree[5])   # Output: value3