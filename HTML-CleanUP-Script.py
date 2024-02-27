import os
import zipfile
import yaml
import re
import urllib.parse
from urllib.parse import unquote
from bs4 import BeautifulSoup

# Specify the YAML file path directly
yaml_file_path = "config.yml"


# Load YAML configuration
with open(yaml_file_path, 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)

# Get the path where to extract the contents
extract_to = config.get('extract_to')
if not extract_to:
    print("Error: 'extract_to' path not found in the YAML file.")
    exit(1)

video_snippet = config.get('Video_html_Code_Snippet')
if not video_snippet:
    print("Error: 'extract_to' path not found in the YAML file.")
    exit(1)

Head_snippet = config.get('html_Head_Code_Snippet')
if not Head_snippet:
    print("Error: 'extract_to' path not found in the YAML file.")
    exit(1)

def get_active_zip_file(folder_path):
    zip_files = [file for file in os.listdir(folder_path) if file.endswith('.zip')]
    if not zip_files:
        print("No zip files found in the folder.")
        return None
    return zip_files[0]  # Return the first zip file found

def unzip_folder(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Folder '{zip_file}' successfully extracted to '{extract_to}'")

def rename_folder_and_html(folder_path, old_folder_name):
    old_folder_path = os.path.join(folder_path, old_folder_name)
    new_folder_name = re.sub(r' [a-f0-9]+$', '', old_folder_name)
    new_folder_path = os.path.join(folder_path, new_folder_name)
    os.rename(old_folder_path, new_folder_path)
    print(f"Folder '{old_folder_name}' renamed to '{new_folder_name}'")

    old_html_file_path = os.path.join(folder_path, old_folder_name + ".html")
    new_html_file_path = os.path.join(folder_path, new_folder_name + ".html")
    os.rename(old_html_file_path, new_html_file_path)
    print(f"File '{old_folder_name}.html' renamed to '{new_folder_name}.html'")
    return new_html_file_path

def find_replace_html_file(html_file, old_path, new_path):
    try:
        # Open the HTML file for reading
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Perform the find and replace operation
        updated_content = html_content.replace(old_path, new_path)

        # Write the updated content back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"File location '{old_path}' replaced with '{new_path}' in '{html_file}' successfully.")

    except FileNotFoundError:
        print("Error: HTML file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


#video html tag replacement
def replace_video_html_in_file(html_file):
    try:
        # Read the HTML content from the file
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the pattern to match the existing video link
        pattern = r'<div class="source"><a href="([^"]+)">([^<]+)</a></div>'

        # Perform the replacement
        updated_content = re.sub(pattern, replacement_callback, html_content)

        # Write the updated content back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"HTML content in '{html_file}' replaced successfully.")

    except FileNotFoundError:
        print("Error: HTML file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def replacement_callback(match):
    old_link = match.group(1)
    video_file = unquote(old_link)
    new_link = f'./{video_file}'
    # replacement = f'<br><div style="position: rselative; display: flex; justify-content: center; align-items: center;"><video playsinline="" controls="" preload="metadata" src="{new_link}" style="display: block; width: 80%; background-color: rgba(255, 255, 255, 0.03);"></video></div><br>'
    replacement = video_snippet.format(new_link=new_link)
    return replacement

def replace_html_content(html_file, old_content, new_content):
    # Read the HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace the old content with the new content
    updated_html = html_content.replace(old_content, new_content)

    # Write the updated HTML content back to the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("HTML content replaced successfully.")

#video html tag replacement
def replace_video_html_in_file(html_file):
    try:
        # Read the HTML content from the file
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the pattern to match the existing video link
        pattern = r'<div class="source"><a href="([^"]+)">([^<]+)</a></div>'

        # Perform the replacement
        updated_content = re.sub(pattern, replacement_callback, html_content)

        # Write the updated content back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"HTML content in '{html_file}' replaced successfully.")

    except FileNotFoundError:
        print("Error: HTML file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#replacing the spaces 
def replace_html_in_file(html_file):
    try:
        # Read the HTML content from the file
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Define the pattern to match the existing content
        pattern = r'<p\s+id="([^"]+)"\s*class="">\s*</p>'

        # Perform the replacement
        updated_content = re.sub(pattern, '<br>', html_content)

        # Write the updated content back to the file
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(updated_content)

        print(f"HTML content in '{html_file}' replaced successfully.")

    except FileNotFoundError:
        print("Error: HTML file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def format_html_file(input_file):
    # Read the HTML content from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Prettify the parsed HTML content
    formatted_html = soup.prettify()

    # Overwrite the input file with the formatted HTML content
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(formatted_html)

    print("HTML document formatted and saved successfully.")


if __name__ == "__main__":


    # Get the folder path
    folder_path = os.path.dirname(os.path.abspath(yaml_file_path))

    # Ensure that the destination folder exists, create it if not
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Get the active zip file in the folder
    zip_file = get_active_zip_file(folder_path)
    if not zip_file:
        exit(1)

    # Extract the contents to a temporary location
    temp_extract_to = os.path.join(folder_path, 'temp_extract')
    unzip_folder(os.path.join(folder_path, zip_file), temp_extract_to)

    # Find the folder and file with unique IDs
    unique_id_folder_name = os.listdir(temp_extract_to)[0]
    # unique_id_html_file_name = os.listdir(os.path.join(temp_extract_to, unique_id_folder_name))[0]
    unique_id_html_file_name = unique_id_folder_name + ".html"

    # print(unique_id_html_file_name)
    # Remove the unique IDs from folder and file names
    rename_folder_and_html(temp_extract_to, unique_id_folder_name)


    


    # Update paths in the HTML file
    # print(unique_id_html_file_name)
    new_folder_name = re.sub(r' [a-f0-9]+$', '', unique_id_folder_name)
    unique_id_html_file_name = new_folder_name + ".html"
    html_file_path = os.path.join(temp_extract_to, unique_id_html_file_name)
    
    print(html_file_path)
    print(new_folder_name)
    html_file = html_file_path
    old_path = urllib.parse.quote(unique_id_folder_name) +'/'
    print(old_path)
    new_path = new_folder_name+'/'
    find_replace_html_file(html_file, old_path, new_path)

     # Get the path where to extract the contents
    replace_video_html_in_file(html_file)

    #replacing the head html tags with proper tags 
    old_content = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>'
    replace_html_content(html_file, old_content, Head_snippet)

    #replacing the intent spaces in htm file
    replace_html_in_file(html_file)

    #replacing the head html tags with proper tags 
    old_content = 'white-space: pre-wrap;'
    new_content = '/*white-space: pre-wrap;*/'
    replace_html_content(html_file, old_content,new_content )

    format_html_file(html_file)

    # # Move the folder to the final destination
    final_extract_to = os.path.join(folder_path, config['extract_to'])

    # Move the folder and HTML file to the final destination
    final_folder_path = os.path.join(final_extract_to, new_folder_name)
    # os.makedirs(final_folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    # os.rename(os.path.join(temp_extract_to, new_folder_name), final_folder_path)
    os.rename(os.path.join(temp_extract_to, new_folder_name), os.path.join(final_extract_to, new_folder_name))
    os.rename(os.path.join(temp_extract_to, new_folder_name + ".html"), os.path.join(final_extract_to, new_folder_name + ".html"))
    print("Folder and HTML file moved to the final destination")
    

    # Delete the temporary extraction directory
    os.rmdir(temp_extract_to)
    print("Temporary extraction directory deleted")

    # Delete the zip file after extraction
    os.remove(os.path.join(folder_path, zip_file))
    print(f"Zip file '{zip_file}' deleted.")
