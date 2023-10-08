import os
import re
import subprocess
import ezdxf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Function to clone a GitHub repository
def clone_github_repo(url, folder):
    try:
        subprocess.run(["git", "clone", url, folder])
        print(f"Cloned GitHub repository from {url} to {folder}")
        return True
    except Exception as e:
        print(f"Failed to clone GitHub repository: {e}")
        return False

# Function to list DXF files in a folder
def list_dxf_files(folder):
    dxf_files = [f for f in os.listdir(folder) if f.lower().endswith('.dxf')]
    return dxf_files

# Function to get user-specified color
def get_user_color():
    while True:
        color_input = input("Enter a color (Hex, RGB, or Pantone name): ")
        if re.match(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})$', color_input) or \
           re.match(r'^\d+,\s*\d+,\s*\d+$', color_input):
            return color_input
        else:
            print("Invalid color format. Please enter a valid Hex or RGB color.")

# Function to create a PDF containing DXF files
def create_pdf_with_legends(dxf_files, colors, pdf_name):
    pdf_canvas = canvas.Canvas(pdf_name, pagesize=letter)
    pdf_canvas.setLineWidth(0.5)

    for dxf_file, color in zip(dxf_files, colors):
        doc = ezdxf.readfile(dxf_file)
        msp = doc.modelspace()

        # Plot each DXF entity with the specified color
        for entity in msp.query('*'):
            pdf_canvas.setStrokeColorRGB(*color)
            pdf_canvas.setFillColorRGB(*color)

            if entity.dxftype() == 'LINE':
                pdf_canvas.line(entity.dxf.start.x, entity.dxf.start.y, entity.dxf.end.x, entity.dxf.end.y)
            elif entity.dxftype() == 'CIRCLE':
                pdf_canvas.circle(entity.dxf.center.x, entity.dxf.center.y, entity.dxf.radius)

        # Add legend for each DXF file
        pdf_canvas.setStrokeColorRGB(0, 0, 0)
        pdf_canvas.setFillColorRGB(0, 0, 0)
        pdf_canvas.drawString(20, 20, f"DXF File: {dxf_file}")
        pdf_canvas.drawString(20, 10, f"Color: {color}")

        # Add a page break for the next DXF file
        pdf_canvas.showPage()

    pdf_canvas.save()

# Main script
if __name__ == "__main__":
    folder_path = input("Enter the path to a folder: ")

    # Check if the folder path is a GitHub URL
    if folder_path.startswith("https://github.com/") or folder_path.startswith("git@github.com:"):
        clone_success = clone_github_repo(folder_path, "temp_folder")
        if not clone_success:
            exit()
        folder_path = "temp_folder"

    # List DXF files in the folder
    dxf_files = list_dxf_files(folder_path)

    if not dxf_files:
        print("No DXF files found in the folder.")
    else:
        colors = []
        # Create color_list.txt and write filename-color pairs
        with open("color_list.txt", "w") as color_file:
            for dxf_file in dxf_files:
                print(f"Specify color for {dxf_file}:")
                user_color = get_user_color()
                colors.append(user_color)
                color_file.write(f"{dxf_file}: {user_color}\n")

        pdf_name = input("Enter the filename for the output PDF: ")
        create_pdf_with_legends(dxf_files, colors, pdf_name)
        print(f"PDF {pdf_name} created successfully.")

