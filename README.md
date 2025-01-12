# Data Pipelines for LLM Workshop

These pipelines were used in a workshop on Large Language Models (LLMs) at Tel Aviv University. The goal of the project was to create a novel dataset of theoretical computer science questions for LLMs based on past university exams. A few state-of-the-art models were then tested on the new dataset. The code here is partial to the larger project, and handles:
1. Translate Hebrew-language questions into English (in LaTeX format) using the OpenAI API.
2. Pass the translated questions to a LLaMA model to generate answers and measure success statistics.

> **Note**: The actual data and URLs have been excluded to protect confidentiality and prevent data leakage.

1. **phase_1_translation_script.py**  
   - Receives a DataFrame (containing dataset questions in Hebrew).  
   - Translates the questions to English in LaTeX format using the OpenAI API.  
   - Creates PDFs of the translated questions and answers.  
   - Saves newly translated DataFrames as output.

2. **phase_2_main_llama.py**  
   - Loads the translated DataFrame generated in Phase 1.  
   - Sends the questions to a LLaMA model for answering.  
   - Records the model’s responses, success metrics, and question data in a new DataFrame.  
   - Generates a backup log file.

## Requirements
These piplines were used alongside:  
   - The dataframes and urls for the project's files.
   - A LLaMA model data in the 'llama-8B' folder. 
   - The python libraries listed in 'requirements.txt'.