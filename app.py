from flask import Flask, render_template, request
import os
import cv2
from skimage.metrics import structural_similarity as ssim

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Signature matching function
def match(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)

    if img1 is None or img2 is None:
        raise ValueError("One or both images could not be loaded.")

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))

    score = ssim(img1, img2)
    return score * 100

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file1 = request.files.get('sig1')
        file2 = request.files.get('sig2')

        print("Received files:", file1.filename, file2.filename)

        if not file1 or not file2 or file1.filename == '' or file2.filename == '':
            print("Missing file(s)")
            return render_template('index.html', error="Please upload both images.")

        path1 = os.path.join(UPLOAD_FOLDER, 'sig1.jpg')
        path2 = os.path.join(UPLOAD_FOLDER, 'sig2.jpg')

        file1.save(path1)
        file2.save(path2)

        print("Files saved at:", path1, path2)

        try:
            similarity = match(path1, path2)
            print("Similarity score:", similarity)
            if similarity >= 85:
                result = f"✅ Verified: {similarity:.2f}% similar"
            else:
                result = f"❌ Not Verified: Only {similarity:.2f}% similar"
        except Exception as e:
            print("Exception during match:", str(e))
            result = f"Error: {str(e)}"

        return render_template("index.html", result=result, img1='/' + path1, img2='/' + path2)

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
