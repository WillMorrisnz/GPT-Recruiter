import sqlite3


def insert_job_listing_to_db(job_id, job_data, cover_letter=None):

    # Connect to the SQLite database (this will create the database if it doesn't exist)
    conn = sqlite3.connect('jobs_database.db')
    cursor = conn.cursor()
    
    # Create table if not exists (optional here, assuming table is already created)
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_listings (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        company TEXT,
                        work_type TEXT,
                        description TEXT,
                        url VARCHAR(512),
                        technical_skills_rating INTEGER,
                        education_certifications_rating INTEGER,
                        soft_skills_cultural_fit_rating INTEGER,
                        relevant_experience_rating INTEGER,
                        evaluation_details TEXT,
                        cover_letter TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Check if the job_id already exists in the database
    cursor.execute("SELECT id FROM job_listings WHERE id = ?", (job_id,))
    if cursor.fetchone():
        conn.close()  # Close the connection since no action is needed
        return  # Exit the function

    # Prepare job evaluation details for storage
    job_evaluation =job_data['job_fit_evaluation']
    technical_skills_rating = int(job_evaluation['Technical Skills']['rating'])
    education_certifications_rating = int(job_evaluation['Education and Certifications']['rating'])
    soft_skills_cultural_fit_rating = int(job_evaluation['Soft Skills and Cultural Fit']['rating'])
    relevant_experience_rating = int(job_evaluation['Relevant Experience']['rating'])
    evaluation_details = str(job_evaluation)
    
    # Insert job listing and evaluation into the database
    cursor.execute('''INSERT INTO job_listings (id, title, company, work_type, description, url,
                     technical_skills_rating, education_certifications_rating,
                     soft_skills_cultural_fit_rating, relevant_experience_rating, evaluation_details, cover_letter)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                     (job_id, job_data['title'], job_data['advertiser'], job_data['work_type'], 
                      job_data['description'], job_data['url'], technical_skills_rating, 
                      education_certifications_rating, soft_skills_cultural_fit_rating, 
                      relevant_experience_rating, evaluation_details, cover_letter))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


# -------------------------

    
    
def job_id_exists(job_id):
    """Check if a given job_id exists in the database."""
    conn = sqlite3.connect('jobs_database.db')
    cursor = conn.cursor()

    # SQL query to check if the job_id exists
    query = "SELECT 1 FROM job_listings WHERE id = ? LIMIT 1;"
    cursor.execute(query, (job_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


    