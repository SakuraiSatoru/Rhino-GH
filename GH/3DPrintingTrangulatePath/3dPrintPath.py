import rhinoscriptsyntax as rs
uMax = int(v+1)
vMax = int(u+1)
wMax = int(len(x)/((u+1)*(v+1)))
offDist = y
a = []
b = []
class ptClass:
    
    
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w
        self.pt = uvwPt(u,v,w)
        self.link = []
        self.draw = 0
        
    def getAbove(self):
        if self.w < wMax-1:
            return ptClass(self.u,self.v,self.w+1)
        else:
            return None
    
    def getUp(self):
        if self.v < vMax-1:
            return ptClass(self.u,self.v+1,self.w)
        else:
            return None
    def getDown(self):
        if self.v >0:
            return ptClass(self.u,self.v-1,self.w)
        else:
            return None
    def getLeft(self):
        if self.u < uMax -1:
            return ptClass(self.u+1,self.v,self.w)
        else:
            return None
    def getRight(self):
        if self.u>0:
            return ptClass(self.u-1,self.v,self.w)
        else:
            return None
    def getLink(self,pt):
        return rs.AddLine(self.pt,pt.pt)
    def drawLink(self,pt):
        self.draw += 1
        pt.draw += 1
        return rs.AddLine(findClose(self.pt,pt.pt,2)[0],findClose(self.pt,pt.pt,2)[1])
        '''
        if (self.draw < 3) and (pt.draw < 3):
            return rs.AddLine(self.pt,pt.pt)
        elif (self.draw >= 3) and (pt.draw < 3):
            return rs.AddLine(findClose(self.pt,pt.pt,0)[0],pt.pt)
        elif (self.draw < 3) and (pt.draw >= 3):
            return rs.AddLine(findClose(self.pt,pt.pt,1)[0],self.pt)
        elif (self.draw >= 3) and (pt.draw >= 3):
            return rs.AddLine(findClose(self.pt,pt.pt,2)[0],findClose(self.pt,pt.pt,2)[1])
        else:
            raise Exception('error')
        '''

class ptGrid:
    anchorPt = 0
    
    def __init__(self, p0, p1, p2, p3):
        self.pts = []
        self.pts.append(p0)
        self.pts.append(p1)
        self.pts.append(p2)
        self.pts.append(p3)
        self.stdPath = []#Standard Pts
        self.realPath = []
    def setPath(self,ptsArray):
        if ptsArray:
            self.startPt = ptsArray[0]
            self.endPt = ptsArray[-1]
            self.startRealPt = findClose(ptsArray[0].pt,ptsArray[1].pt,2)[0]
            self.endRealPt = findClose(ptsArray[-2].pt,ptsArray[-1].pt,2)[1]
            if ptGrid.anchorPt == 0 :
                ptGrid.anchorPt = self.endRealPt
            for p in range(len(ptsArray)):
                self.stdPath.append(ptsArray[p])                    
                if p < len(ptsArray) - 1:
                    self.realPath.append(findClose(ptsArray[p].pt,ptsArray[p+1].pt,2)[0])
                    self.realPath.append(findClose(ptsArray[p].pt,ptsArray[p+1].pt,2)[1])
        else:
            raise Exception('error')
        return rs.AddPolyline(self.realPath)

def uvwPt(u,v,w):
    i = int(w*uMax*vMax+v*uMax+u)
    return x[i]
    
def findClose(p1,p2,t):
    returnPt = []
    dif = rs.PointAdd(p2,(0-rs.PointCoordinates(p1)[0],0-rs.PointCoordinates(p1)[1],0-rs.PointCoordinates(p1)[2]))
    dif = rs.AddPoint(dif)
    dis =  float(rs.Distance(p1,p2))
    if t != 2:
        d1 = float(rs.PointCoordinates(dif)[0])/dis*offDist*(1-t*2)
        d2 = float(rs.PointCoordinates(dif)[1])/dis*offDist*(1-t*2)
        d3 = float(rs.PointCoordinates(dif)[2])/dis*offDist*(1-t*2)
        newPt1 = rs.AddPoint(rs.PointAdd(p1,(d1,d2,d3)))
        newPt2 = rs.AddPoint(rs.PointAdd(p2,(d1,d2,d3)))
        if  t==0:
            returnPt.append(newPt1)
        else:
            returnPt.append(newPt2)
    else:
        d1 = float(rs.PointCoordinates(dif)[0])/dis*offDist
        d2 = float(rs.PointCoordinates(dif)[1])/dis*offDist
        d3 = float(rs.PointCoordinates(dif)[2])/dis*offDist
        d4 = float(rs.PointCoordinates(dif)[0])/dis*offDist*(-1)
        d5 = float(rs.PointCoordinates(dif)[1])/dis*offDist*(-1)
        d6 = float(rs.PointCoordinates(dif)[2])/dis*offDist*(-1)
        newPt1 = rs.AddPoint(rs.PointAdd(p1,(d1,d2,d3)))
        newPt2 = rs.AddPoint(rs.PointAdd(p2,(d4,d5,d6)))
        returnPt.append(newPt1)
        returnPt.append(newPt2)
    return returnPt
    


#三?列表
ptArray = [[[0 for nU in range(uMax)]for nV in range(vMax)]for nW in range(wMax)]
for k in range(wMax):
    for j in range(vMax):
        for i in range(uMax):
            ptArray[k][j][i] = ptClass(i,j,k)




