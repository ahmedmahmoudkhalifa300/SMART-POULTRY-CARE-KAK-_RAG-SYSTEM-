"""
Video Color Analyzer v2 - Extract and save frames for visual inspection
"""
import cv2
import numpy as np
import os

def extract_and_save_frames(video_path, output_dir="video_frames"):
    """Extract frames and save them for visual inspection"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video: {os.path.basename(video_path)}")
    print(f"FPS: {fps}, Total frames: {total_frames}, Duration: {duration:.2f}s")
    
    # Extract frames at key moments
    timestamps = [0.5, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 11.5]
    
    for i, ts in enumerate(timestamps):
        cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_dir, f"frame_{i+1:02d}_at_{ts:.1f}s.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved: {filename}")
    
    cap.release()
    print(f"\nAll frames saved to {output_dir}/")

if __name__ == "__main__":
    video_path = "poultry_rag_system/data/hero.mp4"
    extract_and_save_frames(video_path)
