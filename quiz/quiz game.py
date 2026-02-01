import json

with open("questions.json", "r", encoding="utf-8") as file:
    data = json.load(file)


answers_counter = 0


def answer_validator(prompt,question_data):
    answers_list = list(question_data["options"].keys())
    while True:
        answer = input(prompt).lower().strip()
        if answer in answers_list:
            return answer
        else:
            print("you need to only type available options:", ", ".join(answers_list))

while True:
    category = input("which category: ").lower()
    if category in data:
        length = len(data[category])
        for question_data in data[category]:
            print("\n" + question_data["question"])

            for key, value in question_data["options"].items():
                print(f"{key}) {value}")
            answer = answer_validator("What is the answer? ",question_data)

            for value in question_data["correct_answer"]:
                if answer == value:
                    answers_counter += 1
        print(f"\nYou answered correctly {answers_counter} out of {length} questions.")
        break
    else:
        print("No such category")
        



