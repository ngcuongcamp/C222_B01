import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import zxingcpp


path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)


def read_code_wechat(frames):
    print("wechat working")
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            return data[0]
    return read_code_pyzbar(frames)


def read_code_pyzbar(frames):
    print("pyzbar working")
    for frame in frames:
        decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
    return read_code_zxingcpp(frames)


def read_code_zxingcpp(frames):
    print("zxingcpp working")

    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
    return None


image = cv2.imread("./images/2024-03-20 14-18-34.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_AREA)
# cropped_image = gray[120:550, 150:640]
image_crop = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_AREA)
# 640 X 480


def loop_to_die(frame):
    for threshold in range(0, 255, 3):
        huong = (3, 3)
        filt = cv2.GaussianBlur(src=frame, ksize=huong, sigmaX=5, sigmaY=5)
        # gray = cv2.cvtColor(filt, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(filt, threshold, 210, cv2.THRESH_BINARY)

        #   data, points = detector.detectAndDecode(frame)
        #   if len(data) > 0:
        #       return data[0]

        data = read_code_wechat([thresh])

        print("test ", data)

        if data is not None:
            # print("test loop", data)
            break
        cv2.imshow("thresh", thresh)
        cv2.waitKey(1)
    return None


# ok, We will find solution together.
# let's find a thresh value and use it to readcode
data = None
i = 0
while i < 5:
    print("looper")
    i = i + 1
    data = read_code_wechat([image_crop])
    if data is not None:
        break

if data is None:
    data = loop_to_die(image_crop)
    print("loop here", data)


print(data)
cv2.imshow("image", image)
cv2.waitKey(0)
