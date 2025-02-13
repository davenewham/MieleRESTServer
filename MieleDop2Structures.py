class DOP2Annotator(dict):
    def __init__ (self, tree):
        self.tree=tree;
        super().__init__()
    def getAtIndex(self, i):
        return self.tree[i].value;
    def getStringAtIndex (self, i):
        return self.tree[i].value.decode(encoding='utf-8', errors='ignore').strip('\x00');
    def getWifiKeyAtIndex (self, i):
        return self.getStringAtIndex(i).replace('\x07', "*");
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

class DOP2SoftwareBuild (DOP2Annotator):
    def getLeaf():
        return [14, 6194];
    def readFields (self):
        self["date"]=self.getAtIndex(1);
        self["time"]=self.getAtIndex(2);
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
DOP2DeviceState,
DOP2SoftwareBuild,
DOP2XKMState,
DOP2XKMIdentLabel,
DOP2XKMConfigIP ]
