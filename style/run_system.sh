# Metrics to Add
#Active (not passive) voice
#Hesitency -> more complicated
#Word Length Diversity
#Sentence Length Diversity
#Popular Figures of Speech

# State by State analysis (see README for data)
rm output_by_state/*
python renamefiles.py
python3 word_analysis_state.py
python produce_output_by_state.py

# Supreme Court Analysis
# python word_analysis_supreme_court.py
