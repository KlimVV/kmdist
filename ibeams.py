# -------------------------------------------------------------------------------
# Name:        IBeam
# Purpose:
#
# Author:      klimvv
#
# Created:     25.07.2022
# Copyright:   (c) klimvv 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import os, csv, re, math

lmbd = 150 / 1000
i40 = 40

HELPSTRING = "HLP<b>двотавр [16] [короб] [1кг] [10м]</b>\n(параметри в [...] необов'язкові)"


class IBeam:
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Двотавр {name} \
                \nПлоща перерізу {area} см^2 \
                \nПогонна вага {masa} кг/м \
                \nМомент інерції Jy={Jy} см^4\
                \nМомент інерції Jz(min)={Jz} см^4\
                \nРадіус інерції iy={iy} см\
                \nРадіус інерції i_min={iz} см\
                \nРозрахункова длина (гнучкість=150) {freelen:.0f} мм".format(
            name=self.params_row["name"],
            area=self.params_row["A"],
            masa=self.params_row["m"],
            Jy=self.params_row["Jy"],
            Jz=self.params_row["Jz"],
            iy=self.params_row["iy"],
            iz=self.params_row["iz"],
            freelen=self.get_free_length()
        )

    @property
    def b(self):
        return float(self.params_row["b"])

    @property
    def massa(self):
        return float(self.params_row["m"])

    @property
    def area(self):
        return float(self.params_row["A"])

    @property
    def Jy(self):
        return float(self.params_row["Jy"])

    @property
    def Jz(self):
        return float(self.params_row["Jz"])

    @property
    def iy(self):
        return float(self.params_row["iy"])

    @property
    def iz(self):
        return float(self.params_row["iz"])
    

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return l * float(self.params_row["parea"])

    def get_free_length(self, lyamda=150):
        return self.iz * lyamda * 10  # sm -> mm


class IBeamK(IBeam):
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Двотавр {name} (короб) \
                \nПлоща перерізу {area} см^2 \
                \nПогонна вага {masa} кг/м \
                \nМомент інерції Jy={Jy} см^4\
                \nМомент інерції Jz(min)={Jz:.0f} см^4\
                \nРадіус інерції iy={iy} см\
                \nРадіус інерції i_min={iz:.2f} см\
                \nРозрахункова длина (гнучкість=150) {freelen:.0f} мм".format(
            name=self.params_row["name"],
            area=self.area,
            masa=self.massa,
            Jy=self.Jy,
            Jz=self.Jz,
            iy=self.iy,
            iz=self.iz,
            freelen=self.get_free_length()
        )

    @property
    def massa(self):
        return super().massa * 2

    @property
    def area(self):
        return super().area * 2

    @property
    def Jy(self):
        return super().Jy * 2

    @property
    def Jz(self):
        _b = super().b / 2 / 10 # mm -> sm
        return (super().Jz + _b**2 * super().area) * 2

    @property
    def iy(self):
        return super().iy

    @property
    def iz(self):
        return math.sqrt(self.Jz / self.area)

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return l * (float(self.params_row["parea"]) + 2*super().b/1000)

    def get_free_length(self, lyamda=150):
        return self.iz * lyamda * 10  # sm -> mm


class IBeamSortament:
    def __init__(self):
        self.cparams = None

    def findbyname(self, ctype):
        hasfind = False
        file = open(os.path.join(os.path.dirname(__file__),"ibeam.csv"))
        csvr = csv.DictReader(file, delimiter=";")

        for row in csvr:
            if row["name"].startswith(ctype):
                self.cparams = row
                hasfind = True
        file.close()
        return hasfind

    def getIBeamParams(self):
        return self.cparams


def reply_to_message(msg):
    kind = None
    ctype = re.search(r"(\d+(?:\.\d+)?)", msg)
    if ctype:
        s = IBeamSortament()
        if s.findbyname(ctype.group(1)):
            kind = re.search(r"(короб)", msg)
            if kind:
                if kind.group(0) == "короб":
                    ch = IBeamK(s.getIBeamParams())
            else:
                ch = IBeam(s.getIBeamParams())

            answer = ch.__str__()

            ismass = re.search(r"(\d+(?:\.\d+)?)кг", msg)
            if ismass:
                m = float(ismass.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0:.1f} кг це {1:.1f} м профілю\nПлоща фарбування {2:.1f} кв.м".format(
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
                    + "\n~~~\n{0} це {1:.1f} кг профілю\nПлоща фарбування {2:.1f} кв.м".format(
                        islen.group(0), ch.get_mass_by_len(l), ch.get_paint_area(l)
                    )
                )
        else:
            answer = "Нема такого..."
    elif msg.find("?") != -1:
        answer = HELPSTRING
    else:
        answer = \
            "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:" \
            + "\n14, 16, 18, 20, 30, 36, 45" \
            + "\n24М, 36М, 45М" \


    if kind:
        if kind.group(0) == "короб":
            picname = "ibeamK.png"
    else:
        picname = os.path.join(os.path.dirname(__file__), "ibeam.png")

    return answer, os.path.join(os.path.dirname(__file__), picname)


if __name__ == "__main__":
    print(reply_to_message("двотавр короб 16 "))
