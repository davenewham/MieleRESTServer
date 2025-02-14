from binascii import hexlify

class DOP2Annotator(dict):
    def __init__ (self, tree):
        self.tree=tree;
        super().__init__()
    def getAtIndex(self, i):
        return str(self.tree[i].value);
    def getArrayToStrAtIndex (self, i):
        return str([str(x.value) for x in self.tree[i].value])
    def getStringAtIndex (self, i):
        return self.tree[i].value.decode(encoding='utf-8', errors='ignore').strip('\x00');
    def getWifiKeyAtIndex (self, i):
        return self.getStringAtIndex(i).replace('\x07', "*");
    def getStructAtIndex (self, i):
        return self.tree[i].value;
    def getBoolAtIndex( self, i):
        return self.tree[i].value;
    def getEnumAtIndex (self, i):
        return self.tree[i].value;
    def getValueWithInterpretationAtIndex (self, i):
        [requestMask, value, valueInterpretation]=self.getStructAtIndex(i);
        return value.value;
    def getBytesAtIndex (self, i):
        return str(hexlify(self.tree[i].value, " "));
    def getIpAtIndex(self, i):
#         return str(self.tree[i])
        tup=list(self.tree[i].value)
        if (len(tup)!=4):
            raise Exception("not an IP");
        return f"{tup[0]}.{tup[1]}.{tup[2]}.{tup[3]}"
#actuatorstate is 20 bools, 0x14 0x00 0x00...
class DOP2LastUpdateInfo (DOP2Annotator):
    def getLeaf():
        return [15, 199];
    def readFields(self):
        self["filename"]=self.getStringAtIndex(1);

class DOP2UpdateControl (DOP2Annotator): #FTUpdateControl
    def getLeaf():
        return [15, 170];
    def readFields(self):
        self["updateState"]=self.getEnumAtIndex(1);
        self["filename"]=self.getStringAtIndex(2);
        self["flashAccessible"]=self.getAtIndex(3);
        self["progress"]=self.getAtIndex(4);

class DOP2FileInfo (DOP2Annotator): #FTFileInfo
    def getLeaf():
        return [15, 1588];
    def readFields(self):
        self["fileName"]=self.getStringAtIndex(1);
        self["sha256"]=self.getBytesAtIndex(2);
        self["currentSize"]=self.getAtIndex(3);
        self["maxSize"]=self.getAtIndex(4);
        self["crc32"]=self.getAtIndex(5);

class DOP2RSAPublicKey (DOP2Annotator):
    def getLeaf():
        return [15, 287];
    def readFields(self):
        self["rsaPublicKey"]=self.getBytesAtIndex(1);

class DOP2DeviceCombinedState (DOP2Annotator): #TBD -- deviceCombiState
    def getLeaf():
        return [2,1586];
    def readFields(self):
        self["applianceState"]=self.getAtIndex(1);
        self["operationState"]=self.getAtIndex(2);
        self["processState"]=self.getAtIndex(3);

class DOP2CS_DeviceContext (DOP2Annotator): #TBD
    def getLeaf():
        return [999,999];

class DOP2DeviceContext (DOP2Annotator): #GLOBAL_DeviceContext -- not sure yet
    def getLeaf():
        return [2,1585];
    def readFields(self):
        self["deviceCombinedState"]=self.getAtIndex(1);
        self["progAttributes"]=self.getAtIndex(2);
        self["deviceAttributes"]=self.getAtIndex(3);
        self["sessionOwnerEnum"]=self.getAtIndex(10);
        self["mobileStartActive"]=self.getBoolAtIndex(11);
#        self["requestTimeSync"]=self.getBoolAtIndex(13);
class DOP2OperationCycleCounter (DOP2Annotator): # CS_OperationCycleCounter (this shares a signature with "OperationRuntimeCounter)
    def getLeaf():
        return [2, 138]
    def readFields(self):
        self["counterId"]=self.getAtIndex(1);
        self["counterValue"]=self.getAtIndex(2);
class DOP2HoursOfOperation (DOP2Annotator): #CS_HoursOfOperation
    def getLeaf():
        return [2, 119];
    def readFields(self):
        prefix="hoursOfOperation";
        for count, x in enumerate(["", "BeforeReplacement", "SinceLastMaintenance", "Mode1", "Mode2"],start=1):
            self[prefix+x]=self.getAtIndex(count);
class DOP2PartName (DOP2Annotator): #CS_Barcode
    def getLeaf():
        return [2, 173];
    def readFields(self):
        self["partName"]=self.getStringAtIndex(1);
        self["code"]=self.getStringAtIndex(2);

