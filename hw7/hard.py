'''Binary Search Tree deletion has three scenarios: 
For leaf nodes with no children, you remove the node by
setting its parent's pointer to null. For nodes with one child,
bypass the node by connecting its parent directly to its child.
The most complex case handles nodes with two children by first 
replacing the node's value with either the smallest value in right subtree or the 
largest value in left subtree, then deletes that node using one of the simpler cases.
The process relies on maintaining pointer references and ensuring
the properties remain intact throughout, with special consideration
needed for edge cases like deleting the root node or attempting deletion
from an empty tree. Each step carefully preserves the BST's ordering
property where all left subtree values are less than the node's value,
and all right subtree values are greater.'''

