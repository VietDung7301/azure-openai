"""
LLM Sender and related components.
"""

import streamlit as st
from api import get_answer, get_model
from messages import ChatExampleMessage, ChatExplainMessage, HumanVocabMessage, MaziiApiMessage
from langchain.schema import AIMessage
from prompt import example_few_shot_prompt, explain_prompt, create_conversation
from vocabulary_controller import add_vocabulary


_explain_field_list = ["IT", "Business", "Life"]


class ChatMessageSender:
    """
    Send message to llm and add the answer to the chat.
    """

    def __init__(self, llm, to_language="Vietnamese", mongo_user_id=None):
        self.llm = llm
        self.to_language = to_language
        self.user_id = mongo_user_id

    def send_get_example_message(self, idx: str, vocab: str, mean: str):
        with st.spinner("ChatGPT is typing ..."):
            answer, cost = get_answer(
                self.llm,
                create_conversation(
                    {
                        "vocab": vocab,
                        "mean": mean,
                    },
                    example_few_shot_prompt,
                ),
            )
        st.session_state.messages.append(ChatExampleMessage(content=answer))
        st.session_state.costs.append(cost)

    def send_get_explain_message(self, idx: str, vocab: str, mean: str):
        with st.spinner("ChatGPT is typing ..."):
            answer, cost = get_answer(
                self.llm,
                create_conversation(
                    {
                        "vocab": vocab,
                        "mean": mean,
                        "language": self.to_language,
                    },
                    explain_prompt,
                ),
            )
        st.session_state.messages.append(ChatExplainMessage(content=answer))
        st.session_state.costs.append(cost)

    # def send_message(self, message: str):
    #     with st.spinner("ChatGPT is typing ..."):
    #         answer, cost = get_answer(self.llm, create_conversation(message, explain_prompt))
    #     st.session_state.messages.append(AIMessage(content=answer))
    #     st.session_state.costs.append(cost)

    def get_explain_btns(self, idx: str, vocab: str, mean_dict: dict):
        """
        Callback for explain and save buttons
        """
        # print(mean_dict)
        for text, col in zip(_explain_field_list, st.columns(len(_explain_field_list))):
            key = f"example-btn-{idx}-{text}"
            if col.button(f"Example in {text}", key=key):
                print(f"Example of {vocab} in {text} with mean {mean_dict['mean']}")
                self.send_get_example_message(idx, vocab, mean_dict["mean"])

        # st.button(
        #     "Explanation", 
        #     key=f"explain-btn-{idx}",
        #     on_click=lambda: self.send_get_explain_message(idx, vocab, mean_dict["mean"]),
        #     )
        if st.button("Explanation", key=f"explain-btn-{idx}"):
            print(f"Explanation of {vocab} with mean {mean_dict['mean']}")
            self.send_get_explain_message(idx, vocab, mean_dict["mean"])

    def get_save_btn(self, owner_message: HumanVocabMessage, idx: str, vocab: str, phonetic: str, means: dict, conversation: list=None, content=None):
        """
        Callback for explain and save buttons
        """
        # saved = st.session_state.get(f"save-btn-{idx}-saved", False)
        # if not saved:
        if st.button("Save", key=f"save-btn-{idx}"):
            st.session_state[f"save-btn-{idx}-saved"] = True
            # print(f"Saved: vocab: {vocab}, phonetic: {phonetic}, means: {means}")
            other_messages = []
            if conversation is not None:
                # find index of owner_message
                owner_idx = conversation.index(owner_message)
                # end index is the next message of instance of HumanVocabMessage
                end_idx = len(conversation) - 1
                for _idx in range(owner_idx, len(conversation)):
                    message = conversation[_idx]
                    if isinstance(message, HumanVocabMessage):
                        end_idx = _idx - 1
                        break
                other_messages = conversation[owner_idx + 1 : end_idx + 1]
                other_messages = [message.content for message in other_messages]
                print(other_messages)
            add_vocabulary(self.user_id, {
                "vocabulary": vocab,
                # "phonetic": phonetic,
                "example": content,
                "conversation": other_messages,
            })
            print(f"Saved: vocab: {vocab}, ...")
        # else:
        #     st.button("Saved", key=f"save-btn-{idx}", disabled=True)


if __name__ == "__main__":
    from mazii_api import call_mazii_api
    from env import load_dotenv_if_exists
    from Translate import init_messages

    load_dotenv_if_exists()
    # get llm
    llm = get_model("GPT35TURBO")
    init_messages()

    sender = ChatMessageSender(llm)

    word = "緑"
    result = call_mazii_api(word)[0]  # Get the first result
    message = MaziiApiMessage(result, word)

    _init_messages = [
        message,
    ]
    if not st.session_state.messages:
        st.session_state.messages = _init_messages

    for idx, message in enumerate(st.session_state.messages):
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
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
