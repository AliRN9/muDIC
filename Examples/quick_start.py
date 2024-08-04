# This allows for running the example when the repo has been cloned
import sys
from os.path import abspath

sys.path.extend([abspath(".")])
sys.path.append('/home/user/Desktop/NIR/muDIC')
import muDIC as dic
import logging
import os

# Set the amount of info printed to terminal during analysis
logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s', level=logging.INFO)

# Path to folder containing images
# path = r'./example_data/' # Use this formatting on Linux and Mac OS
# path = r'c:\path\to\example_data\\'  # Use this formatting on Windows
path = '/home/user/Desktop/NIR/Data/GoreTexDivno08mm1_1/Image_Selection/'
# Generate image instance containing all images found in the folder
images, len_images = dic.IO.image_stack_from_folder(path, file_type='.tif')
# images.set_filter(dic.filtering.lowpass_gaussian, sigma=1.)


# Generate mesh
mesher = dic.Mesher(deg_e=3, deg_n=3, type="spline")

# If you want to see use a GUI, set GUI=True below
# mesh = mesher.mesh(images,Xc1=316,Xc2=523,Yc1=209,Yc2=1055,n_ely=36,n_elx=9, GUI=False)
mesh = mesher.mesh(images, GUI=True)
# print(f'{mesh.n_elx=}')
# print(f'{mesh.n_ely=}')
# Instantiate settings object and set some settings manually
settings = dic.DICInput(mesh, images)
settings.max_nr_im = 500
# settings.ref_update = [40, 80, 120]
settings.maxit = 1000
settings.tol = 1.e-7
settings.pad = 0
settings.interpolation_order = 4
# If you want to access the residual fields after the analysis, this should be set to True
settings.store_internals = True

# This setting defines the behaviour when convergence is not obtained
settings.noconvergence = "ignore"

# Instantiate job object
job = dic.DICAnalysis(settings)

# Running DIC analysis
dic_results = job.run()

# Calculate field values
fields = dic.post.viz.Fields(dic_results, upscale=10)

# Show a field
viz = dic.Visualizer(fields, images=images )

viz.show(field="displacement", component=(1, 1), frame=49,
             save_path="/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/disp_img_49.png")
viz.show(field="displacement", component=(0, 0), frame=49,
             save_path="/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/disp_img_x_49.png")

viz.show(field="deformationgradient", component=(0, 0), frame=49,
             save_path="/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/def_img_x_49.png")

viz.show(field="deformationgradient", component=(1, 1), frame=49,
             save_path="/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/def_img_y_49.png")

viz.show(field="deformationgradient", component=(1, 0), frame=49,
             save_path="/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/def_img_xy_49.png")


# for i in range(len_images):
#     # Uncomment the line below to see the results
#     #     viz.show(field="deformationgradient", component = (1,1), frame=-1)
#
#     # The save_path flag can be used to save results instead of showing them
#
#     viz.show(field="displacement", component=(1, 1), frame=i,
#              save_path=f"/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/img_{i}.png")
#
#     # Uncomment the line below to export the results to CSV files
#     dic.IO.readWriteUtils.exportCSV(fields, f'/home/user//Desktop/NIR/Data/GoreTexDivno08mm1_1/DIC_output/csv_{i}', i)
