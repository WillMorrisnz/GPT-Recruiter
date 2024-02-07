from openai import OpenAI
import os
from dotenv import load_dotenv
import scrape_service
import json
import database_service



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



cv = read_file_content('cv.txt')
job_description = read_file_content('job_description.txt')
evaluation_categories = [
    'Technical Skills relevant to the role', 
    'Education and Certifications', 
    'Soft Skills and Cultural Fit', 
    'Relevant Experience (e.g. Should be directly related to the requirements for the role and the seniority of the role)',
    ]


# -------------------------


def evaluate_cv_against_job_description(cv, job_description, evaluation_categories):

  evaluation_categories_string = ''
  for index, category in enumerate(evaluation_categories):
      if index + 1 == len(evaluation_categories):
        evaluation_categories_string += category
      else:
         evaluation_categories_string += category + ',\n'

  system_prompt = f"""As an extremely experienced recruiter with an outstanding knowledge of the tech industry, 
  your task is to accurately evaluate the applicant's experience and suitability for the provided job description. 
  Utilize the information from the applicant's CV to assess their fit across the following categories: \n{evaluation_categories_string}\n 
  Please format your response in raw JSON, providing a rating on a scale of 1-5 and a brief reasoning for each category. 
  For example, suppose the categories are Technical Skills, Communication Skills, and Teamwork. 
  In that case, your response should resemble the following structure:
    {{ 
    "Technical Skills": {{ "rating": 4, "reasoning": "Has extensive experience with Java and Python, but lacks experience with cloud technologies which the job requires." }},
    "Communication Skills": {{ "rating": 5, "reasoning": "Demonstrated excellent communication skills through various team projects and presentations." }},
    "Teamwork": {{ "rating": 3, "reasoning": "CV highlights individual achievements well but lacks examples of collaborative projects." }}
    }}
    """

  chat_completion = client.chat.completions.create(
      response_format={ "type": "json_object" },
      messages=[
          {
            "role": "system",
            "content": system_prompt
          },
          {
              "role": "user",
              "content": f"APPLICANT_CV: \n{cv} \nJob JOB_DESCRIPTION: \n{job_description}",
          }
      ],
      model="gpt-4-0125-preview",
  )

  json_res = json.loads(chat_completion.choices[0].message.content)
  for key in json_res:
     print(key, json_res[key]['rating'])
  return json_res
 

# -------------------------


def craft_cover_letter_for_role(cv, job_description):
  system_prompt = """When provided with a job description and an applicant's CV, craft a succinct and professional cover letter tailored to the job opening, ensuring the letter does not surpass 250 words and is structured into three key paragraphs:

Paragraph 1 (Expression of Interest): Start with a personalized greeting to the hiring manager. If the job is posted by a recruiting company, ensure to express the applicant's interest specifically in the position with the recruiting company's client, mentioning the client's company by name if possible. Highlight specific attributes or missions of the client's company that align with the applicant's professional interests and aspirations, demonstrating a keen interest in the role and an understanding of the client's impact in their industry.

Paragraph 2 (Main Body): Focus on detailing the applicant's relevant qualifications, including skills, experiences, and achievements, that match the job requirements outlined by the recruiting company for their client. Use specific examples from the CV, such as job roles, projects, technical expertise, and educational background, that demonstrate the applicant's suitability for the client's needs. The aim here is to draw a clear connection between the applicant's capabilities and the job's demands on behalf of the client.

Paragraph 3 (Conclusion and Fit): Conclude by summarizing why the applicant is an excellent match for the client's company culture and the specific role. Reaffirm the applicant's enthusiasm for contributing to the client's objectives and how their background will be advantageous to the client's projects or team.

Additional Instructions:

Maintain professional language and a tone reflective of industry standards.
Clearly differentiate when to refer to the direct hiring company versus the recruiting company's client, particularly emphasizing the client when the job posting comes from a recruiting agency.
Ensure accuracy by directly referencing the applicant's CV for qualifications and experiences relevant to the client's job requirements.
Adapt the cover letter's focus to highlight the applicant's potential contributions to the client's success, considering the role is presented through a recruiting company.
"""

  chat_completion = client.chat.completions.create(
      messages=[
          {
            'role' : 'system',
            'content': system_prompt
          },
          {
            'role': 'user',
            'content' : f"CV: \n{cv}\njob_description:\n{job_description}"
          }
      ],
            model="gpt-4-0125-preview",
  )
  res = chat_completion.choices[0].message.content
  return res


# -------------------------


def evaluate_seek_job_listings(search_term, num_jobs, save_to_db=True):
  job_data_dict = scrape_service.scrape_seek_job_data(search_term, num_jobs)

  for index, key in enumerate(job_data_dict):
    if not database_service.job_id_exists(f"seek_{key}"):
      print(f"\n{index + 1}/{len(job_data_dict)} Evaluating: {job_data_dict[key]['title']}")
      job_description = f"""
        title: {job_data_dict[key]['title']}
        company: {job_data_dict[key]['advertiser']}
        work_type: {job_data_dict[key]['work_type']}
        description: {job_data_dict[key]['description']}
        """

      try:
        job_data_dict[key]['job_fit_evaluation'] = evaluate_cv_against_job_description(cv, job_description, evaluation_categories)
        if save_to_db:
          job_id = 'seek_' + key
          cover_letter = None
          if int(job_data_dict[key]['job_fit_evaluation']['Relevant Experience']['rating']) >= 4:
            print("-- Creating Cover Letter --")
            cover_letter = craft_cover_letter_for_role(cv, job_description)

          database_service.insert_job_listing_to_db(job_id, job_data_dict[key], cover_letter)

      except json.decoder.JSONDecodeError:
        print('Error decoding json response')      

  return job_data_dict


# -------------------------

# res = craft_cover_letter_for_role(cv, job_description)
# print(res)
seek_jobs_dict = evaluate_seek_job_listings('Front End', 20)