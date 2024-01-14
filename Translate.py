import os

import streamlit as st
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from llm_sender import ChatMessageSender
from mazii_api import call_mazii_api
from messages import ChatExampleMessage, ChatExplainMessage, HumanVocabMessage, MaziiApiMessage
from api import get_model, __model_list
from env import load_dotenv_if_exists


_init_messages = []


def init_page():
    st.set_page_config(page_title="Japanese dictionary", page_icon="📚")
    st.header("Enter word in Japanese")
    st.sidebar.title("Options")


def init_messages():
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = _init_messages
        st.session_state.costs = []


def select_model():
    model_name = st.sidebar.radio(
        "Choose LLM: (require refresh after change)", __model_list
    )
    return get_model(
        model_name=model_name,
    )


def select_language():
    source_language = st.sidebar.selectbox(
        "Source Language", ["Japanese"]
    )
    target_language = st.sidebar.selectbox(
        "Target Language", ["Vietnamese", "English"]
    )
    return source_language, target_language

def main():
    load_dotenv_if_exists()
    _user_id = os.getenv("EXAMPLE_USER_ID")
    assert _user_id, "Please set EXAMPLE_USER_ID in .env file"

    init_page()
    llm = select_model()
    source_language, target_language = select_language()
    sender = ChatMessageSender(llm, to_language=target_language, mongo_user_id=_user_id)
    init_messages()

    # # Supervise user input
    if user_input := st.chat_input("Input your question!"):
        vocab_msg = HumanVocabMessage(content=user_input)
        st.session_state.messages.append(vocab_msg)
        with st.spinner("Processing ..."):
            result = call_mazii_api(user_input, dictionary_type="javi" if target_language == "Vietnamese" else "jaen")[0]
            message = MaziiApiMessage(result, user_input, parent=vocab_msg)
            st.session_state.messages.append(message)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for idx, message in enumerate(messages):
        if isinstance(message, MaziiApiMessage):
            message.render(
                get_per_meaning_component=sender.get_explain_btns,
                get_final_component=sender.get_save_btn,
                idx=idx,
                conversation=st.session_state.messages,
            )
        elif isinstance(message, ChatExplainMessage):
            message.render()
        elif isinstance(message, ChatExampleMessage):
            message.render()
        elif isinstance(message, HumanVocabMessage):
            message.render()
        else: 
            st.warning(f"Unhandled message type: {type(message)}")
        # elif isinstance(message, AIMessage):
        #     with st.chat_message("assistant"):
        #         st.markdown(message.content)
        # elif isinstance(message, SystemMessage):
        #     with st.chat_message(""):
        #         st.text(f"System: {message.content}")
        # elif isinstance(message, AIMessage):
        #     with st.chat_message("assistant"):
        #         st.markdown(message.content)

    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == "__main__":
    main()
