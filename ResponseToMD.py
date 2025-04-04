import json
from markdownify import markdownify as md

# Sample function to load JSON data from a file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to extract questions and convert HTML to Markdown, then save to a Markdown file
def extract_questions_answers(data):
    with open('output.md', 'w') as md_file:
        items = data['data']['items']  # Navigate to the 'items' list in the data
        for item in items:
            for question in item['questions']:
                question_text = md(question['stimulus'])
                correct_value = question['validation']['valid_response']['value'][0]  # Assumes single correct answer
                correct_answer = None
                
                # Find the correct answer label
                for option in question['options']:
                    if option['value'] == correct_value:
                        correct_answer = md(option['label'])
                        break
                
                # Write the question and correct answer to Markdown file
                md_file.write(f"### Question:\n{question_text}\n")
                md_file.write(f"**Correct Answer:** {correct_answer}\n\n")

# Example usage
data = load_json('response.json')  # Load your JSON file here
extract_questions_answers(data)
