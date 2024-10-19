class Node:
    def __init__(self, val=0, left=None, right=None):
        # Initialize the node with a value, and optionally with left and right children
        self.val = val
        self.left = left
        self.right = right

def insert_bst(node, val):
    # If the current node is None, create a new node with the given value and return it
    if node is None:
        return Node(val)

    # If the value to be inserted is less than the current node's value, insert into the left subtree
    if val < node.val:
        node.left = insert_bst(node.left, val)
    # Otherwise, insert into the right subtree
    else:
        node.right = insert_bst(node.right, val)

    # Return the original node to maintain the tree structure
    return node

