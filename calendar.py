# -*- coding: utf-8 -*- 
import sys, os
import svgfig
import math
import numpy

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

class Calendar:
    def __init__(self, dayShapes, timeModelType="top", language="ru"):
        self.canvasSize = (500,707)
        self.canvasMiddle = self.canvasSize[0]/2.0, self.canvasSize[1]/2.0
        self.dayFontFamily = "PT Sans"
        self.dayFontSize = "1.8pt"
        self.rainbowGradient = [[  0,  0,  0,239,255,255,  0,  0],  # Red
                 [254,248,246,194,  0,  0,211,254],  # Green
                 [255,193,  0,  0,  0,210,255,255]]  # Blue
        self.rainbowGradientPoints = [math.pi*2/7*0,
                   math.pi*2/7*1,
                   math.pi*2/7*2,
                   math.pi*2/7*3,
                   math.pi*2/7*4,
                   math.pi*2/7*5,
                   math.pi*2/7*6,
                   math.pi*2/7*7
                  ]
        self.mounthNames = [u'января',\
            u'февраля',\
            u'марта',\
            u'апреля',\
            u'мая',\
            u'июня',\
            u'июля',\
            u'августа',\
            u'сентября',\
            u'октября',\
            u'ноября',\
            u'декабря'\
            ]
        self.mounthSize = [31,28,31,30,31,30,31,31,30,31,30,31]

        self.segmentDay = []
        self.segmentWeek = []
        self.segmentMounth =[]
        self.extra =[]
        self.timeModelType = timeModelType
        self.language = language
        # Загрузим из файла формы для рендеринга дней недели
        self.dayShapes = dayShapes
        self.weekDayShape, self.weekEndShape = self.findDayShapes()

        self.fillSegmentDays()
        self.extra = [ExtraDescription()]


    def fillSegmentDays(self):
        dayAngle = math.pi*2/365
        for index, angle in enumerate(frange(0,math.pi*2,dayAngle)):
            # Находим цвет интерполяцией
            colorTuple = (int(numpy.interp(angle, \
                    self.rainbowGradientPoints, self.rainbowGradient[0])), \
                    int(numpy.interp(angle, \
                    self.rainbowGradientPoints, self.rainbowGradient[1])), \
                    int(numpy.interp(angle, \
                    self.rainbowGradientPoints, self.rainbowGradient[2])))
            color = "rgb%s"%(str(colorTuple))
            # определяем принадлежность выходным
            isWeekEnd = True
            # TODO

            if isWeekEnd:
                sd = SegmentWeekEnd(self.weekEndShape, \
                        angle=angle, \
                        color=color
                        )
            else:
                sd = SegmentWeekDay(self.weekDayShape, \
                        angle=angle, \
                        color=color
                        )
            self.segmentDay.append(sd)

    def render(self):
        # подобираем уравнения для гипоциклоид
        # 6-abs(sin(theta*6)) -- синусоиды, кривовато
        # x = (R - r)*cos(s) + r*cos((R / r - 1)*s)
        # y = (R - r)*sin(s) - r*sin((R / r - 1)*s) - работает
        # http://goo.gl/jUPM5n

        # Создаём объект для рендера
        renderResult = svgfig.SVG("g") # TODO описать положение на листе
        # Рендерим дни календаря
        for segmentDay in self.segmentDay:
            renderResult.append(segmentDay.render())
        # Рендерим недели
        # Рендерим месяца
        # Рендерим дополнительные данные
        for extraItem in self.extra:
            renderResult.append(extraItem.render())

        return renderResult

    def findDayShapes(self):
        weekDayShape = ''
        weekEndShape = ''
        #print repr(self.dayShapes)
        for ti, s in self.dayShapes:
            #print repr(s)
            try:
                for pair in s.attr.items():
                    if pair[0] == u'id':
                        if pair[1] == u'weekday':
                            weekDayShape = s
                            #print "yo1"
                        elif pair[1] == u'weekend':
                            weekEndShape = s
                            #print "yo2"
            except Exception, e:
                continue
        if weekDayShape == '':
            print("Weekday not found in svg")
            raise
        elif weekEndShape == '':
            print("Weekend not found in svg")
            raise
        return weekDayShape, weekEndShape
                
class ExtraDescription:
    def __init__(self):
        pass
    def render(self):
        s = svgfig.SVG("rect", x=10, y=10, width=60, height=60, fill="red")
        s2= svgfig.SVG("rect", x=30, y=30, width=60, height=60, fill="blue")
        g = svgfig.SVG("g", s, s2, fill_opacity="50%")
        return g

class ExtraYearName:
    def __init__(self):
        # http://www.kernjs.com/
        pass

# Абстрактный класс сегмента дня. Наследуется классами SegmentWeekDay, SegmentWeekEnd
class SegmentDay:
    def __init__(self, \
            shape, \
            dateIndex=0, \
            mounthIndex=0, \
            holidayIndex=0, \
            angle=0.0, \
            language="ru", \
            color="#ff0000" \
            ):
        self.dateName = str(dateIndex+1)
        self.mounthName = "TODO"
        self.holidayName = ""
        self.angle = angle
        self.shape = shape

class SegmentWeekDay(SegmentDay):
    def render(self):
        pass

class SegmentWeekEnd(SegmentDay):
    def render(self):
        g = svgfig.SVG("g", \
                svgfig.SVG("rect", x=0, y=0, width=6, height=6, fill="blue"), \
                fill_opacity="5%")
        gScaled = svgfig.SVG("g", \
                g, \
                transform="scale(1)")
        gTranslated = svgfig.SVG("g", \
                gScaled, \
                transform="translate(20)")
        gRotated = svgfig.SVG("g", \
                gTranslated, \
                transform="rotate(%f 0 0)" \
                %(math.degrees(self.angle)))
        return gRotated
            ## Draw a day segments
            #dayLineGroup.add (dwg.line( \
                    #(mid[0]-R_days_beg*sinus,mid[1]+R_days_beg*cosinus), \
                    #(mid[0]-R_days_end *sinus,mid[1]+R_days_end *cosinus), \
                    #stroke=color \
                    #))

        ## Draw a day name
        #if (index-4)%7 == 0 or (index-3)%7 == 0:
            #fillColor = color #"rgb(255,255,255)"
            ##fontWeight = "bold"
            #weekendMargin = 2.0
        #else:
            #fillColor = "rgb(0,0,0)"
            ##fontWeight = "normal"
            #weekendMargin = 0
        #wordGroup = dwg.g(transform="rotate(%f, %f, %f) translate(%f,0)" \
                #%( math.degrees(angle+dayAngle+textAngleShift)+90, mid[0], mid[1], +R_dates+weekendMargin ) \
                #)
        #wordGroup.add( dwg.text( '%s'%(yearDays[index]), \
                #insert=mid, fill=fillColor \
                ##,style="font-weight: %s;"%(fontWeight)
                #))
        #textGroup.add(wordGroup)

if __name__ == '__main__':
    baseDir = os.path.dirname(os.path.realpath(__file__))+"\\"
    #baseDir = "C:\\Users\\ewew\\Dropbox\\_PROJECTS\\2014.08.24 Kruglendar_2015\\python\\"
    dayShapes = svgfig.load(baseDir+"dayShapes.svg")
    # парсить argv:
    outputFile, timeModelType, language = sys.argv[1:]


    c = Calendar(dayShapes, timeModelType, language)
    svg = svgfig.SVG("g", c.render())
    # записать svg
    svg.save(baseDir + outputFile)
    #print(repr(svg))
