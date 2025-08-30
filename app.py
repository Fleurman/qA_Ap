# import qA_Ap
# from qA_Ap.db.flatfiledb import FlatFileDB
# from qA_Ap.db.baserowfreeapidb import BaseRowFreeApiDB
# from qA_Ap.app import compile_catalog, compile_tags_from_catalog
# from qA_Ap.api.server import server
# from qA_Ap.app.ai import vectorize_posts, query, init
# from qA_Ap.app.ai.ollama import OllamaAIInterface
# from qA_Ap.app.ai.cerebras import CerebrasAIInterface

# qA_Ap.state.State.Database = BaseRowFreeApiDB("tyesLJsYXhYHyR2LBI2jZcUG711W1iUu")
# # qA_Ap.state.State.Database = FlatFileDB("db")
# qA_Ap.state.State.AIInterface = CerebrasAIInterface(
#     key="csk-pt2x2jd9yrvddfr92rp4wx4fvd2wkfv8mjewvp3t59f4vyvk", 
#     model_name="llama3.1-8b"
# )
# # qA_Ap.state.State.AIInterface = OllamaAIInterface("qwen3:0.6B")


# compile_catalog()
# compile_tags_from_catalog()
# init()


# print("=====================")
# response = query("Quels outils utiliser pour faire un petit jeu avec des modèles 3d custom ?")
# for chunk in response:
#     print(chunk,end="",flush=True)
# print("\n=====================")

# server.run(host='0.0.0.0', port=80, debug=True)

# db = BaseRowFreeApiDB("tyesLJsYXhYHyR2LBI2jZcUG711W1iUu")

# post, icon = db.get_post("test")

# # print(post, icon)

# data = {}

# import base64

# with open("dummy.png", "rb") as f:
#     icon = f.read()
#     b64 = str(base64.b64encode(icon))

#     print(db.write_comment(
#         post_name="test",
#         commenter="fleurman",
#         content="Ceci est un test de commentaire",
#         screenshots=[b64]))