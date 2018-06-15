#!/usr/bin/env python3

from flask import Flask, render_template, Response
import serial, time
import cv2
import threading
import numpy as np
from imutils.video import WebcamVideoStream

port = "/dev/ttyACM0"
ser = serial.Serial(port , 115200, timeout = 1)
time.sleep(5)

cx = []
speed_go = 255
porog = 1000
porog1 = 0
porog2 = 0
speed_blue = 0
speed = 255
K = 1
see_red = 0
see_blue = 0
x = 0
out_old = 0
i_main = 0
i_mail2arduino = 0
i_see_sign = 0
i_camera2inet = 0
time_main = time.time()
time_mail2arduino = time.time()
time_see_sign = time.time()
time_camera2inet = time.time()
fps_main = 0
fps_mail2arduino = 0
fps_see_sign = 0
fps_camera2inet = 0
pixel_ellips = 0
pixel_ellips_blue = 0

class sign:
    def __init__(self, way_in):
        self.sign_img = cv2.imread(way_in)
        self.sign_img_hsv = cv2.cvtColor(self.sign_img, cv2.COLOR_BGR2HSV)
        self.sign_img_inRange = cv2.inRange(self.sign_img_hsv, (0, 0, 0), (254, 254, 254))

sign_right = sign("/var/www/html/sign_right.png")
sign_left = sign("/var/www/html/sign_left.png")
sign_forward = sign("/var/www/html/sign_forward.png")

sign_direct = sign_right
direct = 0

cap = WebcamVideoStream(src=0).start()
for i in range(5): frame = cap.read()
frame = cap.read()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
frame_gray = cv2.inRange(hsv[420:,:, :], (0, 0, 0), (255, 255, 100))
frame_red = cv2.inRange(hsv[:, 320:, :], (0, 150, 30), (10, 255, 80))
frame_blue = cv2.inRange(hsv[:, 320:, :], (100, 220, 60), (150, 255, 255))

cv2.imwrite('/var/www/html/dgip_frame_all.png', frame)

def mail2arduino_pr1():
    print("Start arduino thread")
    global K, x, out_old, speed_go, speed, i_mail2arduino, fps_mail2arduino, time_mail2arduino
    while 1:
        local_x = x
        if(local_x >= 0): out = "L"
        else: out = "R"
        local_x = abs(int(local_x*K))

        if(local_x > 90): local_x = 90
        if(local_x < 10): out += "0" + str(local_x)
        else: out += str(local_x)

        if(speed >= 100): out += "F" + str(speed)
        elif(speed >= 10): out += "F0" + str(speed)
        else: out += "F00" + str(speed)

        if(out != out_old):
            ser.write(out.encode())
            time_out = time.time()

        if(time.time() - time_out > 2):
            ser.write("0000000".encode())
            time_out = time.time()
        out_old = out
        i_mail2arduino += 1
        if(time.time() - time_mail2arduino > 1):
            time_mail2arduino = time.time()
            fps_mail2arduino = i_mail2arduino
            i_mail2arduino = 0

def image2jpeg(image):
    ret, jpeg = cv2.imencode('.jpg', image)
    return jpeg.tobytes()

