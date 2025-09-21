"""
dateparser handles natural language dates (tomorrow, next Tue, in 3 days, etc.). We set RELATIVE_BASE so parsing is anchored to the current time.

regex (TIME_RE) finds patterns like 2h, 30min, 45 minutes.

spaCy is used to extract noun chunks (best short human titles).

Importance is inferred from short keyword lists (high/medium/low). You can also let users explicitly tag importance in the UI.

The function returns a dictionary with parsed fields you can feed into the prioritizer."""

import re
from datetime import datetime
import dateparser
import spacy

# ============= Load mmodel ================
nlp = spacy.load('en_core_web_sm')

# ============== regrex to capture time expression =================
TIME_RE = re.compile(r'(\d+)\s*(h|hr|hour|hours|m|min|minute|minutes)\b', re.IGNORECASE)
# ============== Keywords for Importance ===================
HIGH_WORDS = ('urgent', 'asap', 'immediately', 'high', 'important', 'priority')
MED_WORDS = {'medium', 'normal', 'typical'}
LOW_WORDS = {'low', 'later', 'someday'}

def parse_task(text, reference=None):
    """Parse a task string and return a dict
    {'raw' : original text, 'title' : short title, 'due' : datetime or None, 'est_minutes' : int or None, 'importance' : 2|1|0|None}
    """
    
    if not text or not text.strip():
        return None
    
    reference = reference or datetime.now()
    
    # parse date (dateparser handles natural language)
    # Use RELTIVE_BASE so tomorrow or next_tue is reltive to reference
    
    try:
        due = dateparser.parse(text, settings={'RELATIVE_BASE': reference, 'PREFER_DATES_FROM': 'future'})
    except Exception:
        due = None
        
    
    # estimate minutes using regex for time mentions
    est_minutes = None
    m = TIME_RE.search(text)
    if m:
        val = int(m.group(1))
        unit = m.group(2).lower()
        
        if unit.startswith('h'):
            est_minutes = val  * 60
        else:
            est_minutes = val
    
    # infer importance from keywords
    lowered = text.lower()
    importance = None
    if any(w in lowered for w in HIGH_WORDS):
        importance = 0
    elif any(w in lowered for w in MED_WORDS):
        importance = 1
    elif any(w in lowered for w in LOW_WORDS):
        importance = -1
        
    
    # build a short title using spacy noun chuncks
    doc = nlp(text)
    title = None
    
    # Try 1 first noun chunck (clened)
    noun_chunks = [chunk.text.strip() for chunk in doc.noun_chunks if len (chunk.text.strip()) > 2]
    
    if noun_chunks:
        title = noun_chunks[0]
    else:
        # Try2: first Verb + object or first sentence
        verbs = [tok for tok in doc if tok.pos_ == 'VERB']
        if verbs:
            # build short phrase around the first verb
            v = verbs[0]
            span = doc[v.left_edge.i : v.right_edge.i + 1].text.strip()
            title = span
        else:
            title = text.strip()
    
    # clean text a bit: remove tralling commas/phrase like '~2h', or 'high importance
    # remove parental content
    title = re.sub(r'\(.*?\)|\[.*?\]', '', title).strip()
    # remove commoon trailling fragments like ", ~2h"
    title = re.sub(r',\s*~?\d+\s*(h|hr|hour|m|min).*', '', title, flags=re.IGNORECASE).strip()
    
    #if title to loog, truncate
    if len(title) > 80:
        title = title[:77].rstrip() + '...'
    
    return {'raw': text, 'title': title, 'due': due, 'est_minutes': est_minutes, 'importance': importance}

# Small demo when running the file directly
if __name__ == "__main__":
    examples = [
        "Finish slides for meeting next Tue, ~2h, high importance",
        "Buy groceries tomorrow",
        "Refactor logging, 30min",
        "Call John ASAP about the budget",
        "Write blog post sometime next month",
        "Prepare presentation (2 hours) by Friday",
        "Quick email to manager, 10 min, low priority"
    ]

 
    print("Reference now:", datetime.now().isoformat())
    for t in examples:
        try:
            parsed = parse_task(t)
            if parsed is not None:
                print("-" * 60)
                print("Raw:", parsed['raw'])
                print("Title:", parsed['title'])
                print("Due:", parsed['due'])
                print("Est minutes:", parsed['est_minutes'])
                print("Importance:", parsed['importance'])
            else:
                print(f"Parsed is None for: '{t}'")
        except Exception as e:
            print(f"Error parsing '{t}': {e}")            