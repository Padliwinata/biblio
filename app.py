from io import StringIO
from math import ceil
import requests
import time

import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


class Work:
    def __init__(self, data):
        self.doi = data.get('doi', '')
        self.title = data.get('title', '')
        self.publication_year = data.get('publication_year', '')
        self.citation = data.get('cited_by_count', '')
        self.language = data.get('language', '')

        primary_location = data.get('primary_location') or {}
        source = primary_location.get('source') or {}
        self.source_name = source.get('display_name', '')

        self.topic = (data.get('primary_topic') or {}).get('display_name', '')

        self.authors = []
        self.institutions = []
        for author_entry in data.get('authorships', []):
            self.authors.append(author_entry.get('author', {}).get('display_name', ''))
            if author_entry.get('institutions'):
                self.institutions.append(author_entry['institutions'][0].get('display_name', ''))
            else:
                self.institutions.append('')

        self.topics = [t.get('display_name', '') for t in data.get('topics', [])]
        self.concepts = [c.get('display_name', '') for c in data.get('concepts', [])]

    def json(self):
        return {
            'doi': self.doi,
            'title': self.title,
            'publication_year': self.publication_year,
            'citation': self.citation,
            'language': self.language,
            'source_name': self.source_name,
            'topic': self.topic,
            'authors': self.authors,
            'institutions': self.institutions,
            'topics': self.topics,
            'concepts': self.concepts,
        }

    def __repr__(self):
        return f"<Work title='{self.title}' doi='{self.doi}'>"


class WorkResult:
    base_url = 'https://api.openalex.org'
    headers = {
        "User-Agent": "JupyterNotebook/1.0 (mailto:you@example.com)"
    }

    def __init__(self, endpoint_or_data):
        self.works = []
        if isinstance(endpoint_or_data, str):
            url = (
                endpoint_or_data
                if endpoint_or_data.startswith("http")
                else f"{self.base_url}{endpoint_or_data}"
            )
            self.url = url
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self._data = response.json()
        elif isinstance(endpoint_or_data, dict):
            self._data = endpoint_or_data
        else:
            raise ValueError("Input must be a URL string or a dict (already fetched JSON).")

        self.results = self._data.get('results', [])
        self.samples = [Work(work_data) for work_data in self.results]
        self.count = self._data.get('meta', {}).get('count', 0)

        # Automatically set metadata attributes
        for key, value in self._data.items():
            if key != "results":
                setattr(self, key, value)

    def __repr__(self):
        return f"<WorkResult count={getattr(self, 'count', 0)}>"

    def get_df(self):
        self.samples = [Work(work_data) for work_data in self.results]
        return pd.DataFrame([sample.json() for sample in self.samples])

    def get_complete_records(self):
        cursor = "*"
        counter = 1

        res = requests.get(f"{self.url}&per-page=200&cursor={cursor}", headers=self.headers)
        self.works.extend([Work(work_data).json() for work_data in res.json().get('results', [])])
        cursor = res.json()['meta']['next_cursor']
        counter += 1
        time.sleep(5)

        num = ceil(self.count/200)
        max_num = 100 - (100 % num)
        step = int(max_num / num)

        bar = st.progress(0, 'Downloading')
        for i in range(step, max_num+1, step):
            try:
                bar.progress(i, 'Downloading')
                res = requests.get(f"{self.url}&per-page=200&cursor={cursor}", headers=self.headers)
                self.works.extend([Work(work_data).json() for work_data in res.json().get('results', [])])
                cursor = res.json()['meta']['next_cursor']
                counter += 1
                time.sleep(5)
            except KeyError as e:
                print("Fetching data finished")
                break

        for i in range(max_num, 101):
            bar.progress(i, 'Downloading')

        # Convert to DataFrame
        df = pd.DataFrame(self.works)

        # Convert to CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')  # utf-8-sig ensures compatibility with Excel
        csv_buffer.seek(0)

        return csv_buffer


def works_to_dataframe(self):
    records = []

    for work in self.works:
        doi = work.get('doi', '')
        title = work.get('title', '')
        publication_year = work.get('publication_year', '')
        citation = work.get('cited_by_count', '')
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

        concepts = []
        for concept in work.get('concepts', []):
            concepts.append(concept.get('display_name', ''))

        record = {
            'DOI': doi,
            'Title': title,
            'Publication Year': publication_year,
            'Citations': citation,
            'Language': language,
            'Source': source_name,
            'Primary Topic': topic,
            'Authors': '; '.join(authors),
            'Institutions': '; '.join(institutions),
            'Topics': '; '.join(topics),
            'Concept': '; '.join(concepts)
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
specific = st.sidebar.toggle('Spesifik')
is_download = st.sidebar.toggle('Download')

topik_str = '|'.join([topik_prof_aqua[i] for i in topik])
tahun_str = '|'.join([str(i) for i in tahun])
bahasa_str = '|'.join([pilihan_bahasa [i] for i in bahasa])


title_contains = ''
if specific:
    title_contains = st.sidebar.text_input('Keyword')


@st.cache_resource
def get_sample(topik_param, tahun_param, bahasa_param, title_contains_param):
    request_url = f"/works?filter=primary_topic.id:{topik_param},language:{bahasa_param},institutions.country_code:id,publication_year:{tahun_param}&per-page=200"
    if title_contains_param:
        request_url = f"/works?filter=primary_topic.id:{topik_param},language:{bahasa_param},institutions.country_code:id,publication_year:{tahun_param},title.search:{title_contains_param}&per-page=200"
    # res = requests.get(request_url)
    res = WorkResult(request_url)
    return res


if topik_str and tahun_str and bahasa_str:
    result_obj = get_sample(topik_str, tahun_str, bahasa_str, title_contains)
    data_df = result_obj.get_df()

    st.write(f"Total jumlah data {result_obj.count}")
    st.dataframe(data_df.reset_index(drop=True))

    if is_download:
        csv_data = result_obj.get_complete_records().getvalue()
        st.download_button(
            "Download Complete Records",
            data=csv_data,
            file_name="openalex_result.csv",
            mime="text/csv"
        )

    # # Define bins and labels based on your data's distribution
    # bins = [-1, 0, 2, 5, 10, 20, 50, float('inf')]
    # labels = ['0', '1–2', '3–5', '6–10', '11–20', '21–50', '51+']
    #
    # # Perform binning without modifying df
    # citation_ranges = pd.cut(data_df['Citations'], bins=bins, labels=labels)
    #
    # # Create frequency table
    # freq_table = citation_ranges.value_counts(sort=False).reset_index()
    # freq_table.columns = ['citation', 'n']
    # freq_table['percentage'] = (freq_table['n'] / freq_table['n'].sum() * 100).round(2)
    #
    # st.dataframe(freq_table)
    #
    # st.title(f"Download full {data['meta']['count']} data")


