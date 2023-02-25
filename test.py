from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from decouple import config
import flask
import os
import glob

app = flask.Flask(__name__)

class App:
    def __init__(self):
        # Replace with a valid key
        self.prediction_key = config('PREDICTION_KEY')
        self.prediction_resource_id = config('PREDICTION_RESOURCES_ID')
        self.ENDPOINT = config('ENDPOINT')


    def img_class(self):
        # Now there is a trained endpoint that can be used to make a prediction

        credentials = ApiKeyCredentials(in_headers={"Prediction-key": self.prediction_key})
        predictor = CustomVisionPredictionClient(self.ENDPOINT, credentials)

        # Open the sample image and get back the prediction results.
        path = os.getcwd() + "\images"
        files = glob.glob(path + "\*.jpeg")
        for filename in files:
            with open(filename, mode="rb") as test_data:
                results = predictor.classify_image(
                project_id=config('PROJECT_ID'),
                publish_iteration_name="Iteration 2",
                published_name="Iteration2",
                image_data=test_data.read())
    
        # Display the results.
            for prediction in results.predictions:
                print ("\t" + prediction.tag_name +
                       ": {0:.2f}%".format(prediction.probability * 100))       

@app.route('/')
def index():
    app = App()
    app.img_class()
    return render_template("index.html")

if __name__ == '__main__':
    #app.run(debug=True)
    app = App()
    app.img_class()

    
