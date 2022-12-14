# -------------------------------------------------------------------------------
# Name:        channels
# Purpose:
#
# Author:      klimvv
#
# Created:     02.06.2022
# Copyright:   (c) klimvv 2022
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import os, csv, re, math

lmbd = 150 / 1000
i40 = 40

HELPSTRING = "HLP<b>швелер [16] [двотавр|короб] [1кг] [10м]</b>\n(параметри в [...] необов'язковi)"


class Channel:
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Швелер {name} \
                \nПлоща перерiзу {area} см^2 \
                \nПогонна вага {masa} кг/м \
                \nМомент iнерцiї Jy={Jy} см^4\
                \nМомент iнерцiї Jz(min)={Jz} см^4\
                \nРадiус iнерцiї iy={iy} см\
                \nРадiус iнерцiї i_min={iz} см\
                \nЦентр ваги y0={y0} мм \
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм".format(
            name=self.params_row["name"],
            area=self.params_row["A"],
            masa=self.params_row["m"],
            Jy=self.params_row["Jy"],
            Jz=self.params_row["Jz"],
            iy=self.params_row["iy"],
            iz=self.params_row["iz"],
            y0=self.params_row["y0"],
            freelen=self.get_free_length(),
        )

    @property
    def massa(self):
        return float(self.params_row["m"])

    @property
    def b(self):
        return float(self.params_row["b"])
    
    @property
    def h(self):
        return float(self.params_row["h"])
    
    @property
    def s(self):
        return float(self.params_row["s"])

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

    @property
    def y0(self):
        return float(self.params_row["y0"])
    
    @property
    def parea(self):
        return float(self.params_row["parea"])

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return l * float(self.params_row["parea"])

    def get_free_length(self, lyamda=150):
        r = self.iz * lyamda * 10
        return r


class ChannelT(Channel):
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Швелер {name} (двотавр) \
                \nПлоща перерiзу {area} см^2 \
                \nПогонна вага {masa} кг/м \
                \nМомент iнерцiї Jy={Jy:.0f} см^4\
                \nМомент iнерцiї Jz(min)={Jz:.0f} см^4\
                \nРадiус iнерцiї iy={iy:.2f} см\
                \nРадiус iнерцiї i_min={iz:.2f} см\
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм \
                \nКрок сухарiв (40i) {step:.0f} мм".format(
            name=self.params_row["name"],
            area=self.area,
            masa=self.massa,
            Jy=self.Jy,
            Jz=self.Jz,
            iy=self.iy,
            iz=self.iz,
            freelen=self.get_free_length(),
            step=self.step,
        )

    @property
    def area(self):
        return super().area * 2

    @property
    def massa(self):
        return super().massa * 2

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        return l * super().parea * 2

    @property
    def Jy(self):
        return super().Jy * 2

    @property
    def Jz(self):
        a = (super().y0 + 1 * self.s / 2) / 10  # mm -> sm
        return (super().Jz + a**2 * super().area) * 2

    @property
    def iy(self):
        return super().iy

    @property
    def iz(self):
        return math.sqrt(self.Jz / self.area)

    @property
    def step(self):
        return super().iz * 40 * 10

    def get_free_length(self, lyamda=150):
        return self.iz * lyamda * 10


class ChannelK(Channel):
    def __init__(self, sort_row):
        self.params_row = sort_row

    def __str__(self):
        return "Швелер {name} (короб) \
                \nПлоща перерiзу {area} см^2 \
                \nПогонна вага {masa} кг/м \
                \nМомент iнерцiї Jy={Jy:.0f} см^4\
                \nМомент iнерцiї Jz(min)={Jz:.0f} см^4\
                \nРадiус iнерцiї iy={iy:.2f} см\
                \nРадiус iнерцiї i_min={iz:.2f} см\
                \nРозрахункова длина (гнучкiсть=150) {freelen:.0f} мм".format(
            name=self.params_row["name"],
            area=self.area,
            masa=self.massa,
            Jy=self.Jy,
            Jz=self.Jz,
            iy=self.iy,
            iz=self.iz,
            freelen=self.get_free_length(),
        )

    @property
    def area(self):
        return super().area * 2

    @property
    def massa(self):
        return super().massa * 2

    def get_mass_by_len(self, l):
        return l * self.massa

    def get_len_by_mass(self, m):
        return m / self.massa

    def get_paint_area(self, l):
        h = self.h / 1000
        b = self.b / 1000
        return l * (h + 2 * b) * 2

    @property
    def Jy(self):
        return super().Jy * 2

    @property
    def Jz(self):
        a = (self.b - self.y0) /10  # mm -> sm
        return (super().Jz + math.pow(a, 2) * super().area) * 2

    @property
    def iy(self):
        return super().iy

    @property
    def iz(self):
        return math.sqrt(self.Jz / self.area)

    def get_free_length(self, lyamda=150):
        return self.iz * lyamda * 10


class ChannelSortament:
    def __init__(self):
        self.cparams = None

    def findbyname(self, ctype):
        hasfind = False
        file = open(os.path.join(os.path.dirname(__file__), "channel.csv"))
        csvr = csv.DictReader(file, delimiter=";")

        for row in csvr:
            if row["name"].startswith(ctype):
                self.cparams = row
                hasfind = True
        file.close()
        return hasfind

    def getChannelParams(self):
        return self.cparams


def reply_to_message(msg):
    kind = None
    ctype = re.search(r"(\d+(?:\.\d+)?)", msg)
    if ctype:
        s = ChannelSortament()
        if s.findbyname(ctype.group(1)):
            kind = re.search(r"(двотавр|короб)", msg)
            if kind:
                if kind.group(0) == "двотавр":
                    ch = ChannelT(s.getChannelParams())
                elif kind.group(0) == "короб":
                    ch = ChannelK(s.getChannelParams())
            else:
                ch = Channel(s.getChannelParams())

            answer = ch.__str__()

            ismass = re.search(r"(\d+(?:\.\d+)?)кг", msg)
            if ismass:
                m = float(ismass.group(1))
                answer = (
                    answer
                    + "\n~~~\n{0:.1f}кг це {1:.1f}м профiлю\nПлоща фарбування {2:.1f} кв.м".format(
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
                    + "\n~~~\n{0} це {1:.1f}кг профiлю\nПлоща фарбування {2:.1f} кв.м".format(
                        islen.group(0), ch.get_mass_by_len(l), ch.get_paint_area(l)
                    )
                )
        else:
            answer = "Нема такого..."
    elif msg.find("?") != -1:
        answer = HELPSTRING
    else:
        answer = (
            "УЦСБ (https://uscc.ua/sortament-metaloprokaty) рекомендує:"
            + "\n6,5У, 8У, 10У"
            + "\n12У"
            + "\n14У, 16У, 18У"
            + "\n20У, 22У, 24У"
            + "\n27У, 30У"
            + "\n------"
        )
    if kind:
        if kind.group(0) == "двотавр":
            picname = "channelT.png"
        elif kind.group(0) == "короб":
            picname = "channelK.png"
    else:
        picname = "channel.png"

    return answer, os.path.join(os.path.dirname(__file__), picname)


if __name__ == "__main__":
    print(reply_to_message("швелер 20У короб"))
