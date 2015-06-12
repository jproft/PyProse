# grammar.py
#
# The grammar for PyProse

GRAMMAR = {

    "AdjUnit": [
        "#PushPlur #ForceSing Noun #PopPlur",
        "#PushPlur Substance #PopPlur",
        "9 Adjective",
        "6 InPresPart",
        "3 Possessive"
    ],

    "AdvbPhrase": [
        "!as #PushPlur Adverb !as Noun #PopPlur",
        "8 Adverb",
        "4 PrepPhrase"
    ],

    "CompPhrase": [
        "#PushPlur !as Adjective !as Noun #PopPlur",
        "#PushPlur !more Adjective !than Determiner Noun #PopPlur",
        "#PushPlur Adjective !as Noun #PopPlur"
    ],

    "DepClause": [
        "SubordConj !to IntransInf #ForceSing #ForceThird VerbPhrase",
        "5 SubordConj NounPhrase VerbPhrase",
        "8 SubordConj SubjPron VerbPhrase"
    ],

    "IndClause": [
        "!to IntransInf #ForceSing #ForceThird VerbPhrase",
        "NounPhrase @( NounPhrase @) VerbPhrase",
        "9 NounPhrase VerbPhrase",
        "6 SubjPron VerbPhrase"
    ],

    "IntrVbUnit": [
        "Adverb IntrVerb",
        "IntrVerb",
        "AuxInf !to IntransInf",
        "AuxVerb IntransInf",
        "Copula InPresPart",
        "2 IntrVerb",
        "ToHave InPastPart"
    ],

    "NounPhrase": [
        "!so #ForceSing Adjective IndefArt Noun",
        "!the Noun !of #PushPlur Substance #PopPlur",
        "#ForcePlur Noun",
        "4 Determiner AdjUnit Noun",
        "8 Determiner Noun",
        "3 NounPhrase PrepPhrase",
        "3 PossPron Noun",
        "Substance"
    ],

    "ObjPhrase": [
        "NounPhrase",
        "ObjPron"
    ],

    "PrepPhrase": [
        "!between #PushPlur Determiner Noun #PopPlur \
         !and #PushPlur Determiner Noun #PopPlur",
        "8 Prepos #PushPlur NounPhrase #PopPlur"
    ],

    "Question": [
        "#ForceThird ToHave NounPhrase InPastPart",
        "#ForceThird ToHave NounPhrase TrPastPart NounPhrase",
        "AuxVerb NounPhrase IntransInf",
        "AuxVerb NounPhrase TransInf NounPhrase",
        "IntObjPron #ForceThird Copula NounPhrase TrPresPart",
        "IntObjPron #ForceThird ToHave NounPhrase TrPastPart",
        "IntObjPron AuxVerb NounPhrase TransInf",
        "IntObjPron Copula SubjPron TrPresPart",
        "IntObjPron ToHave SubjPron TrPastPart",
        "IntPron #ForceThird Copula NounPhrase InPresPart",
        "IntPron #ForceThird ToHave NounPhrase InPastPart",
        "IntPron AuxVerb NounPhrase IntransInf",
        "IntPron Copula SubjPron InPresPart",
        "IntPron ToHave SubjPron InPastPart",
        "ToHave SubjPron InPastPart",
        "ToHave SubjPron TrPastPart NounPhrase"
    ],

    "Sentence": [
        "DepClause @, IndClause @, !and IndClause @.",
        "2 DepClause @, IndClause @.",
        "DepClause @, Question @?",
        "IndClause @, !and IndClause @.",
        "IndClause @, !but IndClause @.",
        "7 IndClause @.",
        "IndClause @; !and Sentence",
        "IndClause @; Sentence",
        "NounPhrase @- Question @?",
        "NounPhrase @: NounPhrase @.",
        "6 Question @?",
        "!he !who #ForceSing #ForceThird VerbPhrase VerbPhrase @."
    ],

    "TranVbUnit": [
        "Adverb TransVerb",
        "4 TransVerb",
        "AuxInf !to TransInf",
        "2 AuxVerb TransInf",
        "3 TransVerb",
        "Copula TrPresPart",
        "ToHave TrPastPart"
    ],

    "VerbPhrase": [
        "Copula NounPhrase",
        "IntrVbUnit",
        "TranVbUnit ObjPhrase"
    ]

}
