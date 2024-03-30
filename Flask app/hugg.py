from hugchat import hugchat
from hugchat.login import Login


class hugCommands:
    def __init__(self, username: str, pw: str, ):
        print('initalized')
        sign = Login(username, pw)
        cookies = sign.login()
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)  # hugging face api calls
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # prompt below
    def pretentious_score(self, prompt: str, list: str, ) -> str:
        query_result = self.chatbot.chat(prompt + "\n" + "list: " + ''.join(list))
        return query_result.__str__()