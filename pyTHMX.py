import os
import xml.etree.ElementTree as ET
import pandas as pd

def process_file(file_path):
    # Parse XML directly from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []

    # Iterate over all 'Case' elements
    for case in root.findall('Case'):
        case_name = case.find('Name').text
        # Iterate over all 'U-factors' elements
        for ufactors in case.findall('U-factors'):
            tag = ufactors.find('Tag').text
            if tag in ['Frame', 'Edge']:
                delta_t = ufactors.find('DeltaT').attrib['value']
                # Iterate over all 'Projection' elements
                for projection in ufactors.findall('Projection'):
                    length_type = projection.find('Length-type').text
                    length = projection.find('Length').attrib['value']
                    u_factor = projection.find('U-factor').attrib.get('value', 'NA')
                    data.append([case_name, tag, delta_t, length_type, length, u_factor])

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Case Name', 'Tag', 'DeltaT', 'LengthType', 'Length', 'U-Factor'])
    return df

# The top argument for walk (your directory path)
topdir = 'THERM 8.0'

# The arg argument for walk, and subsequently ext for step
exten = '.thmx'

dataframes = []

for dirpath, dirnames, files in os.walk(topdir):
    for name in files:
        if name.lower().endswith(exten):
            df = process_file(os.path.join(dirpath, name))
            dataframes.append(df)

# Concatenate all dataframes
final_df = pd.concat(dataframes)

# Save to CSV
final_df.to_csv('output.csv', index=False)
