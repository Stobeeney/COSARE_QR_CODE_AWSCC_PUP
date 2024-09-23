from PIL import Image

from qrcode_styled import ERROR_CORRECT_Q, QRCodeStyled

qr = QRCodeStyled()

# Save to the file
with open('test.png', 'wb') as _fh:
    qr.get_image('https://www.facebook.com/AWSCloudClubPUPManila').save(
        _fh, 'PNG', lossless=False, quaility=80, method=2)

# Get BytesIO buffer
qrcode = qr.get_buffer('https://www.facebook.com/AWSCloudClubPUPManila', _format='PNG',
                       lossless=False, quality=80, method=2)

# You may put Image in the center of a QR Code
im = Image.open("aws alf.png")

qr.error_correction = ERROR_CORRECT_Q
qrcode = qr.get_buffer(
    'https://www.facebook.com/AWSCloudClubPUPManila', image=im, _format='PNG')

# Print real bytes from buffer
print(qrcode.getvalue())
