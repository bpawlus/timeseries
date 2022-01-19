import entryvalidators as ev
import dataGenerator as dg
import numpy as np
import loader
import ruptures as rpt
from ruptures.metrics import *

class RupturesEvaluations:
    """Class concatenating evaluations of change point finding algorithms.
    """

    hs = None
    """List of Hausdorff Metrics results."""
    ris = None
    """List of Rand index Metrics results."""
    ps = None
    """List of Precision Metrics results."""
    rs = None
    """List of Recall Metrics results."""
    l = None
    """Estimated:True change point count ratio"""

    def appendAll(self,*args):
        """Adds a record to metrics arrays

        :param args: Array of metrics to add.
        """
        self.hs.append(args[0][0])
        self.ris.append(args[0][1])
        self.ps.append(args[0][2])
        self.rs.append(args[0][3])
        self.l.append(args[0][4])

    def __init__(self) -> None:
        self.hs = []
        self.ris = []
        self.ps = []
        self.rs = []
        self.l = []

class RupturesEfficiency:
    """Class evaluating efficiency of implemented change point detection algorithms.
    It has no gui, it's intended to be displayed in command prompt.
    """

    f = None
    """Handle to file, where results should be stored."""


    def provideFloat(self, display: str) -> float:
        """Asks user for input in form of float value.
        
        :param display: Display that helps the user what he is about to put.
        """
        print("===============")
        print(display + "(" + loader.lang["efficiency"]["types"]["float"] + "):")
        while True:
            a = input()
            if ev.validate_float(a):
                return float(a)
            else:
                print(loader.lang["efficiency"]["types"]["error"])

    def providePositiveFloat(self, display: str) -> float:
        """Asks user for input in form of positive float value.
        
        :param display: Display that helps the user what he is about to put.
        :returns: User input.
        """
        print("===============")
        print(display + "(" + loader.lang["efficiency"]["types"]["floatpos"] + "):")
        while True:
            a = input()
            if ev.validate_float_pos(a):
                return float(a)
            else:
                print(loader.lang["efficiency"]["types"]["error"])

    def providePositiveFloatOrZero(self, display: str) -> float:
        """Asks user for input in form of positive float (or zero) value.
        
        :param display: Display that helps the user what he is about to put.
        :returns: User input.
        """
        print("===============")
        print(display + "(" + loader.lang["efficiency"]["types"]["floatposzero"] + "):")
        while True:
            a = input()
            if ev.validate_float_pos_zero(a):
                return float(a)
            else:
                print(loader.lang["efficiency"]["types"]["error"])

    def providePositiveInt(self, display: str) -> int:
        """Asks user for input in form of positive int value.
        
        :param display: Display that helps the user what he is about to put.
        :returns: User input.
        """
        print("===============")
        print(display + "(" + loader.lang["efficiency"]["types"]["digit"] + "):")
        while True:
            a = input()
            if ev.validate_int_pos(a):
                return int(a)
            else:
                print(loader.lang["efficiency"]["types"]["error"])

    def providePositiveBool(self, display: str) -> bool:
        """Asks user for input in form of bool value.
        
        :param display: Display that helps the user what he is about to put.
        :returns: User input.
        """
        print("===============")
        print(display + "(T/F):")
        while True:
            a = input()
            if a == "T":
                return True
            elif a == "F":
                return False
            print(loader.lang["efficiency"]["types"]["error"])

    def provideFromMap(self, display: str, dict: map) -> str:
        """Asks user for input in form of single occurence from the map.
        
        :param display: Display that helps the user what he is about to put.
        :param dict: Map with possible values.
        :returns: User input.
        """
        print("===============")
        print(display + "(" + loader.lang["efficiency"]["types"]["frommap"] + "):")
        print([a for a in dict.keys()])
        while True:
            a = input()
            if a in dict.keys():
                return a
            print(loader.lang["efficiency"]["types"]["error"])


    def evaluate(self, settrue: list, seteval: list, m: float) -> tuple:
        """Evaluates change point detection results.
        
        :param settrue: Set of true change points.
        :param seteval: Set of estimated change points.
        :param m: Precision's and recall's margin argument.
        :returns: User input.
        """

        if(len(settrue) >= 2 and len(seteval) >= 2):
            h = hausdorff(settrue, seteval)
            ri = randindex(settrue, seteval)
            p, r = precision_recall(settrue, seteval, margin=m)
            return (h, ri, p, r, (len(seteval)-1)/(len(settrue)-1)), True
        else:
            return (), False

    def outputSummary(self, header: str, eval: RupturesEvaluations):
        """Writes results of evaluation metrics
        
        :param header: Display that helps the user read final file.
        :param eval: Class concatenating evaluations of change point finding algorithms.
        """
        self.f.write(header+"\n")
        self.f.write("Hausdorff [DATA + MEAN + STD]:\n")
        #self.f.write(str(eval.hs)+"\n")
        self.f.write(str(np.mean(np.array(eval.hs)))+"\n")
        self.f.write(str(np.std(np.array(eval.hs)))+"\n")
        
        self.f.write("==========\n")

        self.f.write("Rand index [DATA + MEAN + STD]:\n")
        #self.f.write(str(eval.ris)+"\n")
        self.f.write(str(np.mean(np.array(eval.ris)))+"\n")
        self.f.write(str(np.std(np.array(eval.ris)))+"\n")

        self.f.write("==========\n")

        self.f.write("Precision [DATA + MEAN + STD]:\n")
        #self.f.write(str(eval.ps)+"\n")
        self.f.write(str(np.mean(np.array(eval.ps)))+"\n")
        self.f.write(str(np.std(np.array(eval.ps)))+"\n")

        self.f.write("==========\n")

        self.f.write("Recall [DATA + MEAN + STD]:\n")
        #self.f.write(str(eval.rs)+"\n")
        self.f.write(str(np.mean(np.array(eval.rs)))+"\n")
        self.f.write(str(np.std(np.array(eval.rs)))+"\n")

        self.f.write("==========\n")

        self.f.write("Estimated:True change point count ratio [DATA + MEAN + STD]:\n")
        #self.f.write(str(eval.h)+"\n")
        self.f.write(str(np.mean(np.array(eval.l)))+"\n")
        self.f.write(str(np.std(np.array(eval.l)))+"\n")
        self.f.write("\n")     

    def outputCPs(self, header: str, res: list):
        """Writes results of change point detection algorithms in single iteration.
        
        :param header: Display that helps the user read final file.
        :param res: List of change points
        """
        self.f.write(header+"\n")
        self.f.write("Change Points:\n")
        self.f.write(str(res)+"\n")
        self.f.write("\n")

    def run(self):
        """Runs evaluation of efficiency of implemented change point detection algorithms.
        """

        self.f = open(loader.dirs["exporteval"], "w")
        print(loader.lang["efficiency"]["description"])

        iterations: int = self.providePositiveInt(loader.lang["efficiency"]["iterations"])

        samples: int = self.providePositiveInt(loader.lang["settings-gen"]["generator"]["samples"])
        cpcount: int = self.providePositiveInt(loader.lang["settings-gen"]["generator"]["cpcount"])
        mean: float = self.provideFloat(loader.lang["settings-gen"]["generator"]["mean"])
        spread: float = self.providePositiveFloatOrZero(loader.lang["settings-gen"]["generator"]["spread"])
        cpspread: float = self.providePositiveFloatOrZero(loader.lang["settings-gen"]["generator"]["cpspread"])
        spreadcpspread: float = self.providePositiveFloatOrZero(loader.lang["settings-gen"]["generator"]["spreadcpspread"])

        dictCost = {
            "l1": loader.lang["modules"]["changepoints"]["costs"]["l1"],
            "l2": loader.lang["modules"]["changepoints"]["costs"]["l2"],
            "normal": loader.lang["modules"]["changepoints"]["costs"]["normal"]
        }

        cpointsconsider: bool = self.providePositiveBool(loader.lang["modules"]["changepoints"]["cpointsconsider"])
        costfc: str = self.provideFromMap(loader.lang["modules"]["changepoints"]["costfcs"], dictCost)
        penalty: float = None
        cpoints: int = None
        if cpointsconsider:
            cpoints: int = self.providePositiveInt(loader.lang["modules"]["changepoints"]["cpoints"])
        else:
            penalty: float = self.providePositiveFloat(loader.lang["modules"]["changepoints"]["penalty"])
            
        winwidth: int = self.providePositiveInt(loader.lang["modules"]["changepoints"]["window"]["width"])
        margin: float = self.providePositiveFloatOrZero(loader.lang["modules"]["evaluation"]["margin"])
        sg = dg.SignalGenerator()

        eval1 = RupturesEvaluations()
        eval2 = RupturesEvaluations()
        eval3 = RupturesEvaluations()
        eval4 = RupturesEvaluations()
        i = 0

        if cpointsconsider:           
            while i < iterations:
                sg.generateSignal(samples, cpcount, mean, spread, cpspread, spreadcpspread)
                signal = np.array(sg.getSignal())
                (resTrue, genMeans, genSpreads) = sg.getGeneratedSignalProperties()

                algo2 = rpt.Window(model=costfc, width=winwidth).fit(signal)
                algo3 = rpt.Binseg(model=costfc).fit(signal)
                algo4 = rpt.BottomUp(model=costfc).fit(signal)

                res2 = algo2.predict(n_bkps=cpoints)
                res3 = algo3.predict(n_bkps=cpoints)
                res4 = algo4.predict(n_bkps=cpoints)

                res2[len(res2)-1] -= 1
                res3[len(res3)-1] -= 1
                res4[len(res4)-1] -= 1

                tp2, err2 = self.evaluate(resTrue, res2, margin)
                tp3, err3 = self.evaluate(resTrue, res3, margin)
                tp4, err4 = self.evaluate(resTrue, res4, margin)

                if(err2 and err3 and err4):
                    print(loader.lang["efficiency"]["iteration"] + ": " + str(i+1) + "/" + str(iterations))
                    self.f.write("=================== I: " + str(i+1) + " ===================\n")
                    self.outputCPs("========== RESULT TRUE ==========", resTrue)
                    self.outputCPs("========== ESTIMATED RESULTS WINDOW ==========", res2)
                    self.outputCPs("========== ESTIMATED RESULTS BINSEG ==========", res3)
                    self.outputCPs("========== ESTIMATED RESULTS BOTTOMUP ==========", res4)
                    self.f.write("\n")

                    eval2.appendAll(tp2)
                    eval3.appendAll(tp3)
                    eval4.appendAll(tp4)
                    i += 1
        else:
            while i < iterations:
                sg.generateSignal(samples, cpcount, mean, spread, cpspread, spreadcpspread)
                signal = np.array(sg.getSignal())
                (resTrue, genMeans, genSpreads) = sg.getGeneratedSignalProperties()

                algo1 = rpt.Pelt(model=costfc).fit(signal)
                algo2 = rpt.Window(model=costfc, width=winwidth).fit(signal)
                algo3 = rpt.Binseg(model=costfc).fit(signal)
                algo4 = rpt.BottomUp(model=costfc).fit(signal)

                res1 = algo1.predict(pen=penalty)
                res2 = algo2.predict(pen=penalty)
                res3 = algo3.predict(pen=penalty)
                res4 = algo4.predict(pen=penalty)

                res1[len(res1)-1] -= 1
                res2[len(res2)-1] -= 1
                res3[len(res3)-1] -= 1
                res4[len(res4)-1] -= 1

                tp1, err1 = self.evaluate(resTrue, res1, margin)
                tp2, err2 = self.evaluate(resTrue, res2, margin)
                tp3, err3 = self.evaluate(resTrue, res3, margin)
                tp4, err4 = self.evaluate(resTrue, res4, margin)

                if(err1 and err2 and err3 and err4):
                    print(loader.lang["efficiency"]["iteration"] + ": " + str(i+1) + "/" + str(iterations))
                    self.f.write("=================== I: " + str(i+1) + " ===================\n")
                    self.outputCPs("========== RESULT TRUE ==========", resTrue)
                    self.outputCPs("========== ESTIMATED RESULTS PELT ==========", res1)
                    self.outputCPs("========== ESTIMATED RESULTS WINDOW ==========", res2)
                    self.outputCPs("========== ESTIMATED RESULTS BINSEG ==========", res3)
                    self.outputCPs("========== ESTIMATED RESULTS BOTTOMUP ==========", res4)
                    self.f.write("\n")

                    eval1.appendAll(tp1)
                    eval2.appendAll(tp2)
                    eval3.appendAll(tp3)
                    eval4.appendAll(tp4)
                    eval1.l
                    i += 1
    
        self.f.write("\n\n")
        self.f.write("==================== END ====================\n")
        if(not cpointsconsider):
            self.outputSummary("========== ESTIMATED RESULTS PELT MEAN ==========", eval1)
        self.outputSummary("========== ESTIMATED RESULTS WINDOW MEAN ==========", eval2)
        self.outputSummary("========== ESTIMATED RESULTS BINSEG MEAN ==========", eval3)
        self.outputSummary("========== ESTIMATED RESULTS BOTTOMUP MEAN ==========", eval4)
        self.f.write("\n\n")
        self.f.write("==================== FOR PARAMS ====================\n")
        self.f.write("iterations\n")
        self.f.write(str(iterations)+"\n")
        self.f.write("samples cpcount mean spread cpspread spreadcpspread\n")
        self.f.write(str(samples)+" ")
        self.f.write(str(cpcount)+" ")
        self.f.write(str(mean)+" ")
        self.f.write(str(spread)+" ")
        self.f.write(str(cpspread)+" ")
        self.f.write(str(spreadcpspread)+"\n")
        if(cpointsconsider):
            self.f.write("costfc cpoints winwidth\n")
            self.f.write(str(costfc)+" ")
            self.f.write(str(cpoints)+" ")
            self.f.write(str(winwidth)+"\n")
        else:
            self.f.write("costfc penalty winwidth\n")
            self.f.write(str(costfc)+" ")
            self.f.write(str(penalty)+" ")
            self.f.write(str(winwidth)+"\n")
        self.f.write("margin\n")
        self.f.write(str(margin))
        self.f.close()

        print(loader.lang["efficiency"]["finish"]+loader.dirs["exporteval"])