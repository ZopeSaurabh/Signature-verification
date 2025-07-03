import cv2
from skimage.metrics import structural_similarity as ssim

def match(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        raise ValueError("One or both images could not be loaded. Check file paths.")

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    # Optional: comment out to avoid conflict with tkinter
    # cv2.imshow("One", img1)
    # cv2.imshow("Two", img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    similarity_value = "{:.2f}".format(ssim(img1, img2) * 100)
    return float(similarity_value)
