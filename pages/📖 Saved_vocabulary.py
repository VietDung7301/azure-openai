import streamlit as st
import os

from vocabulary_controller import find_user_vocabulary_by_id
from env import load_dotenv_if_exists

load_dotenv_if_exists()

_user_id = os.getenv("EXAMPLE_USER_ID")
assert _user_id, "Please set EXAMPLE_USER_ID in .env file"

def init():
    st.set_page_config(page_title="Saved vocabularies")
    st.header("Saved vocabularies")


def show_learned_word():
    list_word = find_user_vocabulary_by_id(_user_id)
    # print(list_word)
    return st.table(list_word['document']['vocabularies'])


if __name__ == "__main__":
    init()
    show_learned_word()
