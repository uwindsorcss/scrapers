"""
Note: This parser has been taken from https://github.com/jere-mie/uwindsor-room-schedule
It is updated as of 2022/12/14.
If you're interested in using this parser, please check out that repository first to see if there is a more updated version.
If there is a more updated version, we'd appreciate if you could copy the contents here and make a pull request!

Below is an excerpt from the README of the original repository:

The parser works by extracting useful information from the text of the official UWindsor Timetable PDFs,
and generating a javascript file which has the data prepopulated into a handy object.

The parser should work for any term as long as the PDF format remains the same.

To run the parser for a new term, simply:

1. Grab the timetable PDF from [here](https://www.uwindsor.ca/registrar/541/timetable-information)
2. Copy and paste the contents of the PDF file into a new text file in the `data/` directory.
   For example, if the term is Winter 2024, create the file `data/W24.txt`
3. Edit the `term` variable in the `room_availability.py` file to the new term (in our above example, we would set it to `W24`)
4. Run the `room_availability.py` script
     - You should notice a new file, `data/W24.js` is created
5. Profit

If the format of the PDF changes, you may not get accurate results from the parser. This means you'll need to make
some adjustments to `room_availability.py` to get it working.
"""

import re

term = 'F22'

with open(f'data/{term}.txt', 'r') as f:
    # each room booking starts with "Section"
    text = f.read().split('Section')

    # removing new lines
    text = [i.replace('\n', '').strip() for i in text]

    # removing online courses
    text = filter(lambda x: 'synchronous' not in x.lower(), text)
    
    # removing trailing stuff
    text = [re.sub(r',\w+', '', i) for i in text]

    # removing more trailing stuff
    text = [re.sub(r' \(-\).+', '', i) for i in text]

    # removing dates
    text = [re.sub(r'\d\d\d\d-\d\d-\d\d', '', i) for i in text]

    # grabbing the info
    text = [re.search(r"(M|T|W|TH|F|MW|TTH) (\d\d:\d\d) (AM|PM) (\d\d:\d\d(AM|PM))(BiologyBuilding|Erie Hall|Dillon Hall|Toldo HealthEducationCtr|Chrysler HallSouth|Chrysler HallNorth|OdetteBuilding|LambtonTower|Essex Hall|MemorialHall|HK Building|EducationBuilding|LeddyLibrary|West Library|FreedomWay|JackmanDramatic ArtCntre|O'NeilMedicalEduc Centr)[ ]*(B\d+|G\d+|\d+)", i) for i in text]

    # filtering out stuff
    text = [i.groups() if i is not None else '' for i in text]
    text = list(filter(lambda x: x != '', text))

# unique elems only
text = list(set(text))

# out file
f = open(f'data/{term}.js', 'w')

# writing the JS object
f.write(f"const data = [\n")
for i in range(len(text)):
    f.write(f'    {{"day":"{text[i][0]}", "start":"{text[i][1]+text[i][2]}", "end":"{text[i][3]}", "building":"{text[i][5]}", "room":"{text[i][6]}"}}' + ',\n' if i != len(text)-1 else '\n')
f.write(']')
f.close()
print(f'Successfully parsed {len(text)} room bookings!')
