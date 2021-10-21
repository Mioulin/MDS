from func import *
from init import *
from sklearn.manifold import MDS
from matplotlib import pyplot as plt
import pandas as pd
import os

# Create dictionary with all data
all_corr_matrix = dict()
all_corr_matrix['HC'] = dict()
all_corr_matrix['ASD'] = dict()
all_corr_matrix['DMT'] = dict()
all_corr_matrix['PCB'] = dict()

os.chdir('/Users/mioulin/Desktop/DATA/ABIDE/SCANS/HC')
rest_files_hc = [x for x in os.listdir('.') if x.endswith('.nii')]
for file in rest_files_hc:
    all_corr_matrix['HC'][file[5:12]] = get_corr_matrix(file)
os.chdir('/Users/mioulin/Desktop/DATA/ABIDE/SCANS/ASD')
rest_files_asd = [x for x in os.listdir('.') if x.endswith('.nii')]
for file in rest_files_asd:
    all_corr_matrix['ASD'][file[5:12]] = get_corr_matrix(file)
os.chdir('/Users/mioulin/Desktop/DATA/DMT/SCANS/DMT')
rest_files_dmt = [x for x in os.listdir('.') if x.endswith('.nii.gz')]
for file in rest_files_dmt:
    all_corr_matrix['DMT'][file[51:53]] = get_corr_matrix(file)
os.chdir('/Users/mioulin/Desktop/DATA/DMT/SCANS/PCB')
rest_files_pcb = [x for x in os.listdir('.') if x.endswith('.nii.gz')]
for file in rest_files_pcb:
    all_corr_matrix['PCB'][file[51:53]] = get_corr_matrix(file)

# Create dictionary wih upper triangle of FC matrix and keys which correspond to data_type(HC/ASD/DMT/PCB)
triangle_dict = upper_triangle(all_corr_matrix)
dict_all = combine_dict(triangle_dict)
index_dict, index_list, all_matrix_list = index_matrices(dict_all)
mds_hurray = mds_dim(all_matrix_list)
mds_hc, mds_hc_index, mds_asd, mds_asd_index, mds_dmt, mds_dmt_index, mds_pcb, mds_pcb_index = split_mds(mds_hurray,
                                                                                                         index_list)
mds_hc_np = np.array(mds_hc)
mds_asd_np = np.array(mds_asd)
mds_dmt_np = np.array(mds_dmt)
mds_pcb_np = np.array(mds_pcb)

# Create 2D plot to show MDS results
fig = plt.figure(2, (10, 4))
ax = fig.add_subplot(122)
plt.scatter(mds_asd_np[:, 0], mds_asd_np[:, 1], c='red')
plt.scatter(mds_hc_np[:, 0], mds_hc_np[:, 1], c='blue')
plt.scatter(mds_dmt_np[:, 0], mds_dmt_np[:, 1], c='green')
plt.scatter(mds_pcb_np[:, 0], mds_pcb_np[:, 1], c='purple')
plt.title('Embedding in 2D')
fig.subplots_adjust(wspace=.4, hspace=0.5)
plt.show()
