import spacy
from spacy.matcher import Matcher
import re
import pandas as pd
import nltk
import json
from json.decoder import JSONDecodeError
from nltk.corpus import stopwords
import sys
from editDistance import editDistance
import multiprocessing as mp


def get_file_name_without_extension(fileName):
    return re.search(r"^(.+)(\.[^.]*)$", fileName).group(1)


def get_cv_text(fileName):
    input_format = None
    with open('./input_format_mapping.json', 'r') as f:
        content = json.load(f)
        fileLoc = content[get_file_name_without_extension(fileName)]
        with open(fileLoc) as f:
            input_format = f.read()
        return input_format


def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, [*pattern])

    matches = matcher(nlp_text)
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            return span.text


def extract_mobile_number(text):
    mob_num_regex = r'''(0)?(\+91)?[-\s]?(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\) [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    phone = re.findall(re.compile(mob_num_regex), text)

    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number


def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None


def verify_skills(word, skills_data):
    for skill in skills_data:
        if editDistance(str(word).lower(), str(skill).lower()) < (len(str(word))//2)-1:
            print(str(word)+'----->'+str(skill))
            return str(word)
    return False


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the csv file
    data = pd.read_csv("skills.csv")

    # extract values
    skills_data = list(data.columns.values)

    pool = mp.Pool(mp.cpu_count())

    skills = [pool.apply_async(verify_skills, args=(
        str(word), skills_data))for word in nlp_text.noun_chunks]

    # check for bi-grams and tri-grams (example: machine learning)
    token_skills = [pool.apply_async(verify_skills, args=(
        str(word), skills_data)) for word in tokens]

    skills.extend(token_skills)

    skills = [p.get() for p in skills if p.get() is not False]

    return list(set(skills))


# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
    'BE', 'B.E.', 'B.E', 'BS', 'B.S',
    'ME', 'M.E', 'M.E.', 'MS', 'M.S',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
    'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
]


def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education


if __name__ == '__main__':
    try:
        fileName = sys.argv[1]
        text = get_cv_text(fileName)
        # load pre-trained model
        nlp = spacy.load('en_core_web_sm')
        # noun_chunks = nlp.noun_chunks

        # initialize matcher with a vocab
        matcher = Matcher(nlp.vocab)
        doc = nlp(text)

        print(extract_name(text))
        print(extract_mobile_number(text))
        print(extract_email(text))
        print(extract_skills(text))
        print(extract_education(text))
    except IndexError:
        print('Please provide S3 file Name.')
