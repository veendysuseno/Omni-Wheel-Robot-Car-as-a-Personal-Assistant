import cv2
import motor as motor

Color_Lower = (36, 130, 46)
Color_Upper = (113, 255, 255)
Frame_Width = 640
Frame_Height = 240

camera = cv2.VideoCapture(0)

try:
    while True:
        (_, frame) = camera.read()

        # Lakukan blur pada frame
        frame = cv2.GaussianBlur(frame, (11, 11), 0)

        # Ubah frame ke ruang warna HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Buat mask biner berdasarkan warna hijau
        mask = cv2.inRange(hsv, Color_Lower, Color_Upper)

        # Temukan kontur dalam mask
        (contours, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Inisialisasi pusat massa objek
        center = None

        if len(contours) > 0:
            # Pilih kontur dengan area terbesar
            c = max(contours, key=cv2.contourArea)

            # Temukan lingkaran terkecil yang melingkupi kontur
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # Hitung momen untuk mendapatkan pusat massa
            M = cv2.moments(c)

            try:
                # Hitung pusat massa objek
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # Gambar lingkaran di sekitar objek dan titik pusat massa
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # Kontrol maju/mundur berdasarkan radius objek
                if radius < 90:
                    motor.forward()
                elif radius > 100:
                    motor.backward()
                else:
                    motor.stop()

                # Kontrol belok kanan/kiri berdasarkan posisi objek di frame
                if center[0] > Frame_Width/2 + 50:  # Toleransi lebih besar untuk gerakan kanan
                    motor.turnRight()
                elif center[0] < Frame_Width/2 - 50:  # Toleransi lebih besar untuk gerakan kiri
                    motor.turnLeft()
                else:
                    motor.stop()

            except:
                pass

        # Tampilkan frame jika diperlukan
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

finally:
    motor.cleanup()
    camera.release()
    cv2.destroyAllWindows()
