'''AI Agent API from MicroSoft Autogen
'''

import autogen

assistant = autogen.Assistant(
    name="MathTutor", 
    system_message="You are a helpful math tutor.",)