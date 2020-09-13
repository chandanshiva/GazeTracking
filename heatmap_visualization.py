import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import cv2

# To check the fps of camera
# video = cv2.VideoCapture('anim.mp4')
# n=0
# while True:
#     _, frame = video.read()
#     size = frame.shape
#
#     cv2.imshow("Demo", frame)
#     n = n + 1
#
#     if cv2.waitKey(33) == 27:
#         break
#
# print(size) #>> (720, 1280, 3)
# print(n) #>> 30fps(150 for 5sec)

# data = pd.read_csv('myrecorded_data.csv')

# Accuracy test
data = pd.read_csv('Accuracy Test/myrecorded_data_accuracy_test.csv')
# print(data['quadrant'].count()) #157
# print(data['gaze_center_x'].max()) #674
# print(data['gaze_center_y'].max()) #334
# print(data['gaze_center_x'].min()) #627
# print(data['gaze_center_y'].min()) #317
# print(data['gaze_direction_points'].max()) >> (999, 440)
# print(data['gaze_direction_points'].min()) >> (1000, 442)
# print(data['quadrant'].value_counts())
# 3rd    62
# 2nd    55
# 1st    20
# 4th    20
# Name: quadrant, dtype: int64

# Optional quadrant select based on only gaze cordinates
# first_values_x = (90 < data["gaze_center_x"] < 110)
# second_values_x = (1170 < data["gaze_center_x"] < 1190)
# third_values_x = (90 < data["gaze_center_x"] < 110)
# fourth_values_x = (1170 < data["gaze_center_x"] < 1190)
# first_values_y = (90 < data["gaze_center_y"] < 110)
# second_values_y = (90 <= data["gaze_center_y"] < 110)
# third_values_y = (610 <= data["gaze_center_y"] < 630)
# fourth_values_y = (610 <= data["gaze_center_y"] < 630)

first = data.loc[(data["quadrant"] == '1st')]
second = data.loc[(data["quadrant"] == '2nd')]
third = data.loc[(data["quadrant"] == '3rd')]
fourth = data.loc[(data["quadrant"] == '4th')]
center = []
# print(first[["quadrant", "gaze_center_x", "gaze_center_y"]],'\n',
#       second[["quadrant", "gaze_center_x", "gaze_center_y"]],'\n',
#       third[["quadrant", "gaze_center_x", "gaze_center_y"]],'\n',
#       fourth[["quadrant", "gaze_center_x", "gaze_center_y"]])

# print(first[["gaze_center_x", "gaze_center_y"]].mean(),'\n',
#       second[["gaze_center_x", "gaze_center_y"]].mean(),'\n',
#       third[["gaze_center_x", "gaze_center_y"]].mean(),'\n',
#       fourth[["gaze_center_x", "gaze_center_y"]].mean())

# print(first[["gaze_center_x", "gaze_center_y"]].max(),'\n',
#       second[["gaze_center_x", "gaze_center_y"]].max(),'\n',
#       third[["gaze_center_x", "gaze_center_y"]].max(),'\n',
#       fourth[["gaze_center_x", "gaze_center_y"]].max())


# print(data) # https://www.youtube.com/watch?v=I2wURDqiXdM (6:41)
#       Unnamed: 0  ...                                 translation_Vector
# 0              0  ...  [[ 863.34637839]\n [ -32.67920496]\n [1592.431...
# 1              1  ...  [[ 817.38880298]\n [ -14.00503032]\n [1462.081...
# 2              2  ...  [[ 820.52479096]\n [ -15.95812259]\n [1465.831...
# 3              3  ...  [[ 827.23877241]\n [ -19.73590627]\n [1490.114...
# 4              4  ...  [[ 823.86271328]\n [ -17.00272724]\n [1472.282...
# ...          ...  ...                                                ...
# 2335        2335  ...  [[ 867.03268208]\n [ 138.76486468]\n [1440.506...
# 2336        2336  ...  [[ 893.41867886]\n [ 159.35244253]\n [1503.704...
# 2337        2337  ...  [[ 884.39457354]\n [ 153.8477118 ]\n [1488.534...
# 2338        2338  ...  [[ 970.43273265]\n [ 153.09597493]\n [1680.323...
# 2339        2339  ...  [[ 897.64744054]\n [ 165.73688467]\n [1502.533...
#
# [2340 rows x 9 columns]



# sns.set_theme()


# Custom plot options are:
# sns.jointplot(x=data["gaze_center_x"], y=data["gaze_center_y"], kind='scatter')
# sns.jointplot(x=data["gaze_center_x"], y=data["gaze_center_y"],hue=data["quadrant"], kind='scatter', s=200, color='m', edgecolor="skyblue", linewidth=2)


# sns.barplot(x = data.iloc[:, 0], y = "quadrant", data = data)

# sns.catplot(x = data. iloc[:, 0], y = "quadrant", data = data)
# sns.catplot(data=data, kind="swarm", x="gaze_center_x", y="gaze_center_y", hue="quadrant", dodge=True)

# sns.pairplot(pairplotdata=data, hue="quadrant")

# sns.displot(data=data, x=data["gaze_center_x"], y=data["gaze_center_y"],hue=data["quadrant"], kind="kde")

# plt.show()

# def update_lines(num, data_lines, lines):
#     for line, data in zip(lines, data_lines):
#         # NOTE: there is no .set_data() for 3 dim data...
#         line.set_data(data["gaze_center_x"],data["gaze_center_y"])
#         line.set_3d_properties(data.col["gaze_center_x"],data["gaze_center_y"])
#     return lines
#
# # Attaching 3D axis to the figure
# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")
#
# # Creating fifty line objects.
# # NOTE: Can't pass empty arrays into 3d version of plot()
# lines = [ax.plot(data. iloc[:, 0], data["gaze_center_x"], data["gaze_center_y"])[0] for dat in data]
#
# # Setting the axes properties
# ax.set_xlim3d([0.0, 1.0])
# ax.set_xlabel('X')
#
# ax.set_ylim3d([0.0, 1.0])
# ax.set_ylabel('Y')
#
# ax.set_zlim3d([0.0, 1.0])
# ax.set_zlabel('Z')
#
# ax.set_title('3D Test')
#
# # Creating the Animation object
# line_ani = animation.FuncAnimation(
#     fig, update_lines, 50, fargs=(data, lines), interval=50)
#
# plt.show()