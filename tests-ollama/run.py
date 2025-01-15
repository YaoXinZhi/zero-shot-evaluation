#!/bin/env python


import ollama


instruction = '''
You are an information extraction system. You respond to each message with a json-formatted summary of named entities in the message. Each named entity appears as one entry in a json-formatted list. Each entity must have two properties, its type and its name. Only include entity names that appear in the text. The entity types are:
-	Plant pest
-	Insect vector
-	Host plant
-	Disease
-	Geographic location

You are an information extraction system that extracts entities from messages as before. You also extract oriented relationships between entities. The list of relationships to be extracted by you is : 
- Located in 
- Causes 
- Have been found on. 
The types of entities that are arguments of the relationships are fixed by me. The argument type of each relationship is in brackets. The first argument is before the relationship. The second argument is after the relationship. 
- [pest] Located in [geographical location] 
- [pest] Causes [disease] 
- [pest] Have been found on [host plant]. 
The arguments of the relationships must be entities. You must absolutely respect the type of the relationship arguments. This is very important.'''


document = '''
The bacterium 'Xylella Fastidiosa' was detected in nine more places in the Porto Metropolitan Area, mainly in citrus, and the demarcated area was extended, revealed this Monday the Confederation of Farmers of Portugal (CAP). "As a result of the confirmation of the presence of the bacterium 'Xylella Fastidiosa' in nine new locations, in the municipalities of Vila Nova de Gaia, Santa Maria da Feira, Porto and Espinho."
'''


response = ollama.chat(
    model='mistral', messages=[
    {
     'role': 'user',
     'content': instruction,
     },
    {
     'role': 'user',
     'content': 'Message: ' + document,
     },
     ],
    )

print(response['message']['content'])
