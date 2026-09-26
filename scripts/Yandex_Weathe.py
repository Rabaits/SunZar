import requests
access_key = "9e55e98f-a439-409f-8bbb-5e7c9ba01c2d"

def receipt_data(access_key):
    headers = {
        'X-Yandex-Weather-Key': access_key
    }


    query = """
    {
    weatherByPoint(request: { lat: 56.795707, lon: 61.321252 }) {
        now {
        temperature
        condition
        }
        forecast {
        hours(first: 24) {
            edges {
            node {
                time         
                temperature
                condition
            }
            }
        }
        }
    }
    }
    """

    response = requests.post(
        'https://api.weather.yandex.ru/graphql/query',
        headers=headers,
        json={'query': query}
    )
    data = response.json()
    print(f"json data:\n{data}\n{ "-" * 20 }\n")
    return data
