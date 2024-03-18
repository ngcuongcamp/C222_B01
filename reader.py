from libs.libs import cv2, decode, zxingcpp, ZBarSymbol

path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)


def read_code_wechat(frames):
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            return data[0]
    return read_code_pyzbar(frames)


def read_code_pyzbar(frames):
    for frame in frames:
        decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            return decoded_data[0].data.decode("utf-8")
    return read_code_zxingcpp(frames)


def read_code_zxingcpp(frames):
    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            return data_decodeded[0].text
    return None


def read_looper(self, frame):
    # print(self.MIN_THRESH, self.MAX_THRESH, self.THRESH_JUMP)
    for threshold in range(self.MIN_THRESH, self.MAX_THRESH, self.THRESH_JUMP):
        _, thresh = cv2.threshold(frame, threshold, self.MAX_THRESH, cv2.THRESH_BINARY)
        # print('loop 3')
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            return data[0]
    return None


def process_frame(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        self.BLOCK_SIZE_1,
        self.C1,
    )

    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, thresh, opened, erosion, dilation]
