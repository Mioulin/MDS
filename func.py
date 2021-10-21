import pandas as pd
from scipy.stats import pearsonr
import os
import numpy as np
from init import *
from nilearn.connectome import ConnectivityMeasure


# Extract time-series, make correlation matrix from nf files
def get_corr_matrix(file_name):
    time_series = pd.DataFrame(masker.fit_transform(file_name), columns=labels)
    correlation_measure = ConnectivityMeasure(kind='correlation')
    correlation_matrix = correlation_measure.fit_transform([time_series.values])[0]
    return correlation_matrix


# Cut upper triangle to covert 2D matrix to 1D array (n*(n-1)/2) - 100 point to 4950
def upper_triangle(all_corr_matrix):
    iu1 = np.triu_indices(100, 1)
    tr_dict = dict()  # create a dictionary with data_type(HC/ASD/DMT/PCB)
    for (data_type, data_set) in all_corr_matrix.items():
        tr_dict[data_type] = dict()  # create a dictionary with data_type(HC/ASD/DMT/PCB)
    for (data_type, data_set) in all_corr_matrix.items():
        for (ind, array) in data_set.items():
            tr_dict[data_type][ind] = array[iu1]
    return tr_dict


# combine dictionary with data_type and sample information
def combine_dict(triangle_dict):
    dict_all = dict()
    for data_type, dataset in triangle_dict.items():
        for ind, array in dataset.items():
            dict_all[data_type + ind] = array
    return dict_all


# create data_frame to convert dictionary keys to df
def multidimensional_data(triangle_dict_keys):
    df = pd.DataFrame.from_dict(triangle_dict_keys)
    return df


# create data_frame to convert dictionary array to df
def multidimensional_data_all(triangle_dict):
    dict_all = combine_dict(triangle_dict)
    df = pd.DataFrame.from_dict(dict_all)
    return df


def index_matrices(dict_all):
    index_dict = dict()  # returns the position in the list of arrays
    index_list = []  # same thing but in list
    all_matrix_list = []
    i = 0  # matrix position in the list
    for key, value in dict_all.items():
        all_matrix_list.append(value)
        index_dict[key] = i
        i = i + 1
        index_list.append(key)
    return index_dict, index_list, all_matrix_list


# Apply MDS to matrix
def mds_dim(all_matrix_list):
    from sklearn.manifold import MDS
    mds = MDS(random_state=0)
    matrix_transform = mds.fit_transform(all_matrix_list)
    return matrix_transform


# Split MDS data to separate lists to be able to compare them to each other
def split_mds(mds_all, index_list):
    mds_asd = []
    mds_asd_index = []
    mds_hc = []
    mds_hc_index = []
    mds_dmt = []
    mds_dmt_index = []
    mds_pcb = []
    mds_pcb_index = []
    for i in range(len(mds_all)):
        if 'HC' in index_list[i]:
            mds_hc.append(mds_all[i])
            mds_hc_index.append(index_list[i])
        elif 'ASD' in index_list[i]:
            mds_asd.append(mds_all[i])
            mds_asd_index.append(index_list[i])
        elif 'DMT' in index_list[i]:
            mds_dmt.append(mds_all[i])
            mds_dmt_index.append(index_list[i])
        elif 'PCB' in index_list[i]:
            mds_pcb.append(mds_all[i])
            mds_pcb_index.append(index_list[i])
        else:
            print(index_list[i], ' index is unexpected')
    return mds_hc, mds_hc_index, mds_asd, mds_asd_index, mds_dmt, mds_dmt_index, mds_pcb, mds_pcb_index
