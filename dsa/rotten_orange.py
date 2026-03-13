from collections import deque
from typing import List
class Solution:
    # Rotten Oranges (LC 994) — BFS
    # def orangesRot(self, mat):
    def orangesRot(self, mat: List[List[int]]) -> int:
        m,n = len(mat), len(mat[0])
        q = deque()
        fresh_orange = 0
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 2:
                    q.append((i,j))
                if mat[i][j] == 1:
                    fresh_orange+=1
        
        dirs = [(-1,0), (1,0), (0,1), (0,-1)]
        count = 0
        if fresh_orange == 0:
            return 0
        while q:
            qlen = len(q)
            count+=1
            for i in range(qlen):
                x,y = q.popleft()
                for dx, dy in dirs:
                    nx, ny = x+dx, y+dy
                    if 0<= nx< m and 0<= ny <n:
                        if mat[nx][ny] == 1:
                            mat[nx][ny]=2
                            q.append((nx,ny))
        
        for i in range(m):
            for j in range(n):
                if mat[i][j] == 1:
                    return -1
        return count-1