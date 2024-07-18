import os
import requests
import obsws_python as obs
from jinja2 import Environment, FileSystemLoader

class YoutubePlayer:
    def __init__(self, obs_client: obs.ReqClient, api_key: str):
        self.obs_client = obs_client
        self.api_key = api_key
    
    def search_youtube(self, artist: str, title: str):
        query = f"{artist} - {title}"
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={self.api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                video_id = data['items'][0]['id']['videoId']
                video_title = data['items'][0]['snippet']['title']
                return video_id, video_title
            else:
                return None, "No results found"
        else:
            return None, "Error fetching search results"

    def update_html(self, video_id: str, title: str):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_loader = FileSystemLoader(current_dir)
        env = Environment(loader=file_loader)
        
        template = env.get_template('template.html')

        data = {
            'video_id': video_id,
            'title': title
        }
        
        output = template.render(data)
        output_file = os.path.join(current_dir, 'youtube.html')

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(output)

    def refresh_browser_source(self, source_name: str):
        try:
            self.obs_client.press_input_properties_button(source_name, "refreshnocache")
        except Exception as e:
            print(f"Failed to refresh browser source: {e}")


# {
#   "kind": "youtube#video",
#   "etag": etag,
#   "id": string,
#   "snippet": {
#     "publishedAt": datetime,
#     "channelId": string,
#     "title": string,
#     "description": string,
#     "thumbnails": {
#       (key): {
#         "url": string,
#         "width": unsigned integer,
#         "height": unsigned integer
#       }
#     },
#     "channelTitle": string,
#     "tags": [
#       string
#     ],
#     "categoryId": string,
#     "liveBroadcastContent": string,
#     "defaultLanguage": string,
#     "localized": {
#       "title": string,
#       "description": string
#     },
#     "defaultAudioLanguage": string
#   },
#   "contentDetails": {
#     "duration": string,
#     "dimension": string,
#     "definition": string,
#     "caption": string,
#     "licensedContent": boolean,
#     "regionRestriction": {
#       "allowed": [
#         string
#       ],
#       "blocked": [
#         string
#       ]
#     },
#     "contentRating": {
#       "acbRating": string,
#       "agcomRating": string,
#       "anatelRating": string,
#       "bbfcRating": string,
#       "bfvcRating": string,
#       "bmukkRating": string,
#       "catvRating": string,
#       "catvfrRating": string,
#       "cbfcRating": string,
#       "cccRating": string,
#       "cceRating": string,
#       "chfilmRating": string,
#       "chvrsRating": string,
#       "cicfRating": string,
#       "cnaRating": string,
#       "cncRating": string,
#       "csaRating": string,
#       "cscfRating": string,
#       "czfilmRating": string,
#       "djctqRating": string,
#       "djctqRatingReasons": [,
#         string
#       ],
#       "ecbmctRating": string,
#       "eefilmRating": string,
#       "egfilmRating": string,
#       "eirinRating": string,
#       "fcbmRating": string,
#       "fcoRating": string,
#       "fmocRating": string,
#       "fpbRating": string,
#       "fpbRatingReasons": [,
#         string
#       ],
#       "fskRating": string,
#       "grfilmRating": string,
#       "icaaRating": string,
#       "ifcoRating": string,
#       "ilfilmRating": string,
#       "incaaRating": string,
#       "kfcbRating": string,
#       "kijkwijzerRating": string,
#       "kmrbRating": string,
#       "lsfRating": string,
#       "mccaaRating": string,
#       "mccypRating": string,
#       "mcstRating": string,
#       "mdaRating": string,
#       "medietilsynetRating": string,
#       "mekuRating": string,
#       "mibacRating": string,
#       "mocRating": string,
#       "moctwRating": string,
#       "mpaaRating": string,
#       "mpaatRating": string,
#       "mtrcbRating": string,
#       "nbcRating": string,
#       "nbcplRating": string,
#       "nfrcRating": string,
#       "nfvcbRating": string,
#       "nkclvRating": string,
#       "oflcRating": string,
#       "pefilmRating": string,
#       "rcnofRating": string,
#       "resorteviolenciaRating": string,
#       "rtcRating": string,
#       "rteRating": string,
#       "russiaRating": string,
#       "skfilmRating": string,
#       "smaisRating": string,
#       "smsaRating": string,
#       "tvpgRating": string,
#       "ytRating": string
#     },
#     "projection": string,
#     "hasCustomThumbnail": boolean
#   },
#   "status": {
#     "uploadStatus": string,
#     "failureReason": string,
#     "rejectionReason": string,
#     "privacyStatus": string,
#     "publishAt": datetime,
#     "license": string,
#     "embeddable": boolean,
#     "publicStatsViewable": boolean,
#     "madeForKids": boolean,
#     "selfDeclaredMadeForKids": boolean
#   },
#   "statistics": {
#     "viewCount": string,
#     "likeCount": string,
#     "dislikeCount": string,
#     "favoriteCount": string,
#     "commentCount": string
#   },
#   "player": {
#     "embedHtml": string,
#     "embedHeight": long,
#     "embedWidth": long
#   },
#   "topicDetails": {
#     "topicIds": [
#       string
#     ],
#     "relevantTopicIds": [
#       string
#     ],
#     "topicCategories": [
#       string
#     ]
#   },
#   "recordingDetails": {
#     "recordingDate": datetime
#   },
#   "fileDetails": {
#     "fileName": string,
#     "fileSize": unsigned long,
#     "fileType": string,
#     "container": string,
#     "videoStreams": [
#       {
#         "widthPixels": unsigned integer,
#         "heightPixels": unsigned integer,
#         "frameRateFps": double,
#         "aspectRatio": double,
#         "codec": string,
#         "bitrateBps": unsigned long,
#         "rotation": string,
#         "vendor": string
#       }
#     ],
#     "audioStreams": [
#       {
#         "channelCount": unsigned integer,
#         "codec": string,
#         "bitrateBps": unsigned long,
#         "vendor": string
#       }
#     ],
#     "durationMs": unsigned long,
#     "bitrateBps": unsigned long,
#     "creationTime": string
#   },
#   "processingDetails": {
#     "processingStatus": string,
#     "processingProgress": {
#       "partsTotal": unsigned long,
#       "partsProcessed": unsigned long,
#       "timeLeftMs": unsigned long
#     },
#     "processingFailureReason": string,
#     "fileDetailsAvailability": string,
#     "processingIssuesAvailability": string,
#     "tagSuggestionsAvailability": string,
#     "editorSuggestionsAvailability": string,
#     "thumbnailsAvailability": string
#   },
#   "suggestions": {
#     "processingErrors": [
#       string
#     ],
#     "processingWarnings": [
#       string
#     ],
#     "processingHints": [
#       string
#     ],
#     "tagSuggestions": [
#       {
#         "tag": string,
#         "categoryRestricts": [
#           string
#         ]
#       }
#     ],
#     "editorSuggestions": [
#       string
#     ]
#   },
#   "liveStreamingDetails": {
#     "actualStartTime": datetime,
#     "actualEndTime": datetime,
#     "scheduledStartTime": datetime,
#     "scheduledEndTime": datetime,
#     "concurrentViewers": unsigned long,
#     "activeLiveChatId": string
#   },
#   "localizations": {
#     (key): {
#       "title": string,
#       "description": string
#     }
#   }
# }