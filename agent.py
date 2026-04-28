import json
import re
from typing import Callable, Optional
from openai import OpenAI
from tools import search_company_news, scrape_company_tech_blog, search_job_postings
from prompts import SYSTEM_PROMPT

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_company_news",
            "description": "Search for the latest news, product launches, and strategic announcements about a company",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company to research"
                    },
                    "query_suffix": {
                        "type": "string",
                        "description": "Extra search terms appended to the query (e.g. 'AI product launch 2025')"
                    }
                },
                "required": ["company_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scrape_company_tech_blog",
            "description": "Scrape the company's engineering or tech blog to understand what they are actively building",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company"
                    },
                    "blog_url": {
                        "type": "string",
                        "description": "Optional direct URL to the tech blog if known"
                    }
                },
                "required": ["company_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_job_postings",
            "description": "Search for job postings to understand what technologies and skills the company values most",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company"
                    }
                },
                "required": ["company_name"]
            }
        }
    }
]

TOOL_MAP = {
    "search_company_news": search_company_news,
    "scrape_company_tech_blog": scrape_company_tech_blog,
    "search_job_postings": search_job_postings,
}


def run_agent(
    company_name: str,
    user_skills: str = "",
    progress_callback: Optional[Callable[[str, dict], None]] = None
) -> dict:
    client = OpenAI()

    user_message = f"""
Company to research: {company_name}
My background and skills: {user_skills if user_skills.strip() else "Not provided — suggest broadly applicable projects"}

Please research this company and generate the top 3 personalized project ideas.
"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.7,
        )

        choice = response.choices[0]
        messages.append(choice.message)

        if choice.finish_reason == "stop":
            break

        if choice.finish_reason == "tool_calls":
            for tool_call in choice.message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                if progress_callback:
                    progress_callback(fn_name, fn_args)

                fn = TOOL_MAP.get(fn_name)
                result = fn(**fn_args) if fn else json.dumps({"error": f"Unknown tool: {fn_name}"})

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

    raw_output = choice.message.content or ""

    json_match = re.search(r"```json\s*(.*?)\s*```", raw_output, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    return {"raw": raw_output}
