import cv2
import json
import asyncio
import logging
import os
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import aiohttp_cors
import joblib
import mediapipe as mp
from demo import demo

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] - %(message)s',
)

max_num_hands = 1
min_det_conf = 0.7
min_track_conf = 0.7
model_path = 'models/trained_model.pkl'

class CameraStream(VideoStreamTrack):
    ''' Video stream track captures frames from the camera and processes them. '''
    def __init__(self):
        ''' Initialize the camera stream and related components. '''
        super().__init__()
        # Configure capture properties. Choose a backend appropriate for the OS to avoid
        backend = cv2.CAP_DSHOW if os.name == 'nt' else cv2.CAP_V4L2
        self.cap = cv2.VideoCapture(0, backend)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        logging.info('Camera identified and initialized successfully')

        # Import classifier pre trained.
        try:
            self.classifier = joblib.load(model_path)
            logging.info('Model loaded successfully')
        except Exception:
            logging.exception(f'Failed to load model at {model_path}')
            raise RuntimeError(f"Failed to load model at {model_path}")

        # Configure hand pipeline
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_det_conf,
            min_tracking_confidence=min_track_conf
        )
        logging.info('Initialization complete')

    async def recv(self):
        ''' Capture and process frames from the camera. '''
        pts, time_base = await self.next_timestamp()
        ret, framebox = self.cap.read()

        try:
            if not self.cap.isOpened():
                raise RuntimeError("could not open camera")

            if not ret:
                raise RuntimeError("could not read frame")
        except Exception as e:
            logging.exception(e)
            raise RuntimeError("Error capturing frame from camera")
        # Offload CPU-bound processing (MediaPipe, model.predict, drawing) to a separated thread
        loop = asyncio.get_running_loop()
        try:
            processed = await loop.run_in_executor(
                None, demo, self.mp_drawing, self.hands, self.mp_hands, self.classifier, framebox
            )
            # If demo returns error somehow, we wish to fall back to the original framebox to keep the stream alive.
            if processed is None or isinstance(processed, Exception):
                raise RuntimeError("could not read frame",)
            else:
                processed_frame = processed
        except Exception as e:
            logging.warning('Error while processing frame in demo: %s', e)
            processed_frame = framebox

        new_frame = VideoFrame.from_ndarray(processed_frame, format="bgr24")
        new_frame.pts = pts
        new_frame.time_base = time_base
        return new_frame

# WebRTC offer handler
async def offer(request):
    '''Handle the WebRTC offer from the client and establish a connection.'''
    try:
        # receive the offer
        params = await request.json()
        
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
        
        # create the connection
        pc = RTCPeerConnection()

        pc.addTrack(CameraStream())
        await pc.setRemoteDescription(offer)
        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type="application/json",
            text=json.dumps({ "sdp": pc.localDescription.sdp, "type": pc.localDescription.type, "error": None }),
        )
    except Exception as e:
        return web.Response(
            content_type="application/json",
            text=json.dumps({ "sdp": None, "type": None, "error": str(e) }),
        )
    
# create the web server
app = web.Application() 

# create a POST method
app.router.add_post("/offer", offer) 

# Enable CORS on all routes.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})
for route in list(app.router.routes()):
    cors.add(route)
    
logging.info('Server started on port 8080')
logging.info('POST /offer endpoint ready to accept WebRTC offers')

# start the server on port 8080
web.run_app(app, port=8080) 
