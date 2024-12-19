import cv2
import numpy as np
# from requests.packages import target

target_img = cv2.imread('target.png')
reference_img = cv2.imread('reference.png')

lab_target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2LAB)
lab_reference_img = cv2.cvtColor(reference_img, cv2.COLOR_BGR2LAB)

target_L = lab_target_img[:, :, 0]
target_a = lab_target_img[:, :, 1]
target_b = lab_target_img[:, :, 2]

reference_L = lab_reference_img[:, :, 0]
reference_a = lab_reference_img[:, :, 1]
reference_b = lab_reference_img[:, :, 2]

mean_target_L = np.mean(target_L)
mean_reference_L = np.mean(reference_L)
gamma_value= 1.0
print("mean_target_L: ", mean_target_L)
print("mean_reference_L: ", mean_reference_L)

if mean_target_L < mean_reference_L:
    print("target 이미지가 어둡습니다.")
    complement_value =1-mean_target_L / mean_reference_L
    print("mean_target_L/mean_reference_L: ",100*complement_value,"%")
    gamma_transform_target_L = np.uint8(255*np.float32(mean_target_L)/255 ** (1/(gamma_value+complement_value)))
else:
    print("target 이미지가 밝습니다.")
    complement_value = 1-mean_reference_L / mean_target_L
    print("mean_reference_L/mena_target",100*complement_value, "%")
    gamma_transform_target_L= np.uint8(255*np.float32(mean_target_L)/255 ** (1/(gamma_value-complement_value)))

lab_target_img[:, :, 0] = gamma_transform_target_L
lab_target_img[:, :, 1] = target_a
lab_target_img[:, :, 2] = target_b

convert_rgb_target_img = cv2.cvtColor(lab_target_img, cv2.COLOR_LAB2BGR)
cv2.imshow("convert",target_L)
cv2.imshow("target_img", target_img)
cv2.imshow("convert_rgb_target_img", np.uint8(convert_rgb_target_img/255.0))
cv2.imshow("reference",reference_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

