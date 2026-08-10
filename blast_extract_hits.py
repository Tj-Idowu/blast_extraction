import os
import re
import pandas as pd

folder_path = "path/to/BLAST_files"

file_data = []

file_list = [file for file in os.listdir(folder_path) if file.endswith(".tab")]

for filename in file_list:
    file_path = os.path.join(folder_path, filename)
    
    hits_found_count = 0
    zero_hits_found_count = 0
    non_zero_hits_found_count = 0
    other_values_count = {}

    with open(file_path, 'r') as file:
        for line in file:
            if "hits found" in line:
                hits_found_count += 1
            if "# 0 hits found" in line:
                zero_hits_found_count += 1
            match = re.search(r'# (\d+) hits found', line)
            if match:
                value = int(match.group(1))
                if value != 0:
                    non_zero_hits_found_count += 1
                    if value not in other_values_count:
                        other_values_count[value] = 1
                    else:
                        other_values_count[value] += 1
    
    file_info = {
        "Filename": filename,
        "Hits Found Count": hits_found_count,
        "Zero Hits Found Count": zero_hits_found_count,
        "Non-Zero Hits Found Count": non_zero_hits_found_count,
    }
    file_info.update(other_values_count)
    file_data.append(file_info)

df = pd.DataFrame(file_data)

output_file = os.path.join(folder_path, "reads_extracted_hits_table.tab")
df.to_csv(output_file, sep="\t", index=False)

print("Table saved as extracted_hits_table.tab")
