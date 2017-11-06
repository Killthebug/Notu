import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features

natural_language_understanding = NaturalLanguageUnderstandingV1(
								username="username",
								password="password",
								version="2017-02-27")

response = natural_language_understanding.analyze(
			text="IBM is an American multinational technology company headquartered \
				in Armonk, New York, United States, with operations in over 170 \
				countries.",

	features=[
		Features.Entities(
			emotion=True,
			sentiment=True,
			limit=2
		),
		
		Features.Keywords(
			emotion=True,
			sentiment=True,
			limit=2
		)
	]
)

print(json.dumps(response, indent=2))