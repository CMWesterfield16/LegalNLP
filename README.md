# LegalStyleComparison

To run style comparison for both the Supreme Court opinions and State cases, run:
  ./run_system.sh

If you wish to just run one or the other, comment out the appropriate line in run_system.sh such that:
  - State: Only keep "python word_analysis_state.py"
  - Supreme Court: Only keep "python word_analysis_supreme_court.py"

The state data is too large to store on GitHub, thus you must download it from:
  https://case.law/

Once downloaded, please store each state in the following file path:
  "\_data/states/{NAMEOFSTATE}/"

Then put the unzipped file into this folder. Thus the data.jsonl.xz file should be located at:
  "\_data/states/{NAMEOFSTATE}/data/data.jsonl.xz"

You do not need to unzip the xz file prior to running the code, as the system works with the file while currently zipped. Since the file is so big, this is actually more space efficient. However, per state the program takes around two hours to run.
