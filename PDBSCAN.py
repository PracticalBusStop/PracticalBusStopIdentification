import multiprocessing
import time
import math
import numpy as np
from ParallelClustering import MyCluster

def ParallelClustering(df,shared_queqe,first_data_index,last_data_index,ep,minpt,Visited,lock):
    labels = MyCluster(df, ep,minpt,first_data_index,last_data_index)
    shared_queqe.append(labels)
    
def mergeLabels(shared_list,size_data,df,ep,minpt):
    
    df1 = df['X'].values
    fst_value = []
    lst_value = []
    for lst in shared_list:
        i=0
        j=len(lst)-1
        while lst[i] == -1:
            i = i+1
            if i > len(lst)-1:
                i = len(lst)-1
                break
        while lst[j] == -1:
            j = j-1
            if j < 0:
                j = 0
                break 
        fst_value.append(lst[i])
        lst_value.append(lst[j])
    merge_labels = []
    for lst in shared_list:
        for i in lst:
            merge_labels.append(i)
    gap_x_left = []
    gap_x_right = []    
    for num in range(0,len(fst_value)):
        if num < len(fst_value)-1:
            gap_x_left.append(df.iloc[lst_value[num]]['X']-ep)
            gap_x_right.append(df.iloc[fst_value[num+1]]['X']+ep)

    idx = []
    for num in range(0,len(gap_x_left)):
        idx.append(np.where((df1>gap_x_left[num])*(df1<gap_x_right[num])))
     
    labels = []   
    for lst in idx: 
        if len(lst[0])>0:
            first_data_index = lst[0][0]
            last_data_index = lst[0][len(lst[0])-1]+1
            labels.append(MyCluster(df, ep,minpt,first_data_index,last_data_index))
        else:
            labels.append([])
   
    dict = {}
    for i in range(0,len(idx)):
        for j in range(0,len(idx[i][0])):
                if idx[i][0][j] < len(merge_labels):
                    merge_label_value = merge_labels[idx[i][0][j]]
                    if idx[i][0][j] <=  (i+1) * (size_data - 1):
                        new_label_value = labels[i][j]
                        if labels[i][j] != -1:
                            dict[labels[i][j]] = merge_label_value
                            labels[i][j] = merge_label_value
                    elif idx[i][0][j] > (i*size_data):
                            dict[merge_label_value] =  labels[i][j]             

    keylist=dict.keys()
    for key in dict.keys():
        if dict[key] in keylist:
            if dict[key]!= -1:
                dict[key]=dict[dict[key]]     
   
    for key in dict.keys():
        if key !=dict[key]:
            pos = [i for i, x in enumerate(merge_labels) if x == key]
            for num in range(0,len(pos)):
                    if merge_labels[pos[num]] != -1:
                        merge_labels[pos[num]] = dict[key]
                
    pos = [i for i, x in enumerate(merge_labels) if x == -1]
    for i in range(0,len(idx)):
        for j in range(0,len(idx[i][0])):
            index = idx[i][0][j]
            if index in pos:
                merge_labels[index] = labels[i][j]
        
    return merge_labels
    
                
def PClustering(df1, ep,minpt, mainMethod):
    with multiprocessing.Manager() as manager:
        if mainMethod == '__main__':
            df = df1.sort_values('X')
            number_cpu = multiprocessing.cpu_count()
            manager = multiprocessing.Manager()
            lock = multiprocessing.Lock()
            Visited = manager.list([])
            first_data_index = 0
            jobs = []
            size_data = math.ceil(len(df)/number_cpu)
            last_data_index = size_data + first_data_index
            shared_queqe = manager.list([])
            start_time = time.time()
            shared_label_range = {}
            for i in range(0, number_cpu):
                process = multiprocessing.Process(target=ParallelClustering,args=(df,shared_queqe,first_data_index,last_data_index,ep,minpt,Visited,lock))
                shared_label_range[i]=([first_data_index,last_data_index-1])
                first_data_index = last_data_index
                last_data_index = first_data_index + size_data
                jobs.append(process)

            for j in jobs:
                j.start()
            
            for j in jobs:
                j.join()
                
            shared_list_1 = []   
            for lst in shared_queqe:
                shared_list_1.append(lst)
            
            shred_list_dict = {}
             
            for key in shared_label_range.keys():
                gap = shared_label_range[key]
                for sharedLst in shared_queqe:
                    flag = 0
                    minus_list = 0
                    for label in sharedLst:
                        if label >= 0 and label>=gap[0] and label<=gap[1]:
                            shred_list_dict[key] = sharedLst
                            #print("shred_list_dict[key]",shred_list_dict[key])
                            flag = 1
                            break
                        
                    if flag == 1:
                        break

            shared_list_2 = []
            Key_list = shared_label_range.keys()
    
            for key in Key_list:
                if key not in shred_list_dict.keys():
                    shred_list_dict[key] = [-1]*size_data
            
            for key in sorted(shred_list_dict.keys()):
                shared_list_2.append(shred_list_dict[key])
             
            start_time = time.time()
            Labels = mergeLabels(shared_list_2,size_data,df,ep,minpt)
        
            if len(Labels) > len(df):
                Labels = Labels[:len(df)]
                
            arrayLabels = np.asarray(Labels)
            coords = df.values
            n_clusters_ = len(set(arrayLabels)) - (1 if -1 in arrayLabels else 0) 
            uniqulabel = set(arrayLabels)
            if -1 in uniqulabel:
                uniqulabel.remove(-1)
    
            clusters = [coords[arrayLabels == i] for i in uniqulabel]
    
            return clusters

            
        