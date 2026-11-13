# Traffic Orchestrator

Traffic Orchestrator is a computer-vision prototype for analyzing traffic from a video. It uses YOLOv8 to detect cars, motorcycles, buses, and trucks, then estimates road occupancy and suggests a traffic status, speed, and safety gap.

## Why this project has value

The project is intended to turn ordinary traffic-camera footage into useful traffic information without requiring sensors installed in every vehicle. A working version could help with:

- detecting congestion early;
- monitoring road occupancy by vehicle type;
- suggesting a coordinated speed to reduce stop-and-go traffic;
- supporting traffic-management dashboards and simulations;
- providing a foundation for integration with SUMO or other traffic tools.

The current values are estimates, not measurements suitable for safety-critical or enforcement decisions.

## How it is supposed to work

1. `main.py` opens `data/test_traffic.mp4`.
2. `src/detector.py` loads `yolov8n.pt` and detects selected COCO vehicle classes.
3. `src/brain.py` converts detections into an estimated occupancy percentage.
4. The program displays the annotated video and a dashboard containing status, occupancy, suggested speed, and safety gap.

## Installation

Use Python 3.9 or newer and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -r requirement.txt
```

The repository already includes `yolov8n.pt`. If the model is missing, Ultralytics may try to download it, which requires network access.

## Run

```bash
python main.py
```

Press `q` to stop the video. The default input is `data/test_traffic.mp4`; change `video_path` in `main.py` to use another file.

## Why it currently does not work reliably

The project is not yet a complete production application. Common failure points are:

### 1. OpenCV may not be installed

The first import in `main.py` is `cv2`. If dependencies have not been installed, execution stops with:

```text
ModuleNotFoundError: No module named 'cv2'
```

Install the dependencies with `python -m pip install -r requirement.txt` and make sure the command uses the same Python environment that runs `main.py`.

### 2. A graphical display is required

The program calls `cv2.imshow`, `cv2.waitKey`, and `cv2.destroyAllWindows`. These require a desktop display. They usually fail on headless servers, containers, and some remote environments. A headless mode that writes an output video should be added for those environments.

### 3. The detector does not track vehicles

`TrafficDetector.get_vehicles()` returns class labels, not persistent vehicle IDs. As a result, the same vehicle is counted again in every video frame. The occupancy calculation is therefore a rough per-frame estimate, not a true traffic-density measurement. A tracker such as ByteTrack or BoT-SORT is needed for vehicle counting, speed, and flow calculations.

### 4. The occupancy model is heavily simplified

The calculation assumes that every detected vehicle occupies a fixed amount of road space. It does not account for camera perspective, lane position, region of interest, vehicle distance, occlusion, frame rate, or calibrated road dimensions. The configured 150 m and four lanes are hard-coded assumptions.

### 5. The orchestration layer is unfinished

`src/orchestrator.py` is currently empty, and `main.py` does not use it. The listed `networkx` and `traci` dependencies are not integrated into the running pipeline, so routing and SUMO simulation are not implemented yet.

### 6. Model and detection quality are not guaranteed

`yolov8n.pt` is the smallest YOLOv8 model. Small, distant, partially hidden, or unusual vehicles may be missed. The confidence threshold is intentionally low (`0.15`), which can also produce false detections. Results depend strongly on the input video and camera angle.

## Current status

This is an experimental proof of concept, not a finished traffic-control system. The video-processing path is the part currently implemented. Reliable results require dependency setup, a display or headless output mode, persistent object tracking, camera/road calibration, validation against real traffic data, and completion of the orchestration and simulation components.

## Recommended next steps

1. Add a command-line input path and a headless output-video mode.
2. Add persistent vehicle tracking and count vehicles only once.
3. Define a calibrated region of interest and lane boundaries.
4. Move configuration values out of `main.py`.
5. Add tests for the traffic calculations in `src/brain.py`.
6. Implement and connect the orchestration/SUMO integration.
7. Validate estimates against manually labeled traffic footage.
