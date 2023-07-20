import os
import xml.etree.ElementTree as ET
import csv

# This is the default namespace
ns = {'lbl': 'http://windows.lbl.gov'}


def extract_values_from_file(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract values
    therm_version = root.find('lbl:ThermVersion', ns).text
    cross_section_type = root.find('lbl:CrossSectionType', ns).text
    frame_u_factor = None
    edge_u_factor = None
    for results in root.findall('lbl:Results', ns):
        for case in results.findall('lbl:Case', ns):
            model_type = case.find('lbl:ModelType', ns)
            if model_type is None or model_type.text == "U-factor":
                for u in case.findall('lbl:U-factors', ns):
                    tag_name = u.find('lbl:Tag', ns)
                    for projection in u.findall('lbl:Projection', ns):
                        length_type = projection.find('lbl:Length-type', ns)
                        if length_type is not None and length_type.text == "Projected in glass plane":
                            if tag_name.text == 'Frame':
                                frame_u_factor = projection.find('lbl:U-factor', ns).get('value')
                            elif tag_name.text == 'Edge':
                                edge_u_factor = projection.find('lbl:U-factor', ns).get('value')

    filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]

    return [therm_version, filename_without_ext, cross_section_type, frame_u_factor, edge_u_factor]


def process_all_files(root_directory):
    # Prepare the CSV file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ThermVersion", "Filename", "CrossSectionType", "Frame_U-factor", "Edge_U-factor"])

        # Walk through root_directory
        for dirpath, dirs, files in os.walk(root_directory):
            for filename in files:
                if filename.endswith('.thmx'):
                    file_path = os.path.join(dirpath, filename)
                    values = extract_values_from_file(file_path)
                    writer.writerow(values)  # write to CSV file


# Then you can use the function with your root directory
process_all_files('THERM 8.0')
