#-- include('examples/showgrabfullscreen.py') --#
import pyscreenshot as ImageGrab


if __name__ == "__main__":
    # fullscreen
    im=ImageGrab.grab()
    im.save("/home/edx/1.jpg")
#-#