#四?列表
gridArray = [[[0 for nU in range(uMax-1)]for nV in range(vMax-1)]for nW in range(wMax-1)]
for nW in range(wMax-1):
    for nV in range(vMax-1):
        if nW %2 == 1:
           nV = vMax - 2 - nV
        for nU in range(uMax-1):
            pathArray = []
            if nW %2 == 0:
                if (nV % 2) == 0:#odd v row
                    gridArray[nW][nV][nU] = ptGrid(ptArray[nW][nV][nU],ptArray[nW][nV+1][nU],ptArray[nW][nV][nU+1],ptArray[nW][nV+1][nU+1])
                    
                    pathArray.append(gridArray[nW][nV][nU].pts[0])
                    pathArray.append(gridArray[nW][nV][nU].pts[2])
                    pathArray.append(gridArray[nW][nV][nU].pts[1])
                    pathArray.append(gridArray[nW][nV][nU].pts[0].getAbove())
                    if nU == uMax -2:#last one each u row
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                    else:
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                else:#even v row
                    nU = uMax - 2 - nU
                    gridArray[nW][nV][nU] = ptGrid(ptArray[nW][nV][nU],ptArray[nW][nV+1][nU],ptArray[nW][nV][nU+1],ptArray[nW][nV+1][nU+1])
                    
                    pathArray.append(gridArray[nW][nV][nU].pts[2])
                    pathArray.append(gridArray[nW][nV][nU].pts[0])
                    if nU != 0:
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        pathArray.append(gridArray[nW][nV][nU].pts[0])
                    else:#last one each u row
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[0].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        
                    
                    
                if (nV == vMax -2) and (nU == uMax - 2) and (vMax %2 == 0):#add last row point
                    for uPt in range(uMax - 1):
                        uPt = uMax - 2 - uPt
                        pathArray.append(gridArray[nW][nV][uPt].pts[1])
                    for uPt in range(uMax - 1):
                        pathArray.append(gridArray[nW][nV][uPt].pts[1].getAbove())
                        pathArray.append(gridArray[nW][nV][uPt].pts[3])
                    pathArray.append(gridArray[nW][nV][uMax - 2].pts[3].getAbove())
                elif(nV == vMax -2) and (nU == 0) and (vMax %2 == 1):
                    for uPt in range(uMax-2):
                        pathArray.append(ptArray[nW][nV+1][uPt+1])
                    for uPt in range(uMax):
                        pathArray.append(ptArray[nW][nV+1][uMax- 1 -uPt])
                        pathArray.append(ptArray[nW][nV+1][uMax- 1 -uPt].getAbove())
                        
                            
                a.append(gridArray[nW][nV][nU].setPath(pathArray))
                if nU >0 or nV > 0 or nW >0:
                    b.append(rs.AddLine(gridArray[nW][nV][nU].startRealPt,ptGrid.anchorPt))
                    ptGrid.anchorPt = gridArray[nW][nV][nU].endRealPt
            if nW %2 == 1:
                
                nU = uMax - 2 - nU
                
                
                if (nV % 2) == 0:#odd v row
                    gridArray[nW][nV][nU] = ptGrid(ptArray[nW][nV+1][nU+1],ptArray[nW][nV][nU+1],ptArray[nW][nV+1][nU],ptArray[nW][nV][nU])
                    
                    pathArray.append(gridArray[nW][nV][nU].pts[0])
                    pathArray.append(gridArray[nW][nV][nU].pts[2])
                    pathArray.append(gridArray[nW][nV][nU].pts[1])
                    pathArray.append(gridArray[nW][nV][nU].pts[0].getAbove())
                    
                    if nU == 0:#last one each u row
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                    else:
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                        
                else:#even v row
                    nU = uMax - 2 - nU
                    gridArray[nW][nV][nU] = ptGrid(ptArray[nW][nV+1][nU+1],ptArray[nW][nV][nU+1],ptArray[nW][nV+1][nU],ptArray[nW][nV][nU])
                    
                    pathArray.append(gridArray[nW][nV][nU].pts[2])
                    pathArray.append(gridArray[nW][nV][nU].pts[0])
                    if nU != uMax - 2:
                        pathArray.append(gridArray[nW][nV][nU].pts[3])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        pathArray.append(gridArray[nW][nV][nU].pts[0])
                    else:#last one each u row
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        pathArray.append(gridArray[nW][nV][nU].pts[2])
                        pathArray.append(gridArray[nW][nV][nU].pts[2].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[0].getAbove())
                        pathArray.append(gridArray[nW][nV][nU].pts[1])
                        
                    
                    
                if (nV == 0) and (nU == 0) and (vMax %2 == 0):#add last row point
                    for uPt in range(uMax - 1):
                        pathArray.append(gridArray[nW][nV][uPt].pts[1])
                    for uPt in range(uMax - 1):
                        uPt = uMax -2 -uPt
                        pathArray.append(gridArray[nW][nV][uPt].pts[1].getAbove())
                        pathArray.append(gridArray[nW][nV][uPt].pts[3])
                    pathArray.append(gridArray[nW][nV][0].pts[3].getAbove())
                elif(nV == 0) and (nU == 0) and (vMax %2 == 1):
                    for uPt in range(uMax-2):
                        pathArray.append(ptArray[nW][nV][uPt+1])
                    for uPt in range(uMax):
                        pathArray.append(ptArray[nW][nV][uMax- 1 -uPt])
                        pathArray.append(ptArray[nW][nV][uMax- 1 -uPt].getAbove())
                        
                a.append(gridArray[nW][nV][nU].setPath(pathArray))
                if nU >0 or nV > 0 or nW >0:
                    b.append(rs.AddLine(gridArray[nW][nV][nU].startRealPt,ptGrid.anchorPt))
                    ptGrid.anchorPt = gridArray[nW][nV][nU].endRealPt
                