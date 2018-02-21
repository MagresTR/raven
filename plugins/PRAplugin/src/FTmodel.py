from __future__ import division, print_function , unicode_literals, absolute_import
import warnings
warnings.simplefilter('default', DeprecationWarning)

#External Modules---------------------------------------------------------------
import numpy as np
import math
#External Modules End-----------------------------------------------------------

#Internal Modules---------------------------------------------------------------
from PluginsBaseClasses.ExternalModelPluginBase import ExternalModelPluginBase
from PostProcessors.FTstructure import FTstructure
#Internal Modules End-----------------------------------------------------------


class FTmodel(ExternalModelPluginBase):

  def _readMoreXML(self, container, xmlNode):
    """
      Method to read the portion of the XML that belongs to this plugin
      @ In, container, object, self-like object where all the variables can be stored
      @ In, xmlNode, xml.etree.ElementTree.Element, XML node that needs to be read
      @ Out, None
    """
    container.mapping    = {}
    container.InvMapping = {}

    for child in xmlNode:
      if child.tag == 'topEvents':
        container.topEventID = child.text.strip()
      elif child.tag == 'map':
        container.mapping[child.get('var')]      = child.text.strip()
        container.InvMapping[child.text.strip()] = child.get('var')
      elif child.tag == 'variables':
        variables = [str(var.strip()) for var in child.text.split(",")]
      else:
        print('xml error')

  def initialize(self, container, runInfoDict, inputFiles):
    """
      Method to initialize this plugin
      @ In, container, object, self-like object where all the variables can be stored
      @ In, runInfoDict, dict, dictionary containing all the RunInfo parameters (XML node <RunInfo>)
      @ In, inputFiles, list, list of input files (if any)
      @ Out, None
    """
    #container.faultTreeModel = FTstructure(container['files'], container.topEventID)

  def createNewInput(self, container, inputs, samplerType, **Kwargs):
    container.faultTreeModel = FTstructure(inputs, container.topEventID)
    container.faultTreeModel.FTsolver()
    return Kwargs  
  
  def run(self, container, Inputs):    
    if self.checkTypeOfAnalysis(container,Inputs): 
      value = self.runTimeDep(container, Inputs)
    else:
      value = self.runStatic(container, Inputs)
    
    container.__dict__[container.topEventID]= value[container.topEventID]
      
  def checkTypeOfAnalysis(self,container,Inputs):
    # True:  dynamic
    # False: static
    arrayValues=set()
    for key in Inputs.keys():
      if key in container.mapping.keys():
        arrayValues.add(Inputs[key])
    if arrayValues.difference({0.,1.}):
      return True
    else:
      return False

  def runStatic(self, container, Inputs):
    """
      This is a simple example of the run method in a plugin.
      This method takes the variables in input and computes
      oneOutputOfThisPlugin(t) = var1Coefficient*exp(var1*t)+var2Coefficient*exp(var2*t) ...
      @ In, container, object, self-like object where all the variables can be stored
      @ In, Inputs, dict, dictionary of inputs from RAVEN

    """
    inputForFT = {}
    for key in container.InvMapping.keys():
      inputForFT[key] = Inputs[container.InvMapping[key]]
    value = container.faultTreeModel.evaluateFT(inputForFT)
    return value
    #container.__dict__[container.topEventID]= value[container.topEventID]

  def runTimeDep(self, container, Inputs):
    times = []
    times.append(0.)
    for key in Inputs.keys():   
      if key in container.mapping.keys() and Inputs[key]!=1.:
        times.append(Inputs[key])
    times = sorted(times, key=float)

    outcome={}
    outcome[container.topEventID] = np.asarray([0.])
    
    for time in times:
      inputToPass=self.inputToBePassed(container,time,Inputs)
      tempOut = self.runStatic(container, inputToPass)
      for var in outcome.keys():
        if tempOut[var] == 1.:
          if time == 0.:
            outcome[var] = np.asarray([1.])
          else:
            if outcome[var][0] > 0:
              pass
            else:
              outcome[var] = np.asarray([time])  
    return outcome
    
  def inputToBePassed(self,container,time,Inputs):
    inputToBePassed = {}
    for key in Inputs.keys():
      if key in container.mapping.keys():
        if Inputs[key] == 0. or Inputs[key] == 1.:
          inputToBePassed[key] = Inputs[key]
        else:
          if Inputs[key] > time:
            inputToBePassed[key] = np.asarray([0.])
          else:
            inputToBePassed[key] = np.asarray([1.])
    return inputToBePassed
  
  
  