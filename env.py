from dotenv import load_dotenv, find_dotenv


def load_dotenv_if_exists():
    try:
        return load_dotenv(find_dotenv())
    except Exception:
        print("No .env file found.")