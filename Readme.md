▶️ Usage

# 1. (If not already active) Activate virtual environment:
source venv/bin/activate     # macOS/Linux
# venv\Scripts\activate      # Windows PowerShell

# 2. Run the application:
python main.py
Bring your hand into view and use the gestures to control your slides in real time!
🧰 Troubleshooting

If you face issues, try these:
# If MediaPipe/OpenCV are missing or error out:
pip install mediapipe opencv-python

# If virtual environment didn’t create or activate correctly:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
Happy Presenting! 🎉
