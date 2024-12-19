import cv2
import json

# JSON 파일 읽기
config_file = "config_cam.json"
try:
    with open(config_file, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"{config_file} 파일을 열 수 없습니다!")
    exit(-1)

# 설정값 읽기
frame_width = config.get("frame_width", 640)
frame_height = config.get("frame_height", 480)
fps = config.get("fps", 30)
orientation = config.get("orientation", "h")  # "h" 또는 "v"
autofocus = config.get("autofocus", True)  # True: 활성화, False: 비활성화
focus_value = config.get("focus", 0)  # 수동 포커스 값 (autofocus가 False일 때 적용)
white_balance_auto = config.get("white_balance_auto", True)  # True: 자동, False: 수동
white_balance_value = config.get("white_balance_value", 4000)  # 수동 화이트 밸런스 값 (Kelvin)
output_file = config.get("output_file", "output.mp4")  # 저장 파일 이름

# 카메라 열기
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)  # 0은 기본 카메라
if not cap.isOpened():
    print("카메라를 열 수 없습니다!")
    exit(-1)

# 카메라 해상도 및 FPS 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

# 화이트 밸런스 설정
if white_balance_auto:  # 자동 화이트 밸런스
    if cap.set(cv2.CAP_PROP_AUTO_WB, 1):
        print("화이트 밸런스를 자동으로 설정했습니다.")
    else:
        print("자동 화이트 밸런스를 설정할 수 없습니다.")
else:  # 수동 화이트 밸런스
    if cap.set(cv2.CAP_PROP_AUTO_WB, 0) and cap.set(cv2.CAP_PROP_WB_TEMPERATURE, white_balance_value):
        print(f"화이트 밸런스를 수동으로 설정했습니다: {white_balance_value}K")
    else:
        print("수동 화이트 밸런스를 설정할 수 없습니다!")

# 비디오 파일 저장을 위한 VideoWriter 객체 생성
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
if orientation == "v":
    video_size = (frame_height, frame_width)  # 세로 모드에서는 크기를 반전
else:
    video_size = (frame_width, frame_height)

video_writer = cv2.VideoWriter(output_file, fourcc, fps, video_size)

if not video_writer.isOpened():
    print("비디오 파일을 열 수 없습니다!")
    exit(-1)

# 오토 포커스 설정
if cap.set(cv2.CAP_PROP_AUTOFOCUS, 1 if autofocus else 0):
    print(f"오토 포커스 설정 완료: {'활성화' if autofocus else '비활성화'}")
else:
    print("오토 포커스를 설정할 수 없습니다!")

# 수동 포커스 설정 (오토 포커스 비활성화된 경우)
if not autofocus and cap.set(cv2.CAP_PROP_FOCUS, focus_value):
    print(f"포커스를 수동으로 설정했습니다: {focus_value}")
elif not autofocus:
    print("포커스를 설정할 수 없습니다!")
print("loop")
# 메인 루프
while True:
    # 카메라에서 프레임 캡처
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다!")
        break

    # 세로 모드라면 프레임을 소프트웨어적으로 회전
    if orientation == "v":
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    # 비디오 파일에 프레임 저장
    video_writer.write(frame)

    # 화면에 프레임 출력
    
    cv2.imshow("Recording...", frame)

    # 'q'를 누르면 녹화 종료
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("녹화를 종료합니다.")
        break

# 자원 해제
cap.release()
video_writer.release()
cv2.destroyAllWindows()
