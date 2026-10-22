# Project 03: Computer Vision App (classify, detect, segment)

> **Difficulty:** Intermediate · **Time:** 2-3 hours (plus a 10-30 minute install) · **Runs on:** CPU, no API key needed (internet needed the first time, to download the model files)

## 1. What this project does

You upload a photo in the browser and choose one of three questions:

| Task | Question it answers | Model used |
|---|---|---|
| **Classify** | "What is this a picture of?" (one label for the whole image) | **EfficientNet-B0**, trained on ImageNet's 1,000 everyday categories |
| **Detect** | "Which objects are in it, and where?" (a box around each object) | **YOLOv8n** (the smallest YOLO version 8 model); if that is not available, torchvision's **SSDLite** detector |
| **Segment** | "Which exact pixels belong to each object?" (a **mask** per object) | **MobileSAM**, a small version of the "Segment Anything" model, prompted with the detected boxes |

Nothing is trained here: all of these are **pre-trained models** (already trained by others on huge datasets) that are downloaded and used as they are. This is how most real-world vision apps start.

**What you will learn**

- The difference between classification, object detection and segmentation.
- Image **preprocessing** (resize, crop, turn into a **tensor**, i.e. a grid of numbers, and normalise) and why it must match what the model was trained with.
- Turning raw model scores (**logits**) into percentages with **softmax**.
- Chaining models: using a detector's boxes as **prompts** for a segmentation model.
- Accepting file uploads in FastAPI and validating them properly.

## 2. Folder contents

| File | Purpose |
|---|---|
| `main.py` | The vision logic: `classify()` (EfficientNet-B0), `detect()` (YOLOv8n, or SSDLite as a real fallback), `segment()` (MobileSAM), plus image preprocessing and loading each model once. |
| `api.py` | The FastAPI server: `POST /classify`, `POST /detect`, `POST /segment` (each takes an uploaded image), `GET /health`, and `GET /` (the web page). |
| `templates/index.html` | The web page: drag-and-drop upload, three tabs, results with confidence bars, and boxes drawn on the image for detection. |
| `requirements.txt` | The Python packages (pinned versions) the project needs. |
| `notes/03_computer_vision_app.md` | A longer explanation of the ideas behind the project. |

Files downloaded automatically on first use:

| File | Size | Where it goes |
|---|---|---|
| EfficientNet-B0 weights | about 21 MB | PyTorch's cache folder (`~/.cache/torch/hub/checkpoints/`) |
| `yolov8n.pt` | about 6.5 MB | the folder you start the server from |
| `mobile_sam.pt` | about 40 MB | the folder you start the server from |
| SSDLite weights (only if YOLO is unavailable) | about 13 MB | PyTorch's cache folder |

The ImageNet class names come with torchvision, so classification needs no extra download for labels.

## 3. Prerequisites

Finish these first (paths are relative to the repo root):

- `05_Deep_Learning/00_start_here_pytorch_from_zero.ipynb` and `05_Deep_Learning/03_cnn.ipynb`
- `06_Computer_Vision/00_start_here_images_and_your_first_cnn.ipynb`
- `06_Computer_Vision/02_image_classification.ipynb`, `03_object_detection.ipynb`, `04_image_segmentation.ipynb`
- `12_FastAPI/01_fastapi_intro.ipynb` to `03_ml_serving_with_fastapi.ipynb`
- [Project 01](../01_ml_pipeline/README.md) (same serving structure, simpler model)

**Python:** tested with **Python 3.12**. Use 3.10, 3.11 or 3.12; the pinned `torch==2.4.1` and `numpy==1.26.4` do not support newer versions.

**Disk:** with the CPU-only PyTorch (step 2) the virtual environment was about **1.5 GB**.

## 4. How to run it (tested step by step)

Every step below was run on Linux with Python 3.12 in a fresh virtual environment, and the outputs shown are the real outputs. Commands are for **macOS/Linux**; Windows versions are given where they differ.

### Step 1: Create a virtual environment

