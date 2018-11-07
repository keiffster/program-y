Implement sentiment analysis on the conversation

Factory pattern to load various sentiment analysis tools, e.g TextBlob

1) Each sentence should have individual sentiment score
2) Overall conversation should also have running score

Also provide sentiment grammar

How happy are you
    -> calls sentiment_service which returns value based on conversation sentiment score
        Very Unhappy, Unhappy, ok, happy, Very Happy
Is  a nI hate youice thing to say
    -> calls sentiment_service with "I hate you" and returns a value Yes, No, Maybe,
