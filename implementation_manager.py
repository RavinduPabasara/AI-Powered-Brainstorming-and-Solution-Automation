#implementation_manager.py
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from file_system_handler import FileSystemHandler
from ai_assistant_factory import AIAssistantFactory


class ImplementationManager:
    def extract_tech_stack(implementation_design):
        try:
            sentences = sent_tokenize(implementation_design)
            tech_stack_sentence = next((s for s in sentences if "tech stack" in s.lower()), "")

            if tech_stack_sentence:
                stop_words = set(stopwords.words('english'))
                lemmatizer = WordNetLemmatizer()
                words = word_tokenize(tech_stack_sentence)
                tech_words = [lemmatizer.lemmatize(word) for word in words if
                              word.lower() not in stop_words and word.isalnum()]
                return ", ".join(tech_words)
            else:
                return "Not specified"
        except Exception as e:
            print(f"Error in extract_tech_stack: {e}")
            return "Error extracting tech stack"

    def extract_implementation_parts(implementation_design):
        try:
            # Use regex to find numbered or bulleted lists in the implementation design
            pattern = r"(?:(?:\d+\.\s)|(?:-\s))(.*?)(?:\n|$)"
            matches = re.findall(pattern, implementation_design)
            implementation_parts = [match.strip() for match in matches if match.strip()]
            return implementation_parts if implementation_parts else ["Not specified"]
        except Exception as e:
            print(f"Error in extract_implementation_parts: {e}")
            return ["Error extracting implementation parts"]

    def implement_solution_part(client, implementation_design, part, tech_stack):
        try:
            prompt = (f"As a software developer, implement the following part of the solution: '{part}'. "
                      f"Base your implementation on the overall design: '{implementation_design}' and utilize "
                      f"the tech stack: '{tech_stack}'. Generate the code or configuration files as required.")
            response = AIAssistantFactory.api_call_with_delay(client, prompt)

            # Parse the response to extract file names and content
            # Assuming the response contains blocks like `filename.extension` followed by code
            files = []
            file_pattern = r"(?<=```)([\s\S]*?)(?=```)"
            code_blocks = re.findall(file_pattern, response)

            for block in code_blocks:
                lines = block.splitlines()
                filename = lines[0].strip()
                content = "\n".join(lines[1:])
                files.append((filename, content))

            return files
        except Exception as e:
            print(f"Error implementing solution part '{part}': {e}")
            return None

    def generate_readme(client, topic, goal, synthesized_solution, implementation_design, tech_stack, files):
        try:
            prompt = (f"Generate a README.md file for a project with the following details:\n\n"
                      f"Topic: {topic}\n"
                      f"Goal: {goal}\n"
                      f"Synthesized Solution: {synthesized_solution}\n"
                      f"Implementation Design: {implementation_design}\n"
                      f"Tech Stack: {tech_stack}\n"
                      f"Generated Files: {', '.join(files)}\n\n"
                      f"Structure the README with sections for Introduction, Features, Setup, Usage, and Contributors.")
            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response.strip()
        except Exception as e:
            print(f"Error generating README.md: {e}")
            return "# README\n\nError generating README content."
