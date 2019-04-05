import matplotlib.pyplot as plt
from Qucickhull import get_hull_points
import numpy as np

def remove_duplicates(clusterPoints): 
    res_list = [] 
    for i in range(len(clusterPoints)): 
        if clusterPoints[i] not in clusterPoints[i + 1:]: 
            res_list.append(clusterPoints[i])

    return res_list

def minimum_bounding_rectangle(points):
    pi2 = np.pi/2.

    hull_points = get_hull_points(points)
    hull_points.reverse()
    edges = np.zeros((len(hull_points)-1, 2))
    firstlist = hull_points[1:]
    secondlist = hull_points[:-1]
    edges = []
    hullpointTranspos = []
    TransposX = []
    TransposY = []
    for i in range(0,len(hull_points)-1):
        TransposX.append(hull_points[i][0])
        TransposY.append(hull_points[i][1])
    
    hullpointTranspos.append(TransposX)
    hullpointTranspos.append(TransposY)
    hullpointTranspos = np.asarray(hullpointTranspos)
    
    for i in range(0,len(firstlist)):
        edges.append([firstlist[i][0]-secondlist[i][0],firstlist[i][1]-secondlist[i][1]])
    
    edges = np.asarray(edges)
    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])
    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T

    rotations = rotations.reshape((-1, 2, 2))

    rot_points = np.dot(rotations, hullpointTranspos)

    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    parimeter = (max_x - min_x) + (max_y - min_y)
    best_idx = np.argmin(2*parimeter)

    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((5, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)
    rval[4] = np.dot([x1, y2], r)
    
    return rval, hull_points




def mbr(clusterpoints):

    clusterpoints = remove_duplicates(clusterpoints)
   
    points = []
    
    X = []
    Y = []
    for num in clusterpoints:
        X.append(num[0])
        Y.append(num[1])
    
    if len(X) <= 3:
            if len(X) == 1:
                x1 = X[0] - 1                
                y1 = Y[0] + 1
                x2 = X[0] + 1
                y2 = Y[0] + 1
                x3 = X[0] + 1
                y3 = Y[0] - 1
                X.append(x1)
                Y.append(y1)
                X.append(x2)
                Y.append(y2)
                X.append(x3)
                Y.append(y3)
                
            if len(X) == 2:
                x2 = X[0] - 1
                y2 = Y[0] + 1
                x3 = X[1] + 1
                y3 = X[1] - 1
                X.append(x2)
                Y.append(y2)
                X.append(x3)
                Y.append(y3)    
                    
            else:
                x3 = X[0] - 1
                y3 = Y[0] + 1
                X.append(x3)
                Y.append(y3)
    
    result = zip(X,Y)            
    points = np.array(list(result))
    
    
    bbox, hull_points1= minimum_bounding_rectangle(points)
    plt.scatter(points[:,0], points[:,1])

    plt.plot(points[:,0], points[:,1], 'o',color='Green')
    
    hull_points1.append(hull_points1[0]) 
    
    xs, ys = zip(*hull_points1) 
    plt.plot(xs,ys)
    fig, ax = plt.subplots()
    plt.fill(bbox[:,0], bbox[:,1], alpha=0.5)
    plt.axis('equal')
    plt.close()

    return bbox,hull_points1
    