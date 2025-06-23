import requests

import pandas as pd
import streamlit as st


def works_to_dataframe(works):
    records = []

    for work in works:
        doi = work.get('doi', '')
        title = work.get('title', '')
        publication_year = work.get('publication_year', '')
        language = work.get('language', '')

        primary_location = work.get('primary_location') or {}
        source = primary_location.get('source') or {}
        source_name = source.get('display_name', '')

        topic = (work.get('primary_topic') or {}).get('display_name', '')

        authors = []
        institutions = []
        for author_entry in work.get('authorships', []):
            authors.append(author_entry.get('author', {}).get('display_name', ''))
            if author_entry.get('institutions'):
                institutions.append(author_entry['institutions'][0].get('display_name', ''))
            else:
                institutions.append('')

        topics = []
        for subtopic in work.get('topics', []):
            topics.append(subtopic.get('display_name', ''))

        record = {
            'DOI': doi,
            'Title': title,
            'Publication Year': publication_year,
            'Language': language,
            'Source': source_name,
            'Primary Topic': topic,
            'Authors': '; '.join(authors),
            'Institutions': '; '.join(institutions),
            'Topics': '; '.join(topics)
        }

        records.append(record)

    return pd.DataFrame(records)


headers = {
    "User-Agent": "JupyterNotebook/1.0 (mailto:you@example.com)"
}

base_url = 'https://api.openalex.org'

topik_prof_aqua = {"Gender and Women's Rights": 'T13948',
 'Cultural and Artistic Studies': 'T14105',
 'Islamic Finance and Communication': 'T14281',
 'Linguistics and Language Analysis': 'T13538',
 'Gender, Feminism, and Media': 'T11540',
 'Asian Studies and History': 'T11256',
 'Educational Methods and Media Use': 'T13602',
 'Communication Studies and Media': 'T13716',
 'Literary Theory and Cultural Hermeneutics': 'T13024',
 'Educational Methods and Impacts': 'T14462',
 'Media, Gender, and Advertising': 'T12908',
 'Diverse Cultural Media Analysis': 'T14145',
 'Asian Culture and Media Studies': 'T13303',
 'Cultural and Religious Practices in Indonesia': 'T14022',
 'SMEs Development and Digital Marketing': 'T13053',
 'Legal and Social Justice Studies': 'T13101',
 'Gender Roles and Identity Studies': 'T11888',
 'Media Studies and Communication': 'T10133',
 'Educational Research and Methods': 'T10561',
 'Education, Sociology, Communication Studies': 'T14125',
 'Islamic Studies and Radicalism': 'T14110',
 'Cultural Identity and Representation': 'T13788',
 'Music History and Culture': 'T11113',
 'Language Acquisition and Education': 'T14485',
 'Youth Education and Societal Dynamics': 'T12714'}

pilihan_tahun = [i for i in range(2020, 2026)]
pilihan_bahasa = {
    'Indonesia': 'id',
    'English': 'en'
}

topik = st.sidebar.multiselect('Topik', topik_prof_aqua.keys())
tahun = st.sidebar.multiselect('Tahun', pilihan_tahun)
bahasa = st.sidebar.multiselect('Bahasa', pilihan_bahasa)

topik_str = '|'.join([topik_prof_aqua[i] for i in topik])
tahun_str = '|'.join([str(i) for i in tahun])
bahasa_str = '|'.join([pilihan_bahasa [i] for i in bahasa])


@st.cache_data
def get_sample(topik_param, tahun_param, bahasa_param):
    request_url = f"{base_url}/works?filter=primary_topic.id:{topik_param},language:{bahasa_param},institutions.country_code:id,publication_year:{tahun_param}&per-page=200"
    res = requests.get(request_url)
    return res.json()


if topik_str and tahun_str and bahasa_str:
    data = get_sample(topik_str, tahun_str, bahasa_str)
    data_df = works_to_dataframe(data['results'])

    st.write(f"Total jumlah data {data['meta']['count']}")
    st.dataframe(data_df)


