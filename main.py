import xmltodict
import json

elements = []

class NeptuneElement:
  def __init__(self):
    self.id = None
    self.parent = None
    self.object = None
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
    elements.append(element)

currentElement = None
for attribute in attributes:
    if(currentElement == None or currentElement.id != attribute["FIELD_ID"]):
        currentElement = findInElements(elements, attribute["FIELD_ID"])
    currentElement.attributes.append(attribute)



    

nep = NeptuneElement()
nep.id = "00080"



jsonFile = open("a.json","w+")
for element in elements:
    jsonFile.write(json.dumps(element.object))

jsonFile.close()

