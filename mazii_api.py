import requests
import json

def process_api_response(api_response):
    processed_data = []
    
    for item in api_response:
        processed_item = {
            "phonetic": item.get("phonetic", ""),
            "means": []
        }
        
        for mean in item.get("means", []):
            processed_mean = {
                "examples": mean.get("examples", []),
                "mean": mean.get("mean", ""),
                "transcription": mean.get("transcription", "")
            }
            
            processed_item["means"].append(processed_mean)
        
        processed_data.append(processed_item)
    
    return processed_data

"""
    dictionary_type: javi, jaen
"""
def call_mazii_api(query, dictionary_type="javi", limit=20, page=1, result_type="word"):
    api_url = "https://mazii.net/api/search"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "dict": dictionary_type,
        "limit": limit,
        "page": page,
        "query": query,
        "type": result_type
    }

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Decode the JSON response
        result = response.json()

        # Filter the result to keep only the desired fields
        filtered_result = process_api_response(result['data'])

        return filtered_result

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return None

# Example usage:
# query_result = call_mazii_api("途中")
# if query_result:
#     print("API Response:")
#     print(json.dumps(query_result, indent=2, ensure_ascii=False))
# else:
#     print("API request failed.")