def camera2inet_pr2():
    print("Start inet thread")
    global frame_gray, frame, frame_red, hsv, i_camera2inet, time_camera2inet,  fps_camera2inet, direct, pixel_ellips_blue
    global fps_main, fps_see_sign, fps_mail2arduino, fps_camera2inet, pixel_ellips, see_red, sign_direct
    global porog1, porog2, see_blue
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    def gen_gray():
        while True:
            frame_inet = cv2.inRange(hsv[460:, :, :], (0, 0, 0), (150, 255, 80))
            cv2.putText(frame_inet,"fps: "+str(fps_main)+" "+str(fps_see_sign)+" "+str(fps_mail2arduino), (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)
            frameinet = image2jpeg(frame_inet)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameinet + b'\r\n\r\n')
    def gen_frame():
        while True:
            frame_inet = frame
            frameinet = image2jpeg(frame_inet)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameinet + b'\r\n\r\n')
    def gen_red():
        while True:
            cv2.putText(frame_red,"red_see: "+str(see_red), (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            cv2.putText(frame_red,"red_pixel: "+str(pixel_ellips), (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            frameinet = image2jpeg(frame_red)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameinet + b'\r\n\r\n')
    def gen_direct():
        while True:
            frameinet = image2jpeg(sign_direct)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameinet + b'\r\n\r\n')
    def gen_blue():
        while True:
            cv2.putText(frame_blue,"direct: "+str(direct), (0,10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)
            cv2.putText(frame_blue,"pixel_ellips_blue: "+str(pixel_ellips_blue), (0,20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255,255,255), 1)
            frameinet = image2jpeg(frame_blue)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameinet + b'\r\n\r\n')

    @app.route('/video_frame')
    def video_frame():
        return Response(gen_frame(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route('/video_line')
    def video_line():
        return Response(gen_gray(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route('/video_red')
    def video_red():
        return Response(gen_red(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route('/video_direct')
    def video_direct():
        return Response(gen_direct(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    @app.route('/video_blue')
    def video_blue():
        return Response(gen_blue(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    time.sleep(0.3)
    i_camera2inet += 1
    if(time.time() - time_camera2inet > 1):
        time_camera2inet = time.time()
        fps_camera2inet = i_camera2inet
        i_camera2inet = 0

    app.run(host='0.0.0.0', debug=False,threaded=True)

def see_sign_pr3():
    print("Start see red thread")
    global K, see_blue, pixel_ellips, speed_blue, pixel_ellips_blue, see_red, hsv, frame_red, i_see_sign, time_see_sign, fps_see_sign, direct, sign_direct, frame_blue
    print(frame_red.dtype)
    time_last_see_red = time.time()-10
    search_red = True
    time_last_see_blue = time.time()-10
    search_blue = True
    time_see_sign_forward = time.time()-10
    pre_direct = 0
    while 1:
        frame_red = cv2.inRange(hsv[:, 320:, :], (10, 10, 30), (10, 255, 255))
        frame_blue = cv2.inRange(hsv[:, 320:, :], (90, 200, 50), (150, 255, 255))
        if(search_red):
            frame_copy = frame_red.copy()
            _, con, hierarchy = cv2.findContours(frame_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for i in con:
                if len(i)>10:
                    ellipse = cv2.fitEllipse(i)
                    _, y1 = ellipse[0]
                    _, y2 = ellipse[1]
                    pixel_ellips = abs(y2-y1)*0.3 + 0.7 * pixel_ellips
                    if(pixel_ellips > 1000):
                        pixel_ellips = 0
                        see_red = 1
                        search = False
                        time_last_see_red = time.time()
                        cv2.ellipse(frame_red, ellipse, (255,0,0), 2)
                    else: see_red = 0
                    break
                else:
                    see_red = 0
        if(time.time() - time_last_see_red <= 10):
            see_red = 1
        if(time.time() - time_last_see_red > 10):
            see_red = 0
            K = 0.1
        if(time.time() - time_last_see_red >= 12):
            K = 1
        if(time.time() - time_last_see_red >= 20):
            search_red = True

        if(search_blue and np.sum(frame_blue)>1200000):
            see_blue = 1
            frame_copy = frame_blue.copy()
            _, con, hierarchy = cv2.findContours(frame_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            max_con = []
            for i in range(len(con)):
                if len(con[i])>len(max_con):
                    max_con = con[i]

            ellipse = cv2.fitEllipse(max_con)

            x1, y1 = ellipse[0]
            x2, y2 = ellipse[1]

            t1 = ((int(x1)-int(x2/2)), (int(y1)-int(y2/2)))
            t2 = ((int(x1)+int(x2/2)), (int(y1)+int(y2/2)))

            pixel_ellips_blue = abs((int(y1)-int(y2/2))-(int(y1)+int(y2/2)))*0.15 + 0.85 * pixel_ellips_blue
            cv2.rectangle(frame_blue, t1, t2, (100, 100, 100), 3)

            if(pixel_ellips_blue < 90 and pixel_ellips_blue > 70):
                time_last_see_blue = time.time()

                pre_sign_direct = frame_blue[int(y1)-int(y2/2):int(y1)+int(y2/2), int(x1)-int(x2/2):int(x1)+int(x2/2)]
                if(pre_sign_direct.shape[0]>0 and pre_sign_direct.shape[1]>0): sign_direct = cv2.resize(pre_sign_direct, (64, 64), interpolation=cv2.INTER_AREA)

                sum_matr = [np.sum(sign_direct*sign_left.sign_img_inRange),
                            np.sum(sign_direct*sign_forward.sign_img_inRange),
                            np.sum(sign_direct*sign_right.sign_img_inRange)]

                if(np.argmax(sum_matr) == 2):
                    direct += 1
                elif(np.argmax(sum_matr) == 0):
                    direct -= 1
                elif(np.argmax(sum_matr) == 1):
                    direct == 0
                    K = 0.1
                    time_see_sign_forward = time.time()
        else :
            see_blue = 0
        if(time.time() - time_last_see_blue > 15):
            direct = 0
        if(time.time() - time_see_sign_forward > 15):
            K = 1
        i_see_sign += 1
        if(time.time() - time_see_sign > 1):
            time_see_sign = time.time()
            fps_see_sign = i_see_sign
            i_see_sign = 0

pr2 = threading.Thread(target=camera2inet_pr2)
pr2.daemon = True
pr2.start()
time.sleep(5)

pr1 = threading.Thread(target=mail2arduino_pr1)
pr1.daemon = True
pr1.start()
pr3 = threading.Thread(target=see_sign_pr3)
pr3.daemon = True
pr3.start()

while 1:
    frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_gray = cv2.inRange(hsv[460:, :, :], (0, 0, 0), (150, 255, 128))
    if(np.sum(frame_gray) > porog and see_red != 1):
        if(see_blue != 1): speed = 255
        else: speed = 120
        cx.clear()
        min = 1000
        _, contours, hierarchy = cv2.findContours(frame_gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i in contours:
            if(i is not None):
                area = cv2.contourArea(i)
                if(area>=250):
                    M = cv2.moments(i)
                    pre_x = int(M['m10']/M['m00'])
                    cx.append(pre_x)
                    if(direct == 0):
                        if(abs(pre_x-320)<min):
                            min = abs(pre_x-320)
                            x = 320 - pre_x
                    elif(direct > 0):
                        if(abs(pre_x-640)<min):
                            min = abs(pre_x-640)
                            x = 320 - pre_x
                    elif(direct < 0):
                        if(pre_x<min):
                            min = pre_x
                            x = 320 - pre_x
    else:
        speed = 0
    i_main += 1
    if(time.time() - time_main > 1):
        time_main = time.time()
        fps_main = i_main
        i_main = fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))