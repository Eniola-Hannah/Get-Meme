from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# The following function will throw an error, The error occurs because the response from the meme API does not contain valid JSON data.
# This suggests that the response body is empty or not in the expected JSON format.

def get_meme():
    url = "https://meme-api.herokuapp.com/gimme"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["preview"][-2]
    subreddit = response["subreddit"]
    return meme_large, subreddit


@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

# This enables the debugger and provides more detailed error messages. Keep in mind that debug mode should not be used in a production environment.
if __name__ == "__main__":
    app.run(debug=True)

# set FLASK_APP = main
# flask run