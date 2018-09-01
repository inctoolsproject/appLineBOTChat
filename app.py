from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json


import errno
import os
import sys, random
import tempfile

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
lineline_bot_api = LineBotApi('eMP9kyzNSliBsyazokMsfvF+eEqkOBfDmZEC+d6aR3zuQf0B+2pJKnnE8lsU854BLYSjMVFiPVjhdYtRc//LpbPz5Y85G6l7OfKs8zEjlvYK1yQl0dZRiiurgazRxh3ecsCAdx4xSUzZjFV6EaXEJvG4OuO4kxFOqqsgh4cUjrSEA6VBhXF/fHu1nGP874gV') #p0XYHyv+vaz/gu4mU2yBjOKCY7s7H/g4kvtBHJ2Ln84/oDHXPQli/UkU3y0Yli+unc+fdZB80n/8d6Ud+U3BVTf6DY71tXkmwiecDHUCTjQT/hT7R8M878XrGzE2TSbX138NGViJlhOOrK4rZm7mawdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('u0165214dec9f120d39ac46acfe18db8b') #a635011dbf5f265661ea83c64d0faf52')
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
#=====[ LEAVE GROUP OR ROOM ]==========[ ARSYBAI ]======================
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
#===================================================
    elif 'gambar' in text:
        separate = text.split(" ")
        search = text.replace(separate[0] + " ","")
        r = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(search))
        data = r.text
        data = json.loads(data)

        if data["result"] != []:
            items = data["result"]
            path = random.choice(items)
            a = items.index(path)
            b = len(items)

        image_message = ImageSendMessage(
            original_content_url=path,
            preview_image_url=path
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )

#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
