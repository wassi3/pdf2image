# pdf2image.py - extracts images from PDF files and stores them in a subfolder with the name of the PDF
import os
import sys
import subprocess
import shutil

QUIET = False

COMPOSITIONS = [
    "CopyOpacity",
]

metadata_parts = [
    'page',
    'num',
    'type',
    'width',
    'height',
    'color',
    'comp',
    'bpc',
    'enc',
    'interop',
    'object',
    'id',
    'x_ppi',
    'y_ppi',
    'size',
    'ratio'
]

class PdfImageMetadata:
    def __init__(self, text):
        parts = text.split()
        for meta in metadata_parts:
            if len(parts) <= 0:
                break
            self.__setattr__(meta, parts.pop(0))
        self.num = int(self.num)
        self.object = int(self.object)

def log(message):
    if not QUIET:
        print(message)

def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    result = process.returncode
    if result != 0:
        print("An error occurred while running {}".format(command))
        print("stdout: {}".format(stdout))
        print("stderr: {}".format(stderr))
        sys.exit(1)
    return {
        "result": result,
        "stdout": stdout.decode('utf-8').split('\n'),
        "stderr": stderr.decode('utf-8').split('\n')
    }

def extract_images(input_pdf_file, extract_dir):
    log(f"Extract image data from PDF to [{extract_dir}]")
    command = f'pdfimages -png "{input_pdf_file}" "{extract_dir}/image"'
    execute(command)

def gather_extracted_image_paths(extract_dir):
    log("Gather extracted image paths")
    extracted_images = {}
    for root, dirs, files in os.walk(extract_dir):
        for ff in files:
            if ff.startswith('image-'):
                image_num = int(ff.split('-')[1].split('.')[0])
                extracted_images[image_num] = os.path.join(root, ff)
    return extracted_images

def parse_pdf_image_metadata(input_pdf_file):
    log("Parse PDF image metadata")
    command = f'pdfimages -list "{input_pdf_file}"'
    list_results = execute(command)
    pdf_objects = {}
    count = 0
    for line in list_results['stdout']:
        count += 1
        if count < 3:
            continue
        if len(line) <= 2:
            continue
        image = PdfImageMetadata(line)
        if not 'image' in image.type and not 'smask' in image.type:
            continue
        if not image.object in pdf_objects:
            pdf_objects[image.object] = {}
        pdf_objects[image.object][image.type] = image
    return pdf_objects

def compose(image, mask, destination, mode, output_dir):
    file_name = f'{os.path.basename(output_dir)}-{destination:03d}.png'
    merged_path = os.path.join(output_dir, file_name)
    command = f'convert "{image}" "{mask}" -compose {mode} -composite "{merged_path}"'
    execute(command)

def process_images(pdf_objects, extracted_images, output_dir):
    log("Merging masked images, copying standalone images")
    merged_count = 0

    for idx, (k, v) in enumerate(pdf_objects.items(), start=1):
        if 'smask' in v and 'image' in v:
            image = extracted_images[v['image'].num]
            mask = extracted_images[v['smask'].num]
            compose(image, mask, idx, "CopyOpacity", output_dir)
            merged_count += 1
        elif 'image' in v:
            source = extracted_images[v['image'].num]
            file_name = f'{os.path.basename(output_dir)}-{idx:03d}.png'
            shutil.copy(source, os.path.join(output_dir, file_name))
    log(f"Images sorted and merged using CopyOpacity in [{output_dir}]")
    return merged_count

def cleanup_temp_images(extract_dir):
    for root, dirs, files in os.walk(extract_dir):
        for ff in files:
            if ff.startswith('image-'):
                os.remove(os.path.join(root, ff))

def main():
    if len(sys.argv) < 2:
        print("An input PDF file is required")
        sys.exit(1)

    input_pdf_file = sys.argv[1]
    output_dir = os.path.splitext(input_pdf_file)[0]

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    extract_images(input_pdf_file, output_dir)
    extracted_images = gather_extracted_image_paths(output_dir)
    pdf_objects = parse_pdf_image_metadata(input_pdf_file)
    process_images(pdf_objects, extracted_images, output_dir)
    cleanup_temp_images(output_dir)

if __name__ == "__main__":
    main()
