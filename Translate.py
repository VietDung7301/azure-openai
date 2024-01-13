import streamlit as st
from langchain.schema import SystemMessage, HumanMessage, AIMessage

import example_user
from api import get_answer, get_model, __model_list
from env import load_dotenv_if_exists
from vocabulary_controller import add_vocabulary

_user_id = example_user.user_id
_username = example_user.username

# custom it for 2 tasks
_init_messages = [
    # SystemMessage(
    #     content="You are a helpful AI assistant. Respond your answer in mardkown format."
    # )
    # SystemMessage(
    #     content="""
    #     Your responbility are solve programming problems.
    #     You can create algorithms, data structures and code for different programming languages.
    #     """
    # ),
    # SystemMessage(content="""
    # I want you to act as a assistant for study programming.
    # I will provide you with a programming problem and you will have to solve it.
    # Your task is to describe many algorithm for solving the problem.
    # """),
    # Please output the usage example using <code></code>.
    # Note: 
    # User: "repeart me"
    # AI: "I apologize, but I don't understand what you mean by "repeart me." Could you please provide more context or clarify your request?" -> Not good
    # AI: "No vocab found!" -> Good because "repeart me" is not a word in japanese
    # User: "こんにちは"
    # AI: "No vocab found!" -> Not good because "こんにちは" is a word in japanese
SystemMessage(
content="""
You are a machine which create usage example of vocabulary in japanese. 
Your task is take a word in japanese and return meaning, usage example of that word in japanese.
First, output meaning of the word in japanese and translate it to english in one line with format: meaning_japanese - meaning_english.
Second, output from 1 to 5 usage examples. Each output sentence in one line. Output sentence must be formal and polite. Respond with "No vocab found!" if no relevant vocabluary were found. 
Do not write something like "I apologize, but I don't understand what you mean by "repeart me." Could you please provide more context or clarify your request?".
"""
),
    # SystemMessage(
    #     content="""
    # You are an assistant designed to extract entities from text. 
    # Users will paste in a string of text and you will respond with entities you've extracted from the text as a JSON object. 
    # Here's an example of your output format: { "word": source, "output: target, "example": "", } and do not output anything else.
    # """
    # )
]


def init_page():
    st.set_page_config(page_title="Personal ChatGPT")
    st.header("Personal ChatGPT")
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
    # temperature = st.sidebar.slider(
    #     "Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.01
    # )
    return get_model(
        model_name=model_name,
        # temperature=temperature,
    )


def on_click_save(messages, key, idx):
    st.session_state[key] = True
    _ = add_vocabulary(
        _user_id,
        [{"vocabulary": messages[idx-1].content, "example": messages[idx].content}]
    )
    print(_)
    print(
        f"Saved: vocab: {messages[idx-1].content}, answers: {messages[idx].content}"
    )


def main():
    load_dotenv_if_exists()

    init_page()
    llm = select_model()
    init_messages()

    # # Supervise user input
    if user_input := st.chat_input("Input your question!"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("ChatGPT is typing ..."):
            answer, cost = get_answer(llm, st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=answer))
        st.session_state.costs.append(cost)

    # Display chat history
    messages = st.session_state.get("messages", [])
    for idx, message in enumerate(messages):
        if isinstance(message, SystemMessage):
            with st.chat_message(""):
                st.text(f"System: {message.content}")
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                key = f"save-{idx}"
                disabled = st.session_state.get(key, False)
                st.markdown(message.content)
                if message.content != "No vocab found!":
                    st.button(
                        "Save" if not disabled else "Saved",
                        key=key + "-enable" if not disabled else key + "-disable",
                        on_click=on_click_save,
                        args=(messages, key, idx),
                        disabled=disabled,
                    )
        elif isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

    costs = st.session_state.get("costs", [])
    st.sidebar.markdown("## Costs")
    st.sidebar.markdown(f"**Total cost: ${sum(costs):.5f}**")
    for cost in costs:
        st.sidebar.markdown(f"- ${cost:.5f}")


if __name__ == "__main__":
    main()
