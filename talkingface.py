import cv2
import numpy as np
import moviepy.editor as mpy
import mediapipe as mp

class TalkingFace:
    def __init__(self, image_path):
        self.image_path = image_path
        self.face_image = cv2.imread(image_path)
        self.height, self.width = self.face_image.shape[:2]
        self.mouth_y = int(self.height * 0.7)
        self.mouth_h = int(self.height * 0.08)

    def animate(self, text, output_path, duration_per_char=0.15):
        frames = []
        total_duration = max(1.0, len(text) * duration_per_char)
        fps = 15
        total_frames = int(total_duration * fps)

        for i in range(total_frames):
            frame = self.face_image.copy()

            # Simular movimiento de cabeza leve
            dx = int(2 * np.sin(2 * np.pi * i / 30))
            dy = int(1 * np.cos(2 * np.pi * i / 30))
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            frame = cv2.warpAffine(frame, M, (self.width, self.height))

            # Simular movimiento de boca
            mouth_open = (i % 10) < 5
            if mouth_open:
                mouth_frame = frame.copy()
                y1 = self.mouth_y
                y2 = y1 + self.mouth_h
                cv2.rectangle(mouth_frame, (self.width // 3, y1), (2 * self.width // 3, y2), (0, 0, 0), -1)
                alpha = 0.5
                frame = cv2.addWeighted(mouth_frame, alpha, frame, 1 - alpha, 0)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)

        clip = mpy.ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(output_path, codec='libx264', audio=False, verbose=False, logger=None)
