
Dialog Flow Generate
=====================

Given a simple set of steps and basic instructions generates a flow based conversational dialog

The first line of the csv should have the follow headers
```csv
Step,Prompt,Variable,Type,Next,Condition
```

Each preceeding line should then match these columns headers as follows

> Step - The name of the step, used to direct the flow
> Prompt - Text to display as the question ( template )
> Variable - The name of the variable capturing the user input
> Type - The type of the variable ( see below )
> Next - Next Step ( repeats see below )
> Condition - The condition that would move the flow to the Next Step ( repeats see below )

Type
----
BotFlow currenty supports the follow types of variable

> Int. A integer value that can have optional min and max restrictors
        Int         - Int no min or max value
        Int(m)      - Int with a max value
        Int(n,m)    - Int with a min n, and max m value
    If the validation fails then the same question is asked for again

> Select. A list of items for the user to select from.
        Select(Item1, Item2, ... Itemn)
    If the validation fails then the same question is asked for again

> Date. A date value in the format dd/mm/yyyy
    A future release will allow the developer to set the date validation format
    If the validation fails then the same question is asked for again

Entry/Exit
----------
Flowbot creates a single entry step called START 'FLOWNAME', which you can call from outside of the flowbot grammar.
Typically you would include in your grammar the following

    <category>
        <pattern>I WANT TO BOOK A FLIGHT</pattern>
        <template>
            <srai>START FLIGHTBOOK</srai>
        </template>
    </category>

When the conversation finishes, the bot calls EXECUTE 'FLOWNAME', This grammar is not included and you should create
your own static grammar to pick up the variables and process them. An example would be

    <category>
        <pattern>EXECUTE FLIGHTBOOK</pattern>
        <template>
            Ok, I'll book a flight matching the following:
            flying from <get name="City" />,
            <get name="London" />,
            to <get name="Destination" />,
            on <get name="Date" />,
            with <get name="Passengers" /> passengers,
            in <get name="Class" /> Class,
        </template>
    </category>

Next/Condition
--------------
A list of pairs consisting of a Destination tag which should be a valid step in a subsequent item and a condition
for which the step should be moved to. Typically this is one of the items from a Select statement. The first
of the pairs should be =* which is the default Step if no other validation succeeds or exists.


Example
-------
The example below shows all the currently available formats for a BotFlow csv file
It demonstrates a basic flow for booking a flight.
```csv
Step,Prompt,Variable,Type, Next, Condition
SOURCE,Where would you like to fly from,City,"Select(London, Edinburgh, Glasgow, Manchester)", DEST, =*, LONDON, =London
LONDON,Where from in London are you flying from,London,"Select(Stanstead, Heathrow, Gatwick)", DEST, =*
DEST,Where would you  like to fly to,Destination,"Select(New York, Washington, San Francisco)",DATE, =*
DATE,When would you like to fly,Date,Date(DD/MM/YYYY),PASSENGERS, =*
PASSENGERS,How many people are flying,Passengers,"Int(1,5)", CLASS, =*
CLASS,What class do you want to fly,Class,"Select(Economy, Premium Economy, Business, First)",
```
The steps are as follows
SOURCE - Ask the user which city they want to fly from
LONDON - If the user says London, an optional additional step that asks which airport in London to fly from
DEST - Where do they want to fly to
DATE - When do they want to fly
PASSENGERS - How many are flying ( between 1 and 5 allowed )
CLASS - Which class do they want to fly

