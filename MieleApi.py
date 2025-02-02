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
from enum import Enum

class ProgramType:
        BuiltInFunction = 1
        UserDefined = 2
        Automatic = 3
        CleaningProgram = 4
        CustomerService = 5
        Helper = 6
class RemoteControl(Enum):
        Disabled = 0
        EnabledButNotPossible = 7
        Full = 15
        Unknown = 2147483647

class DeviceType (Enum):
        NoUse = 0
        WashingMachine = 1
        TumbleDryer = 2
        WashingMachineSemiPro = 3
        TumbleDryerSemiPro = 4
        WashingMachinePro = 5
        TumbleDryerPro = 6
        Dishwasher = 7
        DishwasherSemiPro = 8
        DishwasherPro = 9
        Range = 10
        RangeWithMicrowave = 11
        Oven = 12
        OvenWithMicrowave = 13
        Cooktop = 14
        SteamOven = 15
        Microwave = 16
        CoffeeMaker = 17
        Hood = 18
        Fridge = 19
        Freezer = 20
        FridgeWithFreezer = 21
        ChestFreezer = 22
        RobotVacuum = 23
        WasherDryer = 24
        WarmingDrawer = 25
        BeverageMaker = 26
class DryingStep (Enum):
        ExtraDry=0
        NormalPlus=1
        Normal=2
        SlightlyDry=3
        HandIron1=4
        HandIron2=5
        MachineIron=6
        HygieneDry=7

class Light (Enum):
        NotSupported=0
        Enabled=1
        Disabled=2
class Status (Enum):
        NoUse = 0
        Off = 1
        On = 2
        Programmed = 3
        WaitingToStart = 4
        Running = 5
        Paused = 6
        EndedSuccessfully = 7
        Failure = 8
        Abort = 9
        Idle = 10
        Rinse = 11
        Service = 12
        SuperFreeze = 13
        SuperCool = 14
        SuperHeat = 15
        Default = 144
        Lock = 145
        SuperCoolSuperFreeze = 146
class ProgramId (Enum):
        NotSelected = 0
        Automatic = 1
        WhitesCottons = 2
        MinimumIron = 3
        Wool = 4
        Delicate = 5
        HotAir = 6
        ColdAir = 7
        Express = 8
        Cotton = 9
        Gentle = 10
        CottonHygiene = 11
        Cottons40Celsius = 27
        Cottons25Celsius = 28
        MinimumIron25Celsius = 29
        SyntheticBedding = 30
        NaturalBedding = 31
        Microfiber = 32
        WetcareIntensive = 33
        WetcareSensitive = 34
        WetcareSilk = 35
        LargeItems = 36
        Reactivate = 37
        Smoothing = 38
        CottonsWhiteHygiene = 39
        ProgramFortyCelsius = 59

class ProgramPhase(Enum):
        NotUsed = 0
        Progress = 1
        BatteryCharging = 2
        WashingMachineIdle = 256
        WashingMachinePreWash = 257
        WashingMachineSoak = 258
        WashingMachinePreRinse = 259
        WashingMachineWashing = 260
        WashingMachineRinse = 261
        WashingMachineRinseHold = 262
        WashingMachineClean = 263
        WashingMachineCooldown = 264
        WashingMachineDrain = 265
        WashingMachineSpin = 266
        WashingMachineAntiCrease = 267
        WashingMachineFinished = 268
        WashingMachineVenting = 269
        WashingMachineStarch = 270
        WashingMachineMoisting = 271
        WashingMachineRemoisting = 272
        WashingMachineHygiene = 279
        WashingMachineDrying = 280
        WashingMachineDisinfection = 285
        WashingMachineSteamSmoothing = 295
        TumbleDryerIdle = 512
        TumbleDryerProgramStart = 513
        TumbleDryerDrying = 514
        TumbleDryerMachineIron = 515
        TumbleDryerHandIron2 = 516
        TumbleDryerNormal = 517
        TumbleDryerNormalPlus = 518
        TumbleDryerComfortCooldown = 519
        TumbleDryerHandIron1 = 520
        TumbleDryerAntiCreaseFinish = 521
        TumbleDryerFinished = 522
        TumbleDryerExtraDry = 523
        TumbleDryerHandIronWithoutDrop = 524
        TumbleDryerHygieneDrying = 525
        TumbleDryerWetting = 526
        TumbleDryerSpin = 527
        TumbleDryerFanActive = 528
        TumbleDryerHotAir = 529
        TumbleDryerSteamSmooth = 530
        TumbleDryerCooling = 531
        TumbleDryerFluff = 532
        TumbleDryerRinse = 533
        TumbleDryerSmooth = 534
        TumbleDryerUnknown1 = 535
        TumbleDryerRemoteStart = 536
        TumbleDryerDelayedRun = 537
        TumbleDryerSlightlyDry = 538
        TumbleDryerSafetyCooldown = 539
        DishwasherNoProgram = 1792
        DishwasherRegenerate = 1793
        DishwasherPreRinse = 1794
        DishwasherClean = 1795
        DishwasherRinse = 1796
        DishwasherRinseInterim = 1797
        DishwasherRinseClear = 1798
        DishwasherDrying = 1799
        DishwasherFinished = 1800
        DishwasherPreRinse2 = 1801
        OvenCooldown = 3072
        OvenHeating = 3073
        OvenTempHold = 3074
        OvenDoorOpen = 3075
        OvenPyrolyze = 3076
        OvenMicrowave = 3077
        OvenProgramDone = 3078
        OvenLight = 3079
        OvenSearing = 3080
        OvenRoasting = 3081
        OvenDefrost = 3082
        OvenCooldown2 = 3083
        OvenEnergySave = 3084
        OvenHoldWarm = 3094
        OvenDescale = 3098
        OvenPreheat = 3099
