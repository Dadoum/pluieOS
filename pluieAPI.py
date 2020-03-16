# Object oriented implementation to permit third party apps
import posix
import signal
import os

from PIL import Image, ImageDraw, ImageFont

pluieos_version = 10000 # pluieos 1.00.00

# Start Initialisation
width = 128
height = 64
image = Image.new('1', (width, height))


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw.font = ImageFont.truetype('DejaVuSansMono.ttf', 9)# ImageFont.load_default()
F1 = signal.SIGUSR1
F2 = signal.SIGUSR2
F3 = signal.SIGALRM

class View:
    sig = int
    def __init__(self, header, action1, action2, action3):
        self.header = str(header)
        self.action1 = str(action1)
        self.action2 = str(action2)
        self.action3 = str(action3)
        return

    def receive_signal(self, signum, stack):
        self.sig = signum

    def reset(self):
        self.sig = int

    def run(self):
        if self.sig != int:
            self.reset()
        signal.signal(signal.SIGUSR1, self.receive_signal)
        signal.signal(signal.SIGUSR2, self.receive_signal)
        signal.signal(signal.SIGALRM, self.receive_signal)

        draw.rectangle((0, 0, width, height), 0)
        self.draw(draw)
        self.draw_view()

        if os.uname().machine == "x86_64":
            image.save("./debug.png")

        if self.action1 == "" and self.action2 == "" and self.action3 == "":
            self.run_view()
            return 0

        while self.sig == int:
            "wait for action"

        if self.sig == F1:
            return 1
        elif self.sig == F2:
            return 2
        elif self.sig == F3:
            return 3

        return -1

    def run_view(self):
        pass

    def draw(self, image):
        pass

    def draw_view(self):
        # Draw header bar
        w, h = draw.textsize(self.header)
        draw.rectangle((0, 0, 128, h), 255)
        # Draw header text
        draw.text(((width-w)/2, 0), self.header, 0)

        if self.action1 == "" and self.action2 == "" and self.action3 == "":
            print(self.__class__.__name__ + " is an expanding view. No actions will be drawn.")
            return

        # Draw action box
        cellsize = int(width / 3)
        w, h = draw.textsize(self.action1)
        draw.line((0, height-h-2, width, height-h-2), 255)
        draw.line((cellsize, height - h - 2, cellsize, height), 255)
        draw.line((2 * cellsize, height - h - 2, 2 * cellsize, height), 255)

        # First action computing => F1 button
        while w > cellsize:

            self.action1 = self.action1[:-1]
            w, h = draw.textsize(self.action1 + "...")

            if w <= cellsize:
                self.action1 += "..."

        draw.text(((cellsize - w) / 2, height - h - 1), self.action1, 255)

        # Second action computing => F2 button
        w, h = draw.textsize(self.action2)
        draw.line((0, height - h - 2, width, height - h - 2), 255)

        while w > cellsize:
            self.action2 = self.action2[:-1]
            w, h = draw.textsize(self.action2 + "...")

            if w <= cellsize:
               self.action2 += "..."

        draw.text((((cellsize - w) / 2) + cellsize, height - h - 1), self.action2, 255)

        # Third action computing => F3 button
        w, h = draw.textsize(self.action3)
        draw.line((0, height - h - 2, width, height - h - 2), 255)

        while w > cellsize:
            self.action3 = self.action3[:-1]
            w, h = draw.textsize(self.action3 + "...")

            if w <= cellsize:
                self.action3 += "..."

        draw.text((((cellsize - w) / 2) + (2 * cellsize), height - h - 1), self.action3, 255)
        return


class Application():
    pluieos_version = 10000
    def __init__(self):
        if pluieos_version > self.pluieos_version:
            print(self.__class__.__name__ + " is made for an older version of pluieOS, use it at your own risks !")
        pass

    def run(self, app_path):
        pass

