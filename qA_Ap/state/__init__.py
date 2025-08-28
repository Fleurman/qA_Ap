from ..db.qaapdb import qaapDB
from ..app.ai.vectorstore import VectorStore
# from ..app.ai.AIInterface import AIInterface
# from ..app.catalog import Catalog

class State():
    """
        This class stores the active objects needed accross the application.
        
        - DATABASE is a database instance used for all files related processes
        - VECTORSTORE is the database of embeddings used by langchain for the RAG functionalities
    """
    DATABASE: qaapDB = None
    AIINTERFACE = None
    VECTORSTORE: VectorStore = None
    CATALOG  = None

