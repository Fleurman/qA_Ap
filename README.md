# qA_Ap 
## query About Anything package

![Python](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-green)

## 📝 Description

This package is a simple solution for implementing a **Retrieval Augmented Generation** _(RAG)_ on custom documents. The database and LLM interfaces are modular.

Supports an all local setup with a flat file database and **Ollama** to a totally cloud based setup with a **Baserow** database and **Cerebras** _(both free to use)_.

An optional API server _(bottle.py)_ with custom authentication and an integrated frontend is available to query your documents simply and immediately.

## 📦 Key Dependencies

```
oyaml: 1.0
faiss-cpu: 1.11.0.post1
sentence-transformers: 5.0.0
bottle: 0.13.4
safer: 5.1.0
ollama: 0.5.3
semantic-text-splitter: 0.27.0
cerebras-cloud-sdk: 1.46.0
```

## 📁 Package Structure
```python
qA_Ap # setup method and aliases to core components

qA_Ap.app # documents manipulation methods

qA_Ap.app.catalog # Catalog related functions

qA_Ap.app.ai # internal Vectorstore class for the RAG
qA_Ap.app.ai.interfaces # abstract classes for AI interface
qA_Ap.app.ai.interfaces.ollama # Ollama interface
qA_Ap.app.ai.interfaces.cerebras # Cerebras 'personal tier' interface
qA_Ap.app.ai.methods # AI related methods

qA_Ap.classes # Document and Note classes
qA_Ap.classes.errors # application errors
qA_Ap.classes.errors.db # databse errors

qA_Ap.db # abstract class for database
qA_Ap.db.baserowfreeapi # Baserow free API database class
qA_Ap.db.flatfiledb # flat file stuctured database class

qA_Ap.state # global objects used accross the app

qA_Ap.web # control integrated frontend view
qA_Ap.web.api # API server
```

## 🛠️ How to use

### Python Setup
1. Install Python (v3.8+ recommended)
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

### `qA_Ap.init()` method

All the setup can be made with one method call:

```python
qp.init(
   database: str | qaapdb.qaapDB = "data/qaap_db",
   ai: AIInterface | str = "qwen3:0.6b",
   embeddings_model: str = "Qwen3-Embedding-0.6B",
   object_of_search: str = "solutions",
   system_prompt: str = default_system_prompt,
   api_server: int | dict = 8080,
   allow_post: bool = False,
   frontend: bool = False,
   catalog: bool = True,
   attributes: list[str] = None
)
```

### 

## 👥 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/Fleurman/qA_Ap.git`
3. **Create** a new branch: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add some feature'`
5. **Push** to your branch: `git push origin feature/your-feature`
6. **Open** a pull request

Please ensure your code follows the project's style guidelines and includes tests where applicable.

## 📜 License

This project is licensed under the MIT License.

---
*This README was generated with ❤️ by ReadmeBuddy*