from __future__ import print_function
import random

# --------------- Main handler ------------------


def lambdaHandler(event, context):
   
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
        
        
#---------------------Events-------------------------------

def on_launch(launch_request, session):
    """ This function lets the user know more about skill when 
        they have not specified thier intent
    """
    return getWelcomeResponse()
    
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "GetWordIntent" or intent_name =="AMAZON.NextIntent":
        return getNewWordResponse(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return getHelpResponse()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handleSessionEndRequest()
    else:
        raise ValueError("Invalid intent") 
        
        
        
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +", sessionId=" + session['sessionId'])        
    
# --------------- Functions that control the skill's behavior ------------------


def getWelcomeResponse():
    
    #If we wanted to initialize the session to have some attributes we could
    #add those here
    session_attributes = {}
    card_title = "Hey Fella"
    speech_output = "Welcome to Synonym Teller" \
                    "You can know the synonym of a new word by saying " \
                    "tell the synonym"
    reprompt_text = "You can know the synonym of a new word by saying " \
                    "tell the synonym"
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)) 
        


def getHelpResponse():
    
    #If we wanted to initialize the session to have some attributes we could
    #add those here
    session_attributes = {}
    card_title = "Hey Fella"
    speech_output = "Welcome to Synonym Teller. " \
                    "I'm here to help you. You can know the synonym of a new word by saying " \
                    "tell the synonym. "
    reprompt_text = "You can know the synonym of a new word by saying " \
                    "tell the synonym. "
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)) 
        


def getNewWordResponse(intent,session):
    """ 
     Takes a new word tells its meaning and synonym
    """
    wO = [v for v in wordOptions if v[3] == 0]
    newWord = random.choice(wO)
    newWord[3]=1
        
    cardTitle = intent['name']
    sessionAttributes = {}
    shouldEndSession = False
    speechOutput = "A new word for you is-  " + newWord[0] + \
                    " Which means, " + newWord[1] + \
                    " and it's synonyms are , "  + newWord[2]
                    
    repromptText = "You can ask me a new tech word to add to your Vocabulary by saying, " \
                    "Tell me a new Tech Term"
                        
    return build_response(sessionAttributes, build_speechlet_response(cardTitle, speechOutput, repromptText, shouldEndSession))
        
        
def handleSessionEndRequest():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Synonym Teller. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
        
# ---------------- Responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title , 
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
        
# -----------------------------Words-----------------------------------   

