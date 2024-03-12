import os

root_dir = "E:\\WordPress\\wp-typescript-starter\\wp-typescript-starter"
temp_dir = "E:\\temporary"

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        print(os.path.join(subdir, file))
        relative_path = os.path.relpath(os.path.join(subdir, file), root_dir)
        print(os.path.join(temp_dir, relative_path))


# import re

# def are_characters_unique(s):
#     sorted_string = ''.join(sorted(s))
#     return not re.search(r'(.)\1', sorted_string)

# # Test the function
# string = "abcdefg"
# print(are_characters_unique(string))  # True

# string = "abcdeff"
# print(are_characters_unique(string))  # False
