import streamlit as st
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from api import get_answer, get_model, __model_list
from env import load_dotenv_if_exists

# custom it for 2 tasks
_init_messages = [
            SystemMessage(
                content="You are a helpful AI assistant. Respond your answer in mardkown format."
            )
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
    model_name = st.sidebar.radio("Choose LLM: (require refresh after change)", __model_list)
    # temperature = st.sidebar.slider(
    #     "Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.01
    # )
    return get_model(
        model_name=model_name,
        # temperature=temperature,
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
    for message in messages:
        if isinstance(message, SystemMessage):
            with st.chat_message(""):
                st.text(f"System: {message.content}")
        if isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
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
