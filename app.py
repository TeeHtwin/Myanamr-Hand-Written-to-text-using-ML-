from flask import Flask, request,jsonify,Response
import base64
import io
from PIL import Image
from 

# Azure Ink Recognizer API endpoint and subscription key
#ink_recognizer_url = "https://api.cognitive.microsoft.com/inkrecognizer/v1.0-preview/recognize"
#subscription_key = "YOUR_SUBSCRIPTION_KEY"
text = ""
app = Flask(__name__)

@app.route('/image', methods=['POST'])
def save_image():
    # read image data from request
    img_bytes = request.data
    img = Image.open(io.BytesIO(img_bytes))
    # save image as PNG file
    try:
        img.save('image.png')
        response = {'success': True, 'message': 'Image saved successfully!'}
    except Exception as e:
        response = {'success': False, 'message': str(e)}


    '''
    #The following codes will implement with Microsoft Azure Ink Recognizer
     payload = {
        "applicationType": "drawing",
        "language": "en-US",
        "strokes": [{"id": "0", "points": img_b64}],
    }
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    
    response = requests.post(ink_recognizer_url, headers=headers, json=payload)
    response_json = json.loads(response.text)

    
    recognized_text = ""
    for line in response_json["recognitionUnits"][0]["recognizedText"]:
        recognized_text += line["text"]
    '''

    return jsonify(response)

#get image 
@app.route('/get_image', methods=['GET'])
def get_image():
    try:
        img = Image.open('image.png', mode='r')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        my_encoded_img = base64.encodebytes(img_byte_arr.getvalue()).decode('ascii')
        return jsonify({'success':True,'image':my_encoded_img})
    except Exception as e:
        response = {'success': False, 'message': str(e)}
        return jsonify(response)


#Post detected ocr result
@app.route('/ocr_result', methods=['POST'])
def ocr_result():
    global text
    data = request.get_json()
    # Use the data to get text from other app
    # Example:
    text = data.get('text')
    response = {'success': True, 'data': text}
    return jsonify(response)


#Get OCR Result from mobile
@app.route('/get_result', methods=['GET'])
def get_result():
    global text
    response = {'success': True, 'text': text}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)



    
