def search_bst(node, val):
    # Base case: if the current node is None, the value is not in the tree
    if node is None:
        return False

    # If the current node's value matches the search value, return True
    if node.val == val:
        return True
    # If the search value is less than the current node's value, search in the left subtree
    elif val < node.val:
        return search_bst(node.left, val)
    # If the search value is greater than the current node's value, search in the right subtree
    else:
        return search_bst(node.right, val)
