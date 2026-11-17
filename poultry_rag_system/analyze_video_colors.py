"""
Video Color Analyzer - Extract dominant colors from poultry video
"""
import cv2
import numpy as np
import os
from collections import Counter

def extract_frames(video_path, num_frames=5):
    """Extract frames at different timestamps"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps > 0 else 0
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Duration: {duration:.2f} seconds")
    
    frames = []
    timestamps = [duration * 0.1, duration * 0.3, duration * 0.5, duration * 0.7, duration * 0.9]
    
    for ts in timestamps:
        cap.set(cv2.CAP_PROP_POS_MSEC, ts * 1000)
        ret, frame = cap.read()
        if ret:
            frames.append((ts, frame))
            print(f"Extracted frame at {ts:.2f}s")
    
    cap.release()
    return frames

def get_dominant_colors(frame, k=5):
    """Extract dominant colors using K-means"""
    # Reshape frame to list of pixels
    pixels = frame.reshape(-1, 3)
    
    # Convert to float32 for k-means
    pixels = np.float32(pixels)
    
    # Define criteria, number of clusters (K) and apply k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k = min(k, len(np.unique(pixels, axis=0)))
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert to integer
    centers = np.uint8(centers)
    
    # Count labels to find most dominant
    _, counts = np.unique(labels, return_counts=True)
    
    # Sort by frequency
    sorted_indices = np.argsort(-counts)
    dominant_colors = centers[sorted_indices]
    
    return dominant_colors

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def analyze_brightness_contrast(frame):
    """Analyze brightness and contrast"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    contrast = np.std(gray)
    return brightness, contrast

def main():
    video_path = "poultry_rag_system/data/hero.mp4"
    if not os.path.exists(video_path):
        # Try parent directory
        video_path = "../poultry_rag_system/data/hero.mp4"
    
    print("=" * 60)
    print("POULTRY VIDEO COLOR ANALYSIS")
    print("=" * 60)
    
    # Extract frames
    frames = extract_frames(video_path, num_frames=5)
    
    all_dominant_colors = []
    
    print("\n" + "=" * 60)
    print("FRAME ANALYSIS")
    print("=" * 60)
    
    for ts, frame in frames:
        print(f"\n--- Frame at {ts:.2f}s ---")
        
        # Get dominant colors
        dominant = get_dominant_colors(frame, k=5)
        print("Dominant colors (RGB):")
        for i, color in enumerate(dominant):
            hex_color = rgb_to_hex(color)
            print(f"  {i+1}. RGB{tuple(color)} = {hex_color}")
            all_dominant_colors.append(color)
        
        # Analyze brightness/contrast
        brightness, contrast = analyze_brightness_contrast(frame)
        print(f"Brightness: {brightness:.1f}/255")
        print(f"Contrast: {contrast:.1f}")
    
    # Overall analysis
    print("\n" + "=" * 60)
    print("OVERALL VIDEO COLOR PROFILE")
    print("=" * 60)
    
    all_dominant_colors = np.array(all_dominant_colors)
    overall_mean = np.mean(all_dominant_colors, axis=0)
    overall_std = np.std(all_dominant_colors, axis=0)
    
    print(f"\nOverall mean color (RGB): {tuple(overall_mean.astype(int))}")
    print(f"Overall std dev (RGB): {tuple(overall_std.astype(int))}")
    print(f"Overall mean hex: {rgb_to_hex(overall_mean)}")
    
    # Categorize colors
    print("\nColor Categories:")
    for i, color in enumerate(all_dominant_colors[:10]):
        r, g, b = color
        if r > 150 and g > 100 and b < 100:
            category = "Warm/Yellowish"
        elif g > r and g > b:
            category = "Green"
        elif r > g and r > b:
            category = "Red/Brown"
        elif b > r and b > g:
            category = "Blue"
        elif abs(int(r) - int(g)) < 30 and abs(int(g) - int(b)) < 30:
            category = "Gray/Neutral"
        elif r > 180 and g > 180 and b > 180:
            category = "Light/Bright"
        elif r < 80 and g < 80 and b < 80:
            category = "Dark"
        else:
            category = "Mixed"
        
        print(f"  {rgb_to_hex(color)} - {category}")

if __name__ == "__main__":
    main()
