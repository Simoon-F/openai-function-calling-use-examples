import streamlit as st
import openai
import json
import requests as rq
from dotenv import dotenv_values


class IntentsList:
    def __init__(self):
        """
        The api of Gaud Open Platform is used here.

        https://lbs.amap.com/api/webservice/guide/api/weatherinfo
        """
        self.weather_api_url = "https://restapi.amap.com/v3/weather/weatherInfo"
        self.amap_api_key = env['AMAP_API_KEY']

    def query_city_weather(self, city):
        """
        Query the weather temperature of the city.

        Args:
            city (str): Cities that should be queried.
        """
        params = {
            "key": self.amap_api_key,
            "city": city,
            "output": "json",
            "extensions": "all",
        }

        response = rq.get(self.weather_api_url, params=params)

        response.raise_for_status()

        weather_data = response.json()

        for item in weather_data['forecasts']:
            st.markdown(f"{item['province'] + item['city']} is as follows：")
            for cast in item['casts']:
                st.markdown(
                    f"**{cast['date']}**  ：`dayweather`：{cast['dayweather']}，`nightweather`：{cast['nightweather']}, `daytemp`: {cast['daytemp']}, `nighttemp`：{cast['nighttemp']}")

    @staticmethod
    def send_email(to_email, title, body):
        st.markdown(f"Recipient：{to_email}")
        st.markdown(f"Email Title：{title}")
        st.markdown(f"Email Body：{body}")


def call_gpt(user_input):
    """
    Make a ChatCompletion API call to OpenAI GPT-3.5-turbo model.

    Args:
        user_input (str): The user's prompt or input text.

    Returns:
        str: The generated response from the API call.
    """
    messages = [{"role": "user", "content": user_input}]

    function = [
        {
            "name": "query_city_weather",
            "description": "query weather temperature",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city",
                    },
                },
                "required": ["city"],
            },
        },
        {
            "name": "send_email",
            "description": "Send email information",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_email": {
                        "type": "string",
                        "description": "Recipient's email address"
                    },
                    "title": {
                        "type": "string",
                        "description": "The title of the email"
                    },
                    "body": {
                        "type": "string",
                        "description": "The Body of the email"
                    }
                }
            }
        }
    ]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=function,
        function_call="auto",
    )

    return completion.choices[0].message


if __name__ == "__main__":
    st.title("Small assistant")

    env = dotenv_values()

    openai.api_key = env['OPENAI_API_KEY']

    intents_list_obj = IntentsList()

    prompt = st.text_input("Enter your prompt:")

    if prompt:
        reply_content = call_gpt(prompt)

        reply_content_dict = reply_content.to_dict()

        content, function_call = reply_content_dict['content'], reply_content_dict.get(
            'function_call', {})

        if (content):
            st.markdown(f"{content}")
        else:
            method_name = function_call['name']
            method_args = function_call['arguments']

            method_args_dict = json.loads(method_args)

            method = getattr(intents_list_obj, method_name)
            method(**method_args_dict)
