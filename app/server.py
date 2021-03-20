'''
A super simple API for generating keywords for seamless pattern images.
'''
import logging
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from pathlib import Path
import uvicorn, asyncio
import sys, numpy as np

from app.config import GPATH, MODELS_PATH, USE_MODEL, STATIC_CONTENT_PATH, THRESHOLD_FOR_SHOWING_USER, TMP_IMG_FILE, CLASSES

tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory=GPATH/STATIC_CONTENT_PATH))

async def setup_model():
    m = load_model(GPATH/MODELS_PATH/USE_MODEL, compile=False)
    m.compile()
    return m

# Takes in a PIL image and outputs an array that is ready to go into the model
def prepare_image(image, target):
    logging.info('Preparing Image')
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image/255.0  # scaling
    return image

# Takes the predicitons from the model and outputs nice HTML of the top predictions sorted
def decode_predictions(preds):
    cp = list(zip(CLASSES, preds)) # putting class names in with predictions
    cpf = list(filter(lambda x: x[1] > THRESHOLD_FOR_SHOWING_USER, cp)) # filter out the predictions that are lower than the threshold
    cpf = list(filter(lambda x: x[0] != "sea", cpf))   # Don't ask.  Shouldn't have used that keyword, cuz duh it is in every single one cuz it is in 'seamless'
    cpf.sort(key=lambda x:x[1], reverse=True) # sort descending
    logging.info(f"Filtered and Sorted: {cpf}")
    return cpf
    
def get_predictions_html(cpf):
    stringified = ["<li><b>{}</b> ({:.2f})</il> ".format(x[0], x[1]) for x in cpf] # one <li> tag for each prediction       # idea.... color by probability, also maybe different thresholds for different keywords
    return ("<ul>" + " ".join(stringified) + "</ul>") # return the items it inside <ol> tags

# Reads in the tmp image, prepares it, runs it through the model, decodes predictions, and serves up the resulting html
def model_predict(img_path, m):
    img = image.load_img(img_path, target_size=(224, 224)) # Reading in the image from disk
    x = prepare_image(img, target=(224, 224)) # pre-processing the image for the model
    preds = m.predict(x) # running the image through the model to get predictions
    results = decode_predictions(preds[0])
    return results

# Asynchronous Steps
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_model())]
model = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

#################################################
# Web App routes
#################################################

@app.route("/upload", methods=["POST"])
async def upload(request):
    '''This route takes a POSTed image and returns the keyword suggestions.
    '''
    logging.info("/upload endpoint hit")
    data = await request.form()
    img_bytes = await (data["file"].read()) # upload the image
    with open(GPATH/TMP_IMG_FILE, 'wb') as f: f.write(img_bytes) # save the image file to the temp location
    pred = model_predict(GPATH/TMP_IMG_FILE, model)
    results = get_predictions_html(pred)
    result_html1 = GPATH/STATIC_CONTENT_PATH/'result1.html'
    result_html2 = GPATH/STATIC_CONTENT_PATH/'result2.html'
    result_html = str(result_html1.open().read() + str(results) + result_html2.open().read())
    return HTMLResponse(result_html) # return the full page html

@app.route("/")
def form(request):
    '''Home route.
    '''
    logging.info("Serving index.html")
    index_html = GPATH/STATIC_CONTENT_PATH/'index.html'
    return HTMLResponse(index_html.open().read())

#################################################
# API routes
#################################################

@app.route("/api/predict", methods=["POST"])
async def predict(request):
    '''This route takes a POSTed image and returns the keyword suggestions as JSON
    '''
    logging.info("/api/predict endpoint hit")
    data = await request.form()
    img_bytes = await (data["file"].read()) # upload the image
    with open(GPATH/TMP_IMG_FILE, 'wb') as f: f.write(img_bytes) # save the image file to the temp location
    pred = model_predict(GPATH/TMP_IMG_FILE, model)
    pred = [(a, f'{b:.3f}') for (a, b) in pred]
    return JSONResponse(dict(pred))

if __name__ == "__main__":
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8080)
