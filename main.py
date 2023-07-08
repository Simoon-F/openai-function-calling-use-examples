import time
import streamlit as st
import openai
import json
import function as f
import requests as rq
from streamlit_chat import message
from dotenv import dotenv_values


# initialization
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = []


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

        return json.dumps(weather_data)

        for item in weather_data['forecasts']:
            st.markdown(f"{item['province'] + item['city']} is as follows：")
            for cast in item['casts']:
                st.markdown(
                    f"**{cast['date']}**  ：`dayweather`：{cast['dayweather']}, `nightweather`：{cast['nightweather']}, `daytemp`: {cast['daytemp']}, `nighttemp`：{cast['nighttemp']}")

    @staticmethod
    def send_email(to_email, title, body):
        # st.markdown(f"Recipient：{to_email}")
        # st.markdown(f"Email Title：{title}")
        # st.markdown(f"Email Body：{body}")

        return "Mail Sent，Recipient：{to_email}, Email Title: {title}, Email body: {body}"

    @staticmethod
    def addition_function(left, right):
        return left + right

    @staticmethod
    def substruction_function(left, right):
        return left - right


def call_gpt(user_input):
    """
    Make a ChatCompletion API call to OpenAI GPT-3.5-turbo-0613 model.

    Args:
        user_input (str): The user's prompt or input text.

    Returns:
        str: The generated response from the API call.
    """
    # messages = [{"role": "user", "content": user_input}]

    st.session_state['messages'].append(
        {"role": "user", "content": user_input})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",  # gpt-4-0613
        messages=st.session_state['messages'],
        # messages=messages,
        functions=f.function_list,  # Receive a list of functions
        # Indicates whether the OpenAI model should use the functions in the function list, set to auto, which means that the AI model should guess by itself.
        function_call="auto",
    )

    print(completion)

    return completion.choices[0].message


if __name__ == "__main__":
    st.title("Small assistant")

    env = dotenv_values()
    openai.api_key = env['OPENAI_API_KEY']

    intents_list_obj = IntentsList()

    user_input = st.chat_input("Enter your prompt:")

    if user_input:
        assistant_output = call_gpt(user_input)

        st.session_state['past'].append(user_input)

        function_call = assistant_output.get('function_call')

        if (function_call):

            method_name, method_args = function_call.get(
                'name'), function_call.get('arguments')

            method_args_dict = json.loads(method_args)
            method = getattr(intents_list_obj, method_name)
            method_result = method(**method_args_dict)

            # Append output to messages
            st.session_state['messages'].append(assistant_output)

            # Int to string
            if type(method_result) == int:
                method_result = str(method_result)

            # Append method result to messages
            st.session_state['messages'].append(
                {"role": "function", "name": method_name,
                 "content": method_result, })

            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=st.session_state['messages'],
            )

            st.session_state['generated'].append(
                second_response.choices[0].message.get('content'))

        else:
            content = assistant_output.get('content')

            st.session_state['generated'].append(
                assistant_output.get('content'))

            # Append content to messages
            st.session_state['messages'].append(
                {"role": "assistant", "content": content})

    # History chat container
    response_container = st.container()

    # Render session
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i],
                        is_user=True, key=str(i) + '_user')
                message(st.session_state["generated"][i], key=str(i))
