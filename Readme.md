# Hand Gesture Presentation System

A real-time slide controller using hand-gesture recognition (MediaPipe + OpenCV). Navigate, point, draw, and clear slides hands-free!  

---

## Features

- **Next Slide**: Open palm  
- **Previous Slide**: Thumbs-up  
- **Pointer Mode**: L-sign (index + thumb)  
- **Draw Mode**: Pointing (index finger)  
- **Clear / Undo**: “C” sign (open claw)  

---

## Gesture-to-Feature Mapping

| Label | Gesture                | Visual Description                               | Trigger                     |
|:-----:|:-----------------------|:--------------------------------------------------|:----------------------------|
| 0     | **Palm**               | All five fingers spread, palm facing forward      | Next Slide                  |
| 1     | **L Sign**             | Index finger up, thumb out, other fingers folded | Pointer Mode                |
| 2     | **Thumb Up**           | Only thumb raised, others curled (like 👍)        | Previous Slide              |
| 3     | **Index Finger Up**    | Only index raised, pointing gesture               | Draw Mode                   |
| 4     | **C Sign** (Open Claw) | Hand curved like a “C” or holding a ball          | Clear Drawing / Undo        |

---

## Installation

1. Clone the repo:  
   ```bash
   git clone https://github.com/khushi-saxena/AirSlides.git
   cd AirSlides
