Test Creator
============

Creates AIML based unit tests


Usage:
python3 test_creator.py aiml_file test_file ljust replace_file [default]

    aiml_file       - AIML File to create tests from
    test_file       - Test file to create with associated unit tests
    ljust           - Left justifies the first csv column, a good value is 40 or 80
    replace_file    - When creating tests you can specify replacements certain data types
                        *, #, ^, _ - For each wildcard the associated text is set instead of the wildcard
                        SET - Replaces the set with a single value, typically this will be one value from the set
                        BOT - Replaces the bot with a single value, typically this will be one value from the bot
    default         - Optional value which sets a default value for each answer

Example Output File:
(This file is created from the aiml file in y-bot\aiml\core\temporal\datetime_core.aiml)

"SEASON", "Winter", "Spring", "Summer", "Autumn", "Fall"
"DAY", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
"TOMORROW", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
"YEAR", "This is [0-9]*"
"NEXT YEAR", "[0-9]*"
"LAST YEAR", "[0-9]*"
"MONTH", "This is [January|February|March|April|May|June|July|August|September|October|November|December]"
"TIME", "The time is [0-9]{2}:[0-9]{2} [AM|PM]"
"DATE", "Today is *. [0-9]{2},[0-9]{4}"
"DAY PHASE", "Morning", "Noon", "Afternoon", "Night", "Midnight"
"DATE AND TIME", "The date and time is .* .* [0-9]* [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}"
"DAYS UNTIL CHRISTMAS", "[0-9]* days until Christmas."
"DAYS UNTIL JANUARY 01 2020", "[0-9]* days."
"DAYS UNTIL JANUARY 01", "-?[0-9]* days"
"DATE TOMORROW", "[0-9]{2},[0-9]{4}"

Example Replacement File:
    SET,animal:cow
    SET,animals:cows
    SET,number:2
    *:STAR
    #:HASH
    ^:ARROW
    _:UNDERLINE
