import spacy
from .skills import SKILLS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)

    return sorted(set(found))


def calculate_similarity(resume_text, jd_text):

    documents = [resume_text, jd_text]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)

    score = similarity[0][1]

    return round(score * 100, 2)


def compare_skills(resume_text, jd_text):

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(jd_text)

    matched = list(set(resume_skills) & set(jd_skills))

    missing = list(set(jd_skills) - set(resume_skills))

    return {

        "resume_skills": sorted(resume_skills),

        "jd_skills": sorted(jd_skills),

        "matched": sorted(matched),

        "missing": sorted(missing)

    }