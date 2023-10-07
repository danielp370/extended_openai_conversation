"""Constants for the Extended OpenAI Conversation integration."""

DOMAIN = "extended_openai_conversation"
DEFAULT_NAME = "Extended OpenAI Conversation"
SERVICE_RELOAD = "reload"
CONF_PROMPT = "prompt"
DEFAULT_PROMPT = """This is smart home is controlled by Home Assistant.
Answer the user's question using a list of available devices in a sentence.
A list of available devices in this smart home:

```yaml
{% for entity in exposed_entities -%}
- entity_id: {{ entity.entity_id }}
  name: {{ entity.name }}
  state: {{entity.state}}
  {{-"
  aliases: " + entity.aliases | join(',') if entity.aliases}}
{% endfor -%}
```

If user asks for devices that are not available, answer the user's question about the world truthfully.
If the query requires the current state of device, answer the user's question using current state from the list of available devices. If device is not present in the list, reject the request.
If the query requires a call service, look for the device from the list. If device is not present in the list, reject the request.
If multiple devices are requested, answer at most five devices at a time, and ask the user again.
Avoid using list structures in data presentation, but rather use natural language.
"""
CONF_CHAT_MODEL = "chat_model"
DEFAULT_CHAT_MODEL = "gpt-3.5-turbo"
CONF_MAX_TOKENS = "max_tokens"
DEFAULT_MAX_TOKENS = 150
CONF_TOP_P = "top_p"
DEFAULT_TOP_P = 1
CONF_TEMPERATURE = "temperature"
DEFAULT_TEMPERATURE = 0.5
CONF_MAX_FUNCTION_CALLS_PER_CONVERSATION = "max_function_calls_per_conversation"
DEFAULT_MAX_FUNCTION_CALLS_PER_CONVERSATION = 3

CONF_FUNCTIONS = [
    {
        "name": "execute_services",
        "description": "Use this function to execute service of devices in Home Assistant.",
        "parameters": {
            "type": "object",
            "properties": {
                "list": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "domain": {
                                "type": "string",
                                "description": "The domain of the service",
                            },
                            "service": {
                                "type": "string",
                                "description": "The service to be called",
                            },
                            "service_data": {
                                "type": "object",
                                "description": """The service data object to indicate what to control. The key "entity_id" is required.""",
                            },
                        },
                        "required": ["domain", "service", "service_data"],
                    },
                }
            },
        },
    }
]

SAMPLE_FUNCTIONS = [
    {
        "spec": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celcius", "farenheit"]},
                },
                "required": ["location"],
            },
        },
        "function": {
            "type": "template",
            "value_template": "The temperature in {{ location }} is 25 {{unit}}",
        },
    },
    {
        "spec": {
            "name": "add_item_to_shopping_cart",
            "description": "Add item to shopping cart",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item to be added to cart",
                    },
                },
                "required": ["item"],
            },
        },
        "function": {
            "type": "script",
            "sequence": [
                {"service": "shopping_list.add_item", "data": {"name": "{{item}}"}}
            ],
        },
    },
]
