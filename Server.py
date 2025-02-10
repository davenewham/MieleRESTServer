#
# Copyright (c) 2025 Alexander Kappner.
#
# This file is part of MieleRESTServer 
# (see github).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from _version import __version__
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from MieleCrypto import MieleProvisioningInfo, MieleCryptoProvider
from MieleApi import *
from MieleErrors import *

from flask import render_template

import json
import time
import yaml
import sys
import argparse

PRODUCTNAME="MieleRESTServer"
endpoints={};

class MieleHelpers:
    def tuple_to_min (t):
        return t[0]*60+t[1];

class EndpointLastComm:
    def __init__ (self):
        self.time=None;
    def reset(self):
        self.time = time.monotonic();
    def __str__(self):
        if (self.time==None):
            return "never"
        else:
            return f"{time.monotonic()-self.time}";
class MieleEndpointConfig:
    def __init__ (self, host, groupId, groupKey, device_route):
#        self.id = id;
        self.host = host;
        self.provisioningInfo = MieleProvisioningInfo(groupId, groupKey);
        self.cryptoProvider = MieleCryptoProvider(self.provisioningInfo);
        self.device_route = device_route;
        self.last_comm=EndpointLastComm();
    def __init__(self, d):
        self.host=d["host"];
        self.provisioningInfo = MieleProvisioningInfo(d["groupId"], d["groupKey"]);
        self.cryptoProvider = MieleCryptoProvider(self.provisioningInfo);
        self.last_comm=EndpointLastComm();

        if ("route" in d and d["route"] != "auto"):
            self.device_route=d["route"];
        else:
            self.autodetect_route();
            print(f'Autodetected device route for host {self.host}; please add "deviceRoute: "{self.device_route}" in your config file');

    def tryDecodeAndAdd (j, key, e):
        try:
            toDecode=j[key];
            j["Decoded"+key]=e(toDecode).name;
            return j;
        except:
            return j;
    def autodetect_route(self):
        response=self.send_get(f"Devices")
        j=json.loads(response)
        print(j)
        if (len(j.keys())==1):
            self.device_route=list(j.keys())[0];
        else:
            raise Exception("Error autodetecting route");
    def walkdop2tree (self):
        return self.cryptoProvider.readDop2Recursive(self.host, self.device_route);
    def get_device_summary_raw(self):
        return self.send_get(f"Devices/{self.device_route}/State");
    def get_device_ident_raw (self):
        return self.send_get(f"Devices/{self.device_route}/Ident");

    def get_device_summary_annotated (self):
        response=self.get_device_summary_raw();
        j=json.loads(response)
        response2=self.get_device_ident_raw();
        j2=json.loads(response2)
        j=j| j2;
        MieleEndpointConfig.tryDecodeAndAdd(j, "ProgramPhase", ProgramPhase);
        MieleEndpointConfig.tryDecodeAndAdd(j, "ProgramID", ProgramId);
        MieleEndpointConfig.tryDecodeAndAdd(j, "Status", Status);
        MieleEndpointConfig.tryDecodeAndAdd(j, "DeviceType", DeviceType);
        MieleEndpointConfig.tryDecodeAndAdd(j, "DryingStep", DryingStep);
        try:
            elapsed=MieleHelpers.tuple_to_min(j["ElapsedTime"])
            remaining=MieleHelpers.tuple_to_min(j["RemainingTime"])
            total = elapsed + remaining;
            if (total < 0.1):
                progress=0.0;
            else:
                progress=elapsed/(elapsed+remaining);
                print(f"Progress: {100*progress:.2f}%");
            j["RemainingMinutes"]=remaining;
            j["ElapsedMinutes"]=elapsed;
            j["Progress"]=str(progress);
        except:
            j["Progress"]=-1;
            j["RemainingMinutes"]=-1
            j["ElapsedMinutes"]=-1
            pass;
        return j;
    def set_device_action (self):
        command=json.dumps({"ProcessAction": 1});
        print(command)
        decrypted, response=self.cryptoProvider.sendHttpRequest(host=self.host, httpMethod="PUT", resourcePath=f"Devices/{self.device_route}/State", payload=command);
        print(decrypted);
        return json.loads(decrypted)
    def send_get (self, path):
        try:
            response= self.cryptoProvider.sendHttpRequest(host=self.host, resourcePath=path)[0];
            print(response)
            self.last_comm.reset();
            return response;
        except:
            print("Communication error");
            raise;
    def serialize(self):
        return json.dumps( {"host":self.host, "groupid": self.provisioningInfo.groupid, "route":self.device_route, "last_comm": self.last_comm.__str__()} )
    def last_comm (self):
        self.last_comm.reset();

