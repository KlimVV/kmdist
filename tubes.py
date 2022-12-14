# -------------------------------------------------------------------------------
# Name:        tubes
# Purpose:
#
# Author:      klimvv
#
# Created:     27.07.2022
# Copyright:   (c) klimvv 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import os, csv, re, math

USCC_recommend = "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:\n{0}"

HELPSTRING_TUBE = (
    "HLP<b>труба [57*3] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"
)
HELPSTRING_SQTUBE = (
    "HLP<b>тр.кв. [60*3] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"
)
HELPSTRING_PRTUBE = (
    "HLP<b>тр.пр. [60*30*3] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"
)
HELPSTRING_HSS = (
    "HLP<b>hss [80*80*4] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"
)
HELPSTRING_RHS = (
    "HLP<b>rhs [200*100*10] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"
)

PROFTYPE = {
    "кутик": ["angles", "Кутики рiвнополочнi ДСТУ 2251:2018"],
    "швелер": ["channels", "Швелери ДСТУ 3436-96"],
    "двотавр": ["ibeams", "Двотаври ДСТУ 8768:2018 та спецiальнi ДСТУ 8807:2018"],
    "тр.кв.": ["sqtube", "Труби квадратнi ГОСТ 8639-82 (недiюч)"],
    "тр.пр.": ["prtube", "Труби прямокутнi ГОСТ 8645-68 (недiюч)"],
    "труба": ["tube", "Труби електрозварнi прямошовнi ГОСТ 10704-91 (недiюч)"],
    "HSS": ["hss", "Труби квадратнi HSS за EN12019:1997"],
    "RHS": ["rhs", "Труби прямокутнi RHS за EN10219:2006"],
}


class Tube:
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "{pftype} {name} \
                \nПлоща перерiзу {area} кв.см \
                \nПогонна вага {masa} кг/м \
                \nМомент iнерцiї Jy={Jy:.0f} см^4\
                \nМомент iнерцiї Jz={Jz:.0f} см^4\
                \nРадiус iнерцiї iy={iy:.2f} см\
                \nРадiус iнерцiї iz={iz:.2f} см\
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм".format(
            pftype=self.params_row["pftype"],
            name=self.params_row["name"],
            area=self.params_row["A"],
            masa=self.params_row["P"],
            Jy=self.Jy,
            Jz=self.Jz,
            iy=self.iy,
            iz=self.iz,
            freelen=self.get_free_length(),
        )

    @property
    def h(self):
        return float(self.params_row["h"])

    @property
    def b(self):
        return float(self.params_row["b"])

    @property
    def area(self):
        return float(self.params_row["A"])

    @property
    def massa(self):
        return float(self.params_row["P"])

    @property
    def Jy(self):
        return float(self.params_row["Jy"])

    @property
    def iy(self):
        return float(self.params_row["iy"])

    @property
    def Jz(self):
        if "Jz" in self.params_row:
            return float(self.params_row["Jz"])
        else:
            return float(self.params_row["Jy"])

    @property
    def iz(self):
        return math.sqrt(self.Jz / self.area)

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_free_length(self, lyamda=150):
        return self.iz * lyamda * 10

    def get_paint_area(self, l):
        return l * float(self.params_row["parea"])


class Sortament:
    def __init__(self, pftype):
        self.cparams = None
        self.pftype = pftype
        fname = PROFTYPE[pftype][0] + ".csv"
        #file = open(fname + ".csv")
        file = open(os.path.join(os.path.dirname(__file__), fname))
        self.csvr = csv.DictReader(file, delimiter=";")

    def findbyname(self, ctype):
        hasfind = False
        for row in self.csvr:
            if row["name"].startswith(ctype):
                self.cparams = row
                self.cparams["pftype"] = self.pftype
                hasfind = True
                break
        return hasfind

    def getParams(self):
        return self.cparams

    def getNamesList(self):
        nameslist = []
        for row in self.csvr:
            nameslist.append(row["name"])
        return nameslist

    def getNamesListBeauty(self):
        res = ""
        h = ""
        for row in self.csvr:
            if row["h"] != h:
                res += "\n"
            res += row["name"] + "  "
            h = row["h"]
        return res[1:]


def reply_to_message(pftype, msg):
    ctype = re.search(r"(\d{2,3}\*(\d+(?:[\.\,]\d+)?)(\*\d+(?:[\.\,]\d+)?)?)", msg)
    s = Sortament(pftype)
    if ctype:
        if s.findbyname(ctype.group(1)):  # ctype
            ch = Tube(s.getParams())

            answer = ch.__str__()

            ismass = re.search(r"(\d+(?:\.\d+)?)кг", msg)
            if ismass:
                m = float(ismass.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0:.1f} кг це {1:.1f} м профiлю\nПлоща фарбування {2:.1f} кв.м".format(
                        m,
                        ch.get_len_by_mass(m),
                        ch.get_paint_area(ch.get_len_by_mass(m)),
                    )
                )

            islen = re.search(r"(\d+(?:\.\d+)?)м", msg)
            if islen:
                l = float(islen.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0} це {1:.1f} кг профiлю\nПлоща фарбування {2:.1f} кв.м".format(
                        islen.group(0), ch.get_mass_by_len(l), ch.get_paint_area(l)
                    )
                )
        else:
            answer = "Нема такого..."
    # elif msg.find("?") != -1:
    #     answer = HELPSTRING.format(s.pftype, s.getNamesList()[4])
    else:
        answer = (
            USCC_recommend.format(PROFTYPE[pftype][1]) + "\n" + (s.getNamesListBeauty())
        )
    ##            '\n'.join('  '.join(map(str,sl)) for sl in s.getNamesListBeauty())

    picname = PROFTYPE[pftype][0] + ".png" 
    picname = os.path.join(os.path.dirname(__file__), picname)

    return answer, picname


if __name__ == "__main__":
    print(reply_to_message("тр.кв.", "тр.кв. 60*3"))
