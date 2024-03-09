from PIL import Image

def unpackData(imagePath, rgb):
    image = Image.open(imagePath)
    colourData = []

    for x in range(16):
        rowData = []
        for y in range(16):
            pixelColour = image.getpixel((x, y))
            if pixelColour == rgb:
                rowData.append("1")
            else:
                rowData.append("0")

        colourData.append(rowData)

    return colourData

def unpackAll(imagePath: str):
    try:
        return [unpackData(imagePath, (255,0,0,255)),unpackData(imagePath, (0,255,0,255)),unpackData(imagePath, (0,0,255,255))]
    except Exception as err:
        return [err, False, False]