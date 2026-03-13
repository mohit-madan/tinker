class Solution:
    # Kosaraju's Algorithm (LC 802) — SCC
    def kosaraju(self, V, edges):
        # code here
        adj = [[] for _ in range(V)]
        revAdj = [[] for _ in range(V)]
        for u,v in edges:
            adj[u].append(v)
            revAdj[v].append(u)
        
        st = []
        vis = [False]*V
        def dfs(curNode):
            vis[curNode] = True
            for nei in adj[curNode]:
                if not vis[nei]:
                    dfs(nei)
            st.append(curNode)
        for i in range(len(vis)):
            if not vis[i]:
                dfs(i)

        vis = [False]*V
        def dfsRev(curNode):
            vis[curNode] = True
            for nei in revAdj[curNode]:
                if not vis[nei]:
                    dfsRev(nei)
        count = 0
        while st:
            top = st.pop()
            if not vis[top]:
                count+=1
                dfsRev(top)
                
        return count