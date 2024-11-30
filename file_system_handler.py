# file_system_handler/py
import os
from ai_assistant_factory import AIAssistantFactory


class FileSystemHandler:
    def save_implementation(files, solution_name):
        print("saving!")
        folder_name = solution_name.replace(" ", "_").lower()
        os.makedirs(folder_name, exist_ok=True)

        # Keep track of unique files to avoid duplicates
        saved_files = set()

        for file_name, content in files:
            # Normalize the file name to avoid case sensitivity issues
            normalized_file_name = file_name.strip('`').lower()

            if normalized_file_name in saved_files:
                print(f"Skipping duplicate file: {file_name}")
                continue

            try:
                # Create subdirectories if needed
                file_path = os.path.join(folder_name, file_name.strip('`'))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                saved_files.add(normalized_file_name)
                print(f"Successfully saved: {file_name}")

            except IOError as e:
                print(f"Error saving file {file_name}: {str(e)}")
            except Exception as e:
                print(f"Unexpected error while saving {file_name}: {str(e)}")

        print(f"\nImplementation saved in folder: {folder_name}")
        print(f"Total unique files saved: {len(saved_files)}")

    def parse_implementation(implementation):
        files = []
        current_file = None
        current_content = []
        seen_files = set()

        for line in implementation.split('\n'):
            if line.startswith('### Filename:'):
                if current_file and current_file.strip('`').lower() not in seen_files:
                    files.append((current_file, '\n'.join(current_content)))
                    seen_files.add(current_file.strip('`').lower())
                current_file = line.split(':')[1].strip()
                current_content = []
            elif line.startswith(f'### End of {current_file}'):
                if current_file and current_file.strip('`').lower() not in seen_files:
                    files.append((current_file, '\n'.join(current_content)))
                    seen_files.add(current_file.strip('`').lower())
                current_file = None
                current_content = []
            elif current_file:
                current_content.append(line)

        if current_file and current_file.strip('`').lower() not in seen_files:
            files.append((current_file, '\n'.join(current_content)))

        return files

    def generate_readme(client, topic, goal, synthesized_solution, implementation_design, tech_stack,
                        implemented_files):
        try:
            files_list = "\n".join([f"- {file}" for file in implemented_files])
            prompt = f"""
            Create a comprehensive README.md file for the following implemented solution:
    
            Topic: {topic}
            Goal: {goal}
            Synthesized Solution: {synthesized_solution}
            Implementation Design: {implementation_design}
            Tech Stack: {tech_stack}
            Implemented Files:
            {files_list}
    
            The README should include:
            1. Project Title and Description
            2. Installation Instructions
            3. Usage Guide
            4. File Structure
            5. Dependencies
            6. Configuration (if any)
            7. Troubleshooting
            8. Contributors
            9. License
    
            Format the README in Markdown syntax.
            """

            response = AIAssistantFactory.api_call_with_delay(client, prompt)
            return response
        except Exception as e:
            print(f"Error generating README: {e}")
            return "Unable to generate README due to an error."