```bash
cd 21_Projects/03_computer_vision_app
python3 -m venv .venv
source .venv/bin/activate          # Windows (PowerShell): .venv\Scripts\Activate.ps1
                                   # Windows (cmd):        .venv\Scripts\activate.bat
```

### Step 2: Install the packages

A plain `pip install -r requirements.txt` works, but on Linux and Windows it downloads the GPU (CUDA) build of PyTorch plus about a dozen `nvidia-*` packages (several GB). If you do not have an NVIDIA GPU, install the small CPU build of the *same* versions first:

```bash
pip install --upgrade pip
pip install torch==2.4.1 torchvision==0.19.1 --index-url https://download.pytorch.org/whl/cpu   # skip on macOS
pip install -r requirements.txt
```

Both commands finished with no errors or version conflicts; pip accepted the `2.4.1+cpu` build as satisfying `torch==2.4.1`. (A `pip install --dry-run -r requirements.txt` also resolves cleanly.)

### Step 3: Get a test image

Any JPG or PNG photo works. `ultralytics` ships two sample photos you can use:

```bash
python -c "import ultralytics, os; print(os.path.join(os.path.dirname(ultralytics.__file__), 'assets', 'bus.jpg'))"
```

Copy the printed file into this folder as `bus.jpg` (a street scene with a bus and four people, 810x1080 pixels). The very first time, `ultralytics` may print a "Creating new Ultralytics Settings" message before the path; the path is the last line.

### Step 4: Start the server

```bash
uvicorn api:app --port 8000
```

Wait for `Application startup complete.` If port 8000 is already used by another program you will see `address already in use`: choose another number, for example `--port 8002`, and use it in every URL below. (`python api.py` also works, but it always uses port 8002 with auto-reload.) Start it from this folder: `templates/index.html` and the model files are looked up relative to the current folder.

Leave this terminal running and open a **second** terminal (activate the venv there too) for the curl commands.

### Step 5: Open the web page

Go to **http://localhost:8000/**, drop an image on the upload box, choose a tab, and click **Run Inference**. You can also try the endpoints by hand at **http://localhost:8000/docs**.

### Step 6: Try the API with curl

On Windows PowerShell type `curl.exe` instead of `curl`. The `-F "file=@bus.jpg"` part uploads the file, like a web form.

**Health check**

```bash
curl http://localhost:8000/health
```
```json
{"status":"ok"}
```

**Classify** (top 3 instead of the default 5; allowed range 1-20)

```bash
curl -F "file=@bus.jpg" "http://localhost:8000/classify?top_k=3"
```
```json
{"filename":"bus.jpg","predictions":[
  {"label":"minibus","confidence":59.84,"class_id":654},
  {"label":"trolleybus","confidence":9.0,"class_id":874},
  {"label":"passenger car","confidence":6.79,"class_id":705}]}
```

`confidence` is a percentage.

**Detect**

```bash
curl -F "file=@bus.jpg" http://localhost:8000/detect
```
```json
{"filename":"bus.jpg","model":"YOLOv8n (ultralytics)","detections":[
  {"label":"bus","confidence":87.34,"box":{"x1":22.87,"y1":231.28,"x2":805.0,"y2":756.84}},
  {"label":"person","confidence":86.57,"box":{"x1":48.55,"y1":398.55,"x2":245.35,"y2":902.7}},
  {"label":"person","confidence":85.28,"box":{"x1":669.47,"y1":392.19,"x2":809.72,"y2":877.04}},
  {"label":"person","confidence":82.52,"box":{"x1":221.52,"y1":405.8,"x2":344.97,"y2":857.54}},
  {"label":"person","confidence":26.11,"box":{"x1":0.0,"y1":550.53,"x2":63.01,"y2":873.44}},
  {"label":"stop sign","confidence":25.51,"box":{"x1":0.06,"y1":254.46,"x2":32.56,"y2":324.87}}]}
```

(Coordinates shortened here; the real response has many decimals.)

