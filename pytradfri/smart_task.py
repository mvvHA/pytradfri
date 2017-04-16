from datetime import datetime

from .const import *


# The gateway stores days as bit
CONST_ONCE = 0
CONST_MON = 1
CONST_TUE = 2
CONST_WED = 4
CONST_THU = 8
CONST_FRI = 16
CONST_SAT = 32
CONST_SUN = 32

class SmartTask:
    """Represent a group."""
    def __init__(self, gateway, raw):
        self._gateway = gateway
#        self.api = gateway.api
        self.raw = raw

    @property
    def is_transition(self):
        """Boolean representing if this is a transition task."""
        return self.raw.get(ATTR_SMART_TASK_TYPE) == ATTR_SMART_TASK_TRANSITION

    @property
    def is_not_home(self):#OK
        """Boolean representing if this is a not home task."""
        return self.raw.get(ATTR_SMART_TASK_TYPE) == ATTR_SMART_TASK_NOT_HOME

    @property
    def is_on_off(self):#OK
        """Boolean representing if this is an on/off task."""
        return self.raw.get(ATTR_SMART_TASK_TYPE) == ATTR_SMART_TASK_ON_OFF

    @property
    def task_type(self):
        """Return the task type in plain text."""
        if self.is_transition:
            return "Transition"
        if self.is_not_home:
            return "Not Home"
        if self.is_on_off:
            return "Automatic On/Off"

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
    def transition_time(self):#OK
        """A transition runs for this long from the time in task_start."""
        return self.raw.get(ATTR_TRANSITION_TIME)
        
    @property
    def task_start(self):#OK
        """
        Return the hour and minute the task starts.
        
        Sorry for poor programming...
        
        Time is set according to iso8601
        """
        hour = (
            self.raw.get(ATTR_SMART_TASK_TRIGGER_TIME_INTERVAL)[0]
            [ATTR_SMART_TASK_TRIGGER_TIME_START_HOUR])
        min = (
            self.raw.get(ATTR_SMART_TASK_TRIGGER_TIME_INTERVAL)[0]
            [ATTR_SMART_TASK_TRIGGER_TIME_START_MIN])
        
        return (hour, min)

    @property
    def repeat_days(self):
        """Binary representation of weekdays the event takes place."""
        return self.raw.get(ATTR_REPEAT_DAYS)
        
    def __repr__(self):#OK
        state = 'on' if self.state else 'off'
        return '<Task {} - {} - {}>'.format(self.id, self.task_type, state)

    def update(self):#OK
        """Update the group."""
        self.raw = self.api('get', self.path)

"""

DEBUG STUFF

https://gist.github.com/r41d/5d62033f88b3046bccf406c9158d4e59
// Transition
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
}

## Not home
{  
   '9002':1492371443,
   '9041':0,
   '5850':1,
   '9044':[  
      {  
         '9047':30,
         '9049':30,
         '9048':7,
         '9046':6
      }
   ],
   '9042':{  
      '15013':[  
         {  
            '9003':65537
         }
      ],
      '5850':1
   },
   '9003':320223,
   '9040':1,
   '9043':{  
      '15013':[  
         {  
            '9003':65537
         }
      ],
      '5850':0
   }

"""