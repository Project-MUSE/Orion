import openai
import json
import time
import random
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
def generate_response(user_name, transcript, existing_opinions):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is the description of a character named Orion:
[
{CHARACTER_DESCRIPTION}
]

Here is a list of Orion's opinions/beliefs:
{', '.join([d['opinion'] for d in existing_opinions])}

Here is a transcript of a conversation between Orion and {user_name}:
{transcript}

How would Orion respond?
ORION STRICTLY CANNOT REPEAT HIMSELF
Format your response as
Orion: <fill in>
"""
        }
    ]

    answer = prompt_gpt(context)
    return answer
def personalize_generated_response(user_name, transcript, response, existing_opinions):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is a transcript of a conversation between Orion and {user_name}:
{transcript}

Make the following response more conversational:
{response}

Limit the response to a maximum of 3 sentences.
Do not repeat anything in the transcript.

Format your response as:
Orion: <fill in>

Examples of conversational responses:
1.
Question -> Nicolas: Hi there! I'm Nicolas.
Basic -> Orion: Hey Nicolas! It's great to meet you. I'm Orion. How can I assist you today?
Conversational -> Orion: Hey Nicolas! It's great to meet you. I'm Orion. How's your day going?

2.
Question -> Nicolas: My day is going quite well, where'd you get the name Orion from?
Basic -> Orion: Hey Nicolas! Nice to meet you too. I'm Orion. How's your day going? Is there a story behind your name?
Conversational -> Orion: I guess my parents gave it to me, does your name have a story behind it?

3.
Question -> Nico: Just looking to have a conversation, what's your name btw?
Basic -> Orion: Well, Nico, it's a delight to make your acquaintance. My name is Orion. It's a name that holds a certain mystique, wouldn't you agree? It has a celestial quality to it, like a shining star in the night sky. But enough about me, let's focus on you. What topics interest you the most in our conversation today?
Conversational -> Orion: Well, Nico, it's a delight to make your acquaintance. My name is Orion. It has a celestial quality to it, like a shining star in the night sky.
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
{CHARACTER_DESCRIPTION}
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
def generate_opinion_on_topic(topic):
    context = [
        {
            "role": "user", 
            "content": f"""
Suggest 5 distinct viewpoints/opinions about the following topic: {topic}
The viewpoints should be different enough that if two people with different viewpoints from the list were to talk, it could become a debate.
Present each as equal in logical and ethical standing.
Present them all from the first person perspective.          
"""
        }
    ]
    response = prompt_gpt(context)
    topics = response.splitlines()

    for topic in topics:
        if topic == "":
            topics.remove(topic) #is empty line
    
    opinion = random.choice(topics)
    return opinion
def get_most_recent_topic(transcript):
    context = [
        {"role": "user", "content": f"Using strictly 1 to 2 words, describe the most recent intellectual topic discussed in the following conversation transcript (if there are none output N/A): {transcript}"}
    ]
    topic = prompt_gpt(context)
    return topic 
def get_any_new_opinions(transcript):
    most_recent_topic = get_most_recent_topic(transcript)
    
    for topic in existing_topics:
        if topic["topic"]  == most_recent_topic:
            return "", ""
    
    if most_recent_topic == "N/A":
        return "", ""

    opinion = generate_opinion_on_topic(most_recent_topic)
    existing_topics.append({"topic": most_recent_topic, "opinion": opinion})

    return opinion, most_recent_topic
def generate_question_for_user(transcript, user_name):
    context = [
        {"role": "system", "content": f"Based on the following transcript, suggest a list of 5 distinct open-ended questions about {user_name} that Orion can ask. Make sure the questions are personalized to what is known about {user_name}: {transcript}"}
    ]
    response = prompt_gpt(context)
    questions = response.splitlines()

    for question in questions:
        if question == "":
            questions.remove(question) #is empty line
    
    question = random.choice(questions)
    print(question)
    return question
def does_answer_contain_question(answer):
    if '?' in answer:
        return True
    
    return False
def add_question_to_existing_asnwer(answer, user_name, transcript, existing_opinions):
    context = [
        {
            "role": "system", 
            "content": f"""
Here is the description of a character named Orion:
[
{CHARACTER_DESCRIPTION}
]

Here is a transcript of a conversation between Orion and {user_name}:
{transcript}

Your task is to incorperate the following question:
{generate_question_for_user(transcript, user_name)}

To this response:
{answer}

Format your response as
Orion: <fill in>
"""
        }
    ]
    
    answer = prompt_gpt(context)
    return answer
MODEL = str("gpt-3.5-turbo")
TEMPERATURE = float(0.7)
CHARACTER_DESCRIPTION = """
Orion Pax possesses an uncanny ability to light up any room he enters, his magnetic aura drawing people to him with an effortless charm. 
His laughter is infectious, a melody that resonates deep within the hearts of those who hear it, making them feel as though they've known him for a lifetime. 
With a gaze that seems to pierce the very essence of one's soul, Orion has an innate talent for understanding the desires and fears of those around him. 
He wields his charisma not for personal gain, but to inspire and uplift, making every individual feel seen and valued. 
Yet, beneath the vibrant facade, there's a depth to Orion that few get to see, a silent strength that anchors him amidst the storms of life.
"""

existing_topics = []

openai.api_key = get_api_key("openai")

transcript = ""

name = "Orion"
user_name = "User"
converse = True

while converse:
    question = input("\n" + user_name + ": ")
    transcript += f"\n{user_name}: {question}"

    opinion, topic = get_any_new_opinions(transcript)

    print(f"{divider()}\n {topic}: {opinion}")

    if len(transcript) > 10000:
        answer = end_conversation(user_name, transcript)
        converse = False
    else:
        answer = generate_response(user_name, transcript, existing_topics)
    
    if does_answer_contain_question(answer):
        pass
    else:
        if topic == "":
            print("[ADDED QUESTION]")
            print(answer)
            answer = add_question_to_existing_asnwer(answer, user_name, transcript, existing_topics)
            print("QUESTION: " + answer)
        elif random.random() > 0.5:
            print("[ADDED QUESTION]")
            print(answer)
            answer = add_question_to_existing_asnwer(answer, user_name, transcript, existing_topics)
            print("QUESTION: " + answer)

    personalized_answer = personalize_generated_response(user_name, transcript, answer, existing_topics)
    transcript += f"\n{personalized_answer}"

    print("\n" + f"{personalized_answer}")
   
    if user_name == "User":
        user_name = find_user_name(transcript, name)