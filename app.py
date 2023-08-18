from flask import Flask, render_template, request, send_file
import numpy as np
import cv2
import io

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image_by_percentage(image_data, percentage):
    nparr = np.frombuffer(image_data, np.uint8)  # 'fromstring' is deprecated, use 'frombuffer' instead
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    width = int(img.shape[1] * percentage / 100)
    height = int(img.shape[0] * percentage / 100)

    resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

    return resized

def denoise_image(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

def adaptive_histogram_equalization(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    final = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
    return final

def enhance_image_colored(img):
    denoised = denoise_image(img)
    enhanced = adaptive_histogram_equalization(denoised)
    return enhanced

def enhance_grayscale_image(img):
    # Sadece grayscale görseller için gürültü kaldırma
    denoised_gray = cv2.fastNlMeansDenoising(img, None, 30, 7, 21)

    # Grayscale görseller için adaptif histogram eşitleme
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(denoised_gray)
    
    return enhanced_gray


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['photo']
        if file and allowed_file(file.filename):
            percentage = float(request.form.get('percentage'))
            
            image_data = file.read()
            img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            
            enhance_option = request.form.get('enhance')
            color_option = request.form.get('color')
            
            # If enhancement is requested
            if enhance_option == 'yes':
                if color_option == 'colored':
                    img = enhance_image_colored(img)
                elif color_option == 'gray':
                    img = enhance_grayscale_image(img)
            
            # Resize the image
            width = int(img.shape[1] * percentage / 100)
            height = int(img.shape[0] * percentage / 100)
            resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)

            _, buffer = cv2.imencode('.png', resized_img)
            io_buf = io.BytesIO(buffer)
            
            return send_file(io_buf, mimetype='image/png', as_attachment=True, download_name="processed_image.png")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)