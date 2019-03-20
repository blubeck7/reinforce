"""
Directed graph module.

This module implements a directed graph with basic functionality for creating
and using a directed graph.

Classes:
    DGIF - directed graph interface
    DG - basic directed graph implementation

Functions:

Constants:

Exceptions:
"""


import abc


class DGIF(abc.ABC):
    """
    Declares the basic methods for creating and using a directed graph (DG).
 
    This class declares the methods for creating and using a DG. Clients can
    store objects called attributes at the nodes and edges in order to
    customize the behavior DG. 
    """

    @abc.abstractmethod
    def add_node(self, label, **attrs):
        """
        Adds a node to the DG.
 
        This method adds a node to the DG and stores any attributes at the
        node.
 
        Params:
            label: hashable - node identifier.
            attrs: dict - additional node attributes.
 
        Raises:
            TypeError - (label) is not hashable.
            KeyError - (label) is already a node.
        """

        pass

    @abc.abstractmethod
    def add_edge(self, from_label, to_label, **attrs):
        """
        Adds an edge to the DG.
       
        This method adds an edge to the DG and stores any attributes at the
        edge. 
 
        Params:
            from_label: hashable - from node identifier.
            to_label: hashable - to node identifier.
            attrs: dict - additional edge attributes.
 
        Raises:
            TypeError - (from_label|to_label) is not hashable.
            KeyError - (from_label|to_label) is not a node.
            KeyError - (from_label, to_label) is already an edge.
        """

        pass

    @abc.abstractmethod
    def remove_node(self, label):
        """
        Removes a node from the DG.
 
        This method removes a node from the DG and updates the node's immediate
        predecessors and descendants.
 
        Params:
            label: hasble - node identifier.
 
        Raises:
            TypeError - (label) is not hashable.
            KeyError: (label) is not a node.
        """

        pass

    @abc.abstractmethod
    def remove_edge(self, from_label, to_label):
        """
        Removes an edge from the DG.
 
        This method removes an edge from the DG and updates the edge's nodes.
 
        Params:
            from_label: hashable - from node identifier.
            to_label: hashable - to node identifier.
 
        Raises:
            TypeError - (from_label|to_label) is not hashable.
            KeyError: (from_label, to_label) is not an edge.
        """

        pass

    @abc.abstractmethod
    def add_dg(self, other):
        """
        Adds another DG to this one.
 
        This method adds another DG to this one. Note that this method will
        write over any nodes or edges in this DG with labels that match the
        labels of any nodes or edges in the other DG.
 
        Params:
            other: DGIF - the DG to add to this one.
        """

        pass

    @abc.abstractmethod
    def prune(self, label):
        """
        Prunes the DG starting at a given node.
 
        This method prunes a DG starting at a given node. This method removes
        all the nodes reachable from the starting node and returns a new DG
        consisting of the removed nodes and edges.
 
        Params:
            label: (hashable) - starting node identifier.
 
        Returns:
            DGIF - A new DG consisting of the removed nodes, edges and any
            attributes stored at the removed nodes or edges.

        Raises:
            TypeError - (label) is not hashable.
            KeyError: (label) is not a node.
        """

        pass

    @abc.abstractmethod
    def copy(self, label):
        """
        Creates a copy of the DG starting at a given node.
 
        This method creates a copy of all the nodes reachable from the starting
        node and returns a new DG consisting of the reachable nodes and
        corresponding edges.
 
        Params:
            label: (hashable) - starting node identifier.
 
        Returns:
            DGIF - A new DG consisting of the reachable nodes, corresponding
            edges and any attributes stored at the nodes or edges.

        Raises:
            TypeError - (label) is not hashable.
            KeyError: (label) is not a node.
        """

        pass

    @property
    @abc.abstractmethod
    def nodes(self):
        """
        Returns a dictionary of all the nodes in the DG.
 
        Returns:
            dict - {label: hashable, node: NodeIF}
        """
        
        pass

    @property
    @abc.abstractmethod
    def edges(self):
        """
        Returns a dictionary of all the edges in the DG.
 
        Returns:
            dict - {label: hashable, edge: EdgeIF}
        """
        
        pass


