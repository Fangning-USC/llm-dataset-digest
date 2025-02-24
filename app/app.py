"""streamlit app of QA Retrieval Chatbot."""
import os

import streamlit as st
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import ChatMessage
from langchain.vectorstores import FAISS
from streamlit_extras.add_vertical_space import add_vertical_space


# set for streaming answer
class StreamHandler(BaseCallbackHandler):
    """streamlit callback handler."""

    def __init__(self, container: object, initial_text: str = "") -> None:
        """Callback handler container.

        Args:
        container: streamlit container.
        initial_text: initial text.

        Returns:
            None.

        """
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:  # noqa
        """New token.

        Args:
        token: token.

        Returns:
            None.

        """
        self.text += token
        self.container.markdown(self.text)


# add memory to chatbot
def conversational_chat(query: str) -> str:
    """Generate response from a query.

    Args:
    query: query string.

    Returns:
        response string.

    """
    result = chain({"question": query, "chat_history": st.session_state["history"]})

    st.session_state["history"].append((query, result["answer"]))
    return result["answer"]


# compile vectorestore
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
model_name = "text-embedding-ada-002"

embed = OpenAIEmbeddings(model=model_name, openai_api_key=OPENAI_API_KEY)

vectorstore = FAISS.load_local("vectorstore", embed)


# set streamlit app page
st.set_page_config(page_title=":book: 4C Chatbot - An LLM-powered Streamlit app")


# Side-bar
with st.sidebar:
    st.title(":book: 4C Chatbot")
    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using:
    - [ForeSEE Dashboard](<https://subscribers.4coffshore.com/>)
    - [Streamlit](<https://streamlit.io/>)
    - [Langchain](<https://python.langchain.com/>)
    - [llamaindex](<https://gpt-index.readthedocs.io/en/latest/>)

    """
    )
    add_vertical_space(5)

# initialize chat
if "history" not in st.session_state:
    st.session_state["history"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="I'm 4C Chatbot, How may I help you?")
    ]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

# generate answer given query/prompt
if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        # set streaming handler
        stream_handler = StreamHandler(st.empty())

        # chain llm with retriever
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                streaming=True,
                callbacks=[stream_handler],
                temperature=0,
                model_name="gpt-3.5-turbo",
            ),
            retriever=vectorstore.as_retriever(),
        )

        response = conversational_chat(prompt)
        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response)
        )
