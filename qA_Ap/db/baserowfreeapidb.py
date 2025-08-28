from enum import StrEnum
import requests
import json

from .errors import FileAlreadyExistsError, WriteInDatabaseError
from .ottoDB import ottoDB
from ..classes import Document

class BaseRowFreeApiDB(ottoDB):

    class TABLES(StrEnum):
        POSTS = "646003"
        POSTS_MEDIAS = "650559"
        COMMENTS = "648243"
        COMMENTS_MEDIAS = "650572"
        SUMMARIES = "648264"
        RAG = "648276"

    def __init__(self, token: str):
        """
            Initializes a BaseRowDB instance (inherits from qA_ApDB).

            Args:
                token (str): The API token for authentication with the BaseRow API.
        """
        ottoDB.__init__(self)
        self.token = token

    def _filter_by_fields_value(self, fields: list[tuple[str,str]], orfields: list[tuple[str,str]] = []) -> str:
        """
            Constructs a filter dictionary for querying the BaseRow API.
            This method creates a filter that matches rows based on specified field-value pairs.

            Args:
                fields (list[tuple[str,str]]): A list of tuples where each tuple contains a field name and its corresponding value.

            Returns:
                dict[str, str]: A dictionary representing the filter.
        """
        
        return json.dumps({
            "filter_type": "AND",
            "filters": [
                {
                    "type": "equal",
                    "field": field,
                    "value": value
                } for field, value in fields
            ],
            "groups": [
                {
                    "filter_type": "OR",
                    "filters": [
                        {
                            "type": "equal",
                            "field": field,
                            "value": value
                        } for field, value in orfields
                    ],
                    "groups": []
                }
            ]
        })
    
    def _include_fields(self, fields: list[str]) -> str:
        """
            Constructs an include string for querying the BaseRow API.

            Args:
                fields (list[str]): A list of field names to include in the query.

            Returns:
                str: A string representing the fields to include.
        """
        return ",".join(fields)

    def _get(self, table: TABLES, include: list[str] = None, filters: list[tuple[str,str]] = None, orfilters: list[tuple[str,str]] = [], page: int = None, size: int = None) -> list[dict]:
        """
            Makes a GET request to the BaseRow API to retrieve rows from a specified table.
            WARNNING: Only the fields listed in the include parameter can be used in the filters parameter.

            Args:
                table (TABLES): The table to query, specified as a TABLES enum.
                include (list[str], optional): A list of field names to include in the response. Defaults to None (all fields are used).
                filters (list[tuple[str,str]], optional): A list of tuples where each tuple contains a field name and its corresponding value for filtering. Defaults to None (no filter is applied).
                page (str, optional): The page number to retrieve. Defaults to 1.
                size (str, optional): The number of rows to retrieve per page. Defaults to 100.

            Returns:
                list[dict]: A list of dictionaries representing the rows that match the query.
        """

        url = f"https://api.baserow.io/api/database/rows/table/{table}/"

        params = {
            "user_field_names": "true"
        }

        if include:
            params["include"] = self._include_fields(include)

        if filters:
            params["filters"] = self._filter_by_fields_value(filters, orfilters)

        if page:
            params["page"] = page

        if size:
            params["size"] = size

        headers = {
            "Authorization": f"Token {self.token}"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
        except Exception as e:
            raise FileNotFoundError(f"Error accessing the database: {e}")

        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text} - {response.url}")
        
        return response.json()["results"]

    def _post(self, table: TABLES, body: dict, batchmode: bool = False) -> list[dict]:
        """
            Makes a POST request to the BaseRow API to create a new row in a specified table.
            This method is not implemented and should be overridden in subclasses.

            Args:
                table (TABLES): The table to which the new row will be added.

            Returns:
                list[dict]: A list of dictionaries representing the newly created row(s).

            Raises:
                NotImplementedError: This method is not implemented.
        """
        try:
            response = requests.post(
                f"https://api.baserow.io/api/database/rows/table/{table}/{"batch/" if batchmode else ""}?user_field_names=true",
                headers={
                    "Authorization": f"Token {self.token}",
                    "Content-Type": "application/json"
                },
                json=body
            )
        except Exception as e:
            raise WriteInDatabaseError(f"Error accessing the database: {e}")

        return response

    def _update(self, table: TABLES, row_id: int, field_name: str, content: str) -> bool:
        """
            Makes a POST request to the BaseRow API to create a new row in a specified table.
            This method is not implemented and should be overridden in subclasses.

            Args:
                table (TABLES): The table to which the new row will be added.

            Returns:
                list[dict]: A list of dictionaries representing the newly created row(s).

            Raises:
                NotImplementedError: This method is not implemented.
        """
        try:
            response = requests.patch(
                f"https://api.baserow.io/api/database/rows/table/{table}/{row_id}/?user_field_names=true",
                headers={
                    "Authorization": f"Token {self.token}"
                },
                json={
                    field_name: content
                }
            )
        except Exception as e:
            raise WriteInDatabaseError(f"Error accessing the database: {e}")
        
        return response

    # ====================================================================== CHECK METHODS

    def post_exists(self, post_title: str) -> bool:
        """
            Checks if a document exists.

            Args:
                post_title (str): Name of the document to check.

            Returns:
                bool: True if the document exists, False otherwise.
        """
        result = self._get(
            table=self.TABLES.POSTS,
            include=["title"],
            filters=[("title", post_title)]
        )
        return result != []

    def comment_exists(self, post_title: str, note_title: str) -> bool:
        """
            Checks if a note exists for a specified document by a specified note_title.

            Args:
                post_title (str): Name of the document.
                note_title (str): Name of the note_title.

            Returns:
                bool: True if the note exists, False otherwise.
        """
        result = self._get(
            table=self.TABLES.COMMENTS,
            include=["note_title", "document"],
            filters=[("document", post_title), ("note_title", note_title)]
        )
        return result != []

    def attribute_exists(self, attribute: str, value: str) -> bool:
        """ 
            Checks if a attribute exists.

            Args:
                attribute (str): Name of the attribute to check.

            Returns:
                bool: True if the attribute exists, False otherwise.

            Raises:
                FileNotFoundError: If the attributes does not exist in the database.
        """
        result = False

        attributes = self._get(
            table=self.TABLES.SUMMARIES,
            filters=[("file", attribute)]
        )
        
        if len(attributes) > 0:
            content = attributes[0]["content"]
            lines = content.splitlines()
            result = value in lines

        return result

    # ======================================================================== GET METHODS

    def get_catalog(self) -> str:
        """
            Retrieves the catalog.
            This method fetches the catalog from the database, which is stored in a JSON format.
            If the catalog does not exist, it raises a FileNotFoundError.

            Returns:
                str: The catalog as a JSON string.

            Raises:
                FileNotFoundError: If the catalog is not found in the database.
        """

        lines = self._get(
            table=self.TABLES.SUMMARIES,
            filters=[("file", "catalog")]
        )
        if len(lines) > 0:
            return lines[0]["content"]
        else:
            raise FileNotFoundError("Catalog not found in the database.")

    def get_attribute_values(self, attribute: str) -> str:
        """
            Retrieves the attributes from the database.
            If the attributes file does not exist, it raises a FileNotFoundError.

            Returns:
                str: The attributes as a string, with each value on a new line.

            Raises:
                FileNotFoundError: If the attributes file is not found in the database.
        """

        lines = self._get(
            table=self.TABLES.SUMMARIES,
            filters=[("file", attribute)]
        )
        if len(lines) > 0:
            return lines[0]["content"]
        else:
            print(f"attributes '{attribute}' not found in the database.")
            return ""

    def get_document(self, post_title: str) -> tuple[str, str]:
        """
            Retrieves the content and icon of a specified document.

            Args:
                post_title (str): Name of the document to retrieve.

            Returns:
                tuple[str,str]: A tuple containing the document content and the icon in base64 format.

            Raises:
                FileNotFoundError: If the document does not exist in the database.
        """
        post_content = ""
        icon = ""
        documents = self._get(
            table=self.TABLES.POSTS,
            filters=[("title", post_title)]
        )
        if len(documents) > 0:
            post_content = documents[0]["content"]
            icon = documents[0].get("icon", "") or ""
        else:
            raise FileNotFoundError(f"Document '{post_title}' not found in the database.")
        return (post_content, icon)

    def get_document_medias(self, post_title: str, includes: list[str] = []) -> list[str]:
        """
        Retrieves the base64-encoded images for a specified document from the POSTS_MEDIAS table.

        Args:
            post_title (str): Name of the document.
            includes (list[str]): List of image file stems to include (e.g., ["screen1", "screen2"]).

        Returns:
            list[str]: A list of base64-encoded images for the document.

        Raises:
            FileNotFoundError: If the document does not exist.
        """
        if not self.post_exists(post_title):
            raise FileNotFoundError(f"Document '{post_title}' not found in the database.")

        orfilters = [("file", file_stem) for file_stem in includes] if includes else []
        medias = self._get(
            table=self.TABLES.POSTS_MEDIAS,
            filters=[("document", post_title)],
            orfilters=orfilters
        )
        
        return [media["content"] for media in medias]

    def get_notes_for_post(self, post_title: str, perpage: int = 0, page: int = 1) -> list[tuple[str, str, str]]:
        """
            Retrieves notes for a specified document, with pagination support.
            If perpage is set to 0, all notes will be returned without pagination.
            If the pagination parameters are invalid, an empty list will be returned.

            Args:
                post_title (str): Name of the document to retrieve notes for.
                perpage (int): Number of notes to return per page (0 for no pagination).
                page (int): Page number to retrieve (0-based index).
            
            Returns:
                list[str]: A list of notes for the specified document.
            
            Raises:
                FileNotFoundError: If the document does not exist or if no notes are found.
        """
        
        notes = self._get(
            table=self.TABLES.COMMENTS,
            filters=[("document", post_title)],
            size=perpage if perpage > 0 else None,
            page=page,
        )

        if len(notes) > 0:
            return [(note["content"], note["note_title"], note["document"]) for note in notes]
        else:
            raise FileNotFoundError(f"Document '{post_title}' not found in the database.")

    
    def get_note_medias(self, post_title: str, note_title: str, includes: list[str] = []) -> list[str]:
        """
        Retrieves the base64-encoded images for a specified note of a document from the COMMENTS_MEDIAS table.

        Args:
            post_title (str): Name of the document.
            note_title (str): Name of the note_title.
            includes (list[str]): List of image file stems to include.

        Returns:
            list[str]: A list of base64-encoded images for the note.

        Raises:
            FileNotFoundError: If the note does not exist.
        """
        if not self.comment_exists(post_title, note_title):
            raise FileNotFoundError(f"Note by '{note_title}' on document '{post_title}' not found in the database.")

        orfilters = [("file", file_stem) for file_stem in includes] if includes else []
        medias = self._get(
            table=self.TABLES.COMMENTS_MEDIAS,
            filters=[("document", post_title), ("note_title", note_title)],
            orfilters=orfilters
        )

        return [media["content"] for media in medias]

    # ====================================================================== WRITE METHODS

    def write_catalog(self, json: str):
        """
            Writes the catalog to the database.
            If the catalog already exists, it updates the content.
            If the catalog does not exist, it creates a new file with the specified JSON content.

            Args:
                json (str): The JSON content to write to the catalog.

            Returns:
                bool: True if the write operation was successful.

            Raises:
                WriteInDatabaseError: If there is an error writing to the catalog file.  
        """
        response = self._update(
            table=self.TABLES.SUMMARIES,
            row_id=1,
            field_name="content",
            content= json
        )

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing catalog: {response.status_code} - {response.text} - {response.url}")
    
        return True
        
    
    def write_post(self, post_title: str, content: str, icon: str = "", medias: list[tuple[str,str]] = []) -> bool:
        """
            Writes a document to the database.
            If the document already exists, it raises a FileAlreadyExistsError.

            Args:
                post_title (str): Name of the document to write.
                icon (str): Base64 encoded icon for the document.
                media (list[str]): List of base64 encoded media for the document.

                content (str): Content of the document.
            Returns:
                bool: True if the write operation was successful.

            Raises:
                FileAlreadyExistsError: If the document already exists.
                WriteInDatabaseError: If there is an error writing to the database.
        """
        if self.post_exists(post_title):
            raise FileAlreadyExistsError()
        
        response = self._post(
            table=self.TABLES.POSTS,
            body={
                "title": post_title,
                "content": content,
                "icon": icon
            }
        )

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing document: {response.status_code} - {response.text} - {response.url}")
        
        medias_response = self._post(
            table=self.TABLES.POSTS_MEDIAS,
            body={
                "items":[
                    {
                        "id": i,
                        "document": post_title,
                        "file": media[0],
                        "content": media[1]
                    } for i, media in enumerate(medias)
                ]
            },
            batchmode=True
        )

        print(medias_response)

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing document medias: {medias_response.status_code} - {medias_response.text} - {medias_response.url}")
        
        return True

    
    def write_comment(self, post_title: str, note_title: str, content: str, medias: list[tuple[str,str]] = []) -> bool:
        """
            Writes a note to a specified document.
            If the document does not exist, it raises a FileNotFoundError.
            If the note already exists, it raises a FileAlreadyExistsError.

            Args:
                post_title (str): Name of the document to note on.
                note_title (str): Name of the note_title.
                content (str): Content of the note.
                medias (list[str]): List of base64 encoded screenshots for the note.

            Returns:
                bool: True if the write operation was successful.

            Raises:
                FileNotFoundError: If the document does not exist.
                FileAlreadyExistsError: If the note already exists.
                WriteInDatabaseError: If there is an error writing to the database.
        """
        if not self.post_exists(post_title):
            raise FileNotFoundError(f"The document {post_title} you are trying to note on does not exist.")

        if self.comment_exists(post_title, note_title):
            raise FileAlreadyExistsError(f"The note by {note_title} on the document {post_title} already exists.")

        response = self._post(
            table=self.TABLES.COMMENTS,
            body={
                "document": post_title,
                "note_title": note_title,
                "content": content
            }
        )

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing note: {response.status_code} - {response.text} - {response.url}")

        medias_response = self._post(
            table=self.TABLES.COMMENTS_MEDIAS,
            body={
                "items": [
                    {
                        "id": i,
                        "document": post_title,
                        "note_title": note_title,
                        "file": media[0],
                        "content": media[1]
                    } for i, media in enumerate(medias)
                ]
            },
            batchmode=True
        )

        if medias_response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing note medias: {medias_response.status_code} - {medias_response.text} - {medias_response.url}")

        return True
    
    def write_attribute(self, attribute: str, data: str) -> bool:
        """
            Writes attributes to the database.
            If the attributes file already exists, it updates the content.
            If the attributes file does not exist, it creates a new file with the specified attributes.

            Args:
                attributes (str): The attributes to write, separated by new lines.

            Returns:
                bool: True if the write operation was successful.

            Raises:
                WriteInDatabaseError: If there is an error writing to the attributes file.  
        """

        rows = self._get(
            table=self.TABLES.SUMMARIES,
            include=["file"],
            filters=[("file",attribute)]
        )

        if len(rows) > 0:
            row_id = rows[0]["id"]
            response = self._update(
                table=self.TABLES.SUMMARIES,
                row_id=row_id,
                field_name="content",
                content= data
            )
        else:
            response = self._post(
                table=self.TABLES.SUMMARIES,
                body={
                    "file":attribute,
                    "content":data
                }
            )

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing attributes: {response.status_code} - {response.text} - {response.url}")
    
        return True
        
    def add_attribute_values(self, attribute: str, data: str) -> bool:
        """
            Adds a attribute to the database.
            If the attribute already exists, it returns True without adding it again.
            If the attribute does not exist, it appends the attribute to the attributes file and returns True.

            Args:
                attribute (str): The attribute to add.

            Returns:
                bool: True if the attribute was added successfully, False if it already exists.

            Raises:
                WriteInDatabaseError: If there is an error writing to the attributes file.  
        """
        if self.attribute_exists(attribute,data):
            return True
        
        newdata = self.get_attribute_values(attribute)
        newdata += f"\n{data}"
        newdata = newdata.strip()
        return self.write_attribute(attribute, newdata)

    # ======================================================================== RAG METHODS

    def get_all_documents_data(self) -> list[dict[str,str]]:
        """
            Retrieves all documents data from the database.
            Each document is represented as a dictionary with "content" and "title" keys.

            Returns:
                list[dict[str,str]]: A list of dictionaries containing the content and title of each document.

            Raises:
                FileNotFoundError: If no documents are found in the database.
        """
        
        docs = []

        documents = self._get(
            table=self.TABLES.POSTS
        )
        if len(documents) > 0:
            for document in documents:
                title = document["title"]
                content = document["content"]
                post_object: Document = Document.from_text(title,content)
                docs.append(
                    {
                        "content":content,
                        "title": title,
                        "metadata": post_object.metadatas
                    }
                )
        else:
            raise FileNotFoundError(f"No documents found in the database.")
        
        return docs

    def get_vector_store(self) -> bytes:
        """
            Retrieves the vector store from the database.

            Returns:
                bytes: The vector store data in bytes format.

            Raises:
                FileNotFoundError: If the vector store is not found in the database.
        """
        lines = self._get(
            table=self.TABLES.RAG,
            filters=[("file", "store")]
        )
        if len(lines) > 0:
            content = lines[0]["content"]
            if content != "":
                return bytes.fromhex(content)
        else:
            raise FileNotFoundError("Vector store not found in the database.")

    def write_vector_store(self,bytes_data: bytes) -> bool:
        """
            Writes the vector store to the database.

            Args:
                bytes_data (bytes): The vector store data in bytes format.

            Returns:
                bool: True if the write operation was successful.

            Raises:
                WriteInDatabaseError: If there is an error writing to the vector store.
        """
        
        response = self._update(
            table=self.TABLES.RAG,
            row_id=1,
            field_name="content",
            content= bytes_data.hex()
        )

        if response.status_code != 200:
            raise WriteInDatabaseError(f"Error writing vector store: {response.status_code} - {response.text} - {response.url}")
    
        return True