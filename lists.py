# -------------------------------------------------------------------------------
# Name:        lists
# Purpose:
#
# Author:      klimvv
#
# Created:     01.06.2022
# Copyright:   (c) klimvv 2022
# Licence:     <GPL>
# -------------------------------------------------------------------------------

import re, csv

ro = 7.850 / 1000000

HELPSTRINGLIST = "HLP<b>лист [6*500*500] або '6 10кг'</b>\n(параметри в [...] необов'язкові)"
HELPSTRINGRIF = "HLP<b>риф [6*500*500] або '6 10кг'</b>\n(параметри в [...] необов'язкові)"
HELPSTRINGPVL = "HLP<b>пвл [406*500*500] або '406 10кг'  </b>\n(параметри в [...] необов'язкові)"

class List:
    def __init__(self, t, B, H):
        self.t = t
        self.B = B
        self.H = H

    def __str__(self):
        return "Лист {t:.0f}*{B:.0f}*{H:.0f} \
               \nВага {masa:.1f} кг \
               \nПлоща фарбування з 2х сторін {parea:.1f} кв.м".format(
            masa=self.massa,
            parea=self.paint_area,
            t=self.t,
            H=self.H,
            B=self.B
        )

    @property
    def massa(self):
        return self.t * self.B * self.H * ro

    @property
    def paint_area(self):
        return self.B * self.H * 2 / 1000000


class RifList(List):
    def __init__(self, sortrow):
        self.params = sortrow

    def __str__(self):
        return "Лист риф. {name}\nВага 1 кв.м. {masa} кг".format(
            name=self.params["name"],
            masa=self.params["m"]
        )

    @property
    def masa(self):
        return float(self.params["m"])

    def get_masa_by_dim(self, B, H):
        return B*H/1000000*self.masa

class PVList(List):
    def __init__(self, sortrow):
        self.params = sortrow

    def __str__(self):
        return "Лист {name}\
               \nВага 1 кв.м. {masa:.1f} кг\
               \nТовщина {thick} мм".format(
            name=self.params["name"],
            masa=self.params["m"],
            thick=self.params["t"]
        )

    @property
    def masa(self):
        return float(self.params["m"])

    def get_masa_by_dim(self, B, H):
        return B*H/1000000*self.masa


def get_paintarea_by_mass(t, m):
    return 2 * m / (t * 7.85)

class ListSortament:
    def __init__(self, fname):
        self.aparams = None
        self.fname = fname

    def findbyname(self, _name):
        hasfind = False
        file = open(self.fname)
        csvr = csv.DictReader(file, delimiter=";")

        for row in csvr:
            if row["name"] == _name:
                self.aparams = row
                hasfind = True
        file.close()
        return hasfind

    def getSpecListParams(self):
        return self.aparams


def reply_to_message_list(msg):
    answer = ""
    dims = re.search(r"(\d{1,3})\*(\d{2,5})\*(\d{2,5})", msg)
    if dims:
        t = float(dims.group(1)) / 1000
        B = float(dims.group(2)) / 1000
        H = float(dims.group(3)) / 1000
        masa = t * B * H * 7850
        area = B * H * 2
        answer = "Маса листа {0:.1f} кг, \nПлоща фарбування з 2х сторін {1:.1f} кв.м.".format(masa, area)
    else:
        dims = re.search(r"(\d+(?:\.\d+)?)\s(\d+(?:\.\d+)?)кг", msg)
        if dims:
            t = float(dims.group(1)) / 1000
            m = float(dims.group(2))
            area = m / (t * 7850)
            answer+= "{0}кг це {1:.2f} кв.м листа".format(m, area)

    if answer == "":
        answer = (
                "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:"
                + "\n2, 3, 4, 5, 6, 8 - (С245)"
                + "\n8, 10, 16, 18, 20, 22, 25, 30, 32, 36, 40, 50 - (C255)"
            )
    return answer

def reply_to_message_rif(msg):
    answer = ""
    dims = re.search(r"(\d{1})\*(\d{2,5})\*(\d{2,5})", msg)
    if dims:
        s = ListSortament("riflist.csv")
        if s.findbyname(dims.group(1)):
            t = float(dims.group(1)) / 1000
            B = float(dims.group(2)) / 1000
            H = float(dims.group(3)) / 1000
            masa = float(s.getSpecListParams()["m"])
            area = B * H * 2
            answer = "Маса листа {0:.1f} кг, \nПлоща фарбування з 2х сторін {1:.1f} кв.м.".format(masa, area)
        else:
            answer = "Нема такого"
    else:
        dims = re.search(r"(\d+(?:\.\d+)?)\s(\d+(?:\.\d+)?)кг", msg)
        if dims:
            s = ListSortament("riflist.csv")
            if s.findbyname(dims.group(1)):
                t = float(dims.group(1)) / 1000
                m = float(dims.group(2))
                area = m / float(s.getSpecListParams()["m"])
                answer = "{0}кг це {1:.2f} кв.м листа".format(m, area)
    if answer == "":
        answer = (
                "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:"
                + "\nРифлений (сочевица): 3, 4, 5, 6 - (С245)"
            )
    return answer

def reply_to_message_pvl(msg):
    answer = ""
    dims = re.search(r"(\d{1,3})\*(\d{2,5})\*(\d{2,5})", msg)
    if dims:
        s = ListSortament("pvlist.csv")
        if s.findbyname(dims.group(1)):
##            t = float(dims.group(1)) / 1000
            B = float(dims.group(2)) / 1000
            H = float(dims.group(3)) / 1000
            masa = float(s.getSpecListParams()["m"])
            t = s.getSpecListParams()["t"]
            area = B * H * 2
            answer = "Маса листа {0:.1f} кг \nТовщина {2} мм \nПлоща фарбування з 2х сторін {1:.1f} кв.м.".format(masa, area,t)
        else:
            answer = "Нема такого"
    else:
        dims = re.search(r"(\d+(?:\.\d+)?)\s(\d+(?:\.\d+)?)кг", msg)
        if dims:
            s = ListSortament("pvlist.csv")
            if s.findbyname(dims.group(1)):
                t = float(dims.group(1)) / 1000
                m = float(dims.group(2))
                area = m / float(s.getSpecListParams()["m"])
                answer = "{0}кг це {1:.2f} кв.м листа".format(m, area)
    if answer == "":
        answer = (
                "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:"
                + "\nПВЛ: 306, 406, 506, 608 - (С235)"
            )
    return answer

if __name__ == "__main__":
        print(reply_to_message_rif("риф 4 16кг"))
##    r=PVList(406, 1000, 1000)
##    print(r.massa)
