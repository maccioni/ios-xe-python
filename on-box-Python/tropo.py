call(['+14081234567'], {
   "callerID":'+140824680'
})

msg2 = "Dismiss or escalate?"

say("<speak><prosody rate='-20%'>"+msg+"</prosody></speak>", {"voice":"Susan"})

result = ask("<speak><prosody rate='-10%'>"+msg2+"</prosody></speak>", {
    "choices":"dismiss,escalate",
    "bargein":False,
    "voice":"Tom"
})
if (str(result.value)=='dismiss'):
     say('Dismissed. Goodbye!', {"voice":"Tom"})
if (str(result.value)=='escalate'):
    say('Escalating via call to your Manager, Jeff McLaughlin', {"voice":"Zoe"})
    message(msg, {
        "to":"+14081234567", "network":"SMS"})
    call(['+14081234567'], {
       "callerID":'+140824680'
    })
    msg3 = "Fabrizio has experience in Ansible, Python and integrating systems via APIs. Give him a 30% salary increse now."
    say("<speak><prosody rate='-20%'>"+msg3+"</prosody></speak>", {"voice":"Zoe"})
    msg4 = "Approve or Deny?"
    result2 = ask("<speak><prosody rate='-10%'>"+msg4+"</prosody></speak>", {
        "choices":"approve,deny",
        "bargein":False,
        "voice":"Zoe"
    })
    if (str(result2.value)=='approve'):
        say('Jeff McLaughlin, You are a great manager! Thank you', {"voice":"Zoe"})
