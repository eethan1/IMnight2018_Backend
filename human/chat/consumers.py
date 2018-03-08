from django.contrib.auth.models import User

from channels import Group
from channels.sessions import channel_session

from human.models import Relationship
from human.chat.models import Message


import re
import json
import logging

testlog = logging.getLogger('testdevelop')


@channel_session
def ws_connect(message):
    """
    called when a websocket is create
    establish a websocket connection and add the user into a chatroom group
    """

    # this is for checking websocket address
    prefix, prefix2, label = message['path'].strip("/").split("/")
    if prefix != 'human' and prefix2 != 'chat':
        testlog.error('invalid ws path=%s', message['path'])
        return
    try:
        room = Relationship.objects.get(label=label)
    except Relationship.DoesNotExist:
        testlog.error('No relationship have this label=%s', label)
        return
    except Exception as error:
        testlog.warning(error)
        return

    # Accept the incoming connection
    message.reply_channel.send(
        {'accept': True}
    )

    message.channel_session['room'] = room.label

    # Add this client to the "chat-{label}" group
    Group('chat-' + label,
          channel_layer=message.channel_layer).add(message.reply_channel)


@channel_session
def ws_receive(message):
    """
    called when message is recieved websocket
    """
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        label = message.channel_session['room']
        room = Relationship.objects.get(label=label)
    except KeyError:
        testlog.error(
            'no room label in channel_session, full message: \n%s', message)
        return
    except Relationship.DoesNotExist:
        testlog.error(
            'recieved message, but no relationship have this label=%s', label)
        return
    except Exception as error:
        testlog.warning(error)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    try:
        data = json.loads(message.content['text'])
    except ValueError:
        testlog.error(
            "message send by ws isn't json text, full message: \n%s", message)
        return
    except Exception as error:
        testlog.warning(error)
        return

    # conform to the expected message format.
    if set(data.keys()) != set(('handle', 'message')):
        testlog.warning(
            "message send by ws contain unexpected format data: \n%s", data)
        return

    if data:
        handle = data["handle"]
        user = User.objects.get(username=handle)
        msg = data["message"]
        m = Message.objects.create(room=room, handle=user, message=msg)

        # send the massage to the clients in Group
        Group('chat-' + label,
              channel_layer=message.channel_layer).send({
                  'text': json.dumps(m.as_dict())
              })
    else:
        testlog.warning(
            "message data send by ws is NULL, full message: \n%s", message)


@channel_session
def ws_disconnect(message):
    """
    called when websocket is closed
    """
    Group('chat-' + label,
          channel_layer=message.channel_layer).discard(message.reply_channel)
