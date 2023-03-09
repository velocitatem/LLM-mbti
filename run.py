import openai
import json

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


def answer_question(obj):
    # obj is a dictionary with keys: question, options, weights
    # options is a list of strings
    # weights is a list of strings
    # question is a string
    # return a string
    promptString = f"{obj['question']}\n 1. {obj['options'][0]}\n 2. {obj['options'][1]}\nRespond with the number of the option you prefer. You must respond.\nNumber:"
    ans = openai.Completion.create(
        engine="text-davinci-003",
        prompt=promptString,
        temperature=0.8,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    output = ans['choices'][0]['text'].strip()
    print(promptString)
    print(output)
    return obj['weights'][int(ans['choices'][0]['text']) - 1]

weighted_answers = []
for item in data:
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
