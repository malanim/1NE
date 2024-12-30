import vk_api
import re

def read_messages(file_path):
    messages = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        entries = content.split('Пользователю:')
        for entry in entries[1:]:
            match = re.search(r'Имя Фамилия\nВремя отправки: (.*?)\nСообщение начало\n(.*?)\nСообщение конец', entry, re.DOTALL)
            if match:
                user_name = match.group(0).strip()
                message_text = match.group(1).strip()
                messages.append((user_name, message_text))
    return messages

def get_friends(api):
    friends = api.friends.get(fields='first_name,last_name')
    return [(friend['id'], f"{friend['first_name']} {friend['last_name']}") for friend in friends['items']]

def send_messages(api, messages, friends):
    for user_name, message_text in messages:
        for friend_id, friend_name in friends:
            if user_name == friend_name:
                api.messages.send(user_id=friend_id, message=message_text, random_id=0)

def main():
    vk_session = vk_api.VkApi(token='YOUR_ACCESS_TOKEN')
    api = vk_session.get_api()

    messages = read_messages('text.txt')
    friends = get_friends(api)
    send_messages(api, messages, friends)

if __name__ == '__main__':
    main()
