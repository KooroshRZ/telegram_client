from telethon import TelegramClient, utils
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

api_id = 0
api_hash = ''

client = TelegramClient('session', api_id, api_hash)
client.start()


def count_members_pm(entity, entity_type, msg_limit):

    temp_participants = []

    # indexing users in dictionaries for better performance
    index_to_id_participants = {}
    id_to_name_participants = {}
    name_to_count_participants = {}

    d_index_to_id_participants = {}
    d_id_to_name_participants = {}
    d_name_to_count_participants = {}

    deleted_members = []

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
    d = 0
    while not i == index:
        name_to_count_participants[id_to_name_participants[index_to_id_participants[i]]] = 0
        i += 1

    for msg in client.get_messages(entity, limit=msg_limit):
        try:
            name_to_count_participants[id_to_name_participants[msg.from_id]] += 1
        except Exception as e:
            if not msg.from_id in deleted_members:
                deleted_members.append(msg.from_id)
                d_index_to_id_participants[d] = msg.from_id
                d_id_to_name_participants[msg.from_id] = utils.get_display_name(msg.sender)
                d_name_to_count_participants[utils.get_display_name(msg.sender)] = 1
                d += 1
            else:
                d_name_to_count_participants[d_id_to_name_participants[msg.from_id]] += 1

    print("\n\n\nExisting users in group!\n")
    while name_to_count_participants:
        stuff = name_to_count_participants.popitem()
        print(stuff)

    if d_name_to_count_participants:
        print("\n\n\nThese users does not exist in group anymore!\n")
        while d_name_to_count_participants:
            stuff = d_name_to_count_participants.popitem()
            print(stuff)


if __name__ == '__main__':
    entity_name = input("enter entity name >> ")
    msg_limit = input("enter messages limit >> ")
    for dialog in client.get_dialogs(limit=1000):
        if dialog.name == entity_name:
            print("counting: ", dialog.name)
            if hasattr(dialog.entity, 'broadcast') and dialog.entity.broadcast:
                print("Entity " + dialog.name + " is a channel!")
                exit(0)
            else:
                if hasattr(dialog.entity, 'broadcast'):
                    entity_type = 'super_group'
                else:
                    entity_type = 'group'
                count_members_pm(dialog.entity, entity_type, msg_limit)