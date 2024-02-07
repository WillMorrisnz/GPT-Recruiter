# GPT-Recruiter

GPT-Recruiter is a sophisticated job search and application assistant that automates the process of finding, evaluating, and applying for jobs listed on Seek, one of the leading job boards. This innovative project leverages the power of OpenAI's ChatGPT to intelligently evaluate job listings against specified criteria, generating personalized cover letters for positions that meet or exceed a defined evaluation threshold. By integrating advanced natural language processing capabilities, GPT-Recruiter offers a unique blend of automation and personalization, streamlining the job application process for job seekers.

## Key Features

- **Automated Job Scraping:** Seamlessly scrapes job listings from Seek based on user-defined search terms, providing a comprehensive and up-to-date overview of the job market.
- **Intelligent Job Evaluation:** Utilizes ChatGPT to evaluate each job listing against a set of criteria, including technical skills, educational qualifications, soft skills, and relevant experience. Each job is rated to determine its suitability for the user.
- **Dynamic Cover Letter Generation:** For jobs that surpass the evaluation threshold, GPT-Recruiter crafts personalized cover letters, tailored to highlight the user's qualifications and interest in the specific role, maximizing the chances of standing out to potential employers.
- **Persistent Data Storage:** All scraped job listings, evaluations, and generated cover letters are systematically saved to an SQLite database, enabling efficient tracking and management of job applications.
- **Evaluation Threshold Customization:** Users can set and adjust the evaluation threshold to match their career goals and preferences, ensuring that only the most relevant opportunities trigger the generation of cover letters.

## How It Works

1. **Scraping:** The system scrapes Seek for job listings based on predefined or user-input search terms.
2. **Evaluation:** Each listing is evaluated using ChatGPT, with jobs rated on technical skills, education, soft skills, and experience.
3. **Cover Letter Generation:** For listings that meet or exceed the threshold, personalized cover letters are generated, emphasizing the user's suitability and enthusiasm for the position.
4. **Database Storage:** Job listings, evaluations, and cover letters are stored in an SQLite database, with functionality to check for duplicate listings to avoid reprocessing.

## Getting Started
- OpenAI API Key
- Scraping Bee API Key
  
 --- WIP ---

## Acknowledgments

- OpenAI for providing the powerful GPT API.
