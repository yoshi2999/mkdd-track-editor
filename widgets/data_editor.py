from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QComboBox, QSizePolicy
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from math import inf
from lib.libbol import (EnemyPoint, CheckpointGroup, Checkpoint, Route, RoutePoint,
                        MapObject, KartStartPoint, Area, Camera, BOL, JugemPoint, MapObject,
                        LightParam, MGEntry, OBJECTNAMES, REVERSEOBJECTNAMES, temp_add_invalid_id)

from PyQt5.QtCore import pyqtSignal


class DataEditor(QWidget):
    emit_3d_update = pyqtSignal()

    def __init__(self, parent, bound_to):
        super().__init__(parent)

        self.bound_to = bound_to
        self.vbox = QVBoxLayout(self)
        self.setLayout(self.vbox)

        self.description = self.add_label("Object")

        self.setup_widgets()

    def catch_text_update(self):
        self.emit_3d_update.emit()

    def setup_widgets(self):
        pass

    def update_data(self):
        pass

    def create_label(self, text):
        label = QLabel(self)
        label.setText(text)
        return label

    def add_label(self, text):
        label = self.create_label(text)
        self.vbox.addWidget(label)
        return label

    def create_labeled_widget(self, parent, text, widget):
        layout = QHBoxLayout(parent)
        label = self.create_label(text)
        label.setText(text)
        layout.addWidget(label)
        layout.addWidget(widget)
        return layout

    def create_labeled_widgets(self, parent, text, widgetlist):
        layout = QHBoxLayout(parent)
        label = self.create_label(text)
        label.setText(text)
        layout.addWidget(label)
        for widget in widgetlist:
            layout.addWidget(widget)
        return layout

    def add_checkbox(self, text, attribute, off_value, on_value):
        checkbox = QCheckBox(self)
        layout = self.create_labeled_widget(self, text, checkbox)

        def checked(state):
            if state == 0:
                setattr(self.bound_to, attribute, off_value)
            else:
                setattr(self.bound_to, attribute, on_value)

        checkbox.stateChanged.connect(checked)
        self.vbox.addLayout(layout)

        return checkbox

    def add_integer_input(self, text, attribute, min_val, max_val):
        line_edit = QLineEdit(self)
        layout = self.create_labeled_widget(self, text, line_edit)

        line_edit.setValidator(QIntValidator(min_val, max_val, self))

        def input_edited():
            text = line_edit.text()
            print("input:", text)

            setattr(self.bound_to, attribute, int(text))

        line_edit.editingFinished.connect(input_edited)

        self.vbox.addLayout(layout)

        return line_edit

    def add_integer_input_index(self, text, attribute, index, min_val, max_val):
        line_edit = QLineEdit(self)
        layout = self.create_labeled_widget(self, text, line_edit)

        line_edit.setValidator(QIntValidator(min_val, max_val, self))

        def input_edited():
            text = line_edit.text()
            print("input:", text)
            mainattr = getattr(self.bound_to, attribute)
            mainattr[index] = int(text)

        line_edit.editingFinished.connect(input_edited)
        label = layout.itemAt(0).widget()
        self.vbox.addLayout(layout)

        return label, line_edit

    def add_decimal_input(self, text, attribute, min_val, max_val):
        line_edit = QLineEdit(self)
        layout = self.create_labeled_widget(self, text, line_edit)

        line_edit.setValidator(QDoubleValidator(min_val, max_val, 6, self))

        def input_edited():
            text = line_edit.text()
            print("input:", text)

            setattr(self.bound_to, attribute, float(text))

        line_edit.editingFinished.connect(input_edited)

        self.vbox.addLayout(layout)

        return line_edit

    def add_text_input(self, text, attribute, maxlength):
        line_edit = QLineEdit(self)
        layout = self.create_labeled_widget(self, text, line_edit)

        line_edit.setMaxLength(maxlength)

        def input_edited():
            text = line_edit.text()
            text = text.rjust(maxlength)
            setattr(self.bound_to, attribute, text)

        line_edit.editingFinished.connect(input_edited)
        self.vbox.addLayout(layout)

        return line_edit

    def add_dropdown_input(self, text, attribute, keyval_dict):
        combobox = QComboBox(self)
        for val in keyval_dict:
            combobox.addItem(val)

        layout = self.create_labeled_widget(self, text, combobox)

        def item_selected(item):
            val = keyval_dict[item]
            print("selected", item)
            setattr(self.bound_to, attribute, val)

        combobox.currentTextChanged.connect(item_selected)
        self.vbox.addLayout(layout)

        return combobox

    def add_multiple_integer_input(self, text, attribute, subattributes, min_val, max_val):
        line_edits = []
        for subattr in subattributes:
            line_edit = QLineEdit(self)

            line_edit.setValidator(QIntValidator(min_val, max_val, self))

            input_edited = create_setter(line_edit, self.bound_to, attribute, subattr, isFloat=False)

            line_edit.editingFinished.connect(input_edited)
            line_edits.append(line_edit)

        layout = self.create_labeled_widgets(self, text, line_edits)
        self.vbox.addLayout(layout)


        return line_edits

    def add_multiple_decimal_input(self, text, attribute, subattributes, min_val, max_val):
        line_edits = []
        for subattr in subattributes:
            line_edit = QLineEdit(self)

            line_edit.setValidator(QDoubleValidator(min_val, max_val, 6, self))

            input_edited = create_setter(line_edit, self.bound_to, attribute, subattr, isFloat=True)
            line_edit.editingFinished.connect(input_edited)
            line_edits.append(line_edit)

        layout = self.create_labeled_widgets(self, text, line_edits)
        self.vbox.addLayout(layout)

        return line_edits

    def add_multiple_integer_input_list(self, text, attribute, min_val, max_val):
        line_edits = []
        fieldlist = getattr(self.bound_to, attribute)
        for i in range(len(fieldlist)):
            line_edit = QLineEdit(self)
            line_edit.setMaximumWidth(30)

            line_edit.setValidator(QIntValidator(min_val, max_val, self))

            input_edited = create_setter_list(line_edit, self.bound_to, attribute, i)
            line_edit.editingFinished.connect(input_edited)
            line_edits.append(line_edit)

        layout = self.create_labeled_widgets(self, text, line_edits)
        self.vbox.addLayout(layout)

        return line_edits

    def set_value(self, field, val):
        field.setText(str(val))


