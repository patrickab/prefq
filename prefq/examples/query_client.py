"""An example of a query client that sends queries to the server and polls results."""

import json
import os
import time

import requests

AVAILABLE_VIDEOS = 10
QUERY_SERVER_URL = "http://127.0.0.1:5000/"
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
VIDEO_FILENAMES = [f"{str(i).zfill(2)}.mp4" for i in range(1, AVAILABLE_VIDEOS + 1)]


def send_videos():
    """POST-Request: Send videos to Query Server"""

    print("\n\nClient: Starting send_videos() [...]\n")

    videos_sent = 0

    n_pending_queries = AVAILABLE_VIDEOS // 2

    response = requests.post(
        QUERY_SERVER_URL + "videos",
        json={"n_pending_queries": n_pending_queries},
        timeout=10,
    )
    if response.status_code >= 200 & response.status_code < 400:
        print("Client: Expected number of queries communicated to server\n")
    else:
        print("Client: Error: send_videos()    Status code:\n")
        print(response.status_code)

    for i in range(1, AVAILABLE_VIDEOS // 2 + 1):
        # Prepare POST-Request Content
        left_video_file_path = os.path.join(
            ROOT_PATH, "videos/lunarlander_random/", VIDEO_FILENAMES[videos_sent]
        )
        right_video_file_path = os.path.join(
            ROOT_PATH, "videos/lunarlander_random/", VIDEO_FILENAMES[videos_sent + 1]
        )

        with open(left_video_file_path, "rb") as left_video_file, open(
            right_video_file_path, "rb"
        ) as right_video_file:
            # Read the file data into memory
            left_video_data = left_video_file.read()
            right_video_data = right_video_file.read()

        # remove .mp4
        video_filename_left = VIDEO_FILENAMES[videos_sent].split(".")[0]
        video_filename_right = VIDEO_FILENAMES[videos_sent + 1].split(".")[0]
        query_id = video_filename_left + "-" + video_filename_right
        video_filename_left = query_id + "-left.webm"
        video_filename_right = query_id + "-right.webm"

        payload = {
            # Send filepaths as .json
            "left_filename": (
                json.dumps(video_filename_left),
                "application/json",
            ),
            "right_filename": (
                json.dumps(video_filename_right),
                "application/json",
            ),
            # Use the file data directly
            "left_video": (
                VIDEO_FILENAMES[videos_sent],
                left_video_data,
                "application/octet-stream",
            ),
            "right_video": (
                VIDEO_FILENAMES[videos_sent + 1],
                right_video_data,
                "application/octet-stream",
            ),
        }

        videos_sent += 2

        print("Client: " + f"{i:02}" + " Sending data to Server")
        response = requests.post(QUERY_SERVER_URL + "videos", files=payload, timeout=10)

        if response.status_code >= 200 & response.status_code < 400:
            print("Client: " + f"{i:02}" + " Payload transferred")
        else:
            print("Client: Error: send_videos()    Status code:")
            print(response.status_code)
        print("")

    print("Client: [...] Terminating send_videos()")


def wait_for_feedback(url):
    """
    - Enter Blocking State until feedback is fully evaluated
    - Then return feedback data
    """

    while True:
        time.sleep(5)
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            feedback_data = response.json()
            if feedback_data == {}:
                print("Query Client: Waiting for feedback...")
                continue
            print("Query Client: Feedback received")
            break
    return feedback_data


def request_feedback():
    """GET-Request: Receive client feedback from Server"""

    print("\n\nClient: Starting request_feedback() [...]")

    feedback_data = wait_for_feedback(QUERY_SERVER_URL + "feedback")
    print("Client: Feedback data received")
    print(feedback_data)

    return "Client: Reqeuest in request_feedback() failed"


def main():
    """Send the example queries and poll for feedback."""
    send_videos()
    request_feedback()


if __name__ == "__main__":
    main()
