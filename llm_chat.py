import erniebot

erniebot.api_type = 'aistudio'
erniebot.access_token = '********************************'

def generate_response(input):
    response = erniebot.ChatCompletion.create(
        model='ernie-bot',
        messages=[{'role': 'user', 'content': input}],
        top_p=0,
    )
    return response.get_result()