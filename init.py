import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker
import os

# import atlas_file
atlas_file = nib.load(
    '/Users/mioulin/nilearn_data/schaefer_2018/Schaefer2018_100Parcels_7Networks_order_FSLMNI152_2mm.nii.gz')
with open('/Users/mioulin/nilearn_data/schaefer_2018/Schaefer2018_100Parcels_7Networks_order.txt', 'r') as f:
    labels = f.read().split('\n')
masker = NiftiLabelsMasker(labels_img=atlas_file, standardize=True, verbose=1,
                           memory="nilearn_cache", memory_level=2)
labels = [x.split('\t')[1][10:] for x in labels]

# Directory path to HC file
os.chdir('/Users/mioulin/Desktop/DATA/ABIDE/SCANS/HC')
rest_files_hc = [x for x in os.listdir('.') if x.endswith('.nii')]

# Directory path to ASD file
os.chdir('/Users/mioulin/Desktop/DATA/ABIDE/SCANS/ASD')
rest_files_asd = [x for x in os.listdir('.') if x.endswith('.nii')]

# Directory path to DMT file

os.chdir('/Users/mioulin/Desktop/DATA/DMT/SCANS/DMT')
rest_files_dmt = [x for x in os.listdir('.') if x.endswith('.nii.gz')]

# Directory path to PCB file

os.chdir('/Users/mioulin/Desktop/DATA/DMT/SCANS/PCB')
rest_files_pcb = [x for x in os.listdir('.') if x.endswith('.nii.gz')]
