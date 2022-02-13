import sys, os, PyQt5.QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMenu, QMessageBox

from wrapperdialog import *

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.app = app

        self.ui.AddResamplerButton.clicked.connect(self.browseResampler)
        self.ui.RemoveResamplerButton.clicked.connect(self.removeSelection)
        self.ui.WrapButton.clicked.connect(self.wrapResamplers)
        self.ui.ExitButton.clicked.connect(self.exitProgram)

    def browseResampler(self):
        files,_ = QFileDialog.getOpenFileNames(self, "Select resampler...", "", "EXE files (*.exe)", options=QFileDialog.Options())
        if files:
            for f in files:
                newResampler = QtWidgets.QListWidgetItem()
                newResampler.setText(str(f))
                self.ui.ResamplerList.addItem(newResampler)
        return

    def removeSelection(self):
        for i in self.ui.ResamplerList.selectedItems():
            self.ui.ResamplerList.takeItem(self.ui.ResamplerList.row(i))
        return

    def wrapResamplers(self):
        for i in range (self.ui.ResamplerList.count()):
            resampler = self.ui.ResamplerList.item(i).text()
            wrappedDir = os.path.join(os.path.dirname(resampler), "Wrapper")
            if not os.path.exists(wrappedDir):
                os.mkdir(wrappedDir)
            os.rename(resampler, os.path.join(wrappedDir, os.path.basename(resampler)))
            with open(os.path.splitext(resampler)[0], 'w') as f:
                f.write("#!/bin/bash\nme=`basename \"$0\"`\ndr=`dirname \"$0\"`\nwine \"$dr/Wrapper/$me.exe\" \"$@\"")
            os.chmod(os.path.splitext(resampler)[0], 0o755)
        QMessageBox.about(self, "Job completed", "All resamplers have been wrapped.")
        self.ui.ResamplerList.clear()
        return

    def exitProgram(self):
        exit()
        return

def main():
    app = QApplication(sys.argv)
    w = MainWindow(app)
    w.show()
    t = QtCore.QTimer()
    #t.singleShot(0,w.applicationStarted)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()