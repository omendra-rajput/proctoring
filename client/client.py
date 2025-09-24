import requests
import mss
import cv2
import numpy as np
import base64
import time
import pygetwindow as gw

# Vercel upload API URL
# REPLACE WITH YOUR DEPLOYED VERSEL URL
VERCEL_API_URL = "https://your-vercel-project.vercel.app/api/upload"

FPS = 15  # Frames per second

def capture_and_send():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Capture the primary monitor
        print(f"Starting screen capture and sending to {VERCEL_API_URL}")
        
        while True:
            try:
                # Capture the screen
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                
                # Encode as JPEG
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                img_bytes = buffer.tobytes()
                
                # Encode to base64
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                
                # Send to serverless function
                response = requests.post(VERCEL_API_URL, json={"image": img_b64}, timeout=10)
                
                if response.status_code == 200:
                    print("Image uploaded successfully.")
                else:
                    print(f"Error uploading image: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                print("Request timed out. Serverless function might be too slow.")
            except Exception as e:
                print("An error occurred:", e)
            
            time.sleep(1 / FPS)

if __name__ == "__main__":
    capture_and_send()
