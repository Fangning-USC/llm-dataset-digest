"""streamlit app with router and memory."""
import os

import streamlit as st
from langchain.agents import AgentType
from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.callbacks import StreamlitCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import ChatMessage
from langchain.sql_database import SQLDatabase
from langchain.vectorstores import FAISS
from langchain_experimental.sql import SQLDatabaseChain
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


# compile vectorestore
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
model_name = "text-embedding-ada-002"

embed = OpenAIEmbeddings(model=model_name, openai_api_key=OPENAI_API_KEY)

# define vectorstore
vectorstore = FAISS.load_local("vectorstore", embed)

# define sql db
db_table = SQLDatabase.from_uri("sqlite:///foresee.db")


# set streamlit app page
st.set_page_config(
    page_title=":book: 4C Chatbot with router - An LLM-powered Streamlit app"
)

# Side-bar
with st.sidebar:
    st.title(":book: 4C Chatbot with router")
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


# msgs = StreamlitChatMessageHistory(key="langchain_messages")
# memory = ConversationBufferMemory(chat_memory=msgs)


if "history" not in st.session_state:
    st.session_state["history"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="I'm 4C Chatbot, How may I help you?")
    ]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())

        # create llm for db and agent
        llm_db = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            streaming=True,
            # callbacks=[st_callback],
            temperature=0,
            model_name="gpt-3.5-turbo",
        )

        llm_agent = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"
        )

        db_chain = SQLDatabaseChain.from_llm(llm_db, db_table, verbose=False)

        # chain llm with retriever
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(
                openai_api_key=OPENAI_API_KEY,
                streaming=True,
                # callbacks=[st_callback],
                temperature=0.2,
                model_name="gpt-3.5-turbo",
            ),
            retriever=vectorstore.as_retriever(),
        )

        tools_ = [
            create_retriever_tool(
                name="Document Retrieval",
                retriever=vectorstore.as_retriever(),
                # func = chain.run,
                description=(
                    "use this tool when answering queries about summarization and"
                    "general information to get more information about the topic."
                ),
            ),
            Tool(
                name="SQL Database",
                func=db_chain.run,
                description=(
                    "use this tool to find answers from an SQL database"
                    "answer specific questions such as date, time, location, names,"
                    "region, brand, country, etc. to get "
                    "a very specific information about the topic"
                    "or answer a question that the answer cannot be found in"
                    "Document Retrieval tool"
                ),
            ),
        ]

        agent = initialize_agent(
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            tools=tools_,
            llm=llm_agent,
            verbose=True,
            max_iterations=1,
            early_stopping_method="generate",
        )

        response = agent.run(prompt, callbacks=[st_callback])

        st.session_state.messages.append(
            ChatMessage(role="assistant", content=response)
        )

        st.write(response)
