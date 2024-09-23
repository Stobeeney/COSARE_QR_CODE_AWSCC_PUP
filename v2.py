from PIL import Image, ImageOps
import qrcode
from qrcode_styled import ERROR_CORRECT_Q, QRCodeStyled
from io import BytesIO

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
basewidth = 300  # Adjust this value to resize the logo
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)

# Load the QR code image from buffer
qr_code_img = Image.open(BytesIO(qr_code_buffer.getvalue())).convert("RGBA")

# Add color to the QR code
# Convert QR code image to grayscale
qr_code_img_gray = qr_code_img.convert('L')
# Create a new image with the desired color
color = '#330066'
color_img = Image.new('RGBA', qr_code_img.size, color)
# Combine grayscale QR code with color
colored_qr_code_img = Image.composite(color_img, qr_code_img, qr_code_img_gray)

# Calculate the position to paste the logo
qr_width, qr_height = colored_qr_code_img.size
logo_width, logo_height = logo.size
position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

# Paste the logo onto the QR code
# Use the logo itself as the mask
colored_qr_code_img.paste(logo, position, logo)

# Save the final image
colored_qr_code_img.save('test3.png', 'PNG')
