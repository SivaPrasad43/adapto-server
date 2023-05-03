import pandas as pd
import random
import streamlit as st
import os
import time
from timeit import default_timer as timer

data = pd.read_csv("ques.csv")
options = ["A","B","C","D"]
beginner_count=intermediate_count=advanced_count = 0
point = 0 

def typing_display(text, delay=0.1):
    for char in text:
        st.text(char, end='', flush=True)
        time.sleep(delay)
    st.write('')

def program_exp():
    user_ans = st.radio("Do you have programming experience?", ("Yes", "No"))
    return user_ans

def run_quiz():
    st.write("## Pre-Assessment Test")
    st.write("### Subject: PYTHON")
    response = program_exp()
    for count in range(9):
        question_set = question(count)
        selection_set = select_answer()
        check_answer(question_set, selection_set, response)

def select_answer():
    starting_time = timer()
    answer = st.selectbox("Select an option", options)
    end_time = timer()
    time_taken = end_time - starting_time
    return answer,time_taken

def question(count):
    st.write("--------------------------------------")
    random_index = random.choice(data.index)
    random_row = data.loc[random_index]
    question_id = random_row['Question ID']
    question = random_row['Question']
    answer = random_row['Correct Answer']
    level = random_row['Difficulty Level']
    global beginner_count, intermediate_count, advanced_count
    if level == "Beginner" and beginner_count<=3:
        st.write(f"{count+1} - {question}")
        beginner_count+=1
    elif level == "Intermediate" and intermediate_count<=3:
        st.write(f"{count+1} - {question}")
        intermediate_count+=1
    elif level == "Advanced" and advanced_count<=3:
        st.write(f"{count+1} - {question}")
        advanced_count+=1
    for i, op in enumerate(random_row[options]):
        st.write(f"{options[i]}) {op}")
    st.write("--------------------------------------")
    st.write(f"status => big : {beginner_count} inter : {intermediate_count} adv: {advanced_count}\n")
    return question_id, question, answer, level

def check_answer(question_set, selection_set, response):
    global point, status
    if selection_set[0] == question_set[2]:
        st.write("### Correct!!")
        point = mark_obtained(question_set[3])
        status = "correct"
    else:
        st.write("### Wrong!!")
        status = "wrong"
    generate_analysis_report(question_set, selection_set, point, status, response)
    st.write(f"Question Level : {question_set[3]}")
    st.write(f"Time Taken : {'{:.2f}'.format(selection_set[1])} sec")
    point = 0

def mark_obtained(level):
    if level == "Beginner":
        return 1
    elif level == "Intermediate":
        return 2
    else:
        return 3

def generate_analysis_report(question_set, selection_set, point, status, response):
    analysis_data = {
        'qid': question_set[0],
        'prog exp': response,
        'Answer': question_set[2],
        'Selected Answer': selection_set[0],
        'Time Taken': '{:.2f}'.format(selection_set[1]),
        'Status': status,
        'Mark Obtained': point,
        'Level': question_set[3]
    }
    new_row = pd.DataFrame([analysis_data])
    if os.path.isfile('report.csv'):
        df = pd.read_csv('report.csv')
        df = df.append(new_row, ignore_index=True)
        df.to_csv('report.csv', index=False)
    else:
        df = pd.DataFrame([analysis_data])
        df.to_csv('report.csv', index=False)

if __name__ == "__main__":
    run_quiz()