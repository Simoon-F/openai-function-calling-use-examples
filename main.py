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
    # 将用户输入添加到会话状态中的消息列表中
    st.session_state['messages'].append(
        {"role": "user", "content": user_input})

    # 使用OpenAI的GPT-3.5模型进行聊天补全
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        # 将会话状态中的消息列表传递给聊天补全模型
        messages=st.session_state['messages'],
        # messages=messages,
        # 定义可调用的函数列表
        functions=f.function_list,
        # 设置函数调用方式为自动调用
        function_call="auto",
    )

    # 打印补全结果
    print(completion)

    # 返回补全结果中的第一个选项的消息
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
