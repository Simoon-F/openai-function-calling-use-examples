# OpenAi Function Calling Use Examples

A simple example that demonstrates how to use the function call feature of the OpenAI API

## Example

<a href="https://raw.githubusercontent.com/Simoon-F/openai-function-calling-use-examples/master/example.gif"><img src="https://raw.githubusercontent.com/Simoon-F/openai-function-calling-use-examples/master/example.gif"></a>

## Libraries that need to be installed

1. openai
2. streamlit
3. python-dotenv

## installation

1. Clone the current repository

```shell
$ git clone https://github.com/Simoon-F/openai-function-calling-use-exaples
```

2. Enter the project root directory

```shell
$ cd openai-function-calling-use-exaples
```

3. Create the `.env` file and add your api key

4. Set up environment variables:

    - Create a `.env` file in the root of the project.

    - Add your Open AI API key to the .env file:

    ```env
    OPENAI_API_KEY=your Open AI api key
    AMAP_API_KEY=your AMAP api key
    ```
    
`TIPS:` If there is no AMAP_API_KEY, you can comment out the relevant code.

5. Run Project
```shell
$ streamlit run main.py
```

## Official Description

[function-calling-and-other-api-updates](https://openai.com/blog/function-calling-and-other-api-updates)
