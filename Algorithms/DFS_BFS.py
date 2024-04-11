class DirectedGraph:
    def __init__(self, no_of_vertices):
        self.no_of_vertices = no_of_vertices
        self.adj_list = [ [] for i in range(no_of_vertices + 1)] # adjacency list for each vertex
        # Here we added one because in loop iteration starts from zero and we have to account for that as well in number of vertices.

    def addEdge(self, u, v):
        self.adj_list[u].append(v)
    
    def DFS(self, s):
        stack = []
        stack.append(s)
        vistited = [ False for i in range(self.no_of_vertices  + 1)]
        while stack:
            s = stack.pop()
            if not vistited[s]:
                print(s, end= " ")
                vistited[s] = True

            for node in self.adj_list[s]:
                if not vistited[node]:
                    stack.append(node)
        print()
        
    def BFS(self, s):
        q = [];
        q.append(s)
        vistited = [ False for i in range(self.no_of_vertices + 1) ]
        vistited[s] = True
        while q:
            s = q.pop(0);
            print(s, end = ' ')

            for node in self.adj_list[s]:
                if not vistited[node]:
                    vistited[node] = True
                    q.append(node)
        print()
            
if __name__ == "__main__":
    g = DirectedGraph(4)
    g.addEdge(1,2)
    g.addEdge(2,1)
    g.addEdge(1,3)
    g.addEdge(3,1)
    g.addEdge(2,4)
    g.addEdge(4,2)
    g.DFS(4)
    g.BFS(4)
