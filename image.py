from io import BytesIO

def PIL_to_PNG(img):

    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im