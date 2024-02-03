from openai import OpenAI
import os
from dotenv import load_dotenv
import scrape_service
import json


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
            "content": f"""As an extremely experienced recruiter with an outstanding knowledge of the tech industry, your task is to accurately evaluate the applicant's experience and suitability for the provided job description. Utilize the information from the applicant's CV to assess their fit across the following categories: {evaluation_categories_string}. 
            Please format your response in raw JSON, providing a rating on a scale of 1-5 and a brief reasoning for each category. For example, suppose the categories are Technical Skills, Communication Skills, and Teamwork. In that case, your response should resemble the following structure:
            {{ 
              "Technical Skills": {{ "rating": 4, "reasoning": "Has extensive experience with Java and Python, but lacks experience with cloud technologies which the job requires." }},
              "Communication Skills": {{ "rating": 5, "reasoning": "Demonstrated excellent communication skills through various team projects and presentations." }},
              "Teamwork": {{ "rating": 3, "reasoning": "CV highlights individual achievements well but lacks examples of collaborative projects." }}
            }}
            """
          },
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
cv = read_file_content('cv.txt')


def evaluate_seek_job_listings():
  job_data_dict = scrape_service.scrape_seek_job_data(1)

  for key in job_data_dict:
    job_description = f"""
      title: {job_data_dict[key]['title']}
      company: {job_data_dict[key]['advertiser']}
      work_type: {job_data_dict[key]['work_type']}
      description: {job_data_dict[key]['description']}
      """

    job_fit_evaluation = evaluate_cv_against_job_description(cv, job_description, evaluation_categories)
    job_data_dict[key]['job_fit_evaluation'] = job_fit_evaluation
    print(key)
    print(json.dumps(job_data_dict[key], indent=2))

evaluate_seek_job_listings()