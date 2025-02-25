# Langchain Streamlit Chatbot

The Langchain Streamlit Chatbot folder features the Data Parser, Data storing, and Chatbot UI application.

# Table of contents

1. [Introduction](#introduction)
2. [Features](#features)
   - [Text Parser](#textparser)
   - [Vector store](#vectorstore)
   - [Chatbot App](#chatbotapp)
3. [Flowchart](#flowchart)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Pseudocode of ppt parser](#pseudocode1)
7. [Pseudocode of vectorstore](#pseudocode2)
8. [Contributing](#contributing)
9. [License](#license)
10. [Issues](#issues)
11. [Credits](#credits)

# Features

### **Text Parser:**

Parse the text frames in a PowerPoint file, store the text and its metadata into json file.

### **Vector store:**

- Text chunking: [RecursiveCharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/recursive_text_splitter)
- Text embeddig: OPENAI [text-embedding-ada-002](https://platform.openai.com/docs/guides/embeddings/use-cases)
- vector database indexing: [FAISS](https://python.langchain.com/docs/integrations/vectorstores/faiss)

### **Chatbot App:**

- [Streamlit](https://streamlit.io/) (UI)
  - [memory](https://python.langchain.com/docs/integrations/memory/streamlit_chat_message_history)
  - [streaming](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_streaming.py)
- [Langchain](https://www.langchain.com/) (data framework)
  - [router](https://python.langchain.com/docs/modules/chains/foundational/router)
  - [streaming final agent output](https://python.langchain.com/docs/modules/agents/how_to/streaming_stdout_final_only)
  - [SQL Database Agent](https://python.langchain.com/docs/integrations/toolkits/sql_database)
- [llamaindex](https://www.llamaindex.ai/) (data framework)
  - [knowledge graph](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/KnowledgeGraphDemo.html)

# Flowchart of Retrieval-Augmented Generative AI Chatbot

![flowchart](https://github.com/Fangning-USC/llm-dataset-digest/blob/main/media/flowchart.png)

# Installation

```shell
$ poetry install
```

# Usage

To set up OPENAI API Key, follow this [link](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

```shell
Variable name: OPENAI_API_KEY
Variable value: <yourkey>
```

To process PowerPoint text parser and create a vectorstore:

```shell
$ python __main__.py
```

Provide the path to PowerPoints, the storage path to vector database, and the name of the vector database. \
This function excecute the following:

1. Ungroup all the grouped shapes in a PowerPoint and save it in the automatically created 'upgroup' folder.
2. Parse the ungrouped ppt and store text within one page into a json file.
3. Load the saved json file recursively. Perform text chunking, embedding, and indexing.
4. Store the vector database using FAISS.

To open the UI of basic Chatbot with streaming:

```shell
$ streamlit run app.py
```

To open the UI with router:

```shell
$ streamlit run app_router_memory.py
```

# Pseudocode of PowerPoints (ppt) Parsing

![pcodePPT](https://github.com/Fangning-USC/llm-dataset-digest/blob/main/media/ppt_parser_pseudocode.jpg)

# Pseudocode of vector storing

![pcodeVS](https://github.com/Fangning-USC/llm-dataset-digest/blob/main/media/vs_pseudocode.png)

# Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

# License

Distributed under the terms of the [TGS license][license],
_Langchain Streamlit Chatbot_.

# Issues

If you encounter any problems, please file an Azure Boards [work item]
along with a detailed description and link it to the
langchain_streamlit_chatbot repository.

# Credits

This project was generated from [TGS Datascience Cookiecutter] template.

[tgs datascience cookiecutter]: https://dev.azure.com/TGSCloud/Datascience/_git/cookiecutter-datascience-project
[work item]: https://dev.azure.com/TGSCloud/Datascience/_workitems/
[pip]: https://pip.pypa.io/

<!-- azure-only -->

[license]: https://dev.azure.com/TGSCloud/Datascience/_git/langchain_streamlit_chatbot?path=/LICENSE&_a=preview
[contributor guide]: https://dev.azure.com/TGSCloud/Datascience/_git/langchain_streamlit_chatbot?path=/CONTRIBUTING.md&_a=preview
[command-line reference]: https://dsdocs.cloud.tgs.com/langchain_streamlit_chatbot/source/usage.html