def create_setter_list(lineedit, bound_to, attribute, index):
    def input_edited():
        text = lineedit.text()
        mainattr = getattr(bound_to, attribute)
        mainattr[index] = int(text)

    return input_edited


def create_setter(lineedit, bound_to, attribute, subattr, isFloat):
    if isFloat:
        def input_edited():
            text = lineedit.text()
            mainattr = getattr(bound_to, attribute)

            setattr(mainattr, subattr, float(text))
        return input_edited
    else:
        def input_edited():
            text = lineedit.text()
            mainattr = getattr(bound_to, attribute)

            setattr(mainattr, subattr, int(text))

        return input_edited

MIN_SIGNED_BYTE = -128
MAX_SIGNED_BYTE = 127
MIN_SIGNED_SHORT = -2**15
MAX_SIGNED_SHORT = 2**15 - 1
MIN_SIGNED_INT = -2**31
MAX_SIGNED_INT = 2**31 - 1

MIN_UNSIGNED_BYTE = MIN_UNSIGNED_SHORT = MIN_UNSIGNED_INT = 0
MAX_UNSIGNED_BYTE = 255
MAX_UNSIGNED_SHORT = 2**16 - 1
MAX_UNSIGNED_INT = 2**32 - 1


def choose_data_editor(obj):
    if isinstance(obj, EnemyPoint):
        return EnemyPointEdit
    elif isinstance(obj, CheckpointGroup):
        return CheckpointGroupEdit
    elif isinstance(obj, MapObject):
        return ObjectEdit
    else:
        return None


