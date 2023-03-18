import ddddocr

ocr = ddddocr.DdddOcr()

def decodeCaptcha(imgb: bytes) -> str:
    return ocr.classification(imgb)