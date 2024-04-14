import openai
import json
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

# load data.json
with open('data.json') as f:
    data = json.load(f)

# Example item in list of data:
# {
#     "question": "Are you more:",
#     "options": [
#         "Realistic than speculative",
#         "Speculative than realistic"
#     ],
#     "weights": [
#         "s",
#         "n"
#     ]
# },


ASSISTANT_ID = "asst_6MfY2bV0tjC7aPZPYxABZSna"

agent = OpenAIAssistantRunnable(assistant_id=ASSISTANT_ID,
                                as_agent=True)
agent_executor = AgentExecutor(agent=agent,
                               tools=[],
                               verbose=False)
thread = None
def answer_question(obj):
    global thread
    # obj is a dictionary with keys: question, options, weights
    # options is a list of strings
    # weights is a list of strings
    # question is a string
    # return a string
    promptString = f"{obj['question']}\n 1. {obj['options'][0]}\n 2. {obj['options'][1]}\nRespond with the number of the option you prefer. You must respond.\nNumber:"
    inp = {
        "content": promptString
    }
    if thread:
        inp["thread_id"] = thread
    response = agent_executor.invoke(inp)
    if not thread:
        thread = response['thread_id']
    # get the response from the user
    r = response['output']
    # extract the integer any int, response might be ex: 1. Bla Bla
    ints = [int(s) for s in r.split() if s.isdigit()]
    if len(ints) == 0:
        # if no integer is found, return the first option
        return obj['weights'][0]
    # if an integer is found, return the corresponding weight
    return obj['weights'][ints[0] - 1]





weighted_answers = []
# sample 50% of the data
import random
data = random.sample(data, int(len(data) / 2))
print(len(data))
import tqdm
for item in tqdm.tqdm(data):
    try:
        weight_answer = answer_question(item)
        weighted_answers.append(weight_answer)
    except Exception as e:
        print(e)
# plot the frequency of each weight
import matplotlib.pyplot as plt
plt.hist(weighted_answers)
plt.show()

# weights are all the possible characters in the MBTI system
# create a personality type based on the weighted answers
# first index can be: E, I
# second index can be: S, N
# third index can be: T, F
# fourth index can be: J, P
personality_type_indexed_by_weight = {
    'EI': [],
    'SN': [],
    'TF': [],
    'JP': []
}


for weight in weighted_answers:
    # find the right index to append to
    if weight in ['e', 'i']:
        personality_type_indexed_by_weight['EI'].append(weight)
    elif weight in ['s', 'n']:
        personality_type_indexed_by_weight['SN'].append(weight)
    elif weight in ['t', 'f']:
        personality_type_indexed_by_weight['TF'].append(weight)
    elif weight in ['j', 'p']:
        personality_type_indexed_by_weight['JP'].append(weight)

# create a personality type based on the weighted answers
personality_type = ''
for key in personality_type_indexed_by_weight:
    # find the most frequent weight for each index
    # if there is a tie, choose the first one
    # if there is no weight, choose the first one
    if len(personality_type_indexed_by_weight[key]) == 0:
        personality_type += key[0]
    else:
        personality_type += max(set(personality_type_indexed_by_weight[key]), key=personality_type_indexed_by_weight[key].count)

print(personality_type)
