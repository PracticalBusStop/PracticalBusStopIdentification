import numpy


def MyCluster(D, eps, MinPts,first_data_index,last_data_index):
    D = D.iloc[first_data_index:last_data_index]
    D = D.values
    labels = [-2]*len(D)
    ClusterId = 0
    for P in range(0, len(D)):
        if not (labels[P] == -2):
            continue
        NeighborPts = regionQuery(D, P, eps)
        if len(NeighborPts) < MinPts:
            labels[P] = -1
        else: 
            ClusterId = P+first_data_index
            growCluster(D, labels, P, NeighborPts, ClusterId, eps, MinPts)
    return labels

def growCluster(D, labels, P, NeighborPts, ClusterId, eps, MinPts):
    labels[P] = ClusterId
    i = 0
    while i < len(NeighborPts):    
        Pn = NeighborPts[i]
        if labels[Pn] == -1:
            labels[Pn] = ClusterId
        elif labels[Pn] == -2:
            labels[Pn] = ClusterId
            PnNeighborPts = regionQuery(D, Pn, eps)
            if len(PnNeighborPts) >= MinPts:
                NeighborPts = NeighborPts + PnNeighborPts
        i += 1        

def regionQuery(D, P, eps):
    neighbors = []
    for Pn in range(0, len(D)):
        if numpy.linalg.norm(D[P] - D[Pn]) < eps:
            neighbors.append(Pn)
    return neighbors