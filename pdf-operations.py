import fitz  # PyMuPDF
from PIL import Image
import os


def save_pdf_pages_as_images(pdf_path, output_folder, zoom=2, pdf_separatee=False):
    try:
        # Open the PDF file
        pdf_document = fitz.open(pdf_path)

        for page_num in range(pdf_document.page_count):
            # Extract the page with higher resolution
            page = pdf_document.load_page(page_num)
            mat = fitz.Matrix(zoom, zoom)  # Adjust zoom to increase quality
            pix = page.get_pixmap(matrix=mat)

            # Save the page as image with higher DPI
            image_path = f"{output_folder}/page_{page_num + 1}.png"
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            image.save(image_path, dpi=(300, 300))  # Set DPI to 300

            # Save the page as separate PDF
            if pdf_separatee:
                pdf_page_path = f"{output_folder}/page_{page_num + 1}.pdf"
                pdf_bytes = fitz.open()
                pdf_bytes.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
                pdf_bytes.save(pdf_page_path)

        print("Pages have been successfully saved!")
    except FileNotFoundError or FileExistsError:
        print("Folder Doesn't Exist")
    except Exception as e:
        print("Error While Combining images to a single PDF File")


def convert_image_to_pdf(image_path, pdf_path):
    try:
        # Open the image file
        image = Image.open(image_path)

        # Convert the image to RGB mode if it's not already
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Save the image as a PDF with high quality
        image.save(pdf_path, "PDF", resolution=300.0)

        print(f"Image {image_path} has been successfully converted to {pdf_path}.")
    except FileNotFoundError or FileExistsError:
        print("Folder Doesn't Exist")
    except Exception as e:
        print("Error While Combining images to a single PDF File")


def combine_images_to_pdf(image_folder, output_pdf_path):
    try:
        image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if
                       file.endswith(('png', 'jpg', 'jpeg'))]
        image_files.sort()

        # Open images and convert them to RGB
        images = [Image.open(image).convert('RGB') for image in image_files]

        # Save the images as a single PDF
        if images:
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:], resolution=300.0)
            print(f"All images have been successfully combined into {output_pdf_path}.")
        else:
            print("No images found in the specified folder.")
    except FileNotFoundError or FileExistsError:
        print("Folder Doesn't Exist")
    except Exception as e:
        print("Error While Combining images to a single PDF File")


def get_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


if __name__ == '__main__':
    options = """
    Please choose the options from below:
    1. Single Image to a Pdf
    2. Multiple Images to a Pdf
    3. A Pdf divided into Images
    """
    inputval = get_integer(options)
    operation_funcs = {1: lambda: convert_image_to_pdf("image_folder/page_1.png", "image-to-pdf.pdf"),
                       2: lambda: combine_images_to_pdf("image_folder", "images-to-pdf.pdf"),
                       3: lambda: save_pdf_pages_as_images("input.pdf", "output_folder", zoom=2), }
    operation = operation_funcs.get(inputval)
    if operation:
        operation()
    else:
        print("Invalid Choice, Please try Again with valid choice!")
