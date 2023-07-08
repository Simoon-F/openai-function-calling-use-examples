function_list = [
    {
        "name": "query_city_weather",  # Function Name
        "description": "query weather temperature",  # Meta information of function
        "parameters": {  # parameters
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
                },
            "required": ["to_email", "title", "body"],
        }
    },
    {
        "name": "addition_function",
        "description": "Calculate the left and right values ​​of the + method operator symbol",
        "parameters": {
                "type": "object",
                "properties": {
                    "left": {
                        "type": "number",
                        "description": "+The value on the left side of the operator symbol"
                    },
                    "right": {
                        "type": "number",
                        "description": "+The value on the right side of the operator symbol"
                    }
                },
            "required": ["left", "right"]
        }
    },
    {
        "name": "substruction_function",
        "description": "substruction the left and right values ​​of the - method operator symbol",
        "parameters": {
                "type": "object",
                "properties": {
                    "left": {
                        "type": "number",
                        "description": "-The value on the left side of the operator symbol"
                    },
                    "right": {
                        "type": "number",
                        "description": "-The value on the right side of the operator symbol"
                    }
                },
            "required": ["left", "right"]
        }
    }
]
