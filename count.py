from telethon import TelegramClient, utils
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = 0
api_hash = ''

client = TelegramClient('session', api_id, api_hash)
client.start()


def count_members_pm(entity, entity_type, msg_limit):
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

        if participant.first_name:
            index_to_id_participants[index] = participant.id
            id_to_name_participants[participant.id] = str(participant.first_name)
            if participant.last_name:
                id_to_name_participants[participant.id] += " " + str(participant.last_name)

            index += 1

    i = 0
    while not i == index:
        name_to_count_participants[id_to_name_participants[index_to_id_participants[i]]] = 0
        i += 1

    for msg in client.get_messages(entity, limit=msg_limit):
        try:
            name_to_count_participants[id_to_name_participants[msg.from_id]] += 1
        except Exception as e:
            # print(e, " not exits!")
            pass

    i = 0
    while not i == index:
        print(name_to_count_participants.popitem())
        i += 1


if __name__ == '__main__':
    entity_name = input("enter entity name >> ")
    msg_limit = input("enter messages limit >> ")
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
                count_members_pm(dialog.entity, entity_type, msg_limit)
