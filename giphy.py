import argparse
import json
import random
import requests

# Configuration
giphy = {
    "api_key": "dc6zaTOxFJmzC",
    "search_url": "http://api.giphy.com/v1/gifs/search",
    "rating": "r",
    "image_size_prefs": ["original", "fixed_width", "fixed_height", "fixed_height_small", "downsized"]
}

# Parse CI args
parser = argparse.ArgumentParser(description="Search for a random GIF!")
parser.add_argument('query', type=str, help='Search for something, in GIF form.')

def giphy_search(query):
    '''
    Query the Giphy search API to retrieve gifs that match the given query string
    :param query:
    :return results:
    '''
    payload = {"q": query, "api_key": giphy["api_key"], "limit": 25}
    r = requests.get(giphy["search_url"], params=payload)
    results = json.loads(r.text) if r.status_code == requests.codes.ok else None
    return results


def select_gif(response_data):
    '''
    Returns the URL of the first item in the given response data. If response contains no results,
    then return None.
    :param response_data:
    :return result:
    '''
    data = response_data["data"]
    result = None

    if len(data) > 0:
        index = random.randrange(0, len(data) - 1)
        images = response_data["data"][index]["images"]

        if images:
            # Get first available image size preference
            image_size = None

            for key in giphy["image_size_prefs"]:
                if key in images:
                    image_size = key
                    break

            result = images[image_size]["url"]

    return result


def main():
    # Get command line arguments
    args = parser.parse_args()

    # Make request to Giphy API to search for a gif
    response = giphy_search(args.query)

    if response:
        gif = select_gif(response)
        print(gif)
    else:
        print("Oops, we weren't able to GIF you anything.")


if __name__ == "__main__":
    main()
