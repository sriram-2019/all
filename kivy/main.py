from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
import cv2
import requests
import webbrowser
import certifi  # Ensure SSL certs are correct
from kivy.graphics.texture import Texture

class QRScannerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Live Camera Feed
        self.image = Image()
        self.layout.add_widget(self.image)

        # Scan Button
        self.scan_button = Button(text="Scan QR Code", size_hint=(1, 0.2))
        self.scan_button.bind(on_press=self.start_scan)
        self.layout.add_widget(self.scan_button)

        self.capture = None
        self.qr_detector = cv2.QRCodeDetector()  # Initialize QR Code Detector
        return self.layout

    def start_scan(self, instance):
        if self.capture is None:
            self.capture = cv2.VideoCapture(0)  # Open camera
            Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)

            # Detect and decode QR code
            decoded_data, points, _ = self.qr_detector.detectAndDecode(frame)

            if decoded_data:
                print(f"QR Code Data: {decoded_data}")

                # Send request with custom User-Agent
                headers = {"User-Agent": "KivyApp"}
                try:
                    response = requests.get(decoded_data, headers=headers, timeout=5, verify=certifi.where())  # Fix SSL error
                    print(f"Redirecting to: {response.url}")

                    # Open the redirected link in browser
                    webbrowser.open(response.url)
                except requests.exceptions.SSLError as e:
                    print(f"SSL Error: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"Request Error: {e}")

                self.capture.release()
                self.capture = None
                Clock.unschedule(self.update)
                return

            # Convert to Kivy Texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
            self.image.texture = texture

    def on_stop(self):
        if self.capture:
            self.capture.release()


if __name__ == "__main__":
    QRScannerApp().run()
