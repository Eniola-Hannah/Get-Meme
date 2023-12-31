from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# The following function will throw an error, The error occurs because the response from the meme API does not contain valid JSON data.
# This suggests that the response body is empty or not in the expected JSON format.

# def get_meme():
#     url = "https://meme-api.herokuapp.com/gimme"
#     response = json.loads(requests.request("GET", url).text)
#     meme_large = response["preview"][-2]
#     subreddit = response["subreddit"]
#     return meme_large, subreddit

def get_meme():
    try:
        url = "https://meme-api.herokuapp.com/gimme"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        # Check if the response contains valid JSON data
        if response.headers['content-type'] == 'application/json':
            data = response.json()

            # Ensure that the required data is available in the response
            if "preview" in data and data["preview"]:
                meme_large = data["preview"][-2]
            else:
                raise ValueError("Invalid meme response format")

            if "subreddit" in data:
                subreddit = data["subreddit"]
            else:
                raise ValueError("Subreddit not found in meme response")

            return meme_large, subreddit

        else:
            raise ValueError("Invalid content type in response")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching meme: {e}")
        return None, None  # Handle the error gracefully
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing JSON: {e}")
        return None, None  # Handle the error gracefully


@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html", meme_pic=meme_pic, subreddit=subreddit)

# This enables the debugger and provides more detailed error messages. Keep in mind that debug mode should not be used in a production environment.
if __name__ == "__main__":
    app.run(debug=True)

# set FLASK_APP = main
# flask run