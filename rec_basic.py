import cv2

# 웹캠 열기 (기본적으로 첫 번째 카메라 장치를 사용)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("웹캠을 열 수 없습니다.")
    exit()

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        break

    # 프레임을 윈도우에 표시
    cv2.imshow('Webcam Stream', frame)

    # 'q' 키를 누르면 스트림 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 및 윈도우 닫기
cap.release()
cv2.destroyAllWindows()