class DOP2DateOfTest (DOP2Annotator): #CS_DateOfTest
    def getLeaf():
        return [2, 174];
    def readFields(self):
        self["partName"]=self.getStringAtIndex(1);
        self["dateOfTest"]=self.getStringAtIndex(2);

class DOP2SuperVisionListConfig (DOP2Annotator): #SV_ListConfig
    def getLeaf():
        return [14, 1570]
    def readFields(self):
        self["isSuperVisionActive"]=self.getBoolAtIndex(1);
        self["isSuperVisionOnErrorOnly"]=self.getBoolAtIndex(2);
        self["isTimeMaster"]=self.getBoolAtIndex(3);
        self["listSize"]=self.getAtIndex(4);
        self["deviceIdSort"]=self.getAtIndex(5);
        self["deviceIdSortSv"]=self.getAtIndex(6);
        
class DOP2SuperVisionListItem (DOP2Annotator): #SV_ListItem
    def getLeaf():
        return [14, 1571]
    def readFields (self):
        self["deviceId"]=self.getAtIndex(1);
        self["deviceIdEnum"]=self.getAtIndex(2)
        self["deviceName"]=self.getStringAtIndex(3);
        self["connectionState"]=self.getAtIndex(4);
        self["displaySetting"]=self.getBoolAtIndex (5);
        self["signalSetting"]=self.getBoolAtIndex (6);
        self["superVisionActivate"]=self.getBoolAtIndex (7);
        self["superVisionDisplayScreenEnum"]=self.getEnumAtIndex (8);
        self["superVisionDisplayTextEnum"]=self.getEnumAtIndex (9);
        self["longAddress"]=self.getStringAtIndex(17);
        self["programId"]=self.getAtIndex(24);
class DOP2DeviceState (DOP2Annotator):
    def getLeaf():
        return [2, 256];
    def readFields (self):
        self["mainState"]=self.getAtIndex(1)
        self["remoteEnable"]=self.getAtIndex(2)
        self["programType"]=self.getAtIndex(3);
        self["programId"]=self.getAtIndex(4);
        self["programPhase"]=self.getAtIndex(5);
        self["startTimeRelative"]=self.getAtIndex(6);
        self["remainingTime"]=self.getAtIndex(7);
        self["elapsedTimeRelative"]=self.getAtIndex(8);
        self["processTemperatureSet"]=self.getArrayToStrAtIndex(9);
        self["processTemperatureCurrent"]=self.getArrayToStrAtIndex(10);
        self["coreTemperatureSet"]=self.getArrayToStrAtIndex(11);
        self["coreTemperatureCurrent"]=self.getArrayToStrAtIndex(12);
        self["signalDoor"]=self.getAtIndex(13);
        self["signalInfo"]=self.getAtIndex(14);
        self["spinningSpeed"]=self.getAtIndex(15);
        self["dryingStep"]=self.getAtIndex(16);
        self["lightState"]=self.getAtIndex(17);
        self["standbyState"]=self.getAtIndex(18);

class DOP2ProcessData (DOP2Annotator):
    def getLeaf():
        return [2, 6195];
    def readFields(self):
        self["remainingTimeInMinutes"]=self.getValueWithInterpretationAtIndex(4); #progPhase
        self["programPhase"]=self.getValueWithInterpretationAtIndex(5); #progPhase
        self["heaterRelay"]=self.getValueWithInterpretationAtIndex(8); #heizunsrelais
        self["lyePump"]=self.getValueWithInterpretationAtIndex(9); #laugenpumpe
        self["ciculationPump"]=self.getValueWithInterpretationAtIndex(10); #laugenpumpe
        self["coldWaterValve"]=self.getValueWithInterpretationAtIndex(11); #ventilKW
        self["hotWaterValve"]=self.getValueWithInterpretationAtIndex(12); #ventilKW
        self["fuTemperature"]=self.getValueWithInterpretationAtIndex(15); #wasserverbrauchInLiter
        self["energyConsumed"]=self.getValueWithInterpretationAtIndex(16); #wasserverbrauchInLiter
        self["waterConsumedInLitres"]=self.getValueWithInterpretationAtIndex(17); #wasserverbrauchInLiter
        self["rpmCurrent"]=self.getValueWithInterpretationAtIndex(27); #wasserverbrauchInLiter


class DOP2ActuatorData (DOP2Annotator): #CDV_ActuatorData
    def getLeaf():
        return [2, 6192];
    def readFields(self):
        fields=["heater1", "lyePump", "intensiveFlowPump", "valve1", "valve2", "waterDistributorMotor", "heater2",
        "twinDosPump1", "twinDosPump2", "steamHeater", "steamPump", "dosRel1", "dosRel2", "dosRel3",
        "dosRel4", "dosRel5", "dosRel6", "actCoinerEnd", "actCoinerOperation", "sensPeakLoad"]
        for count, x in enumerate(fields, start=1):
            self[x]=self.getValueWithInterpretationAtIndex(count);
