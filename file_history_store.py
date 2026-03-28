import os,json
from typing import Sequence
from langchain_core.messages import BaseMessage,message_to_dict,messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")


class FileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self,session_id,storage_path):
        self.session_id = session_id                #会话id
        self.storage_path = storage_path       #不同会话id的存储文件，所在在的文件路径
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)

        #确保文件路径是正确的
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        #Sequence序列类似list，tuple
        all_messages = list(self.messages)       #已有的消息列表
        all_messages.extend(messages)            #新的和已有的融合成一个list

        # new_messages = []
        # for message in all_messages:
        #     d = message_to_dict(message)
        #     new_messages.append(d)
        new_messages = [message_to_dict(message) for message in all_messages]
        #将数据写入文件
        with open(self.file_path,'w',encoding='utf-8') as f :
            json.dump(new_messages,f)

    @property       #@property装饰器将messages方法变成成员方法属性用
    def messages(self) -> list[BaseMessage]:
        #当前文件内：；list[字典]
        try:
            with open (self.file_path,'r',encoding='utf-8') as f:
                messages_data = json.load(f)   #返回值就是list[字典]
                return messages_from_dict(messages_data) 
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f)




