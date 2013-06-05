'''
Created on May 29, 2013

@author: HI-TECH
'''
import json
"""
if 'extra_id' in j :
                            response += " <br>Report id: " + j['extra_id'] + "</br>"
                        if 'extra_cry' in j :    
                            response += " <br>Did the baby cry spontaneously at birth? " + j['extra_cry'] + "</br>"
                        if 'exra_vent' in j :        
                            response += " <br>Did you have to start bag and mask ventilation? " + j['exra_vent'] + "</br>"
                        if 'extra_alive' in j :                                    
                            response += " <br>New born is: " + j['extra_alive'] + "</br>"
                        if 'extra_primary' in j :
                            response += " <br>Primary cause of death: " + j['extra_primary'] + "</br>"
                            if 'extra_other' in j:
                                response += " <br>details: " + j['extra_other'] + "</br>"
                            if 'extra_problem' in j:
                                response += "<div> "
                                response += "<br>Problems with the system:" + j['extra_problem'] +        
"""
def getID(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_id']
            except:
                ""
            return response
        
def getCry(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_cry']
            except:
                ""
            return response
               
def getCauseOfDeath(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_primary']
            except:
                ""
            return response
def getAlive(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_alive']
            except:
                ""
            return response
                      
def getVent(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['exra_vent']
            except:
                ""
            return response        

def getOther(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_other']
            except:
                ""
            return response              


             
def getProblem(var):
            j = json.loads(var)
            response = ""
            try:
                response = j['extra_problem']
            except:
                ""
            return response              
def toCSV(var):
    j = json.loads(var)
    response = ""
    
    if 'extra_id' in j :
        
            response += j['extra_id']
    response += ","
    if 'extra_alive' in j :
            response += j['extra_alive']
    response += ","
    if 'extra_cry' in j :    
            response +=  j['extra_cry']
    response += ","        

    if 'extra_primary' in j :
        response += j['extra_primary']
    response += ","
    
    if 'exra_vent' in j :
            response +=  j['exra_vent']
    response += ","                    
      
        

    if 'extra_other' in j:
            response +=  j['extra_other']
    response += ","        
             
    if 'extra_problem' in j:
            response +=  j['extra_problem']
    response += ","        
              
    return response