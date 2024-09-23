from PIL import Image, ImageDraw, ImageOps
import qrcode
from qrcode_styled import ERROR_CORRECT_Q, QRCodeStyled
from io import BytesIO


def add_rounded_corners(image, radius):
    """Add rounded corners to an image."""
    # Create a mask for the rounded corners
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(
        [(0, 0), image.size], radius=radius, fill=255
    )
    # Apply the mask to the image
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image


# Initialize QR code styled generator
qr = QRCodeStyled()
qr.error_correction = ERROR_CORRECT_Q

# Generate QR code image
qr_code_img = qr.get_image('https://www.facebook.com/AWSCloudClubPUPManila')

# Generate QR code buffer
qr_code_buffer = qr.get_buffer(
    'https://www.facebook.com/AWSCloudClubPUPManila', _format='PNG', quality=80)

# Load the logo
logo_link = 'aws alf.png'
logo = Image.open(logo_link).convert("RGBA")  # Ensure logo is in RGBA mode

# Resize the logo
basewidth = 450  # Adjust this value to resize the logo
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)

# Add rounded corners to the logo
logo_with_rounded_corners = add_rounded_corners(
    logo, radius=50)  # Adjust the radius as needed

# Load the QR code image from buffer
qr_code_img = Image.open(BytesIO(qr_code_buffer.getvalue())).convert("RGBA")

# Convert QR code image to black and white
qr_code_bw = qr_code_img.convert('1')

# Define the color to replace black
color = '#330066'

# Create a new image with the desired color
color_img = Image.new('RGBA', qr_code_img.size, color)

# Create a mask where the QR code is black
mask = Image.eval(qr_code_bw, lambda px: 255 if px == 0 else 0)

# Combine the color image with the QR code image using the mask
colored_qr_code_img = Image.composite(color_img, qr_code_img, mask)

# Calculate the position to paste the logo
qr_width, qr_height = colored_qr_code_img.size
logo_width, logo_height = logo_with_rounded_corners.size
position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

# Paste the logo onto the QR code
# Use the logo with rounded corners as the mask
colored_qr_code_img.paste(logo_with_rounded_corners,
                          position, logo_with_rounded_corners)

# Save the final image
colored_qr_code_img.save('awsccpup.png', 'PNG')
