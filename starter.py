import json
from credentials import IBM_CREDENTIALS
from ws4py.client.threadedclient import WebSocketClient
from watson_developer_cloud import SpeechToTextV1
import base64, time
from collections import defaultdict
import pickle

'''class SpeechToTextClient(WebSocketClient):
	def __init__(self):
		self.ws_url = "ws://stream.watsonplatform.net/speech-to-text/api/v1/recognize"

		USERNAME = IBM_CREDENTIALS[0]
		PASSWORD = IBM_CREDENTIALS[1]

		authString = USERNAME + ":" + PASSWORD
		temp = bytes(authString, 'utf-8')
		print(type(temp))
		base64String = base64.b64encode(authString.encode())

		try:
			WebSocketClient.__init__(self, self.ws_url,
									headers=[("Authorization", "Basic %s" % base64String)])
			self.connect()
		except Exception as e:
			print("Failed To Connect")
			print(e)

	def opened(self):
		self.send('{"action": "start", "content_type": "audio/116;rate=16000"}')

	def received_message(self, message):
		print(message)

spechTTClient = SpeechToTextClient()
print("Sleeping")
time.sleep(3)
print("Awake")
stt_client.close()
''' 

def cleanJSON():
	file = open('result.json', 'r').read();
	data = json.loads(file);
	wordTimeMap = {};
	
	for x in data['results']:
		for y in x:
			if type(x[y]) == bool:
				continue
			for z in x[y]:
				for item in z['timestamps']:
					wordTimeMap[(item[1], item[2])] = item[0]

	return wordTimeMap

def getSpeakersJSON():
	file = open('result.json', 'r').read();
	data = json.loads(file);
	speakerTimeMap = {}

	for x in data['speaker_labels']:
		fromTime = x['from']
		toTime = x['to']
		speaker = x['speaker']
		confidence = x['confidence']
		end = x['final']

		speakerTimeMap[(fromTime, toTime)] = (speaker, confidence, end)

	return speakerTimeMap

def detectSpeakerText(words, speakers):
	data = defaultdict(list)

	finalOut = ["Speaker 0:"]

	curSpeaker = 0;

	for iterator in words:
		word = words[iterator]
		print(type(word))
		info = speakers[iterator]
		data[info[0]].append(word)

		if(info[2] == True):
			data[info[0]].append("<end>")

		finalOut.append(word)

		if(info[0] != curSpeaker):
			finalOut.append("Speaker " + str(info[0]) + ":")
			curSpeaker = info[0]

	utteranceList = []
	temp = ""

	for word in finalOut:
		if "Speaker" in word:
			utteranceList.append(temp)
			temp = ""
			temp = temp + word
		else:
			temp = temp + " " + word

	file = open("utteranceList.txt", "wb")
	pickle.dump(utteranceList[1:], file)
	file.close()

	print(utteranceList)


IBM_USERNAME = IBM_CREDENTIALS[0]
IBM_PASSWORD = IBM_CREDENTIALS[1]

speechToText = SpeechToTextV1(username=IBM_USERNAME, password=IBM_PASSWORD)
myAudioFile = open("sample.flac", "rb")

print("Sending Request")

file = open('result.json', 'w')

transcription = speechToText.recognize(myAudioFile, 
				content_type="audio/x-flac",
				timestamps=False,
				max_alternatives=1,
				speaker_labels=True)

#json.dump(transcription, file, indent=4)

wordTimeMap = cleanJSON();
speakerTimeMap = getSpeakersJSON();
detectSpeakerText(wordTimeMap, speakerTimeMap)