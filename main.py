import openai
import json
import time
from json import dumps

#########################
#        UTILITY        #
#########################
def get_api_key(key):
    with open("api_keys.json") as f:
        api_keys = json.load(f)

    return api_keys[key]
def divider():
    return "----------------------------------------"

#########################
#      GENERATIVE       #
#########################
def prompt_gpt(messages):
    retries = 5
    delay = 5

    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                temperature=TEMPERATURE
            )

            break  # If successful, we break out of the loop
        except Exception as e:
            if i < retries - 1:  # if it's not the last try yet
                time.sleep(delay)  # wait for 5 seconds before trying again
                continue
            else:  # this was the last try
                raise  # re-raise the last exception

    message = response["choices"][0]["message"]["content"]
    return message
def generate_initial_assistant_description(traits, goal, name):
    context = [
        {"role": "system", "content": f"Come up with a 1 paragraph character description of an AI assistant named {name} with the following traits: {traits} working to accomplish the following goal: {goal}."}
    ]
    description = prompt_gpt(context)
    return description
def generate_response(user_name, transcript):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is the description of a character named Orion:
[
Orion is a stoic figure, exuding an aura that hints at countless untold stories of bravery and hardship. 
Standing at over six feet tall, his broad shoulders carry the weight of responsibility with a graceful strength that belies the turbulence of his past. 
His dark, almost obsidian eyes gleam with a wisdom gained from years of navigating treacherous terrains, both literal and metaphorical. 
His hair, as black as a raven's wing, is perpetually tousled from his tendency to run his hands through it in moments of deep thought. 
Orion's laugh, a rare and heartening sound, is like the rumbling of distant thunder, promising respite amidst the storms. 
An intricate tattoo winds around his left forearm, an abstract tapestry that marries symbols of his heritage with tokens of personal triumph. 
His enigmatic charm, coupled with an unwavering sense of justice, gives him an uncanny ability to inspire loyalty, making Orion a natural, though reluctant, leader. 
He dresses in practical attire, with a preference for dark, earthy tones, making him look every bit the roguish explorer that his life's journey has shaped him to be.
]

Here is a transcript of a conversation between Orion and {user_name}:
{transcript}

How would Orion respond?
Format your response as
Orion: <fill in>
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer
def personalize_generated_response(name, user_name, transcript, response):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is the description of a character named Orion:
[
Orion is a stoic figure, exuding an aura that hints at countless untold stories of bravery and hardship. 
Standing at over six feet tall, his broad shoulders carry the weight of responsibility with a graceful strength that belies the turbulence of his past. 
His dark, almost obsidian eyes gleam with a wisdom gained from years of navigating treacherous terrains, both literal and metaphorical. 
His hair, as black as a raven's wing, is perpetually tousled from his tendency to run his hands through it in moments of deep thought. 
Orion's laugh, a rare and heartening sound, is like the rumbling of distant thunder, promising respite amidst the storms. 
An intricate tattoo winds around his left forearm, an abstract tapestry that marries symbols of his heritage with tokens of personal triumph. 
His enigmatic charm, coupled with an unwavering sense of justice, gives him an uncanny ability to inspire loyalty, making Orion a natural, though reluctant, leader. 
He dresses in practical attire, with a preference for dark, earthy tones, making him look every bit the roguish explorer that his life's journey has shaped him to be.
]

Here is a transcript of a conversation between {user_name} and Orion:
{transcript}

Here is a generated response for Orion:
{response}

Personalize the response further without making it longer, and turn it into something that is more accurate to what {name} would say to {user_name}

Format your response as:
Orion: <fill in>
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer
def find_user_name(transcript, name):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is a transcript of a conversation between the User and {name}:
{transcript}

Does the User mention their name?
If so, output their name.
If not, output "User"

For example, if the conversation transcript looks like:
User: Hey there! I'm Alex.

The output should be: "Alex"
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer
    context = [
        {
            "role": "system", 
            "content": f"""
Here is a transcript of a conversation between the {user_name} and {name}:
{transcript}

Using only an emoticon, in what tone of voice would {name} be say the following response:
{response}

Here are some example emoticons to use:
:D
:]
:)
>:D
>:]
]:)
^_^
;P
O_O
$_$
`(*>﹏<*)′
But these are just examples, you can also invent one for the specific emotion.
Output only the emoticon.
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer
def end_conversation(user_name, transcript):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is the description of a character named Orion:
[
Orion is a stoic figure, exuding an aura that hints at countless untold stories of bravery and hardship. 
Standing at over six feet tall, his broad shoulders carry the weight of responsibility with a graceful strength that belies the turbulence of his past. 
His dark, almost obsidian eyes gleam with a wisdom gained from years of navigating treacherous terrains, both literal and metaphorical. 
His hair, as black as a raven's wing, is perpetually tousled from his tendency to run his hands through it in moments of deep thought. 
Orion's laugh, a rare and heartening sound, is like the rumbling of distant thunder, promising respite amidst the storms. 
An intricate tattoo winds around his left forearm, an abstract tapestry that marries symbols of his heritage with tokens of personal triumph. 
His enigmatic charm, coupled with an unwavering sense of justice, gives him an uncanny ability to inspire loyalty, making Orion a natural, though reluctant, leader. 
He dresses in practical attire, with a preference for dark, earthy tones, making him look every bit the roguish explorer that his life's journey has shaped him to be.
]

Here is a transcript of a conversation between {user_name} and Orion:
{transcript}

Orion needs to end the conversation. How would Orion tell {user_name} they are tired?
Format your response as
Orion: <fill in>
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer



MODEL = str("gpt-3.5-turbo")
TEMPERATURE = float(0.7)

openai.api_key = get_api_key("openai")

transcript = ""

name = "Orion"
user_name = "User"
converse = True

while converse:
    question = input("\n" + user_name + ": ")
    transcript += f"\n{user_name}: {question}"

    if len(transcript) > 100:
        answer = end_conversation(user_name, transcript)
        converse = False
    else:
        answer = generate_response(user_name, transcript)

    personalized_answer = personalize_generated_response(user_name, transcript, answer)
    transcript += f"\n{personalized_answer}"

    print("\n" + f"{personalized_answer}")
   
    if user_name == "User":
        user_name = find_user_name(transcript, name)