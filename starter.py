import json
from credentials import IBM_CREDENTIALS
from watson_developer_cloud import SpeechToTextV1

IBM_USERNAME = IBM_CREDENTIALS[0]
IBM_PASSWORD = IBM_CREDENTIALS[1]

speechToText = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
myAudioFile = open("sample.flac", "rb")

print("Sending Request")

file = open('result.json', 'w')
transcription = speechToText.recognize(myAudioFile, 
				content_type="audio/x-flac",
				continuous=True,
				timestamps=False,
				max_alternatives=1)
json.dump(transcription, file, indent=4)

