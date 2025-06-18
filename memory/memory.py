from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
import os

history_file = os.path.join(os.path.dirname(__file__), "chat_history.json")

history = FileChatMessageHistory(history_file)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    chat_memory=history
)