from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt


class BellWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BellWidget, self).__init__(parent=parent)
        self.widget_layout = QtWidgets.QVBoxLayout(self)

        self.n_notifications = 0

        self.icon_frame = QtWidgets.QFrame(self)
        self.max_width = self.min_width = self.max_height = self.min_height = 75
        self.icon_frame.setMinimumSize(QtCore.QSize(self.min_width, self.min_height))
        self.icon_frame.setMaximumSize(QtCore.QSize(self.max_width, self.max_height))

        self.widget_layout.addWidget(self.icon_frame)

    @staticmethod
    def new_rect(from_rect: QtCore.QRect, topLeft_dx: int = 0, topLeft_dy: int = 0, w: int = 0, h: int = 0):
        _x = from_rect.topLeft().x() + int(topLeft_dx)
        _y = from_rect.topLeft().y() + int(topLeft_dy)

        _w = from_rect.width() + w
        _h = from_rect.height() + h
        return QtCore.QRect(_x, _y, _w, _h)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter()
        painter.begin(self)

        top_right = self.icon_frame.geometry().topRight()
        top_left = self.icon_frame.geometry().topLeft()
        bottom_right = self.icon_frame.geometry().bottomRight()

        adjustment = int(self.max_width * 0.2)  # 20% adjustment for notification count
        # --------- rect to hold image --------------------------
        image_rect = self.new_rect(QtCore.QRect(top_left, bottom_right), 0, 0, -adjustment, -adjustment)

        # --------- top-left position to write the text ----------
        text_top_ = top_right.y() + int(adjustment * 1.5)
        text_left_ = top_right.x() - int(adjustment * 2.2)
        text_top_left = QtCore.QPoint(text_left_, text_top_)

        # --------- create pen for font-color --------------------
        pen = QtGui.QPen()
        pen.setColor(Qt.white)  # red pen color
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)

        # -------------- font-size customizations for fitting "+" sign --------------
        font_size = 8  # default font-size
        if self.n_notifications >= 10:
            font_size -= 1
        if self.n_notifications >= 99:
            font_size -= 1

        # ------------ custom font for notification text ----------------------------
        notification_count_font = QtGui.QFont("sans-serif", font_size, 75)
        notification_count_font.setStyleHint(QtGui.QFont.SansSerif, QtGui.QFont.PreferAntialias)
        painter.setFont(notification_count_font)

        if self.n_notifications > 99:  # for more than 99 notifications, it'll show 99+ as notifications count
            notification_count_string = r"99+"
        else:
            notification_count_string = str(self.n_notifications)

        if self.n_notifications > 0:
            image_path = "./images/notif_bell.png"  # for +1 notifications
        else:
            image_path = "./images/no_notif_bell.png"  # for no notifications
        painter.drawImage(image_rect, QtGui.QImage(image_path))  # for 1+ notifications
        if self.n_notifications > 0:  # draw text iff notifications are more than 0
            painter.drawText(text_top_left, notification_count_string)  # show the notification string

        super(BellWidget, self).paintEvent(event)
        painter.end()

    def add_notification(self):
        self.n_notifications += 1

    def remove_notification(self):
        if self.n_notifications >= 0:
            self.n_notifications -= 1

    def wheelEvent(self, wheel_event: QtGui.QWheelEvent) -> None:
        dy = wheel_event.angleDelta().y()
        if 0 < self.n_notifications or (0 < dy):
            self.n_notifications += dy // 120
        super(BellWidget, self).wheelEvent(wheel_event)
        self.update()  # need to trigger paintEvent
