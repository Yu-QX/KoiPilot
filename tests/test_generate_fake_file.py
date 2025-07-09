import os
import random
import datetime

destination_dir = os.path.join(os.environ["USERPROFILE"], "Desktop", "test_structure")

# Remove the directory and all its contents if it exists
if os.path.exists(destination_dir):
    for root, dirs, files in os.walk(destination_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
else:
    os.makedirs(destination_dir)

# create fake files
date_format_list = ["%Y-%m-%d", "%Y %m %d", "%Y.%m.%d", "%Y%m%d"]
date_range_list = [
    datetime.datetime(2023, 1, 1),  datetime.datetime(2023, 1, 31),
    datetime.datetime(2023, 2, 1),  datetime.datetime(2023, 2, 28),
    datetime.datetime(2023, 3, 1),  datetime.datetime(2023, 3, 31),
    datetime.datetime(2023,4, 1),   datetime.datetime(2023, 5, 1),
    datetime.datetime(2023, 6, 1),  datetime.datetime(2023, 7, 1),
    datetime.datetime(2023, 8, 1),  datetime.datetime(2023, 9, 1),
    datetime.datetime(2023, 10, 1), datetime.datetime(2023, 11, 1),
    datetime.datetime(2023, 12, 1), datetime.datetime(2023, 12, 31),
    datetime.datetime(2024, 1, 1),  datetime.datetime(2024, 1, 31),
    datetime.datetime(2024, 2, 1),  datetime.datetime(2024, 2, 28),
    datetime.datetime(2024, 3, 1),  datetime.datetime(2024, 3, 31),
    datetime.datetime(2024,4, 1),   datetime.datetime(2024, 5, 1),

]

# Filter out non-datetime objects and generate a full list of date formats
date_list = [datetime.datetime.strftime(date, date_format) 
             for date_format in date_format_list 
             for date in date_range_list 
             if isinstance(date, datetime.datetime)]

# File types list
file_types_list = [
    "jpg", "jpeg", "png", "gif", 
    "pdf", "doc", "docx", 
    "xls", "xlsx", 
    "ppt", "pptx", 
    "txt", 
    "zip", "rar", "7z", 
    "exe", 
    "mp3", "mp4", "avi", "wav", "mov", "mkv", 
    "csv", "html", "css", "js", "php", "py", "java", "c", "cpp", "sql", "json", "xml",
]

# File main names list
name_list = [
    # Man of science
    "Newton", "Einstein", "Bohr", "Feynman", "Curie", "Faraday", "Hawking", "Newton", "Einstein", "Bohr", "Feynman", "Curie", "Faraday", "Hawking", "Newton", "Einstein", "Bohr", "Feynman", "Curie", "Faraday", "Hawking", "Newton", "Einstein", "Bohr", "Feynman", "Curie", "Faraday", "Hawking",
    # Man of art
    "Picasso", "Vincent", "Monet", "Dali", "Gauguin", "Kandinsky", "Munch", "Botticelli", "Picasso", "Vincent", "Monet", "Dali", "Gauguin", "Kandinsky", "Munch", "Botticelli", "Picasso", "Vincent", "Monet", "Dali", "Gauguin", "Kandinsky", "Munch", "Botticelli",
    # Man of music
    "Mozart", "Beethoven", "Chopin", "Bach", "Rachmaninoff", "Mendelssohn", "Schubert", "Debussy", "Mozart", "Beethoven", "Chopin", "Bach", "Rachmaninoff", "Mendelssohn", "Schubert", "Debussy",
    # Man of technology
    "Bill Gates", "Steve Jobs", "Larry Page", "Sergey Brin", "Mark Zuckerberg",
    # Technology
    "Computer", "Internet", "Television", "Internet Explorer", "Google", "Facebook", "Twitter", "Instagram", "YouTube", "Netflix", "Amazon", "Microsoft", "Apple", "Samsung",
    # Tourist attractions
    "Eiffel Tower", "Statue of Liberty", "Colosseum", "Taj Mahal", "Great Wall of China", "Machu Picchu", "Chichen Itza", "Petra", "Angkor Wat", "Kyoto", "Mount Everest", "Mount Fuji", "Niagara Falls", "Victoria Falls", "Angel Falls", "Kilimanjaro", "Mount Kilimanjaro", "Mount Everest", "Mount Fuji", "Niagara Falls",
    # Food
    "Pizza", "Burger", "Sushi", "Pasta", "Ramen", "Dim Sum", "Tacos", "Burritos", "Fajitas", "Enchiladas", "Quesadillas", "Pupusas", "Tostadas", "Pierogis", "Pierogi", "Pierogis", "Pierogi", "Pierogis", "Pierogi", "Pierogis", "Pierogi", "Pierogis", "Pierogi",
    # Sports
    "Soccer", "Basketball", "Baseball", "Volleyball", "Tennis", "Golf", "Swimming", "Cycling", "Hockey", "Rugby", "Boxing", "Wrestling", "Fencing", "Archery", "Table Tennis", "Badminton", "Squash", "Cricket", "Football", "Rugby", "Boxing", "Wrestling", "Fencing","Archery", "Table Tennis", "Badminton",
]

# File name format name
name_format_list = [
    "{name}_{date}.{extension}",
    "{date}_{name}.{extension}",
    "{date}{name}.{extension}",
    "{date} {name}.{extension}",
]

def generate_file_name(date_list: list, name_list: list, file_types_list: list) -> str:
    # randomly choose date, name, extension, and name format
    date = random.choice(date_list)
    name = random.choice(name_list)
    extension = random.choice(file_types_list)
    name_format = random.choice(name_format_list)

    # form into a file name
    file_name = name_format.format(date=date, name=name, extension=extension)
    return file_name

file_list = [generate_file_name(date_list, name_list, file_types_list) for _ in range(20)]

# create fake files in destination_dir
for file_name in file_list:
    file_path = os.path.join(destination_dir, file_name)
    with open(file_path, 'w') as f:
        f.write('This is a fake file.')

# create fake folders
for folder_name in ["science", "art", "tech", "tourist_attractions", "food", "sports"]:
    os.makedirs(os.path.join(destination_dir, folder_name))