from datetime import datetime

from .const import *


#ROOT_DEVICES2 = "15002"  # ??
#ATTR_MEMBERS = "9018"
#ATTR_MOOD = "9039"

# The gateway stores days as 
CONST_MON = 1
CONST_TUE = 2
CONST_WED = 4
CONST_THU = 8
CONST_FRI = 16
CONST_SAT = 32
CONST_SUN = 32

"""
{  
   '5850':0, // on/off
   '9044':[ // TRIGGER_TIME_INTERVAL
      {  
         '9047':0,
         '9046':6
      }
   ],
   '9042':{   //start action
      '5850':1, // onoff
      '15013':[  // light setting
         {  
            '9003':65537, // device id
            '5712':18000, // TRANSITION_TIME
            '5851':254 // dimmer
         }
      ]
   },
   '9041':0, // repeat days
   '9040':4 // smart task type
}
"""


class Transition:
    """Represent a group."""
    def __init__(self, gateway, raw):
        self._gateway = gateway
#        self.api = gateway.api
        self.raw = raw

    @property
    def id(self):#OK
        return self.raw.get(ATTR_ID)

    @property
    def created_at(self):#OK
        if ATTR_CREATED_AT not in self.raw:
            return None
        return datetime.utcfromtimestamp(self.raw[ATTR_CREATED_AT])

    @property
    def path(self):#OK
        return [ROOT_TRANSITIONS, self.id]

    @property
    def state(self):#OK
        """Boolean representing the light state of the transition."""
        return self.raw.get(ATTR_LIGHT_STATE) == 1

    @property
    def repeat_days(self):#WIP
        """Binary representation of weekdays the event takes place."""
        return self.raw.get(ATTR_REPEAT_DAYS)
        
    def __repr__(self):#OK
        state = 'on' if self.state else 'off'
        return '<Transition {} - {}>'.format(self.id, state)

    def update(self):#OK
        """Update the group."""
        self.raw = self.api('get', self.path)
