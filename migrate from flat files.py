


"""
    given this folder hierarchy:

    db/
        posts/
            <post_name>/
                post.txt
                icon.png
                screen1.png
                <commenter>/
                    comment.txt
                    screen1.png
        ...

    retrieve all posts with their name, file content and images and upload them into the qA_Ap.state.State.DATABASE
    do the same for all comments

"""
# import os
# import base64
# from pathlib import Path

# def upload_posts_and_comments_from_flatfiles(root_folder: str = "db"):
#     posts_dir = Path(root_folder) / "posts"
#     if not posts_dir.exists():
#         print(f"Posts directory {posts_dir} does not exist.")
#         return

#     for post_folder in posts_dir.iterdir():
#         if not post_folder.is_dir():
#             continue

#         post_name = post_folder.name

#         # Read post content
#         post_txt_path = post_folder / "post.txt"
#         if not post_txt_path.exists():
#             print(f"Missing post.txt for {post_name}, skipping.")
#             continue
#         with open(post_txt_path, encoding="utf-8") as f:
#             post_content = f.read()

#         # Read icon
#         icon_path = post_folder / "icon.png"
#         if icon_path.exists():
#             with open(icon_path, "rb") as f:
#                 icon_b64 = base64.b64encode(f.read()).decode("utf-8")
#         else:
#             icon_b64 = ""

#         # Read screenshots
#         screenshots = []
#         for img_file in sorted(post_folder.glob("screen*.png")):
#             with open(img_file, "rb") as f:
#                 screenshots.append(base64.b64encode(f.read()).decode("utf-8"))

#         # Upload post
#         try:
#             qA_Ap.state.State.DATABASE.write_post(
#                 post_name=post_name,
#                 icon=icon_b64,
#                 screenshots=screenshots,
#                 content=post_content
#             )
#             print(f"Uploaded post: {post_name}")
#         except Exception as e:
#             print(f"Failed to upload post {post_name}: {e}")

#         # Upload comments
#         for commenter_folder in post_folder.iterdir():
#             if not commenter_folder.is_dir():
#                 continue
#             commenter = commenter_folder.name
#             comment_txt_path = commenter_folder / "comment.txt"
#             if not comment_txt_path.exists():
#                 continue
#             with open(comment_txt_path, encoding="utf-8") as f:
#                 comment_content = f.read()
#             comment_screenshots = []
#             for img_file in sorted(commenter_folder.glob("screen*.png")):
#                 with open(img_file, "rb") as f:
#                     comment_screenshots.append(base64.b64encode(f.read()).decode("utf-8"))
#             try:
#                 qA_Ap.state.State.DATABASE.write_comment(
#                     post_name=post_name,
#                     commenter=commenter,
#                     screenshots=comment_screenshots,
#                     content=comment_content
#                 )
#                 print(f"Uploaded comment by {commenter} on post {post_name}")
#             except Exception as e:
#                 print(f"Failed to upload comment by {commenter} on post {post_name}: {e}")

# # Call the function at the appropriate place in your app
# upload_posts_and_comments_from_flatfiles("db")

