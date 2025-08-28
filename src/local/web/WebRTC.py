import cv2
import json
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
import aiohttp_cors

class CameraStream(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(1,cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)


    async def recv(self):
        pts, time_base = await self.next_timestamp()
        ret, frame = self.cap.read()
        if not self.cap.isOpened():
            raise RuntimeError("[logging Cap] No se pudo abrir la cámara", 500)
        if not ret:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        new_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        new_frame.pts = pts
        new_frame.time_base = time_base
        return new_frame

pcs = set()

#recibimos la oferta
async def offer(request):
    params = await request.json()
    #recibimos los parametros
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    #creamos la conexion
    pc = RTCPeerConnection()
    
    pcs.add(pc)

    pc.addTrack(CameraStream())

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),
    )

app = web.Application() # creamos el servidor web
app.router.add_post("/offer", offer) # creamos un metodo post
# Habilita CORS para todos los orígenes
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, port=8080) # iniciamos el servidor en puerto 8080