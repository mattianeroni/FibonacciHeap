import itertools 
import operator 



def doubly_linked_list(root, direction='right'):
    """ 
    Method to iterate through a doubly linked list in 
    the specified direction, starting from the provided 
    node.

    :param root: The starting node
    :param direction: The direction (i.e., left or right)
    """
    yield root 
    cnode = root.__getattr__(direction)
    while cnode != root:
        yield cnode 
        cnode = cnode.__getattr__(direction)



class Node:
    """ An instance of this class represents a node of the Heap """

    def __init__(self, value):
        """
        Initialise.

        :param value: The element to store. It can be a tuple, a number or
                        any sortable element.
        
        :attr parent: The node parent
        :attr child: The reference of the first node child
        :attr left, right: The nodes on the left and right in the doubly linked list
        :attr degree: the number of child nodes
        """
        self.value = value 
        self.parent = None 
        self.child = None 
        self.left = None 
        self.right = None
        self.degree = 0 
    
    def __getattr__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value 

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == other.value 

    def __ne__(self, other):
        if other is None:
            return True
        return self.value != other.value




class FibonacciHeap:

    def __init__(self, nodes=None):
        self.root = None if not nodes else nodes[0]
        self.min = None if not nodes else min(nodes)
        self.count = 0 if not nodes else len(nodes)

        if nodes:
            for i, node in itertools.cycle(nodes):
                if not node.left:
                    node.left = nodes[i - 1]
                    nodes[i - 1].right = node

    
    def insert (self, node):
        """ Method to store  new element in O(1) """
        if not isinstance(node, Node):
            node = Node(node)
        
        self.count += 1 
        
        if self.root is None:
            self.root = node 
            self.root.left = node 
            self.root.right = node
            self.min = node 
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right.left = node
            self.root.right = node

            self.min = min(self.min, node)

    
    def find_min (self):
        """ Method to read the minimum element in O(1) """
        return self.min.value


    def merge (self, heap):
        """ Method to merge in place two heaps in O(1) """
        last = heap.root.left
        heap.root.left = self.root.left
        self.root.left.right = heap.root
        self.root.left = last
        last.right = self.root
        
        # Update min node if needed
        self.min = min(self.min, heap.min)
        
        # Update total nodes
        self.count += heap.count


    def extract_min(self):
        """ method to extract the minimum element in O(log n) """
        result = self.min

        if result is None:
            return

        if count == 1:
            self.root = None 
            self.min = None 
            self.count -= 1 
            return result
        
        # Move minimum element childrens to root doubly linked list
        if (child := result.child) is not None:
            child.left.right = self.root.right
            child.left = self.root
            self.root.right.left = child.left
            self.root.right = child
           
        # Remove min from roots doubly linked list
        if result == self.root:
            self.root = result.right
        result.left.right = result.right
        result.right.left = result.left
            
        # Set new min node in heap
        if result == result.right:
            self.min = None 
            self.root = None
        else:
            self.min = result.right
            self.consolidate()
            
        self.count -= 1
        
        return result


    def consolidate (self):
        pass 
        

if __name__ == '__main__':
    heap = FibonacciHeap()
    heap.insert(0)
    heap.insert(-12)
    heap.insert(88)

    

    print(heap.min, heap.root)
    print(heap.root.left, heap.root.right)
    print(heap.min.left, heap.min.right)

    for i in doubly_linked_list(heap.root):
        print(i, end="-")
    print()
