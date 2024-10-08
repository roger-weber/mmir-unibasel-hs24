# Chapter 3: Classic Text Retrieval

We delve into classical text retrieval models, with a special emphasis on vector space retrieval. Additionally, we explore Lucene, OpenSearch, and Elasticsearch, showcasing the capabilities of these models.

- [Slides](03_ClassicalTextRetrieval.pdf)


## Demos

- [Extract features from images and audio](01-extract-features.ipynb): extracts features from a pdf document and shows varies aspects of classical doucment features
- [Boolean Retrieval with Inverted Files](02-boolean-retrieval.ipynb): demonstrates boolean retrieval with the animals dataset and provides code for streamed evaluation from an inverted files
- [Probabilistic Retrieval with the BIR model](03-probabilistic-retrieval.ipynb): show case for probabilistic retrieval with the BIR model and the movide dataset. Includes an interactive query view with feedback. Contains code for document-at-a-time and term-at-a-time evaluation based on inverted files
- [Vector Space Retrieval](04-vectorspace-retrieval.ipynb): demo for vector space retrieval using inverted files. The exmaple uses the movies data set and allows for combined keyword and predicate search with different scoring functions
- [SQL based Classical Retrieveal](05-sql-retrieval.ipynb): shows how to implement the classical retrieval models with a SQL based database. Uses the movies data set to provide an example
- [Lucene](06-lucene.ipynb): interactive notebook showcasing varioous aspects of Lucene. This requires the installation of the Ganymede kernel for jupyter notebooks


## Installations
- install require python dependencies at root folder
  ```
    pip install -r requirements.txt
  ```

- [Ganymede](https://github.com/allen-ball/ganymede)
  - download the jar `ganymede-nnn.jar`
  - install the new kernel `java -jar ganymede-nnn.jar -i`
  - restart jupyter notebook / VSCode
  - open notebook and select ganymede kernel
  - use `%%pom` to load 3rd party libraries

    ```pom
    %%pom
    dependencies:
    - org.apache.lucene:lucene-core:LATEST
    - org.apache.lucene:lucene-analyzers-common:LATEST
    - org.apache.lucene:lucene-queryparser:LATEST
    ```

## Data sets

- [IMDB Top 1000 movies](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)
- [Music from 1950 to 2019](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019)
- [Song lyrics from 79 musical genres](https://www.kaggle.com/datasets/neisse/scrapped-lyrics-from-6-genres)


