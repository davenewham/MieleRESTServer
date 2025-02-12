from enum import Enum

class MieleIntegerFormat(str, Enum):
    Unsigned="U",
    Signed="S",
    E="E"

class MieleAttribute:
    def __init__ (wireLength, typeName, value):
        self.wireLength = wireLength;
        self.typeName = typeName;
        self.value = value;

class MieleAttributeDecoder:
    def __init__ (self, byteLength, typeName):
        self.byteLength=byteLength;
        self.typeName=typeName;
    def __str__ (self):
        return self.typeName;

class MieleFixedLengthAttributeDecoder (MieleAttributeDecoder):
    def __init__ (self, byteLength, typeName):
        super().__init__(byteLength, typeName);
    
    def decode (payload):
        return MieleAttribute (self.byteLength, 
        self.typeName,
        self.fixed_length_decode (payload[0:self.byteLength]));

class MieleVariableLengthAttributeDecoder (MieleAttributeDecoder):
    def __init__ (self, typeName):
        super().__init__(0, typeName);
    

class MieleBool(MieleAttributeDecoder):
    def __init__ (self):
        super().__init__(1, "bool")
    def fixed_length_decode (payload):
        if (payload == 0x01:
            return True;
        if (payload==0x00):
            return False;
        raise Exception("DOP2 Decode Error -- Boolean not 0x01 or 0x00");

class MieleInteger (MieleAttributeDecoder):
    def __init__ (self, byteLength, integerFormat):
        super().__init__(byteLength, f"{integerFormat}{byteLength*8}")

class MieleFloat (MieleAttributeDecoder):
     def __init__ (self, byteLength):
        super().__init__(byteLength, f"float{byteLength*8}")

class MieleArray (MieleAttributeDecoder):
    def __init__ (self, elementDecoder):
        self.elementDecoder=elementDecoder;
        super().__init__(0, elementDecoder.typeName+"[]");

class MieleStruct(MieleAttributeDecoder):
    def __init__(self):
        super().__init__(0, "struct");

class Dop2Payload:
    def __init__ (unit, node, fields):
        self.unit=unit;
        self.node=node,
        self.fields=fields;

class MieleAttributeParser():
    def registerDecoders(self):
        self.decoders={
            1: MieleBool(),
            2: MieleInteger(1, MieleIntegerFormat.Unsigned),
            3: MieleInteger(1, MieleIntegerFormat.Signed),
            4: MieleInteger(1, MieleIntegerFormat.E), ## 1-byte values end here
            5: MieleInteger(2, MieleIntegerFormat.Unsigned),
            6: MieleInteger(2, MieleIntegerFormat.Signed),
            7: MieleInteger(2, MieleIntegerFormat.E),
            8: MieleInteger(4, MieleIntegerFormat.Unsigned),
            9: MieleInteger(4, MieleIntegerFormat.Signed),
            10: MieleInteger(4, MieleIntegerFormat.E),
            11: MieleInteger(8, MieleIntegerFormat.Unsigned),
            12: MieleInteger(8, MieleIntegerFormat.Signed),
            13: MieleInteger(8, MieleIntegerFormat.E),
            14: MieleFloat(4),
            15: MieleFloat(8),
            16: MieleStruct (),
            17: MieleArray (MieleBool()),
            18: MieleArray(MieleInteger(1, MieleIntegerFormat.Unsigned)),
            } 
    def __init__ (self):
        self.registerDecoders();
    def __str__(self):
        return f"MieleAttributeParser, decoders={[str(x) for x in self.decoders.values()]}";
    def parseBytes (self, response):
        payloadLength=response[1] + (response[0] << 8);
        unitId = (response[2] << 8) + response[3];
        attributeId = ( ( response[4] << 8 )* 1 + response[5]);
        padding_bytes_expected=len(response)-payloadLength-2;

        ## todo: add check that padding is 0x20 only

        payload=response[8:len(response)-padding_bytes_expected]

        if (len(payload)==0):
            print("empty response, returning");
            return Dop2Payload (unit, node, []);
        
        numberOfFields=(payload[3]) + (payload[4] << 8);

        fields=[];
        remainingPayload=payload[5:];
        
        while (len(fields) <= numberOfFields and len(remainingPayload) > 0):
            if (len(fields) + 1 != remainingPayload[0]): #field index does not match
                raise Exception("incorrect field numbering")
            fieldType = remainingPayload[1];
            decoder=self.decoders[fieldType];
            fieldValue = decoder.decode (remainingPayload[2:]);
            remainingPayload=remainingPayload[2+fieldValue.wireLength];
            fields.append(fieldValue);
            
            
