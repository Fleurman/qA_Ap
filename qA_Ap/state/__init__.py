from ..db import qaapDB
from ..app.ai import VectorStore
from ..app.ai.interfaces import AIInterface

class State():
    """
        This class stores the active objects needed accross the application.
        
        - Database is a qA_Ap.db.qaapDB instance used as database.
        - AIInterface is a qA_Ap.app.ai.interfaces.AIInterface used to query a LMM.
        - VectorStore is The qA_Ap.app.ai.VectorStore instance used to store embedded documents and retrieve them by similarity search
    """
    Database: qaapDB = None
    AIInterface: "AIInterface" = None
    VectorStore: "VectorStore" = None

