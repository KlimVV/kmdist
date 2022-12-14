# -------------------------------------------------------------------------------
# Name:        angles
# Purpose:
#
# Author:      klimvv
#
# Created:     23.04.2022
# Copyright:   (c) klimvv 2022
# Licence:     <GPL>
# -------------------------------------------------------------------------------

import os, csv, re, math

i40 = 40


def helpstr():
    return "HLPкутик [50*5] [хрест|тавр|короб] [1кг] [10м]\n(параметри в [...] необов'язковi)"


HELPSTRING = "HLP<b>кутик [50x5] [хрест|тавр|короб] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"


class Angle:
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Кутик L{0} \
               \nПлоща перерiзу {1} см^2 \
               \nПогонна вага {2} кг/м \
               \nМомент iнерцiї Jy=Jz={5} см^4\
               \nМомент iнерцiї Jmin={6} см^4\
               \nРадiус iнерцiї iy={7} см\
               \nРадiус iнерцiї i_min={8} см\
               \nЦентр ваги x0=y0={3} см \
               \nРозрахункова длина (гнучкiсть=150) {4:.0f} мм".format(
            self.params_row["name"],
            self.params_row["A"],
            self.params_row["m"],
            self.params_row["y0"],
            self.get_free_length(),
            self.getparam("Jy"),
            self.getparam("Jv"),
            self.getparam("iy"),
            self.getparam("iv"),
        )

    def getparam(self, pname):
        return self.params_row.get(pname)

    @property
    def B(self):
        return float(self.params_row["B"])

    @property
    def t(self):
        return float(self.params_row["t"])

    @property
    def area(self):
        return float(self.params_row["A"])

    @property
    def Jy(self):
        return float(self.params_row["Jy"])

    @property
    def Ju(self):
        return float(self.params_row["Ju"])

    @property
    def Jv(self):
        return float(self.params_row["Jv"])

    @property
    def massa(self):
        return float(self.params_row["m"])

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return l * float(self.params_row["parea"])

    def get_free_length(self, lyamda=150):
        return self.iv * lyamda * 10

    @property
    def iv(self):
        return float(self.params_row["iv"])

    @property
    def iu(self):
        return float(self.params_row["iu"])

    @property
    def iy(self):
        return float(self.params_row["iy"])

    @property
    def y0(self):
        return float(self.params_row["y0"])


class AngleX(Angle):
    def __init__(self, sort_row):
        super().__init__(sort_row)

    def __str__(self):
        return "Кутик L{name} (хрест) \
                \nПлоща перерiзу {area} см^2 \
                \nПогонна вага {massa} кг/м \
                \nМомент iнерцiї Jy=Jz={Jy:.1f} см^4\
                \nМомент iнерцiї Jmin={Jv:.1f} см^4\
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм \
                \nКрок сухарiв (40i) {step:.0f} мм".format(
            name=self.params_row["name"],
            area=self.area,
            massa=self.massa,
            freelen=self.get_free_length(),
            step=self.step,
            Jy=self.Jy,
            Jv=self.Jv,
        )

    @property
    def massa(self):
        return super().massa * 2

    @property
    def area(self):
        return super().area * 2

    @property
    def Jy(self):
        _t = self.t / 10  # mm -> sm
        return (super().Jy + (super().y0 + 0.5 * _t) ** 2 * super().area) * 2

    @property
    def Jv(self):
        return super().Ju * 2

    @property
    def iv(self):
        return super().iu

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return super().get_paint_area(l) * 2

    def get_free_length(self, lyamda=150):
        """
        радiус iнерции iv хрестового переризу дорiвнює
        радiусу iнерцiї iv одного кутика
        """
        return self.iv * lyamda * 10  # sm -> mm

    @property
    def step(self):
        # згiдно ДБН для хрестових переризiв iv мiнiмальний
        return float(super().iy * i40 * 10)  # sm -> mm


class AngleT(Angle):
    def __init__(self, sort_row):
        super().__init__(sort_row)

    def __str__(self):
        return "Кутик L{0} (тавр) \
                \nПлоща перерiзу {1} см^2 \
                \nПогонна вага {2} кг/м \
                \nМомент iнерцiї Jz={6:.1f} см^4\
                \nМомент iнерцiї Jy_(min)={7:.1f} см^4\
                \nЦентр ваги x0=0; y0={3} см \
                \nРозрахункова длина (гнучкiсть=150) {4:.0f} мм \
                \nКрок сухарiв (40i) {5:.0f} мм".format(
            self.params_row["name"],
            self.area,
            self.massa,
            self.y0,
            self.get_free_length(),
            self.step,
            self.Jz,
            self.Jy,
        )

    @property
    def area(self):
        return super().area * 2

    @property
    def massa(self):
        return super().massa * 2

    @property
    def Jy(self):
        return super().Jy * 2

    @property
    def Jz(self):
        _t = self.t / 10  # mm -> sm
        return (super().Jy + (super().y0 + 0.5 * _t) ** 2 * super().area) * 2

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return super().get_paint_area(l) * 2

    def get_free_length(self, lyamda=150):
        return self.iy * lyamda * 10

    @property
    def iy(self):
        """
        радiус iнерции iv таврового переризу дорiвнює
        радiусу iнерцiї iv одного кутика
        """
        return float(self.params_row["iy"])

    @property
    def step(self):
        # згiдно ДБН для таврових переризiв iv у площинi сухарiв
        return float(super().iy * i40 * 10)  # sm -> mm


