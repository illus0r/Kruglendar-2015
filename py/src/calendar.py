# -*- coding: utf-8 -*- 
import sys, os
import copy
import svgfig
import math
import numpy
#import pdb

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

class Calendar:
    def __init__(self, \
            dayShapes, \
            canvasSize, \
            timeModelType="top", \
            language="ru", \
            ):
        self.canvasSize = canvasSize
        self.dayFontFamily = "PT Sans"
        self.dayFontSize = "1.8pt"
        if timeModelType == "right":
            self.angleShift = 0
        elif timeModelType == "bottom":
            self.angleShift = 1*math.pi/2
        elif timeModelType == "left":
            self.angleShift = 2*math.pi/2
        elif timeModelType == "top":
            self.angleShift = 3*math.pi/2
        else:
            raise
        self.rainbowGradient = [[  0,  0,  0,239,255,255,  0,  0],  # Red
                 [254,248,246,194,  0,  0,211,254],  # Green
                 [255,193,  0,  0,  0,210,255,255]]  # Blue
        self.rainbowGradientPoints = [ self.angleShift+math.pi*2/7*0,
                                       self.angleShift+math.pi*2/7*1,
                                       self.angleShift+math.pi*2/7*2,
                                       self.angleShift+math.pi*2/7*3,
                                       self.angleShift+math.pi*2/7*4,
                                       self.angleShift+math.pi*2/7*5,
                                       self.angleShift+math.pi*2/7*6,
                                       self.angleShift+math.pi*2/7*7
                                      ]
        monthNamesLang = {}
        monthNamesLang['ru'] = [u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря' ]
        monthNamesLang['en'] = [u'January', u'February', u'March', u'April', u'May', u'June', u'July', u'August', u'September', u'October', u'November', u'December']
        self.monthNames = monthNamesLang[language]




        self.monthSize = [31,28,31,30,31,30,31,31,30,31,30,31]
        self.firstWeekEnd = 3 # какой по счёту день является первой субботой года? Можно -1.
        self.currentYear = "2015"

        self.segmentDay = []
        self.segmentWeek = []
        self.segmentMonth =[]
        self.extra =[]
        self.language = language


        # Загрузим из файла формы для рендеринга дней недели
        self.dayShapes = dayShapes
        self.weekDayShape, self.weekEndShape = self.findDayShapes()

        # заполним текстом массив для порядкового именования дней
        self.fillDaysText()
        self.fillSegmentDay()
        self.fillSegmentWeek()
        self.fillSegmentMonth()
        self.extra = [ExtraDescription(), ExtraYearName(self.currentYear)]

    def fillDaysText(self):
        # получим 12 массивов из номеров всех дней месяцев
        allDays = [ range(1,ms+1) \
                for ms in self.monthSize ]
        # умножим на массив названий месяцев
        self.daysText = [ u'%d %s'%(d,m) \
                for ad, m in zip(allDays, self.monthNames) \
                for d in ad]

    def fillSegmentDay(self):
        dayAngle = math.pi*2/365
        # начнём со сдвигом на полдня, закончим также. Так лучше.
        for index, angle in enumerate(frange(self.angleShift+dayAngle/2, \
                                                self.angleShift+math.pi*2+dayAngle/2, \
                                                dayAngle)):
            print index, angle
            # Находим цвет интерполяцией
            color = self.getColorByAngle(angle)
            # определяем принадлежность выходным
            isWeekEnd = False
            if not (index-self.firstWeekEnd)%7 or not (index-self.firstWeekEnd+1)%7:
                isWeekEnd = True
            try:
                if isWeekEnd:
                    sd = SegmentWeekEnd(copy.deepcopy(self.weekEndShape), \
                            self.canvasSize[0], \
                            text = self.daysText[index], \
                            angle=angle, \
                            color=color
                            )
                else:
                    #print index
                    sd = SegmentWeekDay(copy.deepcopy(self.weekDayShape), \
                            self.canvasSize[0], \
                            text = self.daysText[index], \
                            angle=angle, \
                            color=color
                            )
                self.segmentDay.append(sd)
            except:
                continue

    def fillSegmentMonth(self):
        #for month in self.monthSize:
            #self.segmentWeek
        # На этот раз гипоциклоида будет состоять из нескольких дуг. 
        # Каждая дуга будет иметь r, зависящий от числа дней месяца и
        # сдвиг, относительно начала координат, соответствующий числу дней 
        # во всех предыдущих месяцах.
        #
        # Создадим список количеств дней, предшествующих каждому месяцу
        daysInPreviousMonthes = [sum(self.monthSize[:index]) \
                                    for index, ms in enumerate(self.monthSize)  ]
        print daysInPreviousMonthes

        R = 2*0.3684*self.canvasSize[0]/2
        R = R*0.999 # скейлим, так красивее
        weekHypocycloidCoords = []

        #print  zip(self.monthSize, daysInPreviousMonthes)[:2]
        for ms, pd in zip(self.monthSize, daysInPreviousMonthes):
            #print ms, pd
            # Создадим список координат одной гипоциклоиды
            r = R*ms/365
            # Вычислим радиус, который должна проехать внутренняя окружность от начала координат
            # (правая точка календаря)
            loops = (pd+(365*self.angleShift/(2*math.pi)))/ms
            da = loops*(2*math.pi) # сдвиг гипоциклоиды вперёд
            #print math.pi*2*(pd/365), math.pi*2*((pd+ms)/365)
            for angle in frange(self.angleShift+math.pi*2*(pd/365.0), \
                                self.angleShift+math.pi*2*((pd+ms)/365.0), \
                                0.02):
                x = (R - r)*math.cos(angle) + \
                        r*math.cos((R / r - 1)*angle - da)
                y = (R - r)*math.sin(angle) - \
                        r*math.sin((R / r - 1)*angle - da)
                weekHypocycloidCoords.append((x,y,self.getColorByAngle(angle)))
                #print x, y
        for coord1, coord2 in \
                zip(weekHypocycloidCoords[1:], weekHypocycloidCoords[:-1]):
            #print coord1, coord2
            self.segmentMonth.append(svgfig.SVG("line", \
                    x1=str(coord1[0]), \
                    y1=str(coord1[1]), \
                    x2=str(coord2[0]), \
                    y2=str(coord2[1]), \
                    stroke=coord1[2], \
                    stroke_width="0.566", \
                    stroke_linecap="round"
                    ))

    def fillSegmentWeek(self):
        #for month in self.monthSize:
            #self.segmentWeek
        # Создадим список координат гипоциклоиды
        R = 2*0.3684*self.canvasSize[0]/2
        r = R*7/365
        da = (self.firstWeekEnd+1)*(2*math.pi/7) # сдвиг гипоциклоиды вперёд
        weekHypocycloidCoords = []
        for angle in frange(self.angleShift, \
                            self.angleShift+math.pi*2, \
                            0.02*10): #TODO remove multiplicator
            x = (R - r)*math.cos(angle) + \
                    r*math.cos((R / r - 1)*angle - da)
            y = (R - r)*math.sin(angle) - \
                    r*math.sin((R / r - 1)*angle - da)
            weekHypocycloidCoords.append((x,y,self.getColorByAngle(angle)))
        for coord1, coord2 in \
                zip(weekHypocycloidCoords[1:], weekHypocycloidCoords[:-1]):
            #print coord1, coord2
            self.segmentWeek.append(svgfig.SVG("line", \
                    x1=str(coord1[0]), \
                    y1=str(coord1[1]), \
                    x2=str(coord2[0]), \
                    y2=str(coord2[1]), \
                    stroke=coord1[2], \
                    stroke_width="0.03", \
                    stroke_linecap="round"
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
        # http://goo.gl/61uiF9 -- fooplot
        # рисовалки гипоциклоиды
        # http://www.mekanizmalar.com/hypocycloid.html
        # http://www.artbylogic.com/parametricart/spirograph/spirograph.htm 
        # playing with params
        # r/R = 5/12

        # Создаём объект для рендера
        renderResult = svgfig.SVG("g")
        # Рендерим дни календаря
        for segmentDay in self.segmentDay:
            renderResult.append(segmentDay.render())
        # Рендерим недели
        #segmentWeeks = svgfig.SVG("g")
        #segmentWeeks.extend(self.segmentWeek)
        #renderResult.append(segmentWeeks)
        # Рендерим месяца
        segmentMonthes = svgfig.SVG("g")
        segmentMonthes.extend(self.segmentMonth)
        renderResult.append(segmentMonthes)
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
                    #print pair
                    if pair[0] == u'id':
                        if pair[1] == u'weekday':
                            weekDayShape = s
                            #del(weekDayShape.attr['id'])
                            #print "yo1"
                        elif pair[1] == u'weekend':
                            weekEndShape = s
                            #del(weekEndShape.attr['id'])
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
        #s = svgfig.SVG("rect", x=10, y=10, width=6, height=6, fill="red")
        #s2= svgfig.SVG("rect", x=30, y=30, width=6, height=6, fill="blue")
        #g = svgfig.SVG("g", s, s2, fill_opacity="50%")
        g = svgfig.SVG("g", fill_opacity="50%")
        return g

class ExtraYearName:
    def __init__(self, currentYear):
        self.currentYear = currentYear
        # http://www.kernjs.com/
        pass
    def render(self):
        return svgfig.SVG("text",self.currentYear,x="0",y="0",style="font-size:3.5; stroke-width:0; fill:black; text-anchor:middle; letter-spacing:0.1;")

# Абстрактный класс сегмента дня. Наследуется классами SegmentWeekDay, SegmentWeekEnd
class SegmentDay:
    def __init__(self, \
            shape, \
            canvasWidth, \
            text=u'1 января', \
            #dateIndex=0, \
            #monthIndex=0, \
            #holidayIndex=0, \
            angle=0.0, \
            language="ru", \
            color="#ff0000" \
            ):
        #self.dateName = str(dateIndex+1)
        #self.monthName = "TODO"
        #self.holidayName = ""
        self.canvasWidth = canvasWidth
        self.radius = 2*0.3684*self.canvasWidth/2
        self.angle = angle
        self.color = color
        self.shape = shape
        self.text = text

        # поменяем атрибуты формы дня
        self.shape.attr['fill'] = self.color
        self.shape.attr['stroke'] = self.color
        self.shape.attr['stroke-width'] = 0.
        # В файле daySapes.svg линии не отцентрованы. Отцентруем при помощи translate
        #print self.__class__.__name__
        dayShapeOffset = -150 if self.__class__.__name__ == "SegmentWeekEnd" else -50
        #print dayShapeOffset
        self.shape.attr['transform'] = "rotate(-90) scale(%f) translate(%d)" \
                %(0.00017*self.radius, dayShapeOffset)


class SegmentWeekDay(SegmentDay):
    def render(self):
        #g1 = svgfig.SVG("g", \
                #self.shape,
                #transform="translate(0 150)" \
                #)
        #print repr(svgfig.SVG("text",'hello',x=0,y=0))
        g2 = svgfig.SVG("g", \
                    self.shape, \
                    svgfig.SVG("text", \
                            self.text, \
                            x="%f"%(self.radius*0.0225), \
                            y="%f"%(self.radius*0.005), \
                            style="font-size:%f; stroke-width:0; fill:black; text-anchor:start; letter-spacing:0.1;"% \
                            (self.radius*0.0125)), \
                    transform="rotate(%f 0 0) translate(%f)"%
                    (math.degrees(self.angle), self.radius) \
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
                svgfig.SVG("text", 
                        self.text,
                        x="%f"%(self.radius*(0.0225+0.025)), # second num in brackets is shift relative WeekDay
                        y="%f"%(self.radius*0.005),
                        style="font-size:%f; stroke-width:0; fill:%s; text-anchor:start; letter-spacing:0.1;"% \
                        (self.radius*0.0125, self.color)), \
                transform="rotate(%f 0 0) translate(%f)"%
                (math.degrees(self.angle), self.radius) \
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
    canvasSize = (500,707)
    canvasMiddle = canvasSize[0]/2.0, canvasSize[1]/2.0
    #baseDir = "C:\\Users\\ewew\\Dropbox\\_PROJECTS\\2014.08.24 Kruglendar_2015\\python\\"
    dayShapes = svgfig.load(baseDir+"dayShapes-proper.svg")
    # парсить argv:
    outputFile, timeModelType, language = sys.argv[1:]


    # Размер документа
    svgfig._canvas_defaults['width'] = canvasSize[0]
    svgfig._canvas_defaults['height'] = canvasSize[1]
    svgfig._canvas_defaults['viewBox'] = "0 0 %d %d"% \
            (canvasSize[0], canvasSize[1])
    c = Calendar(dayShapes, canvasSize, timeModelType, language)
    svg = svgfig.SVG("g", c.render(), transform="translate(%f %f)" \
            %(canvasSize[0]/2.0,canvasSize[1]/2.0))
    # записать svg
    svg.save(baseDir + outputFile)
    #print(repr(svg))
