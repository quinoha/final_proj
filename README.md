# 🏋️‍♂️ WORKALONE: MediaPipe-based Workout Advisor

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8.x-orange.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**WORKALONE** is a computer vision-based workout assistant designed to track, count, and evaluate exercise routines in real-time. By leveraging Google's MediaPipe Pose detection model, it provides an interactive and structured workout session right on your local machine.

**Referred to the youtube tutorial "https://www.youtube.com/watch?v=06TE_U21FK4&t=642s"**

---

## 🎯 Purpose
The main objective of this project is to build a robust system that can:
1. Receive user specifications and desired workout routines via CLI (Command Line Interface).
2. Initialize and manage a fully automated workout session.
3. Accurately track joint movements to count repetitions and ensure proper exercise form.

---

## 🧠 Core Technology: MediaPipe Pose Model
WORKALONE utilizes the highly efficient MediaPipe Pose model for real-time body landmark detection.

<div align="center">
  <img src="https://i.imgur.com/3j8BPdc.png" height="300px" alt="MediaPipe Pose Landmarks">
</div>

---

## ✨ Key Features
- **CLI-Driven Routine Parsing**: Easily configure your workout session (exercise types, target reps, user specs) directly from the terminal.
- **Real-Time Pose Tracking**: High-speed joint angle calculation and state management.
- **Extensible Architecture**: Object-Oriented design makes it simple to add new exercise types.
- **Performance Profiling**: Built-in latency tracking (Perfetto format) for CPU vs. Hardware acceleration analysis.

## 🏃 Available Exercises
Currently, the system supports the tracking and counting of the following exercises:
- **Bicep Curls** 💪
- **Squats** 🦵
- **Planks** ⏱️ *(Timer-based tracking)*
- **Push-ups** ⬇️⬆️

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/workalone.git](https://github.com/yourusername/workalone.git)
cd workalone

