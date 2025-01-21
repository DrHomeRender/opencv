import cv2
import numpy as np
import glob
import pickle
import json

# 체스판 크기
CHECKERBOARD = (8, 5)
images = glob.glob('img/*.jpg')

if not images:
    print("Error: No images found in the specified path.")
    exit()

# 캘리브레이션 함수
def calibrate_camera(image_paths, checkerboard_size):
    object_points = []
    image_points = []

    objp = np.zeros((checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

    for fname in image_paths:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)

        if ret:
            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1),
                criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            image_points.append(corners2)
            object_points.append(objp)
        else:
            print(f"Failed to find corners in {fname}")

    ret, camera_matrix, distortion_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        object_points, image_points, gray.shape[::-1], None, None)

    return camera_matrix, distortion_coeffs

# 보정 함수
def undistort_image(img, camera_matrix, distortion_coeffs):
    h, w = img.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coeffs, (w, h), 1, (w, h))
    undistorted_img = cv2.undistort(img, camera_matrix, distortion_coeffs, None, new_camera_matrix)
    x, y, w, h = roi
    return undistorted_img[y:y+h, x:x+w]

# 캘리브레이션 수행
camera_matrix, distortion_coeffs = calibrate_camera(images, CHECKERBOARD)

# 결과 저장 (Pickle 형식)
with open('camera_calibration_data.pkl', 'wb') as f:
    pickle.dump({'camera_matrix': camera_matrix, 'distortion_coeffs': distortion_coeffs}, f)

# 결과 저장 (JSON 형식)
calibration_data = {
    "camera_matrix": camera_matrix.tolist(),
    "distortion_coeffs": distortion_coeffs.tolist()
}

with open('camera_calibration_data.json', 'w') as f:
    json.dump(calibration_data, f, indent=4)

# 결과 저장 (텍스트 형식)
np.savetxt('camera_matrix.txt', camera_matrix, fmt='%0.6f')
np.savetxt('distortion_coeffs.txt', distortion_coeffs, fmt='%0.6f')

print("Calibration data saved to 'camera_calibration_data.pkl', 'camera_calibration_data.json', and text files.")

# 보정된 이미지 시각화
img = cv2.imread(images[0])
undistorted_img = undistort_image(img, camera_matrix, distortion_coeffs)

cv2.imshow('Original', img)
cv2.imshow('Undistorted', undistorted_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