wordOptions = [
      ["acme: "," the highest part or point "," height, apex, apogee, capstone, climax, crescendo, crest, crown, culmination, head, high noon, high tide", 0,1 ],
      ["baleful: "," threatening or foreshadowing evil or tragic developments "," forbidding, menacing, minacious, minatory, ominous, sinister, threatening", 0,1 ] ,
      ["bellicose: ","having or showing a ready disposition to fight "," battleful, combative,aggressive", 0,1 ],
      ["clique: "," a small close-knit group of people who do not readily allow others to join them "," coterie, circle, inner circle, crowd, in-crowd, set, club ", 0,1 ],
      ["callow: "," young and inexperienced "," fledgling, unfledged,inexperienced, inexperient ",0,1],
      ["dapper: "," marked by up-to-dateness in dress and manners"," dashing, jaunty, natty, raffish, rakish, snappy, spiffy, spruce ", 0,1 ],
      ["demeanor: "," the way a person behaves toward other people"," behavior, behaviour, conduct, demeanour, deportment", 0,1 ],
      ["elusive: "," Things that are elusive are hard to find, pin down, or remember"," artful,baffling, knotty, problematic,subtle", 0,1 ],
      ["empirical: "," it's based on observation rather than theory."," empiric,confirmable, falsifiable, verifiable",0,1 ],
      ["facetious: "," telling the most advanced form of comedy"," bantering, tongue-in-cheek,humorous, humourous",0,1 ],
      ["flourish: ","  growth"," boom, expand, thrive,fanfare, tucket",0,1 ],
      ["eccentric: ","  not having a common center; not concentric","bizarre, flakey,off-center, off-centered, quirky",0,1 ],
      ["equivocal: ","  uncertain as a sign or indication"," ambiguous, inconclusive, questionable",0,1 ],
      ["goggle: ","  look with amazement; look stupidly; a new way to say ; What are you looking at?! Try: What are you goggling at?!"," gape, gawk, gawp,look",0,1 ],
      ["gelid: ","  extremely cold"," arctic, frigid, glacial, icy, polar",0,1 ],
      ["howdy: ","  an expression of greeting"," hello, hi, how-do-you-do, hullo",0,1 ],
      ["hubris: ","  overbearing pride or presumption"," arrogance, haughtiness, hauteur, high-handedness, lordliness",0,1 ],
      ["inception: ","  an event that is a beginning;"," origin, origination",0,1 ],
      ["itinerant: ","  traveling from place to place to work"," unsettled, gipsy, gypsy",0,1 ],
      ["jocular: ","  characterized by jokes and good humor"," jesting, jocose, joking,jocosely",0,1 ],
      ["jejune: ","  lacking interest or significance or impact"," insipid,adolescent, juvenile, puerile",0,1 ],
      ["kamikaze: "," a pilot trained and willing to cause a suicidal crash", " airplane pilot,attack aircraft, fighter, fighter aircraft",0,1 ],
      ["kowtow: "," bend the knees and bow in a servile manner", " genuflect, scrape,bootlick, fawn ",0,1 ],
      ["latent: "," potentially existing but not presently evident or realized", " potential, inactive ",0,1 ],
      ["loquacious: "," full of trivial conversation", " chatty, gabby, garrulous, talkative, talky, voluble",0,1 ],
      ["melancholy: "," beyond sad", " depression,somber",0,1 ],
      ["magnanimous: "," noble and generous in spirit", " greathearted,noble,generous",0,1 ],
      ["narcissism: "," an exceptional interest in and admiration for yourself", "narcism, self-love",0,1 ],
      ["nympholepsy: "," a frenzy of emotion; as for something unattainable", " craze, delirium,frenzy, fury, hysteria ",0,1 ],
      ["otiose: "," serving no useful purpose; having no excuse for being", " pointless, purposeless, senseless, superfluous, faineant, indolent,futile, ineffectual, unavailing",0,1 ],
      ["ornery: "," having a difficult and contrary disposition", " crotchety, ornery",0,1 ],
      ["poignant: "," keenly distressing to the mind or feelings", " painful,affecting, touching",0,1 ],
      ["platitude: "," a trite or obvious remark", " banality, bromide, cliche, commonplace",0,1 ],
      ["quixotic: "," not sensible about practical matters; idealistic and unrealistic", " romantic, wild-eyed,impractical",0,1 ],
      ["quandary: "," state of uncertainty or perplexity especially as requiring a choice between equally unfavorable options", " dilemma,perplexity,conundrum",0,1 ],
      ["rapport: "," a relationship of mutual understanding or trust and agreement between people", " resonance,affintiy",0,1 ],
      ["ruminate: "," thinking deeply on a subject", " chew over, contemplate, excogitate, meditate,mull over, muse, ponder, reflect, speculate, think over",0,1 ],
      ["specious: "," an argument that seems to be good, correct, or logical, but is not so;deceptively pleasing", " spurious,gilded, meretricious",0,1 ],
      ["slovenly: "," messy or unkempt", " frowsy, frowzy",0,1 ],
      ["tenacious: "," stubbornly unyielding", " dogged, dour, persistent, pertinacious, unyielding, obstinate, stubborn ",0,1 ],
      ["trepidation: "," a feeling of alarm or dread", " apprehension, apprehensiveness, dread",0,1 ],
      ["upheaval: "," a violent or sudden change", " convulsion, agitation,  turbulence,hullabaloo, turmoil,",0,1 ],
      ["uxorious: "," foolishly fond of or submissive to your wife", " loving, devoted",0,1 ],
      ["vapid: "," lacking significance or liveliness ", " bland, flat, flavourless, insipid, savorless, savourless",0,1 ],
      ["venerable: "," profoundly honored", " august, revered",0,1 ],
      ["wuss: "," a person who is physically weak and ineffectual", " doormat, weakling",0,1 ],
      ["whimsical: "," indulging in or influenced by fancy", " capricious, impulsive,fanciful, notional",0,1 ],
      ["xenophobic: "," having abnormal fear or hatred of the strange ", " 	racist, afraid, ethnocentric",0,1 ],
      ["XT: "," the presence of an unwanted signal via an accidental coupling", " crosstalk, disturbance, interference, noise",0,1 ],
      ["yonder: "," distant but within sight ", " yon,distant",0,1 ],
      ["yearn: "," desire strongly or persistently", " hanker, desire, want",0,1 ],
      ["zap: "," strike suddenly and with force", " affect, impress, move",0,1 ],
      ["zit: "," a small inflamed elevation of the skin; ", " hickey, pimple",0,1 ]
      
      ]    
    

  