class NodeIF(abc.ABC):
    """
    Declares the basic methods for creating and using a node.
    """

    @property
    @abc.abstractmethod
    def from_nodes(self):
        """
        Returns a dictionary of the nodes with an edge to this node.
       
        Returns:
            dict - {label: hashable, node: NodeIF}
        """
        
        pass

    @property
    @abc.abstractmethod
    def to_nodes(self):
        """
        Returns a dictionary of the nodes with an edge from this node.
       
        Returns:
            dict - {label: hashable, node: NodeIF}
        """

        pass

    @abc.abstractmethod
    def add_from_node(self, label, node):
        """
        Adds a from node to this node.

        Params:
            label: hashable - node identifier
            node: NodeIF - the actual node

        Raises:
            TypeError - (label) is not hashable.
            TypeError - (node) is not a node object.
            KeyError - (label) is already a from node.
        """
        
        pass

    @abc.abstractmethod
    def add_to_node(self, label, node):
        """
        Adds a to node to this node.

        Params:
            label: hashable - node identifier
            node: NodeIF - the actual node

        Raises:
            TypeError - (label) is not hashable.
            TypeError - (node) is not a node object.
            KeyError - (label) is already a to node.
        """
        
        pass
    
    @abc.abstractmethod
    def remove_from_node(self, label):
        """
        Removes a from node from this node.

        Params:
            label: hashable - node identifier
            node: NodeIF - the actual node

        Raises:
            TypeError - (label) is not hashable.
            KeyError - (label) is not a from node.
        """
        
        pass
    
    @abc.abstractmethod
    def remove_to_node(self, label):
        """
        Removes a to node from this node.

        Params:
            label: hashable - node identifier
            node: NodeIF - the actual node

        Raises:
            TypeError - (label) is not hashable.
            KeyError - (label) is not a to node.
        """
        
        pass
    
    @property
    @abc.abstractmethod
    def attrs(self):
        """
        Returns the attributes stored at the node.
 
        Returns:
            dict - additional attributes stored at the node.
        """

        pass

    @attrs.setter
    @abc.abstractmethod
    def attrs(self):
        """
        Sets the attributes stored at the node.

        Raises:
            TypeError - attrs is not a dictionary
        """

        pass


class EdgeIF(abc.ABC):
    """
    Declares the methods for creating and using an edge.
    """

    @property
    @abc.abstractmethod
    def attrs(self):
        """
        Returns the attributes stored at the edge.
 
        Returns:
            dict - the additional attributes stored at the edge.
        """

        pass
    
    @attrs.setter
    @abc.abstractmethod
    def attrs(self):
        """
        Sets the attributes stored at the edge.

        Raises:
            TypeError - attrs is not a dictionary
        """

        pass