The box numbers are pixels: `x1, y1` is the top-left corner and `x2, y2` the bottom-right corner. `model` tells you which detector answered. Notice the low-confidence guesses at the end (26% "person", 26% "stop sign"): a real app would usually hide anything below, say, 50%.

If `ultralytics` is missing (or `yolov8n.pt` cannot be downloaded), the app uses torchvision's SSDLite detector instead. We tested this: it answered with `"model":"SSDLite320-MobileNetV3 (torchvision)"` and found the bus (98.46%) and three of the people (98.86%, 86.5%, 62.41%).

**Segment**

```bash
curl -F "file=@bus.jpg" http://localhost:8000/segment
```
```json
{"filename":"bus.jpg","width":810,"height":1080,"mode":"objects","num_masks":6,"masks":[
  {"area":260616,"bbox":[7.0,232.0,802.0,721.0],"label":"bus","mask_id":0},
  {"area":46752,"bbox":[52.0,397.0,243.0,901.0],"label":"person","mask_id":1},
  {"area":32812,"bbox":[225.0,406.0,342.0,858.0],"label":"person","mask_id":2},
  {"area":19977,"bbox":[671.0,400.0,809.0,878.0],"label":"person","mask_id":3},
  {"area":9203,"bbox":[0.0,556.0,60.0,860.0],"label":"person","mask_id":4},
  {"area":1873,"bbox":[0.0,254.0,31.0,323.0],"label":"stop sign","mask_id":5}]}
```

The default `mode=objects` first runs the detector, then gives each detected box to MobileSAM, which returns the exact pixels of that object. `area` is the number of pixels in the mask (largest first). The bus mask covers about 260,600 pixels, about 30% of the image (the exact count can differ by a few pixels between runs). You can also ask for SAM's automatic "segment everything" mode with `?mode=everything`, which returns the 5 largest regions without labels, but it is **very slow on a CPU** (it worked, but took 15 minutes for `bus.jpg` on our heavily loaded test machine).

**Errors you can trigger on purpose** (all real responses)

```bash
curl -F "file=@notes.txt" http://localhost:8000/classify
# {"detail":"Unsupported file type: text/plain"}                       (HTTP 400)
curl -F "file=@notes.txt;type=image/png" http://localhost:8000/classify
# {"detail":"The file is not a readable image"}                        (HTTP 400)
curl -F "file=@bus.jpg" "http://localhost:8000/classify?top_k=2000"
# {"detail":[{"type":"less_than_equal","loc":["query","top_k"],"msg":"Input should be less than or equal to 20", ...}]}   (HTTP 422)
```

**Timing.** On our test machine, first calls are slower because the weights are downloaded and loaded. With a lightly loaded machine, warm `/classify` and `/detect` calls took about 3-4 seconds each. While the machine was heavily loaded by other jobs, `/classify` took 14 s, `/detect` 38 s and `/segment` (objects mode) 35-70 s, so expect your numbers to vary a lot. While a slow request runs, the server still answers other requests (a `/health` call during segmentation returned in 0.02 s).

### Step 7: Stop the server

Press `Ctrl+C`. If a long segmentation request is still running, the server waits for it to finish; press `Ctrl+C` again to force it.

## 5. How it works

```
 browser / curl  --upload image-->  api.py
                                      |
                       read_image(): content type is jpeg/png/webp/gif
                       AND Pillow can really open it?  --no-->  HTTP 400
                                      | yes
          +---------------------------+----------------------------+
          |                           |                            |
     /classify                    /detect                      /segment (mode=objects)
          |                           |                            |
  resize 256, crop 224,         YOLOv8n (loaded once)         run /detect first
  to tensor, normalise          or SSDLite fallback                |
          |                           |                       detected boxes = prompts
  EfficientNet-B0 (loaded       boxes: label,                      |
  once, kept in memory)         confidence, x1 y1 x2 y2       MobileSAM (loaded once)
          |                           |                            |
  softmax -> top-k labels             |                       one mask per object:
          |                           |                       label, area, bbox
          +---------------------------+----------------------------+
                                      |
                                JSON response  -->  web page draws bars / boxes / list
```

