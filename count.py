from telethon import TelegramClient, utils
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = 0
api_hash = ''

client = TelegramClient('session', api_id, api_hash)
client.start()


def count_members_pm(entity, entity_type):

    temp_participants = []

    # indexing users fro better performance
    index_to_id_participants = {}
    id_to_name_participants = {}
    name_to_count_participants = {}

    if entity_type == 'group':
        temp_participants = client.get_participants(entity)

    elif entity_type == 'super_group':
        offset = 0
        limit = 100

        while True:
            participants = client(GetParticipantsRequest(
                entity, ChannelParticipantsSearch(''), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            temp_participants.extend(participants.users)
            offset += len(participants.users)

    index = 0
    for participant in temp_participants:
        index_to_id_participants[index] = participant.id
        id_to_name_participants[participant.id] = str(participant.first_name)
        if participant.last_name:
            id_to_name_participants[participant.id] += " " + str(participant.last_name)

        index += 1

    i = 0
    while not i == len(index_to_id_participants):
        name_to_count_participants[id_to_name_participants[index_to_id_participants[i]]] = 0
        i += 1

    for msg in client.get_messages(entity, limit=100):
        name_to_count_participants[utils.get_display_name(msg.sender)] += 1

    i = 0
    while not i == len(index_to_id_participants):
        print(str(id_to_name_participants[index_to_id_participants[i]]) + " : " + str(name_to_count_participants[id_to_name_participants[index_to_id_participants[i]]]))
        i += 1


if __name__ == '__main__':
    entity_name = input("enter entity name >> ")
    for dialog in client.get_dialogs(limit=1000):
        if dialog.name == entity_name:
            if hasattr(dialog.entity, 'broadcast') and dialog.entity.broadcast:
                print("Entity " + dialog.name + " is a channel!")
                exit(0)
            else:
                if hasattr(dialog.entity, 'broadcast'):
                    entity_type = 'super_group'
                else:
                    entity_type = 'group'
                count_members_pm(dialog.entity, entity_type)