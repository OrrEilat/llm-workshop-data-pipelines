# imports

import openai
from openai import OpenAI
import os
import pandas as pd
import random
import pickle

# change to the directory where the data is
# os.chdir(r"C:\Users\USER\Desktop\vscode_env\archive\misc\github") 

#===========================================================================#

# OPEN AI

# set up the openai client
model = "gpt-4o-2024-08-06"
key = "your-key-goes-here"
prompt_header = r"""
translate the following to english. your response should contain only the latex code for the translation - nothing else. mathematical expressions should be properly formated. assume the document has already started with the following code:
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\title{Title}

\begin{document}

\maketitle

\section{Translated question no. 1}
% your response here

the code should compile cleanly without errors. your code will be pasted into the latex document, so don't include anything that is not the latex code for the translation.

question to translate:
"""
client = OpenAI(api_key=key)


# wrapper for translating a question via openai api
def translate(question):
    prompt = prompt_header + question
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

#===========================================================================#

# HELPER FUNCTIONS

# input: a string that is a link to a google doc
# output: the filename of the document
# note: the original implementation was removed to avoid revealing the links. currently, the function is a stub.
def get_filename(s):
    return "filename"
    
# input: a row number in the dataframe
# output: a string that is the title of the question, to be used in the latex document
def make_title(row_number):
    title = "Filename: " + get_filename(df.at[row_number, "Url of the exam file in our shared directory"]) + ", "
    title = title.replace("_", "\_")
    title += "Year: " + str(df.at[row_number, "Exam year"]) + ", "
    title += "Semester: " + str(df.at[row_number, "Semester"]) + ", "
    title += "Moed: " + str(df.at[row_number, "Moed"]) + ", "
    title += "Question Number: " + str(df.at[row_number, "Question number in the exam"])
    return title

# input: a row number in the dataframe
# output: a string that is the latex code for the translated question
def make_latex_item(row_number):
    s = "\section{" + make_title(row_number) + "}\n"
    s += str(df.at[row_number, "Translation of the question to english in Latex format"]) + "\n"
    return s

# input: a row number in the dataframe
# output: a string that is the latex code for the translated answer
def make_latex_answer_item(row_number):
    s = "\section{" + make_title(row_number) + "}\n"
    s += str(df.at[row_number, "Translation of open answer or short explanation"]) + "\n"
    return s

# input: a dataframe
# output: a latex code, creating a file with all the translated questions
def make_latex_file(df):

    s = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\title{T1 Translated Questions}
\author{Submitted by Abed and Orr}
\date{}

\begin{document}

\maketitle

"""

    for i in range(len(df)):
        if df.at[i, "Translation of the question to english in Latex format"] != "N\A":
            s += make_latex_item(i)

    s += r"\end{document}" + "\n"

    return s

# input: a dataframe
# output: a latex code, creating a file with all the translated answers
def make_latex_answers_file(df):

    s = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath}

\title{T1 Translated Questions}
\author{Submitted by Abed and Orr}
\date{}

\begin{document}

\maketitle

"""

    for i in range(len(df)):
        if df.at[i, "Translation of open answer or short explanation"] != "N\A":
            s += make_latex_answer_item(i)

    s += r"\end{document}" + "\n"

    return s

#===========================================================================#

# load dataframe
df = pd.read_excel("question_data1a.xlsx")

# creating a list questions that are of type B, C, or D
BCD_questions = []
for i, row in df.iterrows():
    if row["Type of question"] in ["B", "C", "D"]:
        BCD_questions.append(i)

# choosing a 2/3 of the questions in random
random.shuffle(BCD_questions)
question_to_translate = BCD_questions[:int(len(BCD_questions) * 2 / 3)]

# translating the questions
for i in question_to_translate:
    df.at[i, "Translation of the question to english in Latex format"] = translate(df.at[i, "the question in hebrew "])
    df.at[i, "the request for the translation included both the question and answer"] = True
    print("translated question number", i)

# translating the answers
for i in question_to_translate:
    if df.at[i, "Has solution?"] != True:
        print("no solution")
        continue
    if df.at[i, "Open answer or short explanation"] == "N\A":
        print("no open answer")
        continue
    df.at[i, "Translation of open answer or short explanation"] = translate(df.at[i, "Open answer or short explanation"])
    print("translated question number", i)

# replacing nan with "N\A" in all columns
df = df.fillna("N\A")

# removing the latex header from data
for i in question_to_translate:
    if df.at[i, "Translation of the question to english in Latex format"] != "N\A":
        data = df.at[i, "Translation of the question to english in Latex format"]
        # clean the latex header
        data = data.replace("```latex", "")
        data = data.replace("```", "")
        data = data.replace(r"\end{document}", "")
        df.at[i, "Translation of the question to english in Latex format"] = data
    if df.at[i, "Translation of open answer or short explanation"] != "N\A":
        data = df.at[i, "Translation of open answer or short explanation"]
        # clean the latex header
        data = data.replace("```latex", "")
        data = data.replace("```", "")
        data = data.replace(r"\end{document}", "")
        df.at[i, "Translation of open answer or short explanation"] = data

# create and save questions latex file
with open("translated_questions.tex", "w") as f:
    f.write(make_latex_file(df))

# create and save answers latex file
with open("translated_answers.tex", "w") as f:
    f.write(make_latex_answers_file(df))

# saving the dataframe as a pickle
with open("question_data1a_processed.pkl", "wb") as f:
    pickle.dump(df, f)

# saving the dataframe as an excel file
df.to_excel("question_data1a_processed.xlsx", index=False)

#===========================================================================#

