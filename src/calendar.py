# -*- coding: utf-8 -*- 
import sys, os
import copy
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

        self.fillSegmentDay()
        self.fillSegmentWeek()
        self.extra = [ExtraDescription()]

    def fillSegmentDay(self):
        dayAngle = math.pi*2/365
        for index, angle in enumerate(frange(0,math.pi*2,dayAngle)):
            # Находим цвет интерполяцией
            color = self.getColorByAngle(angle)
            # определяем принадлежность выходным
            firstWeekEnd = 3 # какой по счёту день является первой субботой года? Можно -1.
            isWeekEnd = False
            if not (index-firstWeekEnd)%7 or not (index-firstWeekEnd+1)%7:
                isWeekEnd = True
            if isWeekEnd:
                sd = SegmentWeekEnd(copy.deepcopy(self.weekEndShape), \
                        angle=angle, \
                        color=color
                        )
            else:
                sd = SegmentWeekDay(copy.deepcopy(self.weekDayShape), \
                        angle=angle, \
                        color=color
                        )
            self.segmentDay.append(sd)

    def fillSegmentWeek(self):
        #for mounth in self.mounthSize:
            #self.segmentWeek
        # Создадим список координат гипоциклоиды
        R = 40.0
        r = R*7/365
        weekHypocycloidCoords = []
        for angle in frange(0,math.pi*2/8,0.02):
            x = (R - r)*math.cos(angle) + r*math.cos((R / r - 1)*angle)
            y = (R - r)*math.sin(angle) - r*math.sin((R / r - 1)*angle)
            weekHypocycloidCoords.append((x,y,self.getColorByAngle(angle)))
        # TODO мы пока что сделаем тут один элемент, возможно, надо переделать
        #hypocycloid = svgfig.SVG("poly", weekHypocycloidCoords)
        #hypocycloid = svgfig.SVG("rect", x=10, y=10, width=6, height=6, fill="red")
        # Пройдёмся по массиву точек, сохраним массив svg линий
        #hypocycloid = 
        for coord1, coord2 in zip(weekHypocycloidCoords[1:], weekHypocycloidCoords[:-1]):
            #print coord1, coord2
            self.segmentWeek.append(svgfig.SVG("line", \
                    x1=str(coord1[0]), \
                    y1=str(coord1[1]), \
                    x2=str(coord2[0]), \
                    y2=str(coord2[1]), \
                    stroke=coord1[2], \
                    stroke_width="0.05"
                    ))
        #print self.segmentWeek

    def getColorByAngle(self, angle):
        colorTuple = (int(numpy.interp(angle, \
                self.rainbowGradientPoints, self.rainbowGradient[0])), \
                int(numpy.interp(angle, \
                self.rainbowGradientPoints, self.rainbowGradient[1])), \
                int(numpy.interp(angle, \
                self.rainbowGradientPoints, self.rainbowGradient[2])))
        color = "rgb%s"%(str(colorTuple))
        return color



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
            renderResult.extend(self.segmentWeek)
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
                            del(weekDayShape.attr['id'])
                            #print "yo1"
                        elif pair[1] == u'weekend':
                            weekEndShape = s
                            del(weekEndShape.attr['id'])
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
        s = svgfig.SVG("rect", x=10, y=10, width=6, height=6, fill="red")
        s2= svgfig.SVG("rect", x=30, y=30, width=6, height=6, fill="blue")
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
        self.color = color
        self.shape = shape

        # поменяем атрибуты формы дня
        self.shape.attr['fill'] = self.color
        self.shape.attr['stroke'] = self.color
        # В файле daySapes.svg линии не отцентрованы. Отцентруем при помощи translate
        #print self.__class__.__name__
        dayShapeOffset = -150 if self.__class__.__name__ == "SegmentWeekEnd" else -50
        #print dayShapeOffset
        self.shape.attr['transform'] = "rotate(-90) scale(0.0068) translate(%d)" \
                %(dayShapeOffset)


class SegmentWeekDay(SegmentDay):
    def render(self):
        #g1 = svgfig.SVG("g", \
                #self.shape,
                #transform="translate(0 150)" \
                #)
        g2 = svgfig.SVG("g", \
                self.shape,
                transform="rotate(%f 0 0) translate(40)" \
                %(math.degrees(self.angle)) \
                )
        return g2

class SegmentWeekEnd(SegmentDay):
    def render(self):
        #g1 = svgfig.SVG("g", \
                #self.shape,
                #transform="translate(0 150)" \
                #)
        g2 = svgfig.SVG("g", \
                self.shape,
                transform="rotate(%f 0 0) translate(40)" \
                %(math.degrees(self.angle)) \
                )
        return g2
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