class AngleK(Angle):
    def __init__(self, sort_row):
        super().__init__(sort_row)

    def __str__(self):
        return "Кутик L{name} (короб) \
                \nПлоща перерiзу {area} см^2 \
                \nПогонна вага {massa} кг/м \
                \nМомент iнерцiї Jy=Jz={Jy:.0f} см\
                \nМомент iнерцiї Jv_(min)={Jv} см\
                \nРадiус iнерцiї iy={iy:.1f} см\
                \nРадiус iнерцiї i_min={iv} см\
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм".format(
            name=self.params_row["name"],
            Jy=self.Jy,
            Jv=self.Jv,
            iy=self.iy,
            iv=self.iv,
            area=self.area,
            massa=self.massa,
            freelen=self.get_free_length(),
        )

    @property
    def area(self):
        return super().area * 2

    @property
    def massa(self):
        return super().massa * 2

    @property
    def Jy(self):
        a = (super().B + super().t / 2) / 2 - super().y0 * 10
        return (super().Jy + super().area * a**2) * 2

    @property
    def Jv(self):
        return super().Ju * 2

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        # тiльки наружних граней
        return l * float(self.params_row["B"]) * 4 / 1000

    def get_free_length(self, lyamda=150):
        # минимальнiй радiус iнерцiї вiдносно вiсi, яка проходить скрiзь
        # внутришнiй кут кутика
        return self.iv * lyamda * 10

    @property
    def iy(self):
        return math.sqrt(self.Jy / self.area)

    @property
    def iv(self):
        return super().iu


class AngleSortament:
    def __init__(self):
        self.aparams = None

    def findbyname(self, atype):
        hasfind = False
        file = open(os.path.join(os.path.dirname(__file__), "angle.csv"))
        csvr = csv.DictReader(file, delimiter=";")

        for row in csvr:
            if row["name"] == atype:
                self.aparams = row
                hasfind = True
        file.close()
        return hasfind

    def getAngleParams(self):
        return self.aparams


def reply_to_message(msg):
    kind = None
    atype = re.search(r"(\d{2,3}\*\d{1,2})", msg)
    if atype:
        s = AngleSortament()
        if s.findbyname(atype.group(1)):
            kind = re.search(r"(тавр|хрест|короб)", msg)
            if kind:
                if kind.group(0) == "тавр":
                    ang = AngleT(s.getAngleParams())
                elif kind.group(0) == "хрест":
                    ang = AngleX(s.getAngleParams())
                elif kind.group(0) == "короб":
                    ang = AngleK(s.getAngleParams())
            else:
                ang = Angle(s.getAngleParams())

            answer = ang.__str__()

            ismass = re.search(r"(\d+(?:\.\d+)?)кг", msg)
            if ismass:
                m = float(ismass.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0:.1f}кг це {1:.1f}м профiлю\nПлоща фарбування {2:.1f} кв.м".format(
                        m,
                        ang.get_len_by_mass(m),
                        ang.get_paint_area(ang.get_len_by_mass(m)),
                    )
                )

            islen = re.search(r"(\d+(?:\.\d+)?)м", msg)
            if islen:
                l = float(islen.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0} це {1:.1f}кг профiлю\nПлоща фарбування {2:.1f} кв.м".format(
                        islen.group(0), ang.get_mass_by_len(l), ang.get_paint_area(l)
                    )
                )
        else:
            answer = "Нема такого..."
    elif msg.find("?") != -1:
        answer = HELPSTRING
    else:
        answer = (
            "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:"
            + "\n25*3, 25*4"
            + "\n30*3, 30*4"
            + "\n35*3, 35*4, 35*5"
            + "\n40*3, 40*4"
            + "\n45*4, 45*5"
            + "\n50*3, 50*4, 50*5"
            + "\n63*5, 63*6"
            + "\n75*5, 75*6, 75*8"
            + "\n90*6, 90*7, 90*8"
            + "\n100*7, 100*8, 100*10"
            + "\n125*8, 125*9, 125*10"
            + "\n140*9, 140*10"
            + "\n160*10, 160*12"
            + "\n200*12, 200*14"
        )

    if kind:
        if kind.group(0) == "хрест":
            picname = "angleX.png"
        elif kind.group(0) == "тавр":
            picname = "angleT.png"
        elif kind.group(0) == "короб":
            picname = "angleK.png"
    else:
        picname = "angle.png"

    return answer, os.path.join(os.path.dirname(__file__), picname)


if __name__ == "__main__":
    print(reply_to_message("кутик 90*7"))