class EnemyPointEdit(DataEditor):
    def setup_widgets(self, group_editable=False):
        self.position = self.add_multiple_decimal_input("Position", "position", ["x", "y", "z"],
                                                        -inf, +inf)
        self.pointsetting = self.add_integer_input("Point Setting", "pointsetting",
                                                    MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)
        self.link = self.add_integer_input("Link", "link",
                                           MIN_SIGNED_SHORT, MAX_SIGNED_SHORT)
        self.scale = self.add_decimal_input("Scale", "scale", -inf, inf)
        self.groupsetting = self.add_integer_input("Group Setting", "groupsetting",
                                                   MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)
        self.group = self.add_integer_input("Group", "group",
                                            MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        if not group_editable:
            self.group.setDisabled(True)

        self.pointsetting2 = self.add_integer_input("Point Setting 2", "pointsetting2",
                                                    MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk1 = self.add_integer_input("Unknown 1", "unk1",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk2 = self.add_integer_input("Unknown 2", "unk2",
                                           MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)

        for widget in self.position:
            widget.editingFinished.connect(self.catch_text_update)

    def update_data(self):
        obj: EnemyPoint = self.bound_to
        self.position[0].setText(str(round(obj.position.x, 3)))
        self.position[1].setText(str(round(obj.position.y, 3)))
        self.position[2].setText(str(round(obj.position.z, 3)))
        self.pointsetting.setText(str(obj.pointsetting))
        self.link.setText(str(obj.link))
        self.scale.setText(str(obj.scale))
        self.groupsetting.setText(str(obj.groupsetting))
        self.group.setText(str(obj.group))
        self.pointsetting2.setText(str(obj.pointsetting2))
        self.unk1.setText(str(obj.unk1))
        self.unk2.setText(str(obj.unk2))


class CheckpointGroupEdit(DataEditor):
    def setup_widgets(self):
        self.grouplink = self.add_integer_input("Group Link", "grouplink",
                                                MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)
        self.prevgroup = self.add_multiple_integer_input_list("Previous Groups", "prevgroup",
                                                              MIN_SIGNED_SHORT, MAX_SIGNED_SHORT)
        self.nextgroup = self.add_multiple_integer_input_list("Next Groups", "nextgroup",
                                                              MIN_SIGNED_SHORT, MAX_SIGNED_SHORT)

    def update_data(self):
        obj = self.bound_to
        self.grouplink.setText(str(obj.grouplink))
        for i, widget in enumerate(self.prevgroup):
            widget.setText(str(obj.prevgroup[i]))
        for i, widget in enumerate(self.nextgroup):
            widget.setText(str(obj.nextgroup[i]))


class CheckpointEdit(DataEditor):
    def setup_widgets(self):
        self.start = self.add_multiple_decimal_input("Start", "start", ["x", "y", "z"],
                                                        -inf, +inf)
        self.end = self.add_multiple_decimal_input("End", "end", ["x", "y", "z"],
                                                     -inf, +inf)

        self.unk1 = self.add_integer_input("Unknown 1", "unk1",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk2 = self.add_integer_input("Unknown 2", "unk2",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk3 = self.add_integer_input("Unknown 3", "unk3",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk4 = self.add_integer_input("Unknown 4", "unk4",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)

    def update_data(self):
        obj: Checkpoint = self.bound_to
        self.start[0].setText(str(round(obj.start.x, 3)))
        self.start[1].setText(str(round(obj.start.y, 3)))
        self.start[2].setText(str(round(obj.start.z, 3)))

        self.end[0].setText(str(round(obj.end.x, 3)))
        self.end[1].setText(str(round(obj.end.y, 3)))
        self.end[2].setText(str(round(obj.end.z, 3)))

        self.unk1.setText(str(obj.unk1))
        self.unk2.setText(str(obj.unk2))
        self.unk3.setText(str(obj.unk3))
        self.unk4.setText(str(obj.unk4))


class ObjectEdit(DataEditor):
    def setup_widgets(self):
        self.position = self.add_multiple_decimal_input("Position", "position", ["x", "y", "z"],
                                                        -inf, +inf)
        self.scale = self.add_multiple_decimal_input("Scale", "scale", ["x", "y", "z"],
                                                    -inf, +inf)
        self.objectid = self.add_dropdown_input("Object Type", "objectid", REVERSEOBJECTNAMES)

        self.pathid = self.add_integer_input("Path ID", "pathid",
                                             MIN_SIGNED_SHORT, MAX_SIGNED_SHORT)

        self.unk_28 = self.add_integer_input("Unknown 0x28", "unk_28",
                                             MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)

        self.unk_2a = self.add_integer_input("Unknown 0x2A", "unk_2a",
                                             MIN_UNSIGNED_SHORT, MAX_UNSIGNED_SHORT)
        self.presence_filter = self.add_integer_input("Presence Filter", "presence_filter",
                                                      MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.presence = self.add_integer_input("Presence", "presence",
                                               MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.flag = self.add_integer_input("Flag", "unk_flag",
                                           MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.unk_2f = self.add_integer_input("Unknown 0x2F", "unk_2f",
                                             MIN_UNSIGNED_BYTE, MAX_UNSIGNED_BYTE)
        self.userdata = []
        for i in range(8):
            self.userdata.append(
                self.add_integer_input_index("Obj Data {0}".format(i+1), "userdata", i,
                                             MIN_SIGNED_SHORT, MAX_SIGNED_SHORT)
            )

        self.objectid.currentTextChanged.connect(self.update_name)

        for widget in self.position:
            widget.editingFinished.connect(self.catch_text_update)

    def update_name(self):
        self.bound_to.widget.update_name()
        self.bound_to.widget.parent().sort()
        self.bound_to.widget.setSelected(True)

    def update_data(self):
        obj: MapObject = self.bound_to
        self.position[0].setText(str(round(obj.position.x, 3)))
        self.position[1].setText(str(round(obj.position.y, 3)))
        self.position[2].setText(str(round(obj.position.z, 3)))

        self.scale[0].setText(str(round(obj.scale.x, 3)))
        self.scale[1].setText(str(round(obj.scale.y, 3)))
        self.scale[2].setText(str(round(obj.scale.z, 3)))

        if obj.objectid not in OBJECTNAMES:
            name = "INVALID"
        else:
            name = OBJECTNAMES[obj.objectid]
        index = self.objectid.findText(name)
        self.objectid.setCurrentIndex(index)

        self.pathid.setText(str(obj.pathid))
        self.unk_28.setText(str(obj.unk_28))
        self.unk_2a.setText(str(obj.unk_2a))
        self.presence_filter.setText(str(obj.presence_filter))
        self.presence.setText(str(obj.presence))
        self.flag.setText(str(obj.unk_flag))
        for i in range(8):
            self.userdata[i][1].setText(str(obj.userdata[i]))
