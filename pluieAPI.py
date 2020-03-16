# Object oriented implementation to permit third party apps
import signal

from PIL import Image, ImageDraw, ImageFont

pluieos_version = 10000 # pluieos 1.00.00

# Start Initialisation
width = 128
height = 64
image = Image.new('1', (width, height))


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

F1 = signal.SIGUSR1
F2 = signal.SIGUSR2
F3 = signal.SIGALRM

class View:
    sig = int
    font = ImageFont.load_default() # ImageFont.truetype('DejaVuSansMono.ttf', 8)
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
        self.draw(image)
        self.draw_view()
        image.save("./debug.png")
        while self.sig == int:
            "wait for action"

        if self.sig == F1:
            return 1
        elif self.sig == F2:
            return 2
        elif self.sig == F3:
            return 3

        return -1

    def draw(self, image):
        pass

    def draw_view(self):
        # Draw header bar
        w, h = draw.textsize(self.header, font=self.font)
        draw.rectangle((0, 0, 128, h), 255)
        # Draw header text
        draw.text(((width-w)/2, 0), self.header, 0, font=self.font)

        # Draw action box
        cellsize = int(width / 3)
        w, h = draw.textsize(self.action1, font=self.font)
        draw.line((0, height-h-2, width, height-h-2), 255)
        draw.line((cellsize, height - h - 2, cellsize, height), 255)
        draw.line((2 * cellsize, height - h - 2, 2 * cellsize, height), 255)

        # First action computing => F1 button
        while w > cellsize:

            self.action1 = self.action1[:-1]
            w, h = draw.textsize(self.action1 + "...", font=self.font)

            if w <= cellsize:
                self.action1 += "..."

        draw.text(((cellsize - w) / 2, height - h - 1), self.action1, 255, font=self.font)

        # Second action computing => F2 button
        w, h = draw.textsize(self.action2, font=self.font)
        draw.line((0, height - h - 2, width, height - h - 2), 255)

        while w > cellsize:
            self.action2 = self.action2[:-1]
            w, h = draw.textsize(self.action2 + "...", font=self.font)

            if w <= cellsize:
               self.action2 += "..."

        draw.text((((cellsize - w) / 2) + cellsize, height - h - 1), self.action2, 255, font=self.font)

        # Third action computing => F3 button
        w, h = draw.textsize(self.action3, font=self.font)
        draw.line((0, height - h - 2, width, height - h - 2), 255)

        while w > cellsize:
            self.action3 = self.action3[:-1]
            w, h = draw.textsize(self.action3 + "...", font=self.font)

            if w <= cellsize:
                self.action3 += "..."

        draw.text((((cellsize - w) / 2) + (2 * cellsize), height - h - 1), self.action3, 255, font=self.font)
        return


class Application():
    pluieos_version = 10000
    name = "ApplicationBase"
    def __init__(self):
        if pluieos_version > self.pluieos_version:
            print(self.name + " is made for an older version of pluieOS, use it at your own risks !")
        pass

    def run(self, app_path):
        pass

