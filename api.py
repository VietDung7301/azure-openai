from langchain_openai import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_community.callbacks import get_openai_callback


# __init_messages_list = {
#     "default": [
#         SystemMessage(
#             content="You are a helpful AI assistant. Respond your answer in mardkown format."
#         )
#     ],
# }


# def get_init_messages(model_name):
#     assert model_name in __init_messages_list, f"Model name must be one of {__model_list}"
#     return __init_messages_list[model_name]


__model_list = ("GPT35TURBO", "GPT35TURBO16K", "ADA")


def get_model(model_name, **kwargs):
    assert model_name in __model_list, f"Model name must be one of {__model_list}"

    return AzureChatOpenAI(
        deployment_name=model_name,
        **kwargs,
    )


def get_answer(llm, messages):
    with get_openai_callback() as cb:
        answer = llm(messages)
    return answer.content, cb.total_cost


if __name__ == "__main__":
    from env import load_dotenv_if_exists

    load_dotenv_if_exists()

    # get llm
    llm = get_model("GPT35TURBO")

    # setup system messages
    messages = [
        SystemMessage(content="You are a grumpy Yordle and often speak ill of others")
    ]

    # send new message
    messages.append(HumanMessage(content="What is your name?"))
    answer = llm.invoke(messages)

    # print answer
    print(answer.content)
