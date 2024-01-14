import requests
import json


# dev
_mazii_api_response = {
    "phonetic": "みどり",
    "means": [
        {
            "examples": [
                {
                    "content": "緑は草を連想させる。",
                    "mean": "Màu xanh lá cây được kết hợp với cỏ.",
                    "transcription": "みどりはくさをれんそうさせる。",
                },
            ],
            "mean": "màu xanh lá cây",
        },
        {
            "examples": [
                {
                    "content": "緑の党は核に対して大きな声を上げている。",
                    "mean": "Đảng Xanh đang lớn tiếng phản đối điện hạt nhân.",
                    "transcription": "みどりのとうはかくにたいしておおきなこえをあげている。",
                },
            ],
            "mean": "xanh.",
        },
    ],
}


def search_word_in_dictionary(word, dictionary="javi", limit=20, page=1):
    url = 'https://mazii.net/api/search'
    headers = {'Content-Type': 'application/json'}
    
    data = {
        'dict': dictionary,
        'limit': limit,
        'page': page,
        'query': word,
        'type': 'word'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        result = response.json()
        return {
            "phonetic": result['data'][0]['phonetic'], 
            "means": result['data'][0]['means']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None


class MaziiHumanMessage:
    """
    This class is used to represent a message from a human.
    """

    def __init__(self, content: str):
        self.content = content


class MaziiMessage:
    """
    This class is used to represent a message from Mazii API with markdown style.
    It will be ignored when sending to llm.
    """

    def __init__(self, api_response: dict):
        phonetic = api_response["phonetic"]
        means = api_response["means"]

        contents = [f"*Phoentic*: *{phonetic}*\n\n"]
        for item in means:
            mean = item["mean"]
            examples = item["examples"]
            content = ""
            content += "---\n"
            content += f"*Mean*: {mean}\n\n"
            if examples:
                for example in examples:
                    content += f"{example['content']}\n\n"
                    # content += f"{example['transcription']}\n\n"
                    content += f"{example['mean']}\n\n"
            contents.append(content)
        
        self.contents = contents


if __name__ == "__main__":
    # Example usage:
    word = "緑"
    result = search_word_in_dictionary(word)

    if result:
        print("API Response:")
        print(json.dumps(result, indent=2))
    else:
        print("Failed to retrieve API response.")
    
    mazii_message = MaziiMessage(result)
    
    import streamlit as st
    st.markdown(mazii_message.contents[0])