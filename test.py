from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from decouple import config
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import glob

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = r"C:\Users\jlee0\Desktop\Symtentify\static\images"

class App:
    def __init__(self, image):
        # Replace with a valid key
        self.prediction_key = config('PREDICTION_KEY')
        self.prediction_resource_id = config('PREDICTION_RESOURCES_ID')
        self.ENDPOINT = config('ENDPOINT')
        self.image = image


    def img_class(self):
        # Now there is a trained endpoint that can be used to make a prediction

        credentials = ApiKeyCredentials(in_headers={"Prediction-key": self.prediction_key})
        predictor = CustomVisionPredictionClient(self.ENDPOINT, credentials)

        # Open the sample image and get back the prediction results.
        with open(self.image, mode="rb") as test_data:
            results = predictor.classify_image(
            project_id=config('PROJECT_ID'),
            publish_iteration_name="Iteration 17",
            published_name="Iteration17",
            image_data=test_data.read())
    
        # Display the results.
        return results.predictions    

    def give_results(self, data):
        temp = data.split("\n")
        rashp = temp[0].split(":")[1]
        norashp = temp[1].split(":")
        if "No" in norashp[0]:
            norashp = norashp[1]
        else:
            rashp = norashp[1]
            norashp = temp[0].split(":")[1]
        if rashp > norashp:
            result = "The symptom appears to be rash with a probability of " + rashp
            pcause = "Major causes of rash includes: Chemicals in cosmetics, latex products, posion ivy and oak"
            rtreat = "Recommended treatment for rash is to avoid scratching and apply hydrocortisone cream"
            return [data, result, pcause, rtreat] 
        else:
            result = "The symptom appears to be a non-rash skin-condition with a probability of " + norashp
            pcause = "Possible symptoms include hives and ezema"
            rtreat = ""
            return [data, result, pcause, rtreat]
        

@app.route('/', methods=['GET', 'POST'])
def index():
    data = ""
    if request.method == 'POST':
        image = request.files['file']
        if image.filename == "":
            print("File Name is invalid")
            return redirect(request.url)
        
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        app1 = App(os.path.join(app.config['IMAGE_UPLOADS'], filename))
        results = app1.img_class()
        for result in results:
            data += result.tag_name + ": {0:.2f}%".format(result.probability * 100) + "\n"
        data = app1.give_results(data)
        return render_template("view.html", filename=os.path.join('static', 'images', filename), data=data)
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

    