class DOP2SensorData (DOP2Annotator): #CDV_SensorData
    def getLeaf():
        return [2, 6193];
    def readFields(self):
        self["waterLevel"]=self.getValueWithInterpretationAtIndex(1);
        self["waterInletWay"]=self.getValueWithInterpretationAtIndex(2);
        self["spinSpeed"]=self.getValueWithInterpretationAtIndex(3);
        self["doorSwitch"]=self.getValueWithInterpretationAtIndex(4);
        self["doorLockSwitch"]=self.getValueWithInterpretationAtIndex(5);
        self["wpsSwitch"]=self.getValueWithInterpretationAtIndex(6);
        self["twinDosSwitchContainer1"]=self.getValueWithInterpretationAtIndex(7);
        self["twinDosSwitchContainer2"]=self.getValueWithInterpretationAtIndex(8);
        self["ntcTemperature1"]=self.getValueWithInterpretationAtIndex(9);
        self["ntcTemperature2"]=self.getValueWithInterpretationAtIndex(10);
        self["lanceContact"]=self.getValueWithInterpretationAtIndex(11);
        self["peakLoadSignal"]=self.getValueWithInterpretationAtIndex(12);
        self["detectedCap"]=self.getValueWithInterpretationAtIndex(13);
        self["dispenserDrawerSwitch"]=self.getValueWithInterpretationAtIndex(14);
        self["steamUnitTemperature"]=self.getValueWithInterpretationAtIndex(15);
        self["sensCoinerPayment"]=self.getValueWithInterpretationAtIndex(16);

class DOP2XKMConfigSSIDList (DOP2Annotator):
    def getLeaf ():
        return [14,110]
    def readFields(self):
        self["ssid"]=self.getStringAtIndex(1);
        self["wlanSecurity"]=self.getAtIndex(2);
        self["rssi"]=self.getAtIndex(3);
        self["wifiChannel"]=self.getAtIndex(4);
class DOP2SoftwareBuild (DOP2Annotator): #CDV_SoftwareBuild
    def getLeaf():
        return [2, 6194];
    def readFields (self):
        self["date"]=self.getStringAtIndex(1);
        self["time"]=self.getStringAtIndex(2);
        self["id"] = self.getAtIndex(3);
        self["version"]=self.getAtIndex(4);

class DOP2XKMState (DOP2Annotator):
    def getLeaf():
        return [14, 1568];
    def readFields (self):
        self["state"]=self.getAtIndex(1);
        self["signalQuality"]=self.getAtIndex(2);

class DOP2XKMIdentLabel (DOP2Annotator):
    def getLeaf():
        return [14, 1566]
    def readFields (self):
        self["serialNumber"]=self.getStringAtIndex(1);
        self["fabricationNumber"]=self.getStringAtIndex(2);
        self["technicalType"]=self.getStringAtIndex(3);
        self["materialNumber"]=self.getStringAtIndex(4);

class DOP2XKMConfigIP (DOP2Annotator):
    def getLeaf():
        return [14, 1573]
    def readFields (self):
        self["ipAuto"]=self.getAtIndex(1);
        self["ipAddress"]=self.getIpAtIndex(2);
        self["subnetMask"]=self.getIpAtIndex(3);
        self["gatewayAddress"]=self.getIpAtIndex(4);
        self["dnsServerAuto"]=self.getAtIndex(5);
        self["dnsServer1"]=self.getIpAtIndex(6);
        self["dnsServer2"]=self.getIpAtIndex(7);
        self["wifiKey"]=self.getWifiKeyAtIndex(8);
        self["wifiSSID"]=self.getAtIndex(9);
        self["wifiSecurityType"]=self.getAtIndex(10);
        self["wifiChannel"]=self.getAtIndex(11);

DOP2Annotators = [
DOP2LastUpdateInfo,
DOP2UpdateControl,
DOP2FileInfo,
DOP2RSAPublicKey,
DOP2PartName,
DOP2DateOfTest,
DOP2SuperVisionListItem,
DOP2SuperVisionListConfig,
DOP2ActuatorData,
DOP2SensorData,
DOP2ProcessData,
DOP2DeviceState,
DOP2SoftwareBuild,
DOP2XKMState,
DOP2XKMIdentLabel,
DOP2XKMConfigSSIDList,
DOP2XKMConfigIP ]
