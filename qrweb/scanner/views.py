import cv2
import numpy as np
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

@csrf_exempt
def qr_scanner(request):
    return render(request, "qr_scanner.html")

@csrf_exempt
def qr_redirect(request):
    if request.method == "POST":
        data_url = request.POST.get("image")
        source = request.POST.get("source", "unknown")  # ✅ Get the source identifier

        if not data_url:
            return JsonResponse({"status": "error", "message": "No image data received."})

        try:
            # Extract base64 image data
            if "," in data_url:
                _, encoded = data_url.split(",", 1)
            else:
                return JsonResponse({"status": "error", "message": "Invalid image format."})

            # Decode image
            image_data = base64.b64decode(encoded)
            np_arr = np.frombuffer(image_data, np.uint8)

            if np_arr.size == 0:
                return JsonResponse({"status": "error", "message": "Decoded image is empty."})

            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                return JsonResponse({"status": "error", "message": "Failed to decode image."})

            # QR Code Detection
            qr_detector = cv2.QRCodeDetector()
            decoded_data, points, _ = qr_detector.detectAndDecode(frame)

            if decoded_data:
                print(f"Scanned QR Code URL: {decoded_data}")  # ✅ Print scanned URL
                print(f"Source: {source}")  # ✅ Print source identifier

                # ✅ Redirect based on the source
                if source == "qr_app":
                    return JsonResponse({"status": "success", "url": "https://www.google.com"})
                else:
                    return JsonResponse({"status": "success", "url": "https://google.com"})

            else:
                return JsonResponse({"status": "no_qr", "message": "No QR Code detected."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Exception: {str(e)}"})

    return JsonResponse({"status": "error", "message": "Invalid request method."})
