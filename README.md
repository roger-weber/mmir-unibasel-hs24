# Multimedia Retrieval Course Overview (University of Basel)

This overview provides a summary of the content covered in the Multimedia Retrieval course at the University of Basel. You can find the course material here:
  - [Course in 2024](https://dmi.unibas.ch/de/studium/computer-science-informatik/lehrangebot-hs24/lecture-multimedia-retrieval/)


### Table of contents:
| # | Title | Description |
| :---: | :--- | :--- |
| 01 | [Introduction](01-Introduction/README.md) | In this chapter, we explore the motivation behind multimedia retrieval, trace its historical development, and outline the generic retrieval process along with its variations. We also introduce fundamental machine learning concepts that will be applied in later chapters. |
| 02 | [Evaluation]() | This chapter focuses on evaluating and comparing retrieval systems and machine learning approaches. This serves as the foundation for assessing the effectiveness of methods discussed in most chapters.
| 03 | [Classic Text Retrieval]() | We delve into classical text retrieval models, with a special emphasis on vector space retrieval. Additionally, we explore Lucene, OpenSearch, and Elasticsearch, showcasing the capabilities of these models.

<!--
| 04 | [Advanced Text Retrieval](chapter04/README.md) | Examining natural language processing using NLTK as an example, this chapter also explores modern methods for creating embeddings and leveraging generative AI to enhance retrieval results.
| 05 | [Web & Social Retrieval](chapter05/README.md) | Focusing on web and social media retrieval, this chapter explores methods to influence rankings based on document relationships.
| 06 | [Vector Search](chapter06/README.md) | We explore the challenge of searching through embeddings and feature vectors. Contemporary techniques used by products like Lucene, OpenSearch, and Elasticsearch are studied, along with an exploration of the "curse of dimensionality."
| 07 | [Basic Image Retrieval](chapter07/README.md) | Human perception of visual signal information is covered, along with algorithms for extracting color, texture, and shape features found in images.
| 08 | [Advanced Image Retrieval](chapter08/README.md) | Deep learning and neural networks are delved into in this chapter. These techniques are applied to extract higher-level features, including classifications, facial recognition, and object bounding boxes.
| 09 | [Basic Audio Retrieval](chapter09/README.md) | Human perception of audio signals is explored, studying algorithms for extracting features in both time and frequency domains. The unique case of extracting musical features is also discussed.
| 10 | [Basic Video Retrieval](chapter10/README.md) | Fundamental aspects of motion detection and video segmentation are discussed. The focus is on identifying visual patterns in video content.
| 11 | [ML Methods](chapter11/README.md) | Essential machine learning methods for content analysis and metadata extraction are covered in this chapter. These concepts are revisited and applied throughout the course.

-->


## Helpful software

1. **Installers**
   - [Chocolatey for Windows](https://chocolatey.org/install)
     [Chocolatey package search](https://community.chocolatey.org/packages)
   - [brew for macOS](https://brew.sh/)
     [homebrew formuale](https://formulae.brew.sh/)

2. **Python**
    - **[Download Python](https://www.python.org/downloads/)**
      choco: ```choco install python```
      macOS: ```brew install python```
      Check the version:

      ```bash
        python --version
      ```
  
    - **Set a symlink** for ```python``` to ```python3``` (if it does not exist; or: always use python3 and pip3)

    - **Upgrade pip**

      ```bash
        python -m pip install --upgrade pip
      ```

    - **Best practice**: create a vritual python environment to prevent package version conflicts

      ```bash
        python -m venv .venv

        windows> .venv\scripts\activate
        macOS> source .venv/bin/activate
      ```

      This also works with jupyter notebooks (select the .venv python kernel)
      Deactivate the environment with

      ```bash
        windows> deactivate
        macOS> deactivate
      ```

    - **Keep track of dependencies** with ```requirements.txt``` then use pip to install

      ```bash
        pip install -r requirements.txt
      ```

      Example for ```requirements.txt```:

      ```text
        ###### Requirements without Version Specifiers ######
        nose
        nose-cov
        beautifulsoup4

        ###### Requirements with Version Specifiers ######
        docopt == 0.6.1             # Version Matching. Must be version 0.6.1
        keyring >= 4.1.1            # Minimum version 4.1.1
        coverage != 3.5             # Version Exclusion. Anything except version 3.5
        Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
      ```

    - **[Finding packages (PyPI)](https://pypi.org/)**

3. **Jupyter notebooks**

    - Install Jupyter Notebook, and run from current folder (with *.ipynb files)

      ```bash
        pip install notebook
        jupyter notebook
      ```

    - Optional: install JupyterLab, and run from current folder (with *.ipynb files)

      ```bash
        pip install notebook
        jupyter notebook
      ```

    - Optional: install additional kernels for jupyter
        - [Ganymede](https://github.com/allen-ball/ganymede): JShell Kernel for notebooks
          download the jar `ganymede-nnn.jar`
          install the new kernel `java -jar ganymede-nnn.jar -i`
          restart jupyter notebook / VSCode
          open notebook and select ganymede kernel
          use `%%pom` to load 3rd party libraries

            ```pom
                %%pom
                dependencies:
                - org.apache.lucene:lucene-core:LATEST
                - org.apache.lucene:lucene-analyzers-common:LATEST
                - org.apache.lucene:lucene-queryparser:LATEST
            ```

        - [iRuby](https://github.com/sciruby/iruby#macos)

            ```bash
                gem install iruby
                iruby register --force
            ```

        - [more kernels for other languages](https://github.com/jupyter/jupyter/wiki/Jupyter-kernels)

4. **IDE**

    - [VSCode](https://code.visualstudio.com/)
        Install the following extensions

        ```bash
            Python
            Pylance
            Jupyter
            Java Language Support
            Gradle for Java
            AWS Toolkit
        ```

    - [PyCharm](https://www.jetbrains.com/pycharm/)

    - [Sign-up for Amazon Q (free)](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-free-tier.html)
        (this requires an AWS Builder ID; usage is for free for individual tier; no AWS account required)


## Documentation, tutorials, cheat sheets

- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Python Documentation](https://docs.python.org/3/index.html)
- [Quickstart with Python](https://docs.python.org/3/tutorial/index.html)
- [Python for Data Scientist](https://khuyentran1401.github.io/Efficient_Python_tricks_and_tools_for_data_scientists/README.html)
- [Python Cheat Sheets](https://www.pythoncheatsheet.org/)

## Links

- [Web Site Course (Uni Basel)](https://dmi.unibas.ch/de/studium/computer-science-informatik/lehrangebot-hs24/lecture-multimedia-retrieval/)
- [Link to Adam (Students only)](https://adam.unibas.ch/goto_adam_crs_1738202.html)
