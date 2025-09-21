# <p align="center"> PyPI & Python FAQ

<p align="center"><img src = https://imageio.forbes.com/specials-images/dam/imageserve/1162986933/960x0.jpg?height=533&width=711&fit=bounds></p>

# <p align="center"> CHATBOT

<p align="center">
  <a href="https://radimrehurek.com/gensim/models/word2vec.html" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/word2vec-3C78A9?logo=gensim&logoColor=white" alt="word2vec (gensim)">
  </a>&nbsp;
  <a href="https://github.com/spotify/annoy" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/Annoy-1DB954?logo=spotify&logoColor=white" alt="Annoy">
  </a>&nbsp;
  <a href="https://spacy.io" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/spaCy-09A3D5?logo=spacy&logoColor=white" alt="spaCy">
  </a>&nbsp;
  <a href="https://streamlit.io" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  </a>&nbsp;
  <a href="https://pypi.org/project/rank-bm25/" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/BM25%20Okapi-444444" alt="BM25 Okapi (rank-bm25)">
  </a>&nbsp;
  <a href="https://requests.readthedocs.io/en/latest/" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/Requests-000000" alt="Requests">
  </a>&nbsp;
  <a href="https://www.crummy.com/software/BeautifulSoup/bs4/doc/" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/BeautifulSoup-181717" alt="BeautifulSoup">
  </a>&nbsp;
  <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener">
    <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
</p>


## Content
[1. Project Description](README.md#project-description)

[2. Datasets & Trainings](README.md#datasets-and-training)

[3. Model Deployment](README.md#model-deployment)

[4. Conclusion](README.md#conclusion)

[5. Contacts]()

### Project Description
A lightweight retrieval-augmented chatbot that can (a) recognize the question about a Python package  and return the closest product match from a PyPI-like catalog, or (b) detect general Python questions and answer from a curated FAQ. It uses classic NLP and vector search:
 - **Preprocessing**: spaCy (or fallback tokenizer) & stop-words & lemmatization
 - **Embeddings**: Word2Vec (Gensim) trained on product titles / descriptions + FAQ questions
 - **ANN Search**: Annoy indexes for products and FAQ
 - **Classifier**: TF-IDF and LinearSVC with optional Logistic Regression to gate "product vs. chatter"
 - **Lexical / BM25 guardrails**: exact / overlap match, optional BM25 for FAQ to reduce off-topic hits.

 Works locally via **Streamlit** UI or **FastAPI** API.

[To the top](README.md#content)

### Datasets and Training
1. **Product Catalog** (PyPI - style)
- File: data/products_pypi.csv
- Columns: at minimum product_id, title, description
- Seeded with popular packages (numpy, pandas, requests, scikit-learn, etc.) plus extras fetched from PyPI. This file can be extended or refreshed.

2. **Python FAQ**
- Raw source: data/raw/Python FAQ Dataset.zip (training - time only)
- Used at runtime: none (FAQ is compiled into the Annoy index and saved as maps)
- Training Artifacts (produced by the notebook): models; classifiers.

Rebuild process is in the notebook: it loads the raw CSV/ZIP, preprocesses, trains Word2Vec, builds Annoy indexes, trains classifier(s), and saves the artifacts above.

[To the top](README.md#content)

### Model Deployment
**Run the Streamlit APP**

``` streamlit run app_streamlit.py```

**Run the FastAPI**

```uvicorn api:app --reload```

**Minimal Python Test**

```from bot_core import Chatbot```

```bot = Chatbot(base_dir=".")```

```print(bot.get_answer("pip install numpy"))```

```print(bot.get_answer("How do I create a virtual environment in Python?"))```

```print(bot.get_answer("scikit learn"))```

**Important: spaCy model**

spaCy's English model is **not** included in **requirements.txt**. Install it once per environment:
```python -m spacy download en_core_web_sm```

[To the top](README.md#content)

### Conclusion
The chatbot delivers fast, local inference using simple, inspectable components. Its routing stack - name / pip cues, lexical matching, optional BM25, and semantic search - keeps most queries on track. It is also easy to grow by extending the product catalog and FAQ. Looking ahead, the main opportunity is to enrich the datasets with more PyPI packages and a larger, curated FAQ.

[To the top](README.md#content)

### Contacts

<p align="center">
  <a href="mailto:natalia_konovalova@icloud.com">
    <img src="https://img.shields.io/badge/Email-D14836?logo=gmail&logoColor=white" />
  </a>
  <a href="https://www.linkedin.com/in/natalia-ds-198612241">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?logo=linkedin&logoColor=white" />
  </a>
  <a href="https://www.kaggle.com/nataliamantyk">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?logo=kaggle&logoColor=white" />
  </a>
  <a href="https://t.me/KonovalovaDS">
    <img src="https://img.shields.io/badge/Telegram-26A5E4?logo=telegram&logoColor=white" />
  </a>
</p>

[To the top](README.md#content)