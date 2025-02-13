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
    def getValueWithInterpretationAtIndex (self, i):
        [requestMask, value, valueInterpretation]=self.getStructAtIndex(i);
        return value.value;
    def getIpAtIndex(self, i):
#         return str(self.tree[i])
        tup=list(self.tree[i].value)
        if (len(tup)!=4):
            raise Exception("not an IP");
        return f"{tup[0]}.{tup[1]}.{tup[2]}.{tup[3]}"

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
DOP2ActuatorData,
DOP2SensorData,
DOP2ProcessData,
DOP2DeviceState,
DOP2SoftwareBuild,
DOP2XKMState,
DOP2XKMIdentLabel,
DOP2XKMConfigIP ]
