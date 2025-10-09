# Handsigns Reader: Artificial Vision & WebRTC Project

<img width="638" height="476" alt="Captura de pantalla 2025-10-09 001649" src="https://github.com/user-attachments/assets/98b72694-2406-42a2-8480-e0aeeb237941" />

## 👋 User Introduction

Welcome to Handsigns Reader!
This project lets you **recognize hand gestures in real time** using your webcam and see results instantly in your browser. It's perfect for learning about computer vision, testing gesture recognition models, and experimenting with WebRTC communication.

**What can you do here?**
- Collect hand gesture data using your camera.
- Train a decision tree model to recognize custom gestures.
- Test the model live and see instant results.
- Run a demo including live QR reading.
- Use the web interface to view video and results—no extra software needed.

**Who is it for?**
- Students and AI/vision enthusiasts.
- Teachers looking for practical examples.
- Developers wanting to experiment with MediaPipe, Scikit-learn, and WebRTC in the same project, at once.

---

## 🛠️ Simple Technical Guide

### Project Structure

```
readme.md
data/
    gestures.csv           # Collected gesture data
models/
    trained_model.pkl      # Trained decision tree model
src/
    server/                # WebRTC server and streaming logic
    training/              # Scripts for data collection, training, and testing
view/
    client.html            # Web user interface
    scripts/
        webrtc.js         # WebRTC logic for the browser
    css/
        video.css         # Interface styles
```

### Key Components

#### 1. Data Collection (`src/training/data_preprocess.py`)
- Uses MediaPipe to detect hands and collect landmark coordinates.
- Saves data to `data/gestures.csv` with gesture labels.
- Console interface, shows video and lets you exit with `q`.

#### 2. Training & Testing (`src/training/model_training.py`, `src/training/main.py`)
- Trains a decision tree using Scikit-learn with collected data.
- Lets you tune parameters and save the model to `models/trained_model.pkl`.
- Test the model live with new gestures.

#### 3. WebRTC Server (`src/server/main.py`)
- Uses `aiortc` and `aiohttp` to create a server that streams video and results to the browser.
- Processes each frame with MediaPipe and the trained model.
- Returns results to the web client in real time.
- Handles errors and sends them to the frontend for better user experience.

#### 4. Web Interface (`view/client.html`, `view/scripts/webrtc.js`)
- Lets you connect to the server and view processed video live.
- Shows connection status and detected gesture results.
- Uses WebRTC for efficient, low-latency communication.

---

## 🚀 Utility & Purpose

- **Practical learning:** A starting point for understanding computer vision, from data collection to web deployment.
- **Modern technologies:** Combines pre-trained models (MediaPipe) and custom models (Scikit-learn).
- **WebRTC:** Enables real-time video and data streaming between backend and frontend—great for demos, teaching, and prototyping.
- **Extensible:** Add new gestures, improve the model, or adapt the web interface as needed. Add new other technologies, extend the project scopes.Use this project as starting point to build prototypes.

---

## 📚 For Testing

### Requirements

- Python 3.8+
- Packages: `opencv-python`, `mediapipe`, `scikit-learn`, `aiortc`, `aiohttp`, `joblib`

### How to Use

1. **Collect gestures:**
   Run the data collection script and follow instructions to capture custom gestures.
2. **Train the model:**
   Use the training scripts to create your own recognition model.
3. **Start the server:**
   Run the WebRTC server and open `view/client.html` in your browser.
4. **Connect and test:**
   Click "Start" in the web interface and watch gestures being detected in real time.

### Highlights

- **MediaPipe:** Robust hand detection and 3D landmark extraction.
- **Scikit-learn:** Decision tree model training for gesture classification.
- **WebRTC:** Efficient video/data communication between backend and frontend.
- **Error handling:** Backend errors are sent to the frontend for easier debugging and user feedback.

---

## 💡 Why is this project useful?

- Lets you experiment with the full computer vision cycle: capture, training, inference, and web deployment.
- A foundation for advanced AI, robotics, gesture interfaces, and more.
- Shows how to integrate custom and pre-trained models in practice.
- WebRTC makes it ideal for interactive and collaborative applications via Web.

---

Explore, modify, and create your own gestures!

