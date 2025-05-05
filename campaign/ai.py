import openai
import asyncio
import traceback

# (Make sure you already set openai.api_key earlier in the file)

import openai
from openai import OpenAI
import os

# Instantiate the client (v1+ requirement)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # or hardcode for testing

def generate_choices_with_prompt(context_text: str, topic: str, num_choices: int = 5) -> list:
    """
    Generates multiple smart options (choices) for creative activities using GenAI (GPT-4).
    """

    print("\n-------------------------------------------------------------------------------------------------")
    print("\n ::::: Prompt data :::::")
    
    try:
        prompt = f"""You are a expert in prompt engineering.
        Generate {num_choices} number of groups for following prompt. Complete response of prompt should be treated as one group. In many cases single 
        response of the prompt may generate mulitple options. 
        For an exampple - if the prompt demands x number of options then these will be repeated for each group
          
        :::: Prompt start::::
            {context_text}
        :::: Prompt end ::::: 

        Instructions:
            - Each group should be crisp, persuasive, and suited for marketing
            - ||| seperator should be only used to seperate two groups. It should not be used within the Group text. 
            - Do not repeat words heavily across groups.
            - Always use tag GROUP & index to start the new GROUP.

        Return format:
            GROUP1 text ||| GROUP2 text  ||| GROUP3 text ||| GROUP4 text ||| GROUP5 text
            ... 
        """

        print("\n Final prompt ::::::::::::::::::::::: \n",  prompt)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )

        content = response.choices[0].message.content.strip()
        print("\n\nResponse |||", content, "|||")

        choices = [line.split('.', 1)[-1].strip() for line in content.splitlines() if '.' in line]
        choices = content.split('|||')

        outcomes = choices[:num_choices]
        print("\n\nOutputs::", outcomes)
        return outcomes

    except Exception as e:
        print(f"⚠️ OpenAI API call for choices failed: {e}")
        return ["Default Option 1", "Default Option 2", "Default Option 3"]





def generate_choices_with_prompt_V1(context_text: str, topic: str, num_choices: int = 3) -> list:
    """
    Generates multiple smart options (choices) for creative activities using GenAI (GPT-4).
    """

    print("\n-------------------------------------------------------------------------------------------------")
    print("\n ::::: Prompt data :: " , str)


    try:
        prompt = f"""You are a world-class marketing creative strategist.
                Given the following campaign context, generate {num_choices} highly professional and engaging options for {topic}.

                Context:
                {context_text}

                Instructions:
                - Each option should be crisp, persuasive, and suited for marketing.
                - Don't give any index to any of the choice.
                - Do not repeat words heavily across options.
                - Keep each option under 20 words if possible.
                - Only list the options as separate lines, no explanation needed.

                Return format:
                    Option 1 text
                    Option 2 text
                    Option 3 text
                """
        
        print("\n Final prompt ::::::::::::::::::::::: \n",  prompt)

        response = openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        content = response['choices'][0]['message']['content'].strip()
        print("\n\nResponse ::: ::", content)
        choices = [line.split('.', 1)[-1].strip() for line in content.splitlines() if '.' in line]
        outcomes = choices[:num_choices]
        print("\n\nOutputs::", outcomes)
        return outcomes

    except Exception as e:
        print(f"⚠️ OpenAI API call for choices failed: {e}")

        return ["Default Option 1", "Default Option 2", "Default Option 3"]



async def generate_ai_paragraph(context_text: str, topic: str) -> str:
    """
    Generates a polished executive paragraph based on context and topic using GenAI (GPT-4).
    """
    try:
        prompt = f"""You are a world-class marketing strategist.
Given the campaign context below, generate a sharp, 60-80 word executive paragraph summarizing the {topic}.

Context:
{context_text}

Instructions:
- Tone: Executive, Positive, Crisp
- Avoid jargon or complex buzzwords
- Focus on clarity and professionalism
- Output paragraph directly, no headers or bullet points
"""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=250
        )
        paragraph = response['choices'][0]['message']['content'].strip()
        return paragraph

    except Exception as e:
        print(f"⚠️ OpenAI API call failed: {e}")
        return "Due to an unexpected error, standard paragraph text is used."

