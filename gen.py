import pandas as pd
from rich.console import Console
from rich.theme import Theme
from rich.table import Table

console = Console()

pretest_report = pd.read_csv('report.csv')

difficulty_weights = {'Beginner': 3, 'Intermediate': 5, 'Advanced': 8}
time_thresholds = {'Beginner': 10, 'Intermediate': 20, 'Advanced': 30}
penalty_factor = 1

proficiency_levels = ['Beginner', 'Intermediate', 'Advanced']
min_scores = [0, 30, 60]

total_score = 0
elapsed_time = 0
correct_ans = 0
adv_q = 0
intr_q =0
big_q = 0

for index, row in pretest_report.iterrows():
    user_answer = row['Selected Answer']
    correct_answer = row['Answer']
    time_taken = row['Time Taken']
    difficulty_level = row['Level']
    status = row['Status']

    if status == "correct":
        correct_ans+=1
        if difficulty_level == "Beginner":
            big_q+=1
        elif difficulty_level == "Intermediate":
            intr_q+=1
        elif difficulty_level == "Advanced":
            adv_q+=1

        weight = difficulty_weights[difficulty_level]
        time_threshold = time_thresholds[difficulty_level]
        penalty = penalty_factor * max(0, time_taken - time_threshold)
        bonus = 1 if time_taken < time_threshold else 0
        score = (weight * (1 + bonus)) - penalty
    else:
        score = 0

    total_score += score
    elapsed_time += time_taken

level_index = -1
for i in range(len(proficiency_levels)):
    if total_score >= min_scores[i]:
        level_index = i

if level_index == -1:
    proficiency_level = 'No proficiency level'
else:
    proficiency_level = proficiency_levels[level_index]

table = Table(title="Student Score Report")
table.add_column("Total Score")
table.add_column("Correct Answers")
table.add_column("Beginner")
table.add_column("Intermediate")
table.add_column("Advanced")
table.add_column("Proficiency Level")
table.add_row(str(total_score), str(correct_ans), str(big_q), str(intr_q), str(adv_q), proficiency_level)
console.print(table, justify='center')
# print("Your score is "+ str(total_score))
# print(f"You are Answered {correct_ans} questions Correctly!!\n")
# print(f"They are Beginner:{big_q} Intermediate:{intr_q} Advanced:{adv_q}\n")
# print('The student belongs to', proficiency_level, 'proficiency level\n')
