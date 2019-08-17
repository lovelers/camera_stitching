import cv2
import numpy as np

data_dir            = './data1/'

####0_decoding_video.py###############
video_left          = data_dir + 'left.mp4'
video_right         = data_dir + 'right.mp4'
video_output_left   = data_dir + 'left/'
video_output_right  = data_dir + 'right/'

#####1_rotate_video_frame.py ############
rotate_dir          = data_dir + 'left/'
rotate_angle        = 180

#####2_concatenate_video.py #############
concatenate_left    = 11
concatenate_right   = 10
concatenate_input1  = video_output_left
concatenate_input2  = video_output_right
concatenate_output  = data_dir + 'concatenate/'

#####3_image_3d_rotate.py #############
rotate_3d_src       = data_dir + 'left/'
rotate_3d_angle     = 25
rotate_3d_output    = data_dir + 'left%d/'%rotate_3d_angle

#####4_remove_black.py ###############
black_dir           = rotate_3d_output
black_width         = 1132
black_height        = 720
black_dir_src       = rotate_3d_output
black_dir_output    = rotate_3d_output + 'output/'

#####5_generate_matrix.py ###############
left_points         = np.array([[1075, 118], [ 1072, 365], [1089, 663], [874, 110], [ 872, 367], [ 860, 502]])
right_points        = np.array([[ 325,  95], [ 331,  358], [ 354, 669], [ 36, 47],[ 42, 367], [ 36, 534]])
perspective_output  = data_dir + 'output/'
perspective_input1  = black_dir_output
perspective_input2  = data_dir + 'right/'
perspective_min_row = 58
perspective_max_row = 664
perspective_min_col = 0
perspective_max_col = 1964

#####encoding py ##################
video_fourcc        = cv2.VideoWriter_fourcc('F', 'M', 'P', '4')
video_framerate     = 30

video_output_src    = data_dir + 'output/'
video_output_path   = data_dir + 'video_output.mp4'
video_output_size   = (perspective_max_col - perspective_min_col, perspective_max_row - perspective_min_row)

video_input_src     = concatenate_output
video_input_path    = data_dir + 'video_input.mp4'
video_input_size    = (2560, 720)