The endpoints are plain `def` functions, so FastAPI runs each request in a worker thread and a slow model call does not freeze the server.

## 6. Known limitations

These are not bugs, but things to keep in mind (all checked on the test machine unless stated):

1. **First run needs the internet** to download the weights (see the table in section 2). After that everything works offline. The case "no internet *and* no `yolov8n.pt`" falls back to SSDLite, which also needs its weights downloaded once (not tested offline).
2. **CPU speed.** Segmentation is the slowest task; `mode=everything` takes minutes per image. Smaller images are faster.
3. **Demo segmentation without `ultralytics`.** If the `ultralytics` package is not installed, `/segment` cannot run SAM. It then returns three made-up rectangles, clearly marked: `"mode":"demo"`, `"demo":true` and `"note":"DEMO ONLY: these are fake rectangles, not a real segmentation. Install ultralytics ..."`; the web page shows a "DEMO RESULT" warning. (Tested by hiding `ultralytics`.) `requirements.txt` installs `ultralytics`, so you normally get real masks.
4. **Only objects the detector knows are segmented** in `mode=objects` (the 80 COCO categories such as person, car, dog, bus). For anything else use `mode=everything`.
5. **The page does not draw masks.** For segmentation the web page lists the masks (label and area) but does not colour them on the photo (see exercise 5).
6. **Low-confidence detections are kept.** Everything YOLO returns is shown, including guesses around 25%.
7. **Model files land in the current folder.** `yolov8n.pt` and `mobile_sam.pt` are saved in the folder you start the server from; starting it elsewhere downloads them again. Add `*.pt` to your `.gitignore`.
8. **Licences.** The `ultralytics` package and its YOLO/SAM weights are released under the AGPL-3.0 licence. That is fine for learning, but read the licence before using them in a product.
9. **The web page needs the internet for styling.** It loads Bootstrap from a CDN; offline it still works but looks plain.

### What was fixed (October 2026)

| Problem in the original code | Fix |
|---|---|
| Without `ultralytics`, `/detect` returned the same fake "person (mock)" box for every image, drawn on the photo as if real | Real fallback detector (torchvision SSDLite); the response names the model used |
| `/segment` caught every error and returned fake masks, hiding real problems | Fake masks only when `ultralytics` is missing, clearly marked as DEMO; real errors are reported |
| Segmentation reloaded SAM on every request and took about 6 minutes, blocking the whole server | SAM is loaded once; default `mode=objects` uses detected boxes as prompts; endpoints run in worker threads |
| "Top 5 masks" were just the first 5, including an empty mask (area 0) | Empty masks skipped, sorted by area, labelled with the detected class |
| Labels needed the internet (offline they became `class_654`) | Labels come from torchvision's built-in ImageNet class list |
| A text file sent as `image/png` caused HTTP 500 | Pillow checks the bytes: HTTP 400 "The file is not a readable image" |
| `top_k=2000` caused HTTP 500, `top_k=0` returned nothing | `top_k` must be 1-20 (HTTP 422 otherwise) |

## 7. Ideas to extend it

1. **Easy:** add a `min_confidence` query parameter to `/detect` (default 0.5) and drop detections below it.
2. **Easy:** uninstall `ultralytics` (`pip uninstall ultralytics`), restart, and compare SSDLite's detections with YOLOv8n's on the same five photos.
3. **Medium:** swap EfficientNet-B0 for another torchvision classifier (for example `resnet18` or `mobilenet_v3_small`) and compare speed and top-1 labels.
4. **Medium:** measure the speed of `/segment` with `curl -w "%{time_total}\n"` for a full-size photo and for the same photo shrunk to 640 pixels wide.
5. **Harder:** make `/segment` return the masks as a PNG overlay (colour each mask, blend it with the photo) and show it in the web page instead of a list of areas.