# class BaseDAG(DAGBldrIF, DAGClientIF, DAGSearchIF):
#     """
#     Defines the methods for a mutable and searchable DAG.
#     """
#  
#     def __init__(self):
#         """
#         Initializes the dag.
#         """
#         # nodes: dict - stores the node information as
#         #    {label: int|str, node: NodeIF}.
#         # edges: dict - stores the edge attributes as
#         #    {label: tuple[int|str, int|str], edge: EdgeIF}.
#         # color, pred, dtime, ftime and dist are used for searching.
#  
#         self._nodes = dict()
#         self._edges = dict()
#  
#         self._color = dict()
#         self._pred = dict()
#         self._dtime = dict()
#         self._ftime = dict()
#         self._dist = dict()
#  
#         return
#  
#     def add_node(self, label, **attrs):
#         # if not isinstance(label, int) and not isinstance(label, str):
#             # msg = "{} is not an integer or string".format(label)
#             # raise TypeError(msg)
#  
#         if label in self._nodes:
#             msg = "{} is already a node".format(label)
#             raise KeyError(msg)
#  
#         self._nodes[label] = Node(**attrs)
#  
#         return
#  
#     def add_edge(self, from_label, to_label, **attrs):
#         if from_label not in self._nodes:
#             msg = "{} is not a node".format(from_label)
#             raise KeyError(msg)
#  
#         if to_label not in self._nodes:
#             msg = "{} is not a node".format(to_label)
#             raise KeyError(msg)
#  
#         if (from_label, to_label) in self._edges:
#             msg = "{} is already an edge".format((from_label, to_label))
#             raise KeyError(msg)
#  
#         # Add the edge to the DAG. Then check if it creates a cycle. If so,
#         # then remove the edge.
#         self._edges[(from_label, to_label)] = Edge(**attrs)
#         self._nodes[from_label].add_to_node(to_label, self._nodes[to_label])
#         self._nodes[to_label].add_from_node(from_label, self._nodes[from_label])
#  
#         cycle, path  = self._has_cycle(from_label)
#         if cycle:
#             self.remove_edge(from_label, to_label)
#             msg = "Adding an edge from {} to {} creates a cycle: {}.".format(
#                 from_label, to_label, path)
#             raise ValueError(msg)
#  
#         return
#  
#     def remove_node(self, label):
#         if label not in self._nodes:
#             msg = "{} is not a node".format(label)
#             raise KeyError(msg)
#  
#         for to_label in tuple(self._nodes[label].to_nodes.keys()):
#             self._nodes[to_label].remove_from_node(label)
#             del self._edges[(label, to_label)]
#  
#         for from_label in tuple(self._nodes[label].from_nodes.keys()):
#             self._nodes[from_label].remove_to_node(label)
#             del self._edges[(from_label, label)]
#  
#         del self._nodes[label]
#  
#         return
#  
#     def remove_edge(self, from_label, to_label):
#         if not (from_label, to_label) in self._edges:
#             msg = "From {} to {} is not an edge".format(from_label, to_label)
#             raise KeyError(msg)
#  
#         del self._edges[(from_label, to_label)]
#         self._nodes[from_label].remove_to_node(to_label)
#         self._nodes[to_label].remove_from_node(from_label)
#  
#         return
#  
#     @property
#     def nodes(self):
#  
#         return self._nodes
#  
#     @property
#     def edges(self):
#  
#         return self._edges
#  
#     def add_dag(self, other):
#         if not isinstance(other, DAGClientIF):
#             msg = "{} is not a DAG client.".format(other)
#             raise TypeError(msg)
#  
#         self._nodes.update(other._nodes)
#         self._edges.update(other._edges)
#  
#         return
#  
#     def copy_dag(self, label=None):
#         dag = BaseDAG()
#  
#         if label:
#             labels = self.search_bf(label)
#         else:
#             labels = self._nodes.keys()
#  
#         for label in labels:
#             dag.add_node(label, **self._nodes[label].attrs)
#         for from_label in labels:
#             for to_label in self._nodes[from_label].to_nodes:
#                 l = (from_label, to_label)
#                 dag.add_edge(*l, **self._edges[l].attrs)
#  
#         return dag
#  
#  
#     def prune_dag(self, label=None):
#         # Pruning the dag consists of copying the subdag and then removing it.
#         dag = self.copy_dag(label)
#  
#         for label in dag.nodes:
#             self.remove_node(label)
#  
#         return dag


class Node(NodeIF):
    """
    Defines the methods for creating and using a node.
    """

    def __init__(self, **attrs):
        """
        Initializes the node object.
 
        Params:
            attrs: dict - additional attributes to store at this node.
        """
        # _from_nodes: dict - {label: hashable, node: NodeIF}
        # _to_nodes: dict - {label: hashable, node: NodeIF}

        self._from_nodes = dict()
        self._to_nodes = dict()
        self._attrs = attrs

        return

    @property
    def from_nodes(self):
        
        return self._from_nodes
    
    @property
    def to_nodes(self):
        
        return self._to_nodes

    def add_from_node(self, label, node):
        try:
            hash(label)
        except TypeError:
            msg = "{} is not hashable".format(label)
            raise TypeError(msg)

        if not isinstance(node, NodeIF):
            msg = "{} is not a node object".format(node)
            raise TypeError(msg)

        if label in self._from_nodes:
            msg = "{} is already a from node".format(label)
            raise KeyError(msg)
        
        self._from_nodes[label] = node
        
        return
    
    def add_to_node(self, label, node):
        try:
            hash(label)
        except TypeError:
            msg = "{} is not hashable".format(label)
            raise TypeError(msg)

        if not isinstance(node, NodeIF):
            msg = "{} is not a node object".format(node)
            raise TypeError(msg)

        if label in self._to_nodes:
            msg = "{} is already a to node".format(label)
            raise KeyError(msg)

        self._to_nodes[label] = node
        
        return
    
    def remove_from_node(self, label):
        try:
            hash(label)
        except TypeError:
            msg = "{} is not hashable".format(label)
            raise TypeError(msg)

        if not label in self._from_nodes:
            msg = "{} is not a from node".format(label)
            raise KeyError(msg)
        
        del self._from_nodes[label]
        
        return
    
    def remove_to_node(self, label):
        try:
            hash(label)
        except TypeError:
            msg = "{} is not hashable".format(label)
            raise TypeError(msg)

        if not label in self._to_nodes:
            msg = "{} is not a to node".format(label)
            raise KeyError(msg)
        
        del self._to_nodes[label]
        
        return
    
    @property
    def attrs(self):
        
        return self._attrs
    
    @attrs.setter
    def attrs(self, attrs):
        if not isinstance(attrs, dict):
            msg = "{} is not a dictionary".format(attrs)
            raise TypeError(msg)
        
        self._attrs = attrs

        return


