# -*- coding: utf-8 -*- 
import sys, os, svgfig

class Calendar:
    def __init__(self, dayShapes, timeModelType="top", language="ru"):
        self.segmentDay = []
        self.segmentWeek = []
        self.segmentMounth =[]
        self.extra =[]
        self.timeModelType = timeModelType
        self.language = language
        # day shapes
        self.dayShapes = dayShapes
        self.weekDayShape, self.weekEndShape = self.findDayShapes()
        #print repr(self.weekDayShape), repr(self.weekEndShape) 

    def render(self):
        # подобираем уравнения для гипоциклоид
        # 6-abs(sin(theta*6)) -- синусоиды, кривовато
        # x = (R - r)*cos(s) + r*cos((R / r - 1)*s)
        # y = (R - r)*sin(s) - r*sin((R / r - 1)*s) - работает
        # http://goo.gl/jUPM5n

        pass

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
                

# Абстрактный класс сегмента дня. Наследуется классами SegmentWeekDay, SegmentWeekEnd
class SegmentDay:
    def __init__(self, \
            path, \
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
        self.path = path

class SegmentWeekDay(SegmentDay):
    def render(self):
        pass

class SegmentWeekEnd(SegmentDay):
    def render(self):
        pass

if __name__ == '__main__':
    baseDir = os.path.dirname(os.path.realpath(__file__))
    dayShapes = svgfig.load(baseDir+"\\dayShapes.svg")
    # парсить argv:
    outputFile, timeModelType, language = sys.argv[1:]


    c = Calendar(dayShapes, timeModelType, language)
    svg = c.render()
    # записать svg
