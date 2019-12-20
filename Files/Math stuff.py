import json
import math
# for working out... not finished
#https://michaelreeves.us/pages/LaserSystem.html == documentation
#
settings = {"xShift":0,"yShift":1,"xLeftCalibration":59,"xRightCalibration":120,"yTopCalibration":116,"yBotCalibration":70}#calibration settings used in |
settings1 = json.loads(settings)

w = width
h = height

xDivConst = w / settings1["xRightCalibration"] - settings1["xLeftCalibration]"]
yDivConst = h / settings1["yTopCalibration"] - settings1["yBotCalibration"]

serialPort1.Write("X" + str(90 + settings.xShift) + ":Y" + str(90 + settings.yShift))

return new Point(((int)(settings.xRightCalibration - (point.X / xScaleConst)), int(settings.yTopCalibration) - (point.Y / yScaleConst))))
#                         120 - x /
#i have no idea what the line above means

    xScaleConst = (captureFrameWidth) / (settings.xRightCalibration - settings.xLeftCalibration);
    yScaleConst = (captureFrameHeight) / (settings.yTopCalibration - settings.yBotCalibration);
}

# tl:dr math is hard