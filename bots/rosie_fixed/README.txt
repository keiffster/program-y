The original Rosie AIML is produced by Pandora Bots, and hosted on GitHib https://github.com/pandorabots/rosie

Unfortunately its broken in many ways, grammars are missing, srai tags don't work properly and there are conflicting grammars

This project is therefore an attempt to provide a grammar, based on Rosie that can be an actual base for someone to
use when building their own Chatbot

This README will contain a history of the issues found and the fixes applied

------------------------------------------------------

1) Missing grammars
SOUND is missing
Added mapping file for animal:sound
Added mapping file for animal:legs
Modified grammars so that SOUND and LEGS now work

2) Built in maps, not defined in spec

Pandora, who built rosie have a number of in built maps, the 2 primary ones are
successor and predecessor which turn the next or previous integer respectively

3) Built in set, not defined in spec

Pandora who built rosie, have a number of in built sets, primary one is number
which checks if text passed in is numeric

Added successor map
Added predecessor map
Added singular map -> Also singular mapping file
Added plural map -> Also singular plural file