class SetDeviceActionAPI(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser();
        self.reqparse.add_argument('endpoint', type=str, required=False, help='',location='json');

    def get (self, endpoint):
        endpoint=endpoints[endpoint];
        j=endpoint.set_device_action();
        return j;
class EndpointAPI(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser();
        self.reqparse.add_argument('endpoint', type=str, required=False, help='',location='json');
        super(EndpointAPI,self).__init__()
    def get (self, endpoint=""):
        if (endpoint==""):
            return {x: endpoints[x].serialize() for x in endpoints.keys() };
        else:
            return {endpoint: endpoints[endpoint].serialize() };

class WalkDOP2TreeAPI(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser();
        self.reqparse.add_argument('endpoint', type=str, required=False, help='',location='json');
        super(WalkDOP2TreeAPI,self).__init__()
    def get (self, endpoint):
        endpoint=endpoints[endpoint];
        try:
            t=endpoint.walkdop2tree();
        except MieleRESTException as e:
            return e.asdict(), 400;
        return t;
class DeviceSummaryAPI(Resource):
    def __init__ (self):
        self.reqparse = reqparse.RequestParser();
        self.reqparse.add_argument('endpoint', type=str, required=False, help='',location='json');
        super(DeviceSummaryAPI,self).__init__()
    def get(self, endpoint):
        if (len(endpoint)>0):
            endpoint=endpoints[endpoint];
            j=endpoint.get_device_summary_annotated();
            return j;
class DevicesSummaryAPI(Resource):
    def get(self):
        j={e: x.get_device_summary_annotated() for e, x in endpoints.items() }
        return j;

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog=PRODUCTNAME,
                    description='Provides RESTful interface to Miele@home devices')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-c', '--config', default=f"/etc/{PRODUCTNAME}.config", help="path to configuration file")
    parser.add_argument('-b', '--bind', default=f"127.0.0.1", help="IP address to bind to, default is local only")
    parser.add_argument('-p', '--port', default=5001, help="port to bind to, default is port 5001")
    parser.add_argument('--webui', action='store_true', help="enable experimental web UI, default off")
    parser.add_argument('--debug', action='store_true', help="run REST server in debug mode, default off")

    cmdargs=parser.parse_args()

    with open(cmdargs.config) as stream:
        try:
            config_file=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            print ("Error loading configuration file, exiting");
    for key, value in config_file["endpoints"].items():
        endpoints[key]=MieleEndpointConfig(value);


    app = Flask(__name__, static_url_path="")
    api = Api(app)
    api.add_resource(DevicesSummaryAPI, '/generate-summary')
    api.add_resource(DeviceSummaryAPI, '/generate-summary/<string:endpoint>')
    api.add_resource(WalkDOP2TreeAPI, '/walkdop2tree/<string:endpoint>')
    api.add_resource(EndpointAPI, '/endpoints', '/endpoints/<string:endpoint>')
    api.add_resource(SetDeviceActionAPI, '/start/<string:endpoint>')

    if (cmdargs.webui):
        @app.route("/webui", strict_slashes=False)
        @app.route("/", strict_slashes=False)
        def webui_index():
            return render_template("generate_summary.html");
        @app.route("/webui/<string:endpoint>")
        def webui_endpoint(endpoint):
    #        context=EndpointAPI.get(endpoint);
            context=endpoints[endpoint].get_device_summary_annotated();
            print(context);
            return render_template("generate_summary.html", endpoint=context, endpointName=endpoint);
    else:
        print("WebUI disabled.")

    app.run(debug=cmdargs.debug, host=cmdargs.bind, port=cmdargs.port);
