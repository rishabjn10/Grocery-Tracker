import base64
import json

from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings


def encode_image_to_base64(image_path: str) -> str:
    """Convert image to base64 format for OpenAI API."""
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def parse_order_screenshot(image_path: str):
    """Extract and process order details using OpenAI Vision API."""

    # Convert image to base64 for processing
    base64_image = encode_image_to_base64(image_path)
    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": "For a given order snapshot, extract me the details in a json format",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        }
                    ],
                },
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "order_schema",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "order_date": {
                                "anyOf": [
                                    {
                                        "type": "object",
                                        "properties": {
                                            "day": {
                                                "type": "number",
                                                "description": "Day of the order date, can be between 1 to 31.",
                                            },
                                            "month": {
                                                "type": "number",
                                                "description": "Month of the order date, can be between 1 to 12.",
                                            },
                                            "year": {
                                                "type": "number",
                                                "description": "Year of the order date.",
                                            },
                                        },
                                        "required": ["day", "month", "year"],
                                        "additionalProperties": False,
                                    },
                                    {"type": "null"},
                                ]
                            },
                            "platform": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "description": "The service or platform through which the order was made (e.g., Zepto, Blinkit, Amazon, Local Shop).",
                                    },
                                    {"type": "null"},
                                ]
                            },
                            "items": {
                                "type": "array",
                                "description": "List of items purchased in the order.",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "item_name": {
                                            "type": "string",
                                            "description": "The name of the product purchased in the order.",
                                        },
                                        "category": {
                                            "type": "string",
                                            "description": "The category under which the item falls.",
                                            "enum": [
                                                "Groceries & Staples",
                                                "Fruits & Vegetables",
                                                "Dairy & Bakery",
                                                "Beverages",
                                                "Snacks & Ready-to-Eat",
                                                "Personal Care",
                                                "Household Essentials",
                                                "Meat, Fish & Eggs",
                                                "Baby & Kids Care",
                                                "Health & Wellness",
                                            ],
                                        },
                                        "quantity": {
                                            "type": "number",
                                            "description": "The number of units of the item purchased.",
                                        },
                                        "unit_price": {
                                            "type": "number",
                                            "description": "The price of a single unit of the item.",
                                        },
                                        "total_price": {
                                            "type": "number",
                                            "description": "The total price for the quantity purchased (Quantity * Unit Price).",
                                        },
                                    },
                                    "required": [
                                        "item_name",
                                        "category",
                                        "quantity",
                                        "unit_price",
                                        "total_price",
                                    ],
                                    "additionalProperties": False,
                                },
                            },
                            "total_price": {
                                "type": "number",
                                "description": "The total price for all the items quantity purchased.",
                            },
                            "payment_method": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "description": "The method used to pay for the order (e.g., Credit Card, UPI, Cash).",
                                        "enum": [
                                            "NA",
                                            "Credit Card",
                                            "UPI",
                                            "Debit Card",
                                            "Others",
                                        ],
                                    },
                                    {"type": "null"},
                                ]
                            },
                            "discount": {
                                "type": "number",
                                "description": "Any discount applied to the order (in monetary value).",
                            },
                            "final_price": {
                                "type": "number",
                                "description": "The final amount to be paid after applying discounts.",
                            },
                            "order_source": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                        "description": "The origin of the order, such as online, app-based, or in-store purchase",
                                        "enum": [
                                            "Zomato",
                                            "Swiggy",
                                            "Blinkit",
                                            "Zepto",
                                            "Local Shop",
                                            "Others",
                                        ],
                                    },
                                    {"type": "null"},
                                ]
                            },
                        },
                        "required": [
                            "order_date",
                            "platform",
                            "items",
                            "total_price",
                            "payment_method",
                            "discount",
                            "final_price",
                            "order_source",
                        ],
                        "additionalProperties": False,
                    },
                },
            },
            temperature=1,
            max_completion_tokens=2048,
        )
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_cost = ((prompt_tokens*2.5)/1000000) + ((completion_tokens*1.25)/1000000) #Based on current pricing of OpenAI GPT-4o
        print(f"Total openai usage: ${total_cost}")
        extracted_data = response.choices[0].message.content
        parsed_data = json.loads(extracted_data)

        return parsed_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing the image with OpenAI: {str(e)}"
        )
