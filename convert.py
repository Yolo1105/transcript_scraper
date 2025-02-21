def combine_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Combine all sentences into a single document
    combined_document = ""
    for line in lines:
        # Remove the timestamps and extra spaces
        if '->' in line:
            sentence = line.split('] ')[1].strip()
            combined_document += sentence + " "

    return combined_document.strip()

# Path to the output.txt file
file_path = 'transcription_result9.txt'

# Combine sentences and print the result
document = combine_sentences(file_path)

# Optionally, write the combined document to a new file
with open('combined_document9.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(document)
