import xmltodict
import json
import os


elements = []

class NeptuneElement:
  def __init__(self):
    self.id = None
    self.parent = None
    self.object = None
    self.isContainer = False
    self.attributes = []

def findInElements(elements, id):
    for element in elements:
        if element.id == id:
            return element

print("This line will be printed.")

file = open("ZEC_NAD_TRAINING03_VENDOR.xml", "r")
contents = file.read()

xml = xmltodict.parse(contents)

project = xml['asx:abap']['asx:values']['PROJECT']

objects = xml['asx:abap']['asx:values']['PROJECT']['IT_CONTENT']['_-NEPTUNE_-_OBJ']

objects = xml['asx:abap']['asx:values']['PROJECT']['IT_CONTENT']['_-NEPTUNE_-_OBJ']

attributes = xml['asx:abap']['asx:values']['PROJECT']['IT_ATTRIBUTES']['_-NEPTUNE_-_OBJ_AT']

for object in objects:
    element = NeptuneElement()
    element.id = object["FIELD_ID"]
    element.parent = object["FIELD_PARENT"]
    element.object = object
    if(element.object["IS_CONTAINER"] == "X"):
        element.isContainer == True
    elements.append(element)

currentElement = None
for attribute in attributes:
    if(currentElement == None or currentElement.id != attribute["FIELD_ID"]):
        currentElement = findInElements(elements, attribute["FIELD_ID"])
    currentElement.attributes.append(attribute)

    
def writeFile(file_name, element):
    jsonFile = open(file_name + ".json","w+")
    jsonFile.write(json.dumps(element.object, sort_keys=True, indent=4))
    jsonFile.close()

def createFile(path, element):
    field_name = element.object["FIELD_NAME"]
   
    container_path = path + "\\" + field_name
    os.mkdir(container_path)
    writeFile(container_path + "\\" + field_name, element)
    for child in elements:
        if element.id == child.parent:
            createFile(container_path, child)



# define the name of the directory to be created
path = os.getcwd() + "\\output"


try:
    os.mkdir(path)
    for root in elements:
        if(root.parent == "00000"):
            createFile(path, root)
except OSError:
    print ("Creation of the directory %s failed" % path)
