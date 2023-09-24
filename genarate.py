import json
import random
import string

# Generate a random valid name
def generate_valid_name():
    name_length = random.randint(5, 10)
    return ''.join(random.choice(string.ascii_letters) for _ in range(name_length))

# Generate a random valid project name
def generate_valid_project_name():
    project_names = ["E-commerce Website", "Social Media App", "Inventory Management System", "Online Booking Platform", "Data Analytics Dashboard"]
    return random.choice(project_names)

# Generate a random valid description
def generate_valid_description():
    descriptions = ["A web application for managing your tasks.", "An e-commerce platform for selling fashion items.", "A social media app to connect with friends.", "An inventory management system for small businesses.", "A data analytics dashboard for visualizing your data."]
    return random.choice(descriptions)

# Generate a random valid institution name
def generate_valid_institution_name():
    institution_names = ["University of XYZ", "Tech Institute", "Business School", "Online Courses", "College of Engineering"]
    return random.choice(institution_names)

# Create a dictionary with random but valid data
data = {
    "name": generate_valid_name(),
    "jobrole": generate_valid_name(),
    "description": generate_valid_description(),
    "skills": [generate_valid_name() for _ in range(3)],  # Generate 3 random skills
    "socialmedia": [f"{generate_valid_name()}.com/{generate_valid_name()}" for _ in range(2)],  # Generate 2 random social media links
    "educations": [{
        "institution": generate_valid_institution_name(),
        "startyear": random.randint(2000, 2020),
        "endyear": random.randint(2000, 2021)
    }],
    "projects": [{
        "projectname": generate_valid_project_name(),
        "projectimages": [],
        "projectdesc": generate_valid_description(),
        "projectlinks": [f"{generate_valid_name()}.com" for _ in range(2)]  # Generate 2 random project links
    }],
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data, indent=4)

# Print the JSON string
print(json_data)
