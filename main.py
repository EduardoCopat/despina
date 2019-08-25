import xmltodict
import simplejson as json
import os
from collections import OrderedDict

elements = []

class NeptuneElement:
    def __init__(self):
        self.id = None
        self.parent = None
        self.object = None
        self.attributes = []
        self.scripts = []
        self.events_scripts = []
        
    def to_json(self):
        json_object = self.object.copy()

        json_events = OrderedDict()
        currentEvent = None
        source_code = ""
        for event_script in events_scripts:
            event_name = event_script["EVENT"]
            if(event_name != currentEvent):
                currentEvent = event_name
                source_code = ""
            else:
                if(event_script["TEXT"] != None):
                    source_code = "\r\n" + source_code + event_script["TEXT"]
            json_events[event_name] = source_code.encode()

        json_object["Events_scripts"] = json_events
        json_object["Attributes"] = self._attributes_to_json()
        return json_object

    def _attributes_to_json(self):
        json_attributes = OrderedDict()

        for attribute in attributes:
            group = attribute["GROUPING"]
            
            groupAttributes = json_attributes.get(group)
            if(groupAttributes == None):
                json_attributes[str(group)] = OrderedDict() 
            
            json_attributes[str(group)][attribute["ATTRIBUTE"]] = attribute["VALUE"]

        return json_attributes


def findInElements(elements, id):
    for element in elements:
        if element.id == id:
            return element

file = open("ZEC_NAD_TRAINING03_VENDOR.xml", "r")
contents = file.read()

xml = xmltodict.parse(contents)

project = xml['asx:abap']['asx:values']['PROJECT']

objects = xml['asx:abap']['asx:values']['PROJECT']['IT_CONTENT']['_-NEPTUNE_-_OBJ']

objects = xml['asx:abap']['asx:values']['PROJECT']['IT_CONTENT']['_-NEPTUNE_-_OBJ']

attributes = xml['asx:abap']['asx:values']['PROJECT']['IT_ATTRIBUTES']['_-NEPTUNE_-_OBJ_AT']

scripts = xml['asx:abap']['asx:values']['PROJECT']['IT_SCRIPT']['_-NEPTUNE_-_SCRIPT']

events_scripts = xml['asx:abap']['asx:values']['PROJECT']['IT_EVENT_SCRIPT']['_-NEPTUNE_-_EVTSCR']

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

currentElement = None
for script in scripts:
    if(currentElement == None or currentElement.id != script["FIELD_ID"]):
        currentElement = findInElements(elements, script["FIELD_ID"])
    currentElement.scripts.append(script)    

currentElement = None
for script in events_scripts:
    if(currentElement == None or currentElement.id != script["FIELD_ID"]):
        currentElement = findInElements(elements, script["FIELD_ID"])
    currentElement.events_scripts.append(script)        

    
def writeFile(file_name, element):
    jsonFile = open(file_name + ".json","w+", encoding="utf-8")
    foo = element.to_json()
    asd =  "\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nosDetailOnline.setVisible(true);// Update DataModelData.Update(MasterLFA1,\"LIFNR\",modeloPageDetail.oData.LIFNR,modelDeltaLFA1.oData[0]);ModelData.Update(MasterADRC,\"ADDRNUMBER\",modeloPageDetail.oData.ADRNR,modelDeltaADRC.oData[0]);ModelData.Update(MasterLFM1,\"LIFNR\",modeloPageDetail.oData.LIFNR,modelDeltaLFM1.oData[0]);ModelData.Update(MasterBank,\"LIFNR\",modeloPageDetail.oData.LIFNR,modelDeltaBank.oData);// Set Customer DatasetDataVendor(modeloPageDetail.oData);// Save DatasetCacheMasterLFA1();setCacheMasterADRC();setCacheMasterLFM1();setCacheMasterBank();oApp.setBusy(false);".encode()
    json.dump(foo, jsonFile, sort_keys=True, indent=4, ensure_ascii=False)
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
