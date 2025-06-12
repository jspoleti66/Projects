import os
import numpy as np
import cv2
import warnings

# ✅ Reemplazamos VisibleDeprecationWarning por DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

def align_img(img, lm, image_size=256):
    lm = np.array(lm)

    # Define the standard landmarks
    ref_pts = np.array([
        [30.2946, 51.6963],
        [65.5318, 51.5014],
        [48.0252, 71.7366],
        [33.5493, 92.3655],
        [62.7299, 92.2041]
    ], dtype=np.float32)

    if image_size != 112:
        ref_pts[:, 0] += 8.0

    dst_pts = lm.astype(np.float32)
    tfm = cv2.estimateAffinePartial2D(dst_pts, ref_pts, method=cv2.LMEDS)[0]

    aligned_img = cv2.warpAffine(img, tfm, (image_size, image_size), borderValue=0.0)
    return aligned_img
