###############################################################################
#   Process webchat.html for custom variables and replace it before render
#   So far only $initial_question variable is used in webchat.html but
#   more variables coube be used from confg.yaml in webchat section for instance
#   such variable could be something like:
#   webchat:
#     host: 0.0.0.0
#     port: 8080
#     debug: false
#     head_title: "Program-Y webchat demo"
#     header: |
#       <h1>Welcome to Program-Y Demonstration</h1>
#       <h3>A Fully 2.x AIML Complaint Python 3 based Open Source Chatbot Framework</h3>
#     footer: |
#       <a href="https://github.com/keiffster/program-y">Program-Y on GitHub</a> |
#       <a href="https://github.com/keiffster/program-y/wiki">Documentation</a> |
#       <a href="http://www.keithsterling.com">Meet the Author</a> |
#       <a href="http://servusai.com">Professional Services</a>
#     popular_questions: |
#    	  <p class="welcome">Popular Questions<b></b></p>
#       <ul>
#         <li class="question"><a href="#">Who are you?</a></li>
#         <li class="question"><a href="#">What are you?</a></li>
#         <li class="question"><a href="#">Where are you?</a></li>
#       </ul>       
###############################################################################

from programy.config.sections.bot.bot import BotConfiguration
from programy.config.sections.client.console import ConsoleConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile

def process_htmltemplate(url):
  #############################################################################
  # TODO: 
  #   get bot configuration here from config.yaml
  #   and replace bellow temporary settings
  #############################################################################

  yaml = YamlConfigurationFile()
  
  yaml.load_from_text("""
  bot:
    initial_question: Hello, how do you like your custom initial_question ?
  """, ConsoleConfiguration(), ".")
  bot_config = BotConfiguration()
  bot_config.load_configuration(yaml, ".")

  with open(url, 'r') as file :
    filedata = file.read()
  filedata = filedata.replace('$initial_question', bot_config.initial_question)
  # proposition for other custom webchat sttings that could be set
  #filedata = filedata.replace('$head_title', webchat_config.head_title)
  #filedata = filedata.replace('$header', webchat_config.header)
  #filedata = filedata.replace('$popular_questions', webchat_config.popular_questions)
  #filedata = filedata.replace('$footer', webchat_config.footer)
  return filedata
