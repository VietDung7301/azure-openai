import streamlit as st

from vocabulary_controller import find_user_vocabulary_by_id
import example_user


_user_id = example_user.user_id


def init():
    st.set_page_config(page_title="Saved vocabularies")
    st.header("Saved vocabularies")


def show_learned_word():
    list_word = find_user_vocabulary_by_id(_user_id)
    print(list_word)
    return st.table(list_word['document']['vocabularies'])


if __name__ == "__main__":
    init()
    show_learned_word()
