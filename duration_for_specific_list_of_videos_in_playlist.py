import os
import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = os.environ.get('YT_API_KEY')

youtube = build('youtube', 'v3', developerKey=api_key)

playlist_id = "PLE8kQVoC67PzGwMMsSk3C8MvfAqcYjusF"

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

api_max_results = 50
numbers_of_videos = 4

while True:
	pl_request = youtube.playlistItems().list(
			part='contentDetails',
			playlistId=playlist_id,
			maxResults=numbers_of_videos, 
		)

	pl_response = pl_request.execute()

	vid_ids = []

	for item in pl_response['items']:
		vid_ids.append(item['contentDetails']['videoId'])

	vid_request = youtube.videos().list(
			part="contentDetails",
			id=','.join(vid_ids)
		)

	vid_response = vid_request.execute()

	for item in vid_response['items']:
		duration = item['contentDetails']['duration']

		hours = hours_pattern.search(duration)
		minutes = minutes_pattern.search(duration)
		seconds = seconds_pattern.search(duration)

		hours = int(hours.group(1)) if hours else 0
		minutes = int(minutes.group(1)) if minutes else 0
		seconds = int(seconds.group(1)) if seconds else 0

		video_seconds = timedelta(
				hours = hours,
				minutes = minutes,
				seconds = seconds
			).total_seconds()

		total_seconds += video_seconds

	nextPageToken = pl_response.get('nextPageToken')

	if numbers_of_videos > api_max_results:
		numbers_of_videos -= api_max_results
	else:
		break	

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print('{}:{}:{}'.format(hours, minutes, seconds))