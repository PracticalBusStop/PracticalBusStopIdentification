import pandas as pd
import matplotlib.pyplot as plt
from mbrOfClusterPoints2new import mbr
from intersection_bbox_originalPoints import rangequery
from PDBSCAN import PClustering
import os
import time


def getClusters(df, epsInmeter, minObjects):
    clusters = PClustering(df, epsInmeter,minObjects, __name__)
    return clusters

def main():
    path = '.csv file of Latitude and longitude data for practical stop on specific route R'
    drctry = os.chdir(path)
    listDir = os.listdir(drctry)
    number = 0
    not_match = 0
    
    minpt = 5
    ep_list = [5]
    for ep in ep_list: 
        
        Total_Original_stop = 0
        Total_Cluster_Form = 0
        Total_Correct_Cluster = 0  
        for num in range(0,100):
            df1 = pd.read_csv(path+'\\'+str(listDir[num]))
            df = pd.read_csv('.csv file of latitude and longitude data of planned stop on specific route R')
            xs = df1['X']
            ys = df1['Y']
            stop_id = df1['Stop_ID']
            stop_id = set(stop_id)
            stop_id = list(stop_id)
            stop_id_list = [x for x in stop_id if str(x) != 'nan']
            stop_xs = []
            stop_ys = []
            stop_location = []
            flag = 0
            for stop in stop_id_list:
                for num in df.iterrows():
                    if stop == num[1][0]:
                        flag = 1
                        x = num[1][1]
                        y = num[1][2]
                        stop_xs.append(x)
                        stop_ys.append(y)
              
            if flag ==0:
                not_match = not_match + 1
                
                continue
            else:
                number = number + 1
                
            stop_location = list(zip(stop_xs,stop_ys))
            df2 = pd.DataFrame(stop_location)
            df3=df2.sort_values(by=[0,1])
            Total_Original_stop = Total_Original_stop + len(df3)
            plt.scatter(xs,ys)
            plt.plot(df3[0], df3[1], '-ok',color='Red') 
            stop_location_GPS = list(zip(xs,ys))
            df4 = pd.DataFrame(stop_location_GPS , columns=['X','Y'])
            start_time = time.time()
            Clusters = getClusters(df4, ep, minpt)
            new_time = time.time()
            total_time = new_time - start_time
            Total_Cluster_Form = Total_Cluster_Form + len(Clusters)
            poly_list = []  
            identified_points = 0
            identified_cluster = []
            for clustpoints in Clusters:
                cluster_x = []
                cluster_y = []
                for num in clustpoints:
                    cluster_x.append(num[0])
                    cluster_y.append(num[1])
                plt.scatter(cluster_x,cluster_y,color='Green')
                bbox,hull_points = mbr(clustpoints) 
                plt.plot(bbox[:,0], bbox[:,1], '-ok',color='Black')
                
                identified_cluster = rangequery(hull_points,df3,ep,identified_cluster)
                if len(identified_cluster) >=1:
                    identified_points = identified_points + 1
        
            
            
            plt.show()
            Total_Correct_Cluster = Total_Correct_Cluster + identified_points
                    
        true_positive = Total_Correct_Cluster
        flase_positive = Total_Cluster_Form - Total_Correct_Cluster
        flase_negative = Total_Original_stop - Total_Correct_Cluster
        Recall = Total_Correct_Cluster / Total_Original_stop
        Precision = Total_Correct_Cluster / Total_Cluster_Form
        
        print('true_positive:',true_positive)
        print('flase_positive:',flase_positive)
        print('flase_negative:',flase_negative)
        print('Recall:',Recall)
        print('Precision:',Precision)
        
if __name__ == '__main__':
    main()    
    
        
