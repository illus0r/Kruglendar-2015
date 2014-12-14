import svgwrite

color = "#0083D7"
svg_document = svgwrite.Drawing(filename = "bezier-test.svg",
        size = ("800px", "600px"))

path = svgwrite.path.Path(stroke = color, fill = color, stroke_width = 4)
heightInner = 100
heightOuter = 200
width = 100
path.push('m',(100,100), \
        'c',(width/4, 0, width/4, heightOuter, width/2, heightOuter), \
        'c',(width/4, 0, width/4, -heightOuter, width/2, -heightOuter), \
        'c',(-width/4, 0, -width/4, heightInner, -width/2, heightInner), \
        'c',(-width/4, 0, -width/4, -heightInner, -width/2, -heightInner), \
        'z')
#path.rotate(100)
svg_document.add(path)

svg_document.save()

