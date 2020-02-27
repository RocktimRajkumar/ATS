import boto3
import time
import spacy
from spacy.matcher import Matcher
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords


# textract = boto3.client('textract')

# s3_obj = {"Bucket": "poc-cloudformation-bucket", "Name": "Resume.pdf"}

# response = textract.start_document_text_detection(
#     DocumentLocation={
#         'S3Object': s3_obj
#     }
# )

# time.sleep(5)

# response1 = textract.get_document_text_detection(
#     JobId=response['JobId'],
# )


# print(response)
# status = response1['JobStatus']
# while status == "IN_PROGRESS":
#     time.sleep(5)
#     response1 = textract.get_document_text_detection(
#         JobId=response['JobId'],
#     )
#     status = response1['JobStatus']
#     print("Job status: {}".format(status))

# print(response1['Blocks'][0])

# text = ""
# for item in response1['Blocks']:
#     if item['BlockType'] == 'LINE':
#         print("{}\t{}".format(item['Text'], item['Confidence']))
#         text = text + " "+item['Text']


# with open('resumeText.txt', 'w') as outfile:
#     outfile.write(text)

text = " RAJKUMAR ROCKTIM NARAYAN SINRHA SOFTWARE ENGINEER 12-FEB-1997 ttps://www.linkedin.com/in/rocktim-raikumarl CONTACT OBJECTIVE 8011806053 Enthusiastic IT specialist with 2 years of experience. Skilled in software development, technical, coding and analytical Seeking to boost my software rajkumar.rocktim@gmail.com development skills with modern technology like ML, Block Chain, Cloud and 9 IOT. Rajbari Lane, Jorhat, Assam 785001 EXPERIENCE SKILLS Software Engineer (Internship) DataGrokr (Bangalore) J2EE Jan 2020 - Present PYTHON Build a ML product using AWS service like Textract, EC2, Lambda, API GW, S3 and also used Python as programming language. DS & ALGORITHMS CLOUD COMPUTING (AWS) Software Developer DEVOPS Tata Consultancy Service (Kolkata) July 2018 - Jan 2020 JAVASCRIPT To capture data to transfer and transform it into processing language. To build industry ANGULAR JS specific solution based on industry needs, managed and upgrade existing system. Carries out detailed analysis to understand requirement. Perform unit test as per the WEB APP test plans and test cases. Using Technology Java Spring, Angular JS, PL/SQL and Jenkins for CI/CD. GIT SQL PROJECTS EDUCATION CrowdFunding-Ethereum Jorhat Institute of S & T Block Chain Jan 2019 - Aug 2019 BE 2015-2018 A decentralized application of funding a project or venture by raising a small amount of Bachelor of Science in Information Technology money from a large number of people using Ethereum block chain technology. htteslaithub.com/RocktimraikumalcrowdFunding:Ethereum Luit Valley Academy Technology used Solidity, React JS, GIT, Ethereum Block Chain. 2012-2014 Higher Secondary in Science (12th) Job Porta Android Spring Dale High School Mar 2018 - April 2018 2001-2012 The Objective of the Application is to develop a system using which job applicants and recruiters can communicate with each other. Secondary Schoo (10th) https:/github.com/Rocktimraikumarljob-portal) Technology used JAVA/XML."


# comprehend = boto3.client('comprehend')
# sentiment = comprehend.detect_sentiment(LanguageCode="en", Text=text)
# print("\nSentiment\n==========\n{}".format(sentiment.get('Sentiment')))

# entities = comprehend.detect_entities(LanguageCode='en', Text=text)


# for entity in entities['Entities']:
#     print("{}\t=>\t{}".format(entity['Type'], entity['Text']))


# load pre-trained model
nlp = spacy.load('en_core_web_sm')
# noun_chunks = nlp.noun_chunks


# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

doc = nlp(text)


def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('NAME', None, [*pattern])

    matches = matcher(nlp_text)
    aa = []
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        aa.append(span.text)

    return aa


def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    
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


def extract_skills(resume_text):
    nlp_text = nlp(resume_text)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    
    # reading the csv file
    data = pd.read_csv("skills.csv") 
    
    # extract values
    skills = list(data.columns.values)
    
    skillset = []
    
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in nlp_text.noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
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

print(extract_name(text))
print(extract_mobile_number(text))
print(extract_email(text))
print(extract_skills(text))
print(extract_education(text))

# for ent in doc.ents:

#     print(ent.text, ent.start_char, ent.end_char, ent.label_)
