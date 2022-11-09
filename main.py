import itertools 
import operator 
import math 
import heapq 
import random 
import time 



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
        nextnode = cnode.__getattr__(direction)
        yield cnode 
        cnode = nextnode



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
        return True if other is None else self.value < other.value

    def __le__(self, other):
        return True if other is None else self.value <= other.value 

    #def __eq__(self, other):
    #    return False if other is None else self.value == other.value 

    #def __ne__(self, other):
    #    return True if other is None else self.value != other.value




class FibonacciHeap:

    """ An instance of this class represents a Fibonacci Heap """

    def __init__(self, nodes=None):
        if nodes:
            nodes = tuple(node if isinstance(node,Node) else Node(node) 
                for node in nodes)
            self.root = nodes[0]
            self.min = min(nodes)
            self.count = len(nodes)

            for i, node in enumerate(itertools.cycle(nodes)):
                if node.left:
                    break
                
                node.left = nodes[i - 1]
                nodes[i - 1].right = node
        
        else:
            self.root = None 
            self.min = None 
            self.count = 0

    
    def insert (self, node):
        """ Method to store  new element in O(1) """
        if not isinstance(node, Node):
            node = Node(node)
        
        self.count += 1 
        self.merge_with_root_list(node)
        self.min = min(self.min, node)

    
    def find_min (self):
        """ Method to read the minimum element in O(1) """
        return self.min.value


    def merge (self, heap):
        """ Method to merge in place two heaps in O(1) """
        # Concatenate the roots
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

        # If there are no nodes
        if result is None:
            raise Exception("The heap is empty.")

        # If there is only one node
        if self.count == 1:
            self.root = None 
            self.min = None 
            result.child = None 
            result.parent = None
            self.count -= 1 
            return result
        
        # Move minimum element childrens to root doubly linked list
        if (child := result.child) is not None:
            children = tuple(doubly_linked_list(child))
            for i in children:
                self.remove_from_child_list(result, i)
                self.merge_with_root_list(i)
        
        # Remove min from roots doubly linked list
        self.remove_from_root_list(result)
        if self.root:
            self.consolidate()    
        self.count -= 1
        return result.value


    def consolidate (self):
        """ Consolidate the heap removing as many trees as possible 
        from the list of roots """
        A = [None] * int(math.log(self.count) * 2)
        
        for i, node in enumerate(tuple(doubly_linked_list(self.root))):
            d = node.degree

            # If there is a tree of that degree, the two are merged
            while (base := A[d]) != None:
                
                # Node must always be the min after this check
                if base < node:
                    node, base = base, node 
                
                self.heap_link(base, node)
                
                A[d] = None
                d += 1

            # Place the tree in the correct position
            A[d] = node 
        # find new min node 
        self.min = min(doubly_linked_list(self.root))


    def heap_link(self, child, parent):
        self.remove_from_root_list(child)
        #child.left = child.right = child
        self.merge_with_child_list(parent, child)
        child.parent = parent


    def merge_with_root_list(self, node):
        if self.root is None:
            self.root = node
            self.root.left = node 
            self.root.right = node
        else:
            node.right = self.root.right
            node.left = self.root
            self.root.right.left = node
            self.root.right = node


    def remove_from_root_list(self, node):
        """ Remove a node from the roots list """
        if node == self.root:
            if self.count == 1:
                self.root = None 
            else:
                self.root = node.right

        node.left.right = node.right
        node.right.left = node.left


    def merge_with_child_list(self, parent, node):
        """ Add a node to the child list of another node """
        node.parent = parent
        parent.degree += 1
        if parent.child is None:
            parent.child = node
            parent.child.left = node
            parent.child.right = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node


    def remove_from_child_list(self, parent, node):
        """ Remove a node from children list of another node """
        node.parent = None
        parent.degree -= 1
        if parent.child == node:
            if parent.child == parent.child.right:
                parent.child = None
            else:
                parent.child = node.right
            
        node.left.right = node.right
        node.right.left = node.left
        

if __name__ == '__main__':
    
    

    for N in (100, 500, 1000):
        f = FibonacciHeap()
        h = []
        for i in range(N):
            r = random.randint(1, 1000)
            f.insert(r)
            heapq.heappush(h, r)


        # test fib heap running time 
        start_time = time.time()
        while f.count > 0:
            m = f.extract_min()
        print("%s seconds run time for fib heap" % (time.time() - start_time))

        # test heapq running time 
        start_time = time.time()
        while h:
            m = heapq.heappop(h)
        print("%s seconds run time for heapq" % (time.time() - start_time))

    
