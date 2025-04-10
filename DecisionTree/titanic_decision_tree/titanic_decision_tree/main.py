# Titanic Passenger Decision Tree
# The assignment is to build and test a decision tree
#   using the included Titanic data set.
#
# Required librarys:
#  csv -- library to process CSV files. Libary is included in standard Python install
#  appJar -- GUI framework available through pip


from appJar import gui
import csv

from decision_tree import DecisionTree

# User interface for the application
class MainGui:

    def __init__(self):
        self.appGui = gui()
        self.dt = DecisionTree()


    # add & configure widgets
    def configure(self):
        self.appGui.addLabelFileEntry ("CSV File")
        #TODO: Add a button to test the decision tree
        self.appGui.addButtons(["Read File", "Build Decision Tree"], self.button_press)

    # configure window and start
    def start(self):
        self.configure()
        self.appGui.go()

    # event handler for button presses
    def button_press(self, button):
        if button == "Read File":
            self.read_file(self.appGui.getEntry("CSV File"))
            self.attributes = self.data[0].keys()

        # TODO: handle the other events
        elif button == "Build Decision Tree":
            print ("Building decision tree")


    # read the comma-separated data file and store the contents
    def read_file(self, fileName):
        self.data = []
        print ("Reading File" + fileName)
        with open(fileName) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print (row)
                # TODO: do something meaningful with the data


# Start the GUI if this is the main script
if __name__ == '__main__':
    app = MainGui()
    app.start()