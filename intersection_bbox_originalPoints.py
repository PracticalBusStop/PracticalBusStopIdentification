import math
def ecl_dis(points, origin, radius):
    x1, y1 = origin
    return [(x2,y2) for x2,y2 in points if math.sqrt((x1-x2)**2+(y1-y2)**2) <= radius]

def rangequery(hullpoints,original_list,ep,identified_cluster):
    ans = 0

    for ori_pt in original_list.iterrows():
        n = 0
        pt = [ori_pt[1][0], ori_pt[1][1]]
        ans = ecl_dis(hullpoints, pt,ep)   
        if len(ans)>0:
            for num in ans:
                if num not in identified_cluster:
                    identified_cluster.append(num)
                    n = 1
                    break

        if n ==1:
            break
    return identified_cluster
    