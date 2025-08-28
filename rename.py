import os

# Define the root directory
root_dir = 'data/tools_db'

# Define the file mappings
file_mappings = {
    'post.txt': 'document.txt',
    'comment.txt': 'note.txt'
}

# Walk through the directory tree
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename in file_mappings:
            old_path = os.path.join(dirpath, filename)
            new_path = os.path.join(dirpath, file_mappings[filename])
            os.rename(old_path, new_path)
            print(f'Renamed: {old_path} -> {new_path}')
