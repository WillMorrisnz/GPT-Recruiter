from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------


def read_file_content(filename):
    """Read the content of a file and return it as a string."""
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "File not found."


# -------------------------


def evaluate_cv_against_job_description(cv, job_description, evaluation_categories):

  evaluation_categories_string = ''
  for index, category in enumerate(evaluation_categories):
      if index + 1 == len(evaluation_categories):
        evaluation_categories_string += category
      else:
         evaluation_categories_string += category + ', '


  chat_completion = client.chat.completions.create(
      messages=[
          {
            "role": "system",
            "content": f"""You are a extremly experienced recruiter with an outstanding knowledge of the tech industry. \
              Your task is to evaluate the experience and suitability of the applicant for the provided job description using information from the applicants cv. 
              Please only respond with a rating for the applicant out of 5 for each of the following categories: 
              {evaluation_categories_string}
              Your response should be in json format with a rating and short reasoning for the rating. e.g.{{"Technical Skills": {{rating : 4, reasoning : ... }}}}"""},
          {
              "role": "user",
              "content": f"CV: {cv} \n Job Description: {job_description}",
          }
      ],
      model="gpt-4-0125-preview",
  )
  return chat_completion.choices[0].message.content


# -------------------------

evaluation_categories = [
   'Technical Skills relevant to the role', 
    'Education and Certifications', 
    'Soft Skills and Cultural Fit', 
    'Relevant Experience',
    ]
job_description = read_file_content('job_description.txt')
cv = read_file_content('cv.txt')

print(evaluate_cv_against_job_description(cv, job_description, evaluation_categories))