class Edge(EdgeIF):
    """
    Defines the methods for using an edge.
    """

    def __init__(self, **attrs):
        """
        Initializes the edge object.
 
        Params:
            attrs: dict - additional attributes to store at this edge.
        """
        
        self._attrs = attrs

        return

    @property
    def attrs(self):
        
        return self._attrs
    
    @attrs.setter
    def attrs(self, attrs):
        self._attrs = attrs

        return


# class DAGSearchIF(abc.ABC):
#     """
#     Interface for searching a DAG.
#  
#     This class declares the standard methods for searching over a DAG.
#     """
#    
#     @abc.abstractmethod
#     def search_bf(self, label, ignore=True):
#         """
#         Performs a breath-first search starting at the given node.
#  
#         Params:
#             label: int|str - node identifier.
#             ignore: bool - if false, this method will raise an error if
#                 a cycle is detected.
#  
#         Returns:
#             list - the labels of the nodes reachable from the starting
#             node.
#  
#         Raises:
#             AssertionError - cycle detected.
#         """
#        
#         pass
#  
#     @abc.abstractmethod
#     def search_df(self):
#         """
#         Performs a depth-first search.
#         """
#  
#         pass
#  
#    @abc.abstractmethod
#     def top_sort(self):
#         """
#         Performs a topological sort
#  
#         Returns:
#             tuple - the labels of the nodes in order of dependency.
#         """
#  
#         pass

#     def search_bf(self, label, ignore=True):
#         start = label
#         self._dist.clear()
#         queue = list()
#  
#         for label in self._nodes:
#             self._color[label] = "W"
#             self._pred[label] = None
#         self._color[start] = "G"
#         self._dist[start] = 0
#  
#         queue.append(start)
#         while queue:
#             head = queue[0]
#             for label in self._nodes[head].to_nodes:
#                 if self._color[label] == "W":
#                     self._color[label] = "G"
#                     self._dist[label] = self._dist[head] + 1
#                     self._pred[label] = head
#                     queue.append(label)
#                 elif label == start and not ignore:
#                     path = [head]
#                     while self._pred[path[0]]:
#                         path.insert(0, self._pred[path[0]])
#                     msg = "Cycle detected."
#                     raise AssertionError(msg, path)
#  
#             queue.pop(0)
#             self._color[head] = "B"
#  
#         return list(self._dist.keys())
#  
#     def search_df(self):
#         # There are three colors white (W), gray (G) and black (B).
#         # White indicates that a node has not been visited, gray that a
#         # node has been discovered and black that a node is finished,
#         # i.e. all adjancent nodes have been examined completely
#         for label in self._nodes:
#             self._color[label] = "W"
#             self._pred[label] = None
#  
#         step = [0]
#         for label in self._nodes:
#             if self._color[label] == "W":
#                 self._dfs_visit(label, step)
#  
#         return
#  
#     def _dfs_visit(self, label, step):
#         """
#         Recursively visits the descendants of node
#  
#         This method recursively visits in a depth-first manner the
#         descendant nodes of the passed in node. As it visits each node,
#         it colors the node and records the node's predecessor, discovery
#         time and finish time.
#         """
#  
#         step[0] = step[0] + 1
#         self._color[label] = "G"
#         self._dtime[label] = step[0]
#  
#         for out_label in self._nodes[label].to_nodes:
#             if self._color[out_label] == "W":
#                 self._pred[out_label] = label
#                 self._dfs_visit(out_label, step)
#        
#         # Done exploring the descendants of node
#         self._color[label] = "B"
#         step[0] = step[0] + 1
#         self._ftime[label] = step[0]
#  
#         return
#  
#     def top_sort(self, reverse=True):
#         # This algorithm has three main steps:
#         # Step 1. Call dfs() in order to compute the finishing time of each
#         # node.
#         # Step 2. Sort the nodes in reverse order based on finishing time.
#         # Step 3. Return the nodes as a read-only tuple.
#  
#         self.search_df()
#         items = list(self._ftime.items())
#         items.sort(key=lambda t: t[1], reverse=reverse)
#         nodes = tuple([t[0] for t in items])
#  
#         return nodes
#     def _has_cycle(self, label):
#         cycle = False
#         path = None
#         try:
#             self.search_bf(label, False)
#         except AssertionError as e:
#             cycle = True
#             path = e.args[1]
#  
#         return cycle, path
#  
