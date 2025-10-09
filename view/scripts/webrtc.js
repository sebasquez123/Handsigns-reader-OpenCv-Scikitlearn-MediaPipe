
const url = "http://localhost:8080/offer";

const pc = new RTCPeerConnection();

async function start() {
    try {
        setInnerText("", "Connecting...", true);
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                sdp: pc.localDescription.sdp,
                type: pc.localDescription.type,
            }),
        });

        const answer = await response.json();
        if (answer.error) {
           throw new Error("Server error: " + answer.error);
        }
        await pc.setRemoteDescription(answer);
    } catch (error) {
        console.error("Error:", error);
        setInnerText("Connection failed: " + error.message, "Start", false);
    }
}

const setInnerText = (track, start, disabled) => {
    document.getElementById("track").innerText = track;
    document.getElementById("start").innerText = start;
    document.getElementById("start").disabled = disabled;
}

pc.addTransceiver('video', { direction: 'recvonly' });

pc.ontrack = (event) => {
    console.log("Track retrieved:", event);
    setInnerText("", "Connected!", true);
    const video = document.getElementById("video");
    video.srcObject = event.streams[0];
};
