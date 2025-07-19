import streamlit as st
import sys
import pandas as pd
import random
#from IPython.display import clear_output
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('CopticVocab.csv')

noundf = df[df['PartOfSpeech'].isin(['Noun', 'Pronoun'])]
# noundf.head()

artdf = df[df['PartOfSpeech'].isin(['Article'])]
#artdf.head()

genders = ['M', 'F']
numbers = ['Sg', 'Pl']

# Sample word generator (replace with your own logic)
def generate_puzzle():
    # random choice 1
    # here's how we randomly select a noun/pronoun
    ourchoice = random.choice(range(noundf.shape[0]))
    POS = noundf.iloc[ourchoice, 5]

    if POS == 'Noun':
        # do noun stuff
        
        # random choice 2: pick a grammatical number
            # this is hardcoded per row for pronoun lemmas so we skip it below
        ournumber = random.choice(numbers)
        # we read off the random noun's grammatical gender
        thisgender = noundf.iloc[ourchoice, 6]
        # and winnow down to eligible articles
        artoptions = artdf[artdf['Gender'].isin([thisgender]) | artdf['Gender'].isna()]
        
        if ournumber == 'Pl':
            # random choice 3
            # here's how we randomly select an eligible article
            artoptions = artoptions[~ artoptions['Foreign Plural'].isna()]
            artchoice = random.choice(range(artoptions.shape[0]))    
            
            # we need to compose the Coptic
            # NIM changes the word order
            if artdf.iloc[artchoice, 2] == 'ⲛⲓⲙ':        
                # some coptic words have diff PL forms
                if not pd.isna(noundf.iloc[ourchoice, 2]):
                    coptic =  str(noundf.iloc[ourchoice, 2]) + " " + str(artdf.iloc[artchoice, 2])
                else: 
                    coptic =  str(noundf.iloc[ourchoice, 1]) + " " + str(artdf.iloc[artchoice, 2])
            else: 
                if not pd.isna(noundf.iloc[ourchoice, 2]):                
                    coptic = str(artdf.iloc[artchoice, 2]) + "-" + str(noundf.iloc[ourchoice, 2])
                else: 
                    coptic = str(artdf.iloc[artchoice, 2]) + "-" + str(noundf.iloc[ourchoice, 1])
                    
            # we need to construct the desired English
            if not pd.isna(noundf.iloc[ourchoice, 4]):
                english = str(artdf.iloc[artchoice, 4]) + " " + str(noundf.iloc[ourchoice, 4]).lower()
            ### print(noundf.iloc[ourchoice, 4])
            else:
                # we also need to construct the desired English
                english = str(artdf.iloc[artchoice, 4]) + " " + noundf.iloc[ourchoice, 3].split(",")[0].lower() + "s"
                
        else:
            artoptions = artoptions[~ artoptions['Foreign'].isna()]
            artchoice = random.choice(range(artoptions.shape[0]))   
            # we need to construct the desired English
            english = str(artdf.iloc[artchoice, 3]) + " " + str(noundf.iloc[ourchoice, 3].split(",")[0]).lower()
            # we also need to compose the Coptic
            coptic = str(artdf.iloc[artchoice, 1]) + "-" + str(noundf.iloc[ourchoice, 1]) 

    elif POS == 'Pronoun':
        # do pronoun stuff
        english = noundf.iloc[ourchoice, 3]
        coptic = noundf.iloc[ourchoice, 1]

    return {
        "prompt": f"How do you say '{coptic}' in English?",
        "answer": english
    }


# Initialize session state
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle()
    st.session_state.show_answer = False

# Title
st.title("Welcome to the Coptic Vocab Reviewer! 🇪🇬𓂀⛪")

# Puzzle prompt (always shown)
st.markdown(f"🔍 **Puzzle:** {st.session_state.puzzle['prompt']}")

# Answer area
answer_placeholder = st.empty()

if st.session_state.show_answer:
    answer_placeholder.markdown(f"✅ **Answer:** {st.session_state.puzzle['answer']}")
else:
    # Reserve space for layout consistency
    answer_placeholder.markdown("<div style='height: 42px'></div>", unsafe_allow_html=True)

# Button logic — single click toggles state correctly
button_clicked = st.button("Next word please")

if button_clicked:
    if st.session_state.show_answer:
        # Go to next puzzle
        st.session_state.puzzle = generate_puzzle()
        st.session_state.show_answer = False
    else:
        # Reveal the answer
        st.session_state.show_answer = True

st.markdown("---")  # Optional horizontal rule

st.markdown("ℹ️ **Instructions:** Click the button to reveal the English. Click again to get a new word/phrase.")
st.markdown("𓂀𓋹𓁈𓃠𓆃☥𓆣")
