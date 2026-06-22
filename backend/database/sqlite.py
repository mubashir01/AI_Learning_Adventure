import sqlite3
from collections import defaultdict, deque
from pathlib import Path
from random import choice

from services.xp import calculate_xp

DB_PATH = Path(__file__).resolve().parents[2] / "database" / "app.db"
RECENT_QUESTIONS = defaultdict(lambda: deque(maxlen=12))

SEED_QUESTIONS = [
    ("Mathematics", "Easy", "What is 4 + 3?", "5|6|7|8", "7"),
    ("Mathematics", "Easy", "What is 10 - 6?", "2|3|4|5", "4"),
    ("Mathematics", "Easy", "What is 5 x 2?", "7|10|12|15", "10"),
    ("Mathematics", "Easy", "What is 18 divided by 3?", "3|6|9|12", "6"),
    ("Mathematics", "Easy", "Which number is even?", "7|9|12|15", "12"),
    ("Mathematics", "Easy", "What is 25 + 5?", "20|25|30|35", "30"),
    ("Mathematics", "Easy", "What is 14 - 8?", "4|5|6|7", "6"),
    ("Mathematics", "Easy", "How many sides does a triangle have?", "2|3|4|5", "3"),
    ("Mathematics", "Easy", "What is half of 20?", "5|10|15|20", "10"),
    ("Mathematics", "Easy", "What number comes after 49?", "48|49|50|51", "50"),
    ("Mathematics", "Medium", "What is 6 x 4?", "18|20|24|28", "24"),
    ("Mathematics", "Medium", "What is 45 divided by 5?", "8|9|10|11", "9"),
    ("Mathematics", "Medium", "What is 12 + 18?", "28|30|32|36", "30"),
    ("Mathematics", "Medium", "What is 7 x 8?", "48|54|56|64", "56"),
    ("Mathematics", "Medium", "What is 100 - 37?", "53|63|67|73", "63"),
    ("Mathematics", "Medium", "Which fraction equals one half?", "1/3|2/4|3/5|4/6", "2/4"),
    ("Mathematics", "Medium", "What is the perimeter of a square with side 5?", "10|15|20|25", "20"),
    ("Mathematics", "Medium", "What is 9 squared?", "18|72|81|90", "81"),
    ("Mathematics", "Medium", "What is 3/4 of 20?", "10|12|15|18", "15"),
    ("Mathematics", "Medium", "What is the next number: 4, 8, 12, 16?", "18|20|22|24", "20"),
    ("Mathematics", "Hard", "What is 15 percent of 200?", "15|20|30|45", "30"),
    ("Mathematics", "Hard", "Solve: 3 x (8 + 4)", "24|30|36|42", "36"),
    ("Mathematics", "Hard", "What is the area of a rectangle 9 by 6?", "15|30|54|60", "54"),
    ("Mathematics", "Hard", "What is 2.5 + 3.75?", "5.25|6.25|6.75|7.25", "6.25"),
    ("Mathematics", "Hard", "If x + 12 = 30, what is x?", "12|16|18|20", "18"),
    ("Mathematics", "Hard", "What is the average of 6, 8, 10, and 12?", "8|9|10|11", "9"),
    ("Mathematics", "Hard", "What is 144 divided by 12?", "10|11|12|14", "12"),
    ("Mathematics", "Hard", "Which is a prime number?", "21|27|29|33", "29"),
    ("Mathematics", "Hard", "What is 5 cubed?", "15|25|75|125", "125"),
    ("Mathematics", "Hard", "A book costs 80 after a 20 discount. What was the original price?", "90|96|100|120", "100"),
    ("English", "Easy", "Which word is a noun?", "Run|Happy|Book|Quickly", "Book"),
    ("English", "Easy", "Choose the correct spelling.", "Cat|Kat|Catt|Katt", "Cat"),
    ("English", "Easy", "Which word is an action?", "Jump|Blue|Chair|Soft", "Jump"),
    ("English", "Easy", "What is the opposite of hot?", "Warm|Cold|Fast|Tall", "Cold"),
    ("English", "Easy", "Which sentence ends with a question mark?", "I like apples.|Where are you|Run fast.|The sun is bright.", "Where are you"),
    ("English", "Easy", "Which word rhymes with play?", "Tree|Day|Moon|Book", "Day"),
    ("English", "Easy", "Which word means more than one child?", "Childs|Childes|Children|Childrens", "Children"),
    ("English", "Easy", "Choose the adjective.", "Green|Run|Table|Swim", "Green"),
    ("English", "Easy", "Which word is a pronoun?", "He|House|Laugh|Bright", "He"),
    ("English", "Easy", "Which word should start a sentence?", "small letter|capital letter|number|comma", "capital letter"),
    ("English", "Medium", "Choose the correct spelling.", "Frend|Friend|Freind|Frynd", "Friend"),
    ("English", "Medium", "Which sentence is correct?", "She go home.|She goes home.|She going home.|She gone home.", "She goes home."),
    ("English", "Medium", "What is the past tense of run?", "Runned|Ran|Running|Runs", "Ran"),
    ("English", "Medium", "Which word is an adverb?", "Slowly|Slow|Slowness|Slowed", "Slowly"),
    ("English", "Medium", "Choose the synonym for happy.", "Sad|Glad|Angry|Tired", "Glad"),
    ("English", "Medium", "Choose the antonym for ancient.", "Old|Modern|Historic|Early", "Modern"),
    ("English", "Medium", "Which sentence uses a comma correctly?", "After lunch, we played.|After, lunch we played.|After lunch we, played.|After lunch we played,", "After lunch, we played."),
    ("English", "Medium", "Which word is plural?", "Mouse|Mice|Man|Woman", "Mice"),
    ("English", "Medium", "What is the subject in: The dog barked loudly?", "The dog|Barked|Loudly|Dog barked", "The dog"),
    ("English", "Medium", "Which word completes this sentence: I have ___ apple.", "a|an|the|and", "an"),
    ("English", "Hard", "Which sentence uses their correctly?", "Their going home.|They left their bags.|There bags are red.|They are over their.", "They left their bags."),
    ("English", "Hard", "Identify the compound sentence.", "I ran because I was late.|I ran, and I caught the bus.|Running quickly, I smiled.|The fast bus arrived.", "I ran, and I caught the bus."),
    ("English", "Hard", "Which word is a metaphor?", "The classroom was a zoo.|He ran like wind.|The bell rang loudly.|She smiled brightly.", "The classroom was a zoo."),
    ("English", "Hard", "Choose the correct form: Neither boy ___ ready.", "are|were|is|be", "is"),
    ("English", "Hard", "Which sentence is in passive voice?", "The chef cooked dinner.|Dinner was cooked by the chef.|The chef is cooking.|The chef cooks well.", "Dinner was cooked by the chef."),
    ("English", "Hard", "What is the main clause in: When it rained, we stayed inside?", "When it rained|We stayed inside|It rained|Stayed inside", "We stayed inside"),
    ("English", "Hard", "Which word best means careful and exact?", "Careless|Precise|Rapid|Ordinary", "Precise"),
    ("English", "Hard", "Choose the correctly punctuated sentence.", "Yes I can help.|Yes, I can help.|Yes I, can help.|Yes I can, help.", "Yes, I can help."),
    ("English", "Hard", "Which sentence uses an apostrophe correctly?", "The dogs bone is big.|The dog's bone is big.|The dogs' bone is big for one dog.|The dog bone's is big.", "The dog's bone is big."),
    ("English", "Hard", "What is the tone of: I cannot wait for the trip!", "Excited|Bored|Angry|Confused", "Excited"),
    ("Science", "Easy", "Which planet do we live on?", "Mars|Earth|Venus|Jupiter", "Earth"),
    ("Science", "Easy", "What do plants need to make food?", "Moonlight|Sunlight|Plastic|Smoke", "Sunlight"),
    ("Science", "Easy", "What do humans breathe in?", "Oxygen|Sand|Smoke|Salt", "Oxygen"),
    ("Science", "Easy", "Which animal is a mammal?", "Frog|Fish|Dog|Lizard", "Dog"),
    ("Science", "Easy", "What is water's solid form?", "Steam|Ice|Cloud|Rain", "Ice"),
    ("Science", "Easy", "Which sense uses the eyes?", "Taste|Touch|Sight|Smell", "Sight"),
    ("Science", "Easy", "What pulls objects toward Earth?", "Gravity|Light|Sound|Heat", "Gravity"),
    ("Science", "Easy", "Which part of a plant takes in water?", "Flower|Leaf|Root|Seed", "Root"),
    ("Science", "Easy", "What star gives Earth light?", "Moon|Sun|Mars|Polaris", "Sun"),
    ("Science", "Easy", "Which material is magnetic?", "Wood|Plastic|Iron|Paper", "Iron"),
    ("Science", "Medium", "Which organ pumps blood?", "Lungs|Brain|Heart|Stomach", "Heart"),
    ("Science", "Medium", "What is evaporation?", "Liquid changing to gas|Gas changing to liquid|Solid changing to liquid|Water freezing", "Liquid changing to gas"),
    ("Science", "Medium", "Which gas do plants take in?", "Oxygen|Carbon dioxide|Helium|Nitrogen only", "Carbon dioxide"),
    ("Science", "Medium", "What is the main source of energy for Earth's weather?", "The Sun|The Moon|Volcanoes|Oceans only", "The Sun"),
    ("Science", "Medium", "Which part of the body controls thinking?", "Heart|Brain|Liver|Lungs", "Brain"),
    ("Science", "Medium", "What is a habitat?", "An animal's home|A type of food|A weather tool|A rock layer", "An animal's home"),
    ("Science", "Medium", "Which force slows a rolling ball?", "Friction|Gravity only|Magnetism|Light", "Friction"),
    ("Science", "Medium", "What is the boiling point of water in Celsius?", "0|50|100|150", "100"),
    ("Science", "Medium", "Which simple machine is a ramp?", "Lever|Pulley|Inclined plane|Wheel", "Inclined plane"),
    ("Science", "Medium", "What do food chains show?", "Energy moving between living things|Weather patterns|Rock ages|Planet sizes", "Energy moving between living things"),
    ("Science", "Hard", "Which process makes glucose in plants?", "Respiration|Photosynthesis|Condensation|Digestion", "Photosynthesis"),
    ("Science", "Hard", "What happens to particles when a solid melts?", "They stop moving|They move more freely|They disappear|They become smaller atoms", "They move more freely"),
    ("Science", "Hard", "Which system carries oxygen-rich blood around the body?", "Digestive system|Circulatory system|Skeletal system|Nervous system", "Circulatory system"),
    ("Science", "Hard", "Why does the Moon appear to change shape?", "Its phases change as it orbits Earth|It grows smaller|Clouds cover it forever|It makes its own light", "Its phases change as it orbits Earth"),
    ("Science", "Hard", "What is an adaptation?", "A helpful trait for survival|A type of weather|A broken bone|A planet's path", "A helpful trait for survival"),
    ("Science", "Hard", "Which item is a conductor of electricity?", "Rubber|Glass|Copper|Dry wood", "Copper"),
    ("Science", "Hard", "What causes day and night?", "Earth rotating|Earth changing size|The Moon spinning Earth|Clouds moving", "Earth rotating"),
    ("Science", "Hard", "Which layer protects Earth from many harmful ultraviolet rays?", "Ozone layer|Crust|Core|Mantle", "Ozone layer"),
    ("Science", "Hard", "What is density?", "Mass per unit volume|Weight only|Length of an object|How hot something is", "Mass per unit volume"),
    ("Science", "Hard", "Which statement best describes a balanced ecosystem?", "Producers, consumers, and resources stay in healthy amounts|Only predators survive|No plants grow|All animals eat the same food", "Producers, consumers, and resources stay in healthy amounts"),
    ("General Knowledge", "Easy", "How many days are in a week?", "5|6|7|8", "7"),
    ("General Knowledge", "Easy", "Which color is made by mixing red and white?", "Pink|Green|Blue|Black", "Pink"),
    ("General Knowledge", "Easy", "What do we use to tell time?", "Clock|Plate|Pencil|Shoe", "Clock"),
    ("General Knowledge", "Easy", "How many months are in a year?", "10|11|12|13", "12"),
    ("General Knowledge", "Easy", "Which vehicle travels on rails?", "Train|Boat|Plane|Bicycle", "Train"),
    ("General Knowledge", "Easy", "Which meal is usually eaten in the morning?", "Breakfast|Dinner|Supper|Dessert", "Breakfast"),
    ("General Knowledge", "Easy", "What is the capital of Pakistan?", "Karachi|Lahore|Islamabad|Quetta", "Islamabad"),
    ("General Knowledge", "Easy", "Which shape has four equal sides?", "Circle|Triangle|Square|Oval", "Square"),
    ("General Knowledge", "Easy", "Which object is used for writing?", "Pencil|Spoon|Blanket|Cup", "Pencil"),
    ("General Knowledge", "Easy", "How many wheels does a bicycle usually have?", "1|2|3|4", "2"),
    ("General Knowledge", "Medium", "Which continent is Egypt in?", "Asia|Africa|Europe|Australia", "Africa"),
    ("General Knowledge", "Medium", "Which ocean is the largest?", "Atlantic|Indian|Arctic|Pacific", "Pacific"),
    ("General Knowledge", "Medium", "Who wrote many plays including Hamlet?", "William Shakespeare|Charles Dickens|Jane Austen|Mark Twain", "William Shakespeare"),
    ("General Knowledge", "Medium", "Which instrument has black and white keys?", "Guitar|Piano|Drum|Flute", "Piano"),
    ("General Knowledge", "Medium", "Which country is famous for the Eiffel Tower?", "Italy|France|Spain|Germany", "France"),
    ("General Knowledge", "Medium", "What is the currency of Japan?", "Yen|Dollar|Euro|Rupee", "Yen"),
    ("General Knowledge", "Medium", "Which sport uses a bat and wickets?", "Cricket|Tennis|Football|Swimming", "Cricket"),
    ("General Knowledge", "Medium", "How many minutes are in two hours?", "60|90|120|180", "120"),
    ("General Knowledge", "Medium", "Which device helps people find directions?", "Compass|Thermometer|Microscope|Speaker", "Compass"),
    ("General Knowledge", "Medium", "Which language is widely spoken in Brazil?", "Spanish|Portuguese|French|Arabic", "Portuguese"),
    ("General Knowledge", "Hard", "Which ancient civilization built pyramids at Giza?", "Egyptians|Romans|Vikings|Aztecs", "Egyptians"),
    ("General Knowledge", "Hard", "Which line divides Earth into Northern and Southern Hemispheres?", "Equator|Prime Meridian|Tropic of Cancer|Arctic Circle", "Equator"),
    ("General Knowledge", "Hard", "Which organization works for global health?", "WHO|FIFA|NASA|OPEC", "WHO"),
    ("General Knowledge", "Hard", "What is the longest river commonly listed in the world?", "Nile|Amazon|Indus|Danube", "Nile"),
    ("General Knowledge", "Hard", "Which country has the city of Kyoto?", "China|Japan|Thailand|Vietnam", "Japan"),
    ("General Knowledge", "Hard", "Which explorer is linked with the first voyage around the world?", "Ferdinand Magellan|Marco Polo|Ibn Battuta|Neil Armstrong", "Ferdinand Magellan"),
    ("General Knowledge", "Hard", "Which planet is known for its large rings?", "Mercury|Venus|Saturn|Mars", "Saturn"),
    ("General Knowledge", "Hard", "What does UNESCO help protect?", "World heritage and education|Only sports rules|Bank accounts|Weather forecasts", "World heritage and education"),
    ("General Knowledge", "Hard", "Which mountain range includes Mount Everest?", "Andes|Alps|Himalayas|Rockies", "Himalayas"),
    ("General Knowledge", "Hard", "Which event started in 1896 in its modern international form?", "Olympic Games|World Cup|Cricket World Cup|Commonwealth Games", "Olympic Games"),
]

QUESTION_BANKS = {
    ("Mathematics", "Easy"): [
        ("What is 8 + 6?", "12|13|14|16", "14"),
        ("What is 20 - 9?", "9|10|11|12", "11"),
        ("What is 3 x 5?", "8|12|15|18", "15"),
        ("What is 24 divided by 4?", "4|5|6|8", "6"),
        ("Which number is odd?", "10|12|15|18", "15"),
        ("What is 30 + 12?", "40|41|42|44", "42"),
        ("What is 16 - 7?", "7|8|9|10", "9"),
        ("How many sides does a rectangle have?", "3|4|5|6", "4"),
        ("What is double 9?", "16|18|20|22", "18"),
        ("What is 100 - 25?", "65|70|75|80", "75"),
        ("How many cents make one dollar?", "10|25|50|100", "100"),
        ("What is 2 tens and 5 ones?", "20|25|52|205", "25"),
        ("Which number is greater than 60?", "45|59|61|30", "61"),
        ("What is 7 + 8?", "13|14|15|16", "15"),
        ("What is 6 x 3?", "15|18|21|24", "18"),
        ("What is one quarter of 8?", "1|2|3|4", "2"),
        ("What is 11 + 11?", "20|21|22|23", "22"),
        ("How many minutes are in one hour?", "30|45|60|90", "60"),
        ("Which shape has no corners?", "Square|Triangle|Circle|Rectangle", "Circle"),
        ("What is 5 more than 37?", "40|41|42|43", "42"),
        ("What is 48 divided by 6?", "6|7|8|9", "8"),
        ("Which number comes before 90?", "88|89|90|91", "89"),
        ("What is 4 x 4?", "12|14|16|18", "16"),
        ("What is 33 - 13?", "18|19|20|21", "20"),
        ("How many equal parts are in a half?", "1|2|3|4", "2"),
        ("What is 9 + 9?", "16|17|18|19", "18"),
        ("What is 40 divided by 5?", "6|7|8|9", "8"),
        ("Which number has a 7 in the tens place?", "17|27|72|87", "72"),
        ("What is 6 more than 28?", "32|33|34|35", "34"),
        ("How many sides does a pentagon have?", "4|5|6|8", "5"),
        ("What is 50 - 15?", "25|30|35|40", "35"),
        ("What is 3 groups of 7?", "18|20|21|24", "21"),
        ("Which is the smallest number?", "38|29|41|30", "29"),
        ("What is 12 divided by 2?", "4|5|6|8", "6"),
        ("What is 1 more than 999?", "100|900|1000|1001", "1000"),
        ("What is 13 + 6?", "17|18|19|20", "19"),
        ("What is 4 less than 31?", "25|26|27|28", "27"),
        ("Which number is a multiple of 10?", "22|35|40|51", "40"),
        ("What is 2 x 9?", "16|17|18|20", "18"),
        ("What is 70 + 5?", "57|65|75|80", "75"),
    ],
    ("General Knowledge", "Hard"): [
        ("Which line marks zero degrees longitude?", "Equator|Prime Meridian|Tropic of Capricorn|International Date Line", "Prime Meridian"),
        ("Which document lists basic human rights adopted by the United Nations in 1948?", "Universal Declaration of Human Rights|Magna Carta|Kyoto Protocol|Geneva Map", "Universal Declaration of Human Rights"),
        ("Which country contains Machu Picchu?", "Peru|Mexico|Chile|Greece", "Peru"),
        ("What does GDP mainly measure?", "Total value of goods and services produced|Number of citizens|Size of a country's army|Amount of rainfall", "Total value of goods and services produced"),
        ("Which canal connects the Mediterranean Sea and the Red Sea?", "Panama Canal|Suez Canal|Erie Canal|Grand Canal", "Suez Canal"),
        ("Which city hosted the first modern Olympic Games in 1896?", "Athens|Paris|London|Rome", "Athens"),
        ("Which branch of government interprets laws in many democracies?", "Judicial|Executive|Legislative|Municipal", "Judicial"),
        ("Which treaty ended World War I?", "Treaty of Versailles|Treaty of Paris|Treaty of Tordesillas|Treaty of Rome", "Treaty of Versailles"),
        ("Which desert is the largest hot desert?", "Sahara|Gobi|Kalahari|Thar", "Sahara"),
        ("Which organization publishes the World Heritage list?", "UNESCO|WHO|WTO|FIFA", "UNESCO"),
        ("Which invention is Johannes Gutenberg best known for improving?", "Printing press|Steam engine|Telescope|Compass", "Printing press"),
        ("Which mountain range separates parts of Europe and Asia?", "Ural Mountains|Andes|Atlas Mountains|Alps", "Ural Mountains"),
        ("Which country has both Maori and English as official languages?", "New Zealand|Canada|India|Brazil", "New Zealand"),
        ("What does a constitution usually describe?", "Basic laws and government structure|Daily weather records|School lunch menus|Sports scores", "Basic laws and government structure"),
        ("Which sea lies between Europe and Africa?", "Mediterranean Sea|Caribbean Sea|Baltic Sea|Bering Sea", "Mediterranean Sea"),
        ("Which ancient trade route connected China with Europe?", "Silk Road|Amber Road|Route 66|Inca Trail", "Silk Road"),
        ("Which body of water is the world's largest ocean?", "Pacific Ocean|Atlantic Ocean|Indian Ocean|Arctic Ocean", "Pacific Ocean"),
        ("Which country is known for the Taj Mahal?", "India|Iran|Turkey|Egypt", "India"),
        ("Which international group helps settle disputes between countries at the Hague?", "International Court of Justice|World Bank|Olympic Committee|Red Cross", "International Court of Justice"),
        ("Which calendar is most widely used internationally today?", "Gregorian calendar|Mayan calendar|Julian calendar|Lunar calendar", "Gregorian calendar"),
        ("Which force keeps satellites in orbit around Earth?", "Gravity|Friction|Magnetism only|Sound", "Gravity"),
        ("Which European city is known as the seat of the European Union's main institutions?", "Brussels|Madrid|Vienna|Lisbon", "Brussels"),
        ("Which river flows through London?", "Thames|Seine|Danube|Rhine", "Thames"),
        ("Which country has the Great Barrier Reef nearby?", "Australia|South Africa|Japan|Norway", "Australia"),
        ("Which term means a government by elected representatives?", "Republic|Monarchy|Empire|Tribe", "Republic"),
        ("Which scientist developed the theory of relativity?", "Albert Einstein|Isaac Newton|Marie Curie|Charles Darwin", "Albert Einstein"),
        ("Which language family includes Spanish, French, and Italian?", "Romance languages|Germanic languages|Slavic languages|Semitic languages", "Romance languages"),
        ("Which event is measured by the Richter scale?", "Earthquake strength|Wind speed|Rainfall|Ocean depth", "Earthquake strength"),
        ("Which country is both a continent and a nation?", "Australia|Greenland|Japan|Madagascar", "Australia"),
        ("Which city is famous for canals and gondolas?", "Venice|Berlin|Prague|Dublin", "Venice"),
        ("Which term means the right to vote?", "Suffrage|Inflation|Migration|Diplomacy", "Suffrage"),
        ("Which country gifted the Statue of Liberty to the United States?", "France|Spain|Canada|Italy", "France"),
        ("Which layer of Earth is liquid and lies around the inner core?", "Outer core|Crust|Mantle|Lithosphere", "Outer core"),
        ("Which region is known as the Amazon Basin?", "A large South American rainforest region|A mountain chain in Europe|A desert in Africa|A plain in Australia", "A large South American rainforest region"),
        ("Which term describes goods brought into a country?", "Imports|Exports|Votes|Treaties", "Imports"),
        ("Which global event is held every four years for national football teams?", "FIFA World Cup|Wimbledon|Tour de France|Ashes Series", "FIFA World Cup"),
        ("Which ancient city was buried by Mount Vesuvius?", "Pompeii|Athens|Troy|Babylon", "Pompeii"),
        ("Which field studies past human societies through artifacts?", "Archaeology|Meteorology|Botany|Astronomy", "Archaeology"),
        ("Which country has the city of Marrakesh?", "Morocco|Greece|Nepal|Argentina", "Morocco"),
        ("Which direction is opposite southwest?", "Northeast|Northwest|Southeast|East", "Northeast"),
    ],
}

QUESTION_BANKS[("Mathematics", "Medium")] = [
    ("What is 15 x 4?", "45|50|60|75", "60"),
    ("What is 84 divided by 7?", "10|11|12|14", "12"),
    ("Which fraction is equal to 0.25?", "1/2|1/3|1/4|3/4", "1/4"),
    ("What is the area of a rectangle 8 by 5?", "13|26|40|45", "40"),
    ("What is 35 percent written as a decimal?", "0.035|0.35|3.5|35.0", "0.35"),
    ("What is 120 - 46?", "64|70|74|84", "74"),
    ("What is the next number in 6, 12, 18, 24?", "28|30|32|36", "30"),
    ("A bag has 3 red and 2 blue marbles. How many marbles are there?", "4|5|6|7", "5"),
    ("What is 2/3 of 18?", "6|9|12|15", "12"),
    ("How many degrees are in a right angle?", "45|60|90|180", "90"),
    ("What is 11 x 6?", "56|60|66|72", "66"),
    ("What is 96 divided by 8?", "10|11|12|13", "12"),
    ("Which number is divisible by 3?", "25|31|42|55", "42"),
    ("What is 7.5 + 2.25?", "8.75|9.25|9.75|10.25", "9.75"),
    ("What is the perimeter of a rectangle 7 by 4?", "11|18|22|28", "22"),
    ("Round 348 to the nearest ten.", "340|350|300|400", "350"),
    ("What is 5 squared plus 4?", "20|25|29|34", "29"),
    ("Which value is greatest?", "0.6|0.55|0.09|0.5", "0.6"),
    ("What is 3 hours in minutes?", "90|120|150|180", "180"),
    ("A pencil costs 6 coins. How much do 5 pencils cost?", "24|28|30|36", "30"),
    ("What is 14 x 3?", "37|40|42|45", "42"),
    ("What is 150 divided by 10?", "10|12|15|20", "15"),
    ("Which fraction is larger?", "1/5|1/4|1/8|1/10", "1/4"),
    ("What is 45 plus 38?", "73|83|85|93", "83"),
    ("What is 200 - 125?", "65|70|75|85", "75"),
    ("What is the missing number: 9, 18, 27, __?", "32|34|36|40", "36"),
    ("If 4 notebooks cost 28 coins, what is one notebook?", "6|7|8|9", "7"),
    ("What is 10 percent of 90?", "9|10|18|45", "9"),
    ("Which number is a factor of 36?", "5|7|9|11", "9"),
    ("What is 64 divided by 4?", "12|14|16|18", "16"),
    ("What is 2.5 x 4?", "6|8|10|12", "10"),
    ("A square has side 9. What is its perimeter?", "18|27|36|81", "36"),
    ("What is 5/10 simplified?", "1/2|1/5|2/5|5/1", "1/2"),
    ("What is 13 + 27 + 10?", "40|45|50|55", "50"),
    ("How many centimeters are in one meter?", "10|50|100|1000", "100"),
    ("What is 8 cubed not, but 8 squared?", "16|32|64|512", "64"),
    ("Which angle is larger than a right angle?", "Acute|Obtuse|Zero|Straight only", "Obtuse"),
    ("What is 17 x 2?", "32|34|36|38", "34"),
    ("What is one fifth of 45?", "5|8|9|10", "9"),
    ("What is 6.2 - 1.7?", "3.5|4.5|5.5|6.5", "4.5"),
]

QUESTION_BANKS[("Mathematics", "Hard")] = [
    ("Solve for x: 2x + 5 = 17.", "4|5|6|7", "6"),
    ("What is 18 percent of 250?", "35|40|45|50", "45"),
    ("A triangle has angles 50 and 60. What is the third angle?", "60|70|80|90", "70"),
    ("What is the volume of a box 3 by 4 by 5?", "12|30|45|60", "60"),
    ("What is the average of 12, 18, 20, and 30?", "18|20|22|24", "20"),
    ("Simplify 3/9.", "1/2|1/3|2/3|3/1", "1/3"),
    ("What is 2 to the power of 5?", "10|16|25|32", "32"),
    ("A shirt costs 40 after a 20 percent discount. What was the original price?", "45|48|50|60", "50"),
    ("Which expression equals 36?", "4 x 8|6 x 6|9 x 5|12 x 2", "6 x 6"),
    ("What is the least common multiple of 4 and 6?", "8|10|12|24", "12"),
    ("If y - 14 = 9, what is y?", "5|19|21|23", "23"),
    ("What is 0.75 as a fraction?", "1/4|1/2|3/4|4/5", "3/4"),
    ("A car travels 180 km in 3 hours. What is its average speed?", "45 km/h|50 km/h|60 km/h|90 km/h", "60 km/h"),
    ("What is the area of a triangle with base 10 and height 6?", "16|30|60|120", "30"),
    ("Which number is prime?", "39|49|51|53", "53"),
    ("What is 125 divided by 5?", "15|20|25|30", "25"),
    ("Solve: 4 x (7 + 3) - 6.", "28|34|40|46", "34"),
    ("What is the square root of 196?", "12|13|14|15", "14"),
    ("What is 3.2 + 4.85?", "7.05|8.05|8.15|9.05", "8.05"),
    ("A ratio of 2:3 has 20 red counters. How many blue counters?", "20|25|30|35", "30"),
    ("What is 15 squared?", "125|150|225|250", "225"),
    ("What is 7/8 minus 3/8?", "1/8|1/4|1/2|5/8", "1/2"),
    ("A rectangle area is 72 and length is 9. What is width?", "6|7|8|9", "8"),
    ("What is 40 percent of 75?", "25|30|35|40", "30"),
    ("Which ordered pair has x = 3 and y = 5?", "(5, 3)|(3, 5)|(3, 3)|(5, 5)", "(3, 5)"),
    ("What is the median of 4, 9, 12, 15, 20?", "9|12|13|15", "12"),
    ("What is 1.2 x 0.5?", "0.06|0.6|1.7|6", "0.6"),
    ("A number doubled is 46. What is the number?", "21|22|23|24", "23"),
    ("How many degrees are in a straight angle?", "90|120|180|360", "180"),
    ("What is 11 percent of 300?", "30|31|33|39", "33"),
    ("Simplify 18/24.", "2/3|3/4|4/5|6/8", "3/4"),
    ("What is the greatest common factor of 18 and 24?", "3|6|9|12", "6"),
    ("If 5 boxes hold 45 books, how many books fit in 8 boxes?", "64|70|72|80", "72"),
    ("What is 10 minus 3.75?", "5.25|6.25|6.75|7.25", "6.25"),
    ("Which graph type best shows parts of a whole?", "Pie chart|Line graph|Scatter plot|Map", "Pie chart"),
    ("What is 9 factorial not needed; what is 9 x 8 x 7?", "405|504|567|604", "504"),
    ("A scale says 1 cm represents 5 km. What does 7 cm represent?", "12 km|25 km|35 km|50 km", "35 km"),
    ("What is the probability of flipping heads on a fair coin?", "0|1/4|1/2|1", "1/2"),
    ("Which equation matches: five more than n is 18?", "n - 5 = 18|5n = 18|n + 5 = 18|18 + n = 5", "n + 5 = 18"),
    ("What is 1,000 divided by 25?", "25|40|50|75", "40"),
]

QUESTION_BANKS[("English", "Easy")] = [
    ("Which sentence is complete?", "Because it rained.|The small dog.|Maya packed her bag.|Under the table.", "Maya packed her bag."),
    ("Choose the word that describes a person.", "Teacher|Blue|Quickly|Swim", "Teacher"),
    ("Which word is a verb in this sentence: Birds sing at sunrise?", "Birds|Sing|Sunrise|At", "Sing"),
    ("Which word best completes the sentence: The soup is very ___.", "hot|ran|table|jump", "hot"),
    ("What punctuation belongs at the end of a question?", "Period|Comma|Question mark|Apostrophe", "Question mark"),
    ("Choose the correctly spelled word.", "Becuz|Because|Becaus|Beecause", "Because"),
    ("Which word means the opposite of noisy?", "Quiet|Loud|Sharp|Busy", "Quiet"),
    ("Which word rhymes with light?", "Late|Sight|Leaf|Lock", "Sight"),
    ("Which sentence uses a capital letter correctly?", "sam plays football.|Sam plays football.|sam Plays football.|Sam plays Football.", "Sam plays football."),
    ("Choose the plural form of box.", "Boxs|Boxes|Boxies|Boxen", "Boxes"),
    ("Which word is a pronoun?", "They|Window|Laugh|Yellow", "They"),
    ("What is the noun in: The kite flew high?", "Kite|Flew|High|The", "Kite"),
    ("Choose the best word: A turtle moves ___.", "slowly|brightly|loudly|sweetly", "slowly"),
    ("Which pair are opposites?", "Begin and start|Large and big|Early and late|Small and tiny", "Early and late"),
    ("Which sentence tells about the past?", "I walked home.|I walk home.|I will walk home.|I am walking home.", "I walked home."),
    ("What should a sentence always begin with?", "A comma|A capital letter|A period|A question mark", "A capital letter"),
    ("Which word is an adjective?", "Soft|Run|Desk|Under", "Soft"),
    ("Choose the sentence with correct spacing.", "Thecat slept.|The cat slept.|Thecatslept.|The catslept.", "The cat slept."),
    ("Which word names a place?", "School|Happy|Quickly|Draw", "School"),
    ("Which word is a compound word?", "Sunflower|Sunny|Flower|Light", "Sunflower"),
    ("Choose the word that means small.", "Tiny|Huge|Wide|Tall", "Tiny"),
    ("Which sentence gives a command?", "Please close the door.|The door is blue.|Where is the door?|I like the door.", "Please close the door."),
    ("Which word belongs in: She ___ a story.", "read|blue|chair|soft", "read"),
    ("What is the first word in a dictionary page called?", "Guide word|Password|Title page|Index card", "Guide word"),
    ("Choose the correct article: ___ orange is sweet.", "A|An|The one|And", "An"),
    ("Which word has a long vowel sound?", "Cake|Cat|Bed|Hop", "Cake"),
    ("Which sentence is a statement?", "Do you like art?|Close the book.|The moon is bright.|Wow!", "The moon is bright."),
    ("Choose the synonym for fast.", "Quick|Slow|Late|Still", "Quick"),
    ("Which word is singular?", "Children|Books|Pencils|Child", "Child"),
    ("What does an author do?", "Writes a text|Draws every map|Builds roads|Counts money", "Writes a text"),
    ("Which word fits: The baby laughed ___.", "happily|heavy|square|yesterday", "happily"),
    ("Choose the best title for a story about planting seeds.", "A Day at the Beach|Growing a Garden|Lost in Space|The Big Race", "Growing a Garden"),
    ("Which word is a conjunction?", "And|Chair|Blue|Jump", "And"),
    ("Which sentence shows excitement?", "That was amazing!|That was amazing.|Was that amazing?|Close that book.", "That was amazing!"),
    ("Choose the correct contraction for do not.", "Dont|Do'nt|Don't|Donot", "Don't"),
    ("What does a reader use context clues for?", "To understand a word|To count pages|To sharpen pencils|To draw borders", "To understand a word"),
    ("Which word names a thing?", "Pencil|Bright|Under|Dance", "Pencil"),
    ("Choose the best ending punctuation: Where is my notebook", ".|,|?|'", "?"),
    ("Which word is written in alphabetical order after apple?", "Banana|Ant|Able|Ape", "Banana"),
    ("What is the setting of a story?", "Where and when it happens|The lesson only|The page number|The author's age", "Where and when it happens"),
]

QUESTION_BANKS[("English", "Medium")] = [
    ("Which sentence has correct subject-verb agreement?", "The boys runs fast.|The boys run fast.|The boy run fast.|The boys running fast.", "The boys run fast."),
    ("Choose the best transition: I studied hard; ___, I passed the test.", "therefore|before|under|unless", "therefore"),
    ("What is the main idea of a paragraph?", "The most important point|The longest word|The first comma|The author's name", "The most important point"),
    ("Which sentence uses a homophone correctly?", "Their house is near mine.|There house is near mine.|They're house is near mine.|Theirs house is near mine.", "Their house is near mine."),
    ("Choose the correctly punctuated dialogue.", "\"I am ready,\" said Ali.|\"I am ready, said Ali.\"|I am ready,\" said Ali.|\"I am ready\" said, Ali.", "\"I am ready,\" said Ali."),
    ("Which word has a prefix meaning again?", "Rewrite|Helpful|Careless|Teacher", "Rewrite"),
    ("What is the predicate in: The class built a model bridge?", "The class|Built a model bridge|A model|Bridge", "Built a model bridge"),
    ("Choose the sentence with an adverb.", "Sara spoke softly.|Sara has a soft scarf.|Sara likes soft bread.|Sara drew a soft line.", "Sara spoke softly."),
    ("Which sentence compares two things?", "The lake is deeper than the pond.|The lake is blue.|The pond has ducks.|The lake is nearby.", "The lake is deeper than the pond."),
    ("What does infer mean while reading?", "Use clues to figure something out|Copy every sentence|Skip hard words|Read only titles", "Use clues to figure something out"),
    ("Which sentence is written in future tense?", "We will visit the museum.|We visited the museum.|We visit the museum.|We are visiting now.", "We will visit the museum."),
    ("Choose the correct possessive noun.", "The girl's backpack|The girls backpack|The girl backpack's|The girls's backpack", "The girl's backpack"),
    ("Which word is a suffix in cheerful?", "cheer|ful|chee|erf", "ful"),
    ("What is a summary?", "A short retelling of key ideas|A copy of every word|A list of page numbers|A guess before reading", "A short retelling of key ideas"),
    ("Which sentence is a fragment?", "Because the bell rang.|The bell rang loudly.|Students packed their bags.|We walked outside.", "Because the bell rang."),
    ("Choose the best context meaning of bark: The bark protected the tree.", "Outer covering|Dog sound|Small boat|Sharp cough", "Outer covering"),
    ("Which sentence uses a comma in a series?", "We packed pens, books, and snacks.|We packed, pens books and snacks.|We packed pens books, and snacks.|We, packed pens books and snacks.", "We packed pens, books, and snacks."),
    ("What is a topic sentence?", "A sentence that states the paragraph's main point|A sentence with only one word|A sentence at the end of a book|A question in dialogue", "A sentence that states the paragraph's main point"),
    ("Which sentence shows cause and effect?", "The ground was wet because it rained.|The ground was wet and brown.|The rain was cold.|The ground is outside.", "The ground was wet because it rained."),
    ("Choose the correct irregular plural.", "Geese|Gooses|Goosees|Geeses", "Geese"),
    ("Which word is a preposition?", "Between|Bright|Carry|Friend", "Between"),
    ("What is the theme of a story?", "A message or lesson|The number of pages|The cover color|The longest chapter", "A message or lesson"),
    ("Which sentence avoids a run-on?", "I was tired, so I rested.|I was tired I rested.|I was tired and I rested and I slept and I woke.|I was tired I rested because.", "I was tired, so I rested."),
    ("Choose the best synonym for brave.", "Courageous|Careless|Quiet|Ordinary", "Courageous"),
    ("Which sentence uses an apostrophe for a contraction?", "It's raining today.|The cat's tail moved.|Saras book is here.|The dogs barked.", "It's raining today."),
    ("What does sequence mean in a story?", "The order of events|The place of events|The problem only|The title only", "The order of events"),
    ("Which word is the root in unhappy?", "happy|un|hap|py", "happy"),
    ("Choose the best supporting detail for: Exercise is healthy.", "It can strengthen the heart.|Many shoes are blue.|The park has benches.|Some books are long.", "It can strengthen the heart."),
    ("Which sentence contains a simile?", "The snow was like a blanket.|The snow covered the field.|The snow melted quickly.|The snow fell all night.", "The snow was like a blanket."),
    ("Choose the correct comparative adjective.", "This bag is heavier than that one.|This bag is heaviest than that one.|This bag is more heavy than all.|This bag is heavy than that one.", "This bag is heavier than that one."),
    ("Which detail helps describe a character?", "Lina shared her lunch with a new student.|The bus arrived at eight.|The room had four windows.|The sky was cloudy.", "Lina shared her lunch with a new student."),
    ("What is alliteration?", "Repeated beginning sounds|A surprise ending|A list of facts|A type of punctuation", "Repeated beginning sounds"),
    ("Choose the sentence with correct quotation marks.", "Mina asked, \"Can I join?\"|Mina asked, Can I join?\"|\"Mina asked, Can I join?|Mina \"asked, Can I join?\"", "Mina asked, \"Can I join?\""),
    ("Which word means almost the same as collect?", "Gather|Scatter|Borrow|Forget", "Gather"),
    ("What does the suffix less mean in careless?", "Without|Full of|Before|Again", "Without"),
    ("Which sentence is written from first-person point of view?", "I opened the door slowly.|She opened the door slowly.|They opened the door slowly.|Ali opened the door slowly.", "I opened the door slowly."),
    ("Choose the word that best completes: The team practiced ___ the match.", "before|beautiful|quick|happy", "before"),
    ("Which sentence uses a proper noun?", "Omar visited Lahore.|The boy visited a city.|A student visited a museum.|My friend visited a park.", "Omar visited Lahore."),
    ("What is the purpose of evidence in writing?", "To support an idea|To decorate the page|To make sentences longer|To replace punctuation", "To support an idea"),
    ("Which phrase is an idiom?", "It is raining cats and dogs.|It is raining today.|The clouds are gray.|The street is wet.", "It is raining cats and dogs."),
]

QUALITY_BANKS = {
    ("English", "Hard"): [
        ("Which revision is most concise?", "Due to the fact that it rained, the match ended.|Because it rained, the match ended.|The match ended in relation to rain.|Rain happened and therefore the match was ended.", "Because it rained, the match ended."),
        ("Which sentence uses a semicolon correctly?", "I packed my bag; then I left.|I packed; my bag then I left.|I packed my bag then; I left.|I; packed my bag then I left.", "I packed my bag; then I left."),
        ("Which sentence is passive voice?", "The window was cleaned by Sara.|Sara cleaned the window.|Sara is cleaning the window.|Sara will clean the window.", "The window was cleaned by Sara."),
        ("What is the best evidence for a claim about exercise?", "A study showing stronger hearts after daily activity|A story about new shoes|A list of favorite games|A picture of a park", "A study showing stronger hearts after daily activity"),
        ("Which sentence contains personification?", "The wind whispered through the trees.|The wind was cold.|The wind blew all night.|The wind moved the leaves.", "The wind whispered through the trees."),
        ("Choose the sentence with parallel structure.", "Mina likes reading, swimming, and painting.|Mina likes reading, to swim, and painting.|Mina likes to read, swimming, and paint.|Mina likes reads, swims, and painting.", "Mina likes reading, swimming, and painting."),
        ("Which source is most credible for a science report?", "A current article from a science museum|An anonymous comment|A toy advertisement|A joke website", "A current article from a science museum"),
        ("Which sentence uses a colon correctly?", "Bring these items: pencils, paper, and glue.|Bring: these items pencils, paper, and glue.|Bring these: items pencils, paper, and glue.|Bring these items pencils: paper and glue.", "Bring these items: pencils, paper, and glue."),
        ("What does tone describe?", "The writer's attitude toward the subject|The number of paragraphs|The size of the letters|The story's setting only", "The writer's attitude toward the subject"),
        ("Which is a strong thesis statement?", "School gardens help students learn science and responsibility.|Gardens are nice.|This essay is about gardens.|Many schools have land.", "School gardens help students learn science and responsibility."),
        ("Which sentence avoids a misplaced modifier?", "Wearing a helmet, Amir rode his bike.|Amir rode his bike wearing a helmet on the street.|Riding on the street, the helmet protected Amir.|The bike wearing a helmet carried Amir.", "Wearing a helmet, Amir rode his bike."),
        ("Which sentence uses subjunctive mood?", "If I were taller, I could reach the shelf.|I was taller yesterday.|I am taller than my cousin.|I will be taller soon.", "If I were taller, I could reach the shelf."),
        ("What is an analogy?", "A comparison showing relationships|A repeated vowel sound|A paragraph ending|A list of characters", "A comparison showing relationships"),
        ("Which transition shows contrast?", "However|Therefore|Similarly|First", "However"),
        ("Choose the formal sentence.", "I would like to request more information.|Tell me more stuff.|Can you send the thing?|I wanna know more.", "I would like to request more information."),
        ("Which sentence contains irony?", "The fire station burned down during safety week.|The fire station is red.|The fire station has trucks.|The firefighters trained outside.", "The fire station burned down during safety week."),
        ("What is a counterargument?", "An opposing point of view|The final sentence|A type of comma|A repeated phrase", "An opposing point of view"),
        ("Which sentence uses an appositive?", "My brother, a skilled artist, painted the mural.|My brother painted the mural quickly.|My brother and I painted.|The mural was bright.", "My brother, a skilled artist, painted the mural."),
        ("What is symbolism?", "Using an object to represent a bigger idea|Spelling a word aloud|Writing in alphabetical order|Counting syllables", "Using an object to represent a bigger idea"),
        ("Which word best replaces very tired?", "Exhausted|Sleep|Slow|Weakly", "Exhausted"),
        ("Which sentence is compound-complex?", "When the rain stopped, we packed our bags, and we left.|The rain stopped.|We packed our bags and left.|Because the rain stopped.", "When the rain stopped, we packed our bags, and we left."),
        ("Choose the best paraphrase of: The experiment failed due to insufficient light.", "The test did not work because there was not enough light.|The light was bright and the test worked.|The experiment was easy.|The test failed because of too much water.", "The test did not work because there was not enough light."),
        ("Which phrase is a gerund phrase?", "Swimming in the lake|To swim fast|Swam yesterday|Will swim soon", "Swimming in the lake"),
        ("What is bias in writing?", "A one-sided preference|A direct quote|A page heading|A neutral summary", "A one-sided preference"),
        ("Which sentence has correct pronoun agreement?", "Every student brought his or her notebook.|Every student brought their notebooks in formal singular use.|Every students brought his notebook.|Every student brought our notebook.", "Every student brought his or her notebook."),
        ("Which sentence uses an infinitive?", "Maya wants to learn coding.|Maya learned coding.|Maya is coding.|Maya coded quickly.", "Maya wants to learn coding."),
        ("What is mood in a story?", "The feeling created for the reader|The grammar of verbs|The list of sources|The author's birthplace", "The feeling created for the reader"),
        ("Which sentence uses a dash effectively?", "The answer was clear - practice mattered most.|The answer - was clear practice mattered most.|The - answer was clear practice mattered most.|The answer was clear practice - mattered most.", "The answer was clear - practice mattered most."),
        ("Choose the strongest claim.", "Daily reading can improve vocabulary and focus.|Reading exists.|Books have pages.|Some people read.", "Daily reading can improve vocabulary and focus."),
        ("Which sentence uses active voice?", "The team solved the puzzle.|The puzzle was solved by the team.|The puzzle had been solved.|The puzzle was being solved.", "The team solved the puzzle."),
        ("What is the purpose of citation?", "To show where information came from|To make a paragraph longer|To decorate a title|To replace a conclusion", "To show where information came from"),
        ("Which sentence best combines ideas?", "Although the path was steep, the hikers continued.|The path was steep. The hikers continued. It was a path.|The hikers continued the steep.|Steep path hikers continued.", "Although the path was steep, the hikers continued."),
        ("Which detail suggests the narrator is unreliable?", "The narrator admits forgetting important events.|The narrator describes the weather.|The narrator has a name.|The narrator walks to school.", "The narrator admits forgetting important events."),
        ("Choose the correct conditional sentence.", "If we practice, we will improve.|If we practiced, we will improves.|If we practice, we improving.|If practice, improve we.", "If we practice, we will improve."),
        ("Which sentence contains hyperbole?", "I have told you a million times.|I told you twice.|I spoke quietly.|I counted the books.", "I have told you a million times."),
        ("What does audience mean in writing?", "The people who will read or hear the text|The number of words|The first sentence|The paper size", "The people who will read or hear the text"),
        ("Which sentence uses a relative clause?", "The book that I borrowed is exciting.|The book is exciting.|I borrowed the book.|Exciting books are fun.", "The book that I borrowed is exciting."),
        ("Choose the best concluding sentence.", "For these reasons, saving water helps everyone.|Water is wet.|The end is now.|I have many ideas.", "For these reasons, saving water helps everyone."),
        ("Which phrase is participial?", "Covered in dust|To cover dust|Dust cover|Covers dust", "Covered in dust"),
        ("Which sentence uses a precise verb?", "The eagle soared above the cliffs.|The eagle went above the cliffs.|The eagle did above the cliffs.|The eagle was above the cliffs.", "The eagle soared above the cliffs."),
    ],
    ("Science", "Easy"): [
        ("What do roots help a plant absorb?", "Water|Sunlight only|Wind|Sound", "Water"),
        ("Which object gives off light?", "Lamp|Stone|Book|Spoon", "Lamp"),
        ("What do lungs help people do?", "Breathe|Digest food|Hear sounds|Move bones", "Breathe"),
        ("Which animal has feathers?", "Bird|Fish|Frog|Snake", "Bird"),
        ("What happens to ice when it gets warm?", "It melts|It grows feathers|It becomes rock|It disappears into soil", "It melts"),
        ("Which part of the body helps you think?", "Brain|Elbow|Knee|Stomach", "Brain"),
        ("What do magnets attract?", "Iron objects|Paper only|Glass cups|Wood leaves", "Iron objects"),
        ("Which weather is most likely when clouds are dark and heavy?", "Rain|Snow every time|Sun only|No wind ever", "Rain"),
        ("Which is a source of heat?", "Fire|Ice|Shadow|Sand", "Fire"),
        ("What do seeds grow into?", "Plants|Rocks|Clouds|Batteries", "Plants"),
        ("Which sense helps you hear music?", "Hearing|Taste|Touch|Sight", "Hearing"),
        ("What does gravity do?", "Pulls objects toward Earth|Makes objects invisible|Turns water blue|Stops all motion", "Pulls objects toward Earth"),
        ("Which is a liquid?", "Milk|Brick|Pencil|Chair", "Milk"),
        ("What do animals need to survive?", "Food and water|Only toys|Only sunlight|Only books", "Food and water"),
        ("Which planet is closest to Earth as our home world?", "Earth|Jupiter|Neptune|Mercury", "Earth"),
        ("What protects the brain?", "Skull|Rib|Finger|Tooth", "Skull"),
        ("Which material is usually transparent?", "Clear glass|Wood|Stone|Metal", "Clear glass"),
        ("What does a thermometer measure?", "Temperature|Length|Weight|Sound", "Temperature"),
        ("Which part of a plant makes seeds in many plants?", "Flower|Root|Stem only|Soil", "Flower"),
        ("What is air mostly around us?", "A mixture of gases|A solid wall|A type of water|A bright light", "A mixture of gases"),
        ("Which animal lives mostly in water?", "Fish|Horse|Cat|Eagle", "Fish"),
        ("What do muscles help the body do?", "Move|Read|Shine|Freeze", "Move"),
        ("Which item uses electricity?", "Fan|Rock|Leaf|Cup", "Fan"),
        ("What is the Sun?", "A star|A planet|A moon|A cloud", "A star"),
        ("Which is a natural resource?", "Water|Plastic wrapper|Toy car|Notebook cover", "Water"),
        ("What does a shadow need?", "Light and an object blocking it|Only water|Only sound|Only soil", "Light and an object blocking it"),
        ("Which object can float in water?", "Wooden stick|Iron nail|Stone|Coin", "Wooden stick"),
        ("What do bees help flowers do?", "Pollinate|Freeze|Become rocks|Lose roots", "Pollinate"),
        ("Which force can push a door open?", "A push|Color|Temperature|Smell", "A push"),
        ("What is soil useful for?", "Growing plants|Charging phones|Making clouds|Stopping time", "Growing plants"),
        ("Which is the gas form of water?", "Steam|Ice|Snow|Hail", "Steam"),
        ("What do eyes detect?", "Light|Taste|Smell|Weight", "Light"),
        ("Which animal is an insect?", "Ant|Dog|Frog|Shark", "Ant"),
        ("What happens when water freezes?", "It becomes ice|It becomes sand|It becomes metal|It becomes fire", "It becomes ice"),
        ("Which body part pumps blood?", "Heart|Brain|Lung|Hand", "Heart"),
        ("Which object is nonliving?", "Rock|Tree|Bird|Mushroom", "Rock"),
        ("What does a battery store?", "Energy|Rain|Air|Soil", "Energy"),
        ("Which weather tool measures rain?", "Rain gauge|Ruler|Compass|Clock", "Rain gauge"),
        ("What do leaves often use to make food?", "Sunlight|Moon rocks|Plastic|Salt only", "Sunlight"),
        ("Which is safest during a thunderstorm?", "Go indoors|Stand under a tall tree|Swim outside|Hold metal poles", "Go indoors"),
    ],
    ("Science", "Medium"): [
        ("Why does a puddle get smaller on a sunny day?", "Water evaporates into the air|Water turns into stone|The ground makes new water|The Sun freezes it", "Water evaporates into the air"),
        ("What is the role of producers in a food chain?", "They make their own food|They eat only predators|They break every rock|They control weather", "They make their own food"),
        ("Which change is condensation?", "Water vapor forming droplets on a cold glass|Ice melting on a plate|Sugar dissolving in tea|Paper tearing in half", "Water vapor forming droplets on a cold glass"),
        ("Why do bicycle brakes slow a wheel?", "Friction resists motion|Gravity disappears|Light pushes backward|Air becomes solid", "Friction resists motion"),
        ("Which item would complete a simple electric circuit?", "A closed path with a battery and bulb|A loose wire beside a bulb|A plastic spoon and paper|A cup of cold water", "A closed path with a battery and bulb"),
        ("What does a conductor do?", "Allows electricity to flow easily|Stops all heat forever|Makes magnets vanish|Turns solids into gas", "Allows electricity to flow easily"),
        ("Why do seasons happen?", "Earth is tilted as it orbits the Sun|The Sun turns off each winter|The Moon warms Earth unevenly|Clouds move in circles", "Earth is tilted as it orbits the Sun"),
        ("Which process breaks rocks into smaller pieces?", "Weathering|Pollination|Digestion|Reflection", "Weathering"),
        ("What is a solution?", "A mixture where one substance dissolves in another|A pile of separate stones|A living habitat|A kind of shadow", "A mixture where one substance dissolves in another"),
        ("Why is camouflage helpful?", "It helps an animal blend into its surroundings|It makes animals larger|It changes water into food|It stops all predators", "It helps an animal blend into its surroundings"),
        ("What happens during germination?", "A seed begins to grow|A rock becomes soil|A planet rotates|A magnet loses poles", "A seed begins to grow"),
        ("Which body system breaks food into nutrients?", "Digestive system|Respiratory system|Skeletal system|Nervous system", "Digestive system"),
        ("What does the respiratory system help with?", "Taking in oxygen and removing carbon dioxide|Pumping blood only|Holding bones together|Making skin color", "Taking in oxygen and removing carbon dioxide"),
        ("Which energy source is renewable?", "Wind|Coal|Oil|Natural gas", "Wind"),
        ("Which simple machine is used in a flagpole?", "Pulley|Wedge only|Screwdriver handle|Inclined shadow", "Pulley"),
        ("Why does a ball thrown upward come back down?", "Gravity pulls it toward Earth|Sound pushes it down|The ball runs out of color|Air becomes heavy only at night", "Gravity pulls it toward Earth"),
        ("What is density?", "How much mass is packed into a space|How bright a color is|How loud a sound is|How old a fossil is", "How much mass is packed into a space"),
        ("Which is evidence of a chemical change?", "A new gas forms|Paper is folded|Ice melts|A pencil is sharpened", "A new gas forms"),
        ("What does pollination help plants make?", "Seeds|Clouds|Rocks|Metal", "Seeds"),
        ("Why are decomposers important?", "They recycle nutrients from dead matter|They make sunlight|They stop all rain|They build mountains overnight", "They recycle nutrients from dead matter"),
        ("Which force acts when two surfaces rub?", "Friction|Magnetism only|Reflection|Evaporation", "Friction"),
        ("What causes a lunar month to show different Moon phases?", "The Moon's position around Earth changes|The Moon changes size|Earth stops spinning|The Sun becomes smaller", "The Moon's position around Earth changes"),
        ("Which part of a flower often attracts pollinators?", "Petals|Roots|Stem only|Soil", "Petals"),
        ("What happens to a gas when it cools enough?", "It may condense into a liquid|It always becomes light|It turns into a magnet|It loses all mass", "It may condense into a liquid"),
        ("Which organ is part of the circulatory system?", "Heart|Stomach|Lung only|Brain only", "Heart"),
        ("What is erosion?", "Movement of weathered rock or soil|Growth of a seed|Formation of a shadow|Mixing sugar into tea", "Movement of weathered rock or soil"),
        ("Why does metal feel colder than wood in the same room?", "Metal transfers heat from your hand faster|Metal is always frozen|Wood creates heat|Color changes temperature", "Metal transfers heat from your hand faster"),
        ("Which animal is best adapted for desert water conservation?", "Camel|Penguin|Frog|Salmon", "Camel"),
        ("What does an insulator do in a circuit?", "Slows or blocks electric flow|Makes electricity stronger forever|Creates gravity|Stores rainwater", "Slows or blocks electric flow"),
        ("What is mass?", "The amount of matter in an object|The space an object takes|The speed of a sound|The brightness of light", "The amount of matter in an object"),
        ("Which material dissolves easily in water?", "Salt|Sand|Pebble|Oil slick", "Salt"),
        ("Why do plants need carbon dioxide?", "To make food during photosynthesis|To build bones|To make thunder|To attract magnets", "To make food during photosynthesis"),
        ("What is deposition?", "Dropping sediment in a new place|Breaking food into nutrients|Changing liquid to gas|Making an electric current", "Dropping sediment in a new place"),
        ("Which tool helps observe tiny cells?", "Microscope|Compass|Thermometer|Barometer", "Microscope"),
        ("Why does a compass needle point north?", "It aligns with Earth's magnetic field|It follows the Sun's heat|It smells cold air|It counts longitude lines", "It aligns with Earth's magnetic field"),
        ("What is volume?", "The amount of space something takes up|The amount of matter only|The speed of movement|The pull of gravity", "The amount of space something takes up"),
        ("Which is a consumer in a food web?", "Rabbit|Grass|Algae|Oak tree", "Rabbit"),
        ("Why can birds fly more easily than humans?", "They have wings and lightweight bodies|They do not need oxygen|They are magnetic|They have no muscles", "They have wings and lightweight bodies"),
        ("What happens at water's freezing point?", "Liquid water becomes solid ice|Ice becomes steam only|Water disappears|Salt becomes water", "Liquid water becomes solid ice"),
        ("Which action conserves water?", "Turning off the tap while brushing teeth|Leaving taps running|Washing one shirt at a time|Watering plants at noon every day", "Turning off the tap while brushing teeth"),
    ],
    ("Science", "Hard"): [
        ("Why do vaccines help protect communities?", "They train immune systems and can reduce disease spread|They replace all medicine|They make bacteria larger|They stop every injury", "They train immune systems and can reduce disease spread"),
        ("What does Newton's first law describe?", "Objects keep their motion unless a force acts|All objects are magnetic|Heat always moves upward|Light has no speed", "Objects keep their motion unless a force acts"),
        ("Why is biodiversity valuable in an ecosystem?", "It helps ecosystems stay resilient when conditions change|It makes all animals identical|It removes the need for plants|It stops the water cycle", "It helps ecosystems stay resilient when conditions change"),
        ("What happens in a balanced chemical equation?", "Atoms are conserved on both sides|Atoms disappear after reacting|Only liquids are counted|Energy becomes matter", "Atoms are conserved on both sides"),
        ("Why do tectonic plates move slowly?", "Heat inside Earth drives mantle motion|Ocean waves push them daily|Clouds pull them apart|Magnets from cities move them", "Heat inside Earth drives mantle motion"),
        ("What does chlorophyll do?", "Absorbs light energy for photosynthesis|Stores animal bones|Makes rocks magnetic|Breaks down plastic", "Absorbs light energy for photosynthesis"),
        ("Why are parallel circuits useful in homes?", "One device can turn off while others stay on|They use no wires|They block all current|They only work underwater", "One device can turn off while others stay on"),
        ("What does pH measure?", "How acidic or basic a substance is|How heavy a planet is|How loud a sound is|How fast light travels", "How acidic or basic a substance is"),
        ("Why can fossils show evidence of past environments?", "They preserve remains or traces of organisms from long ago|They predict tomorrow's weather|They are made of fresh clouds|They grow into new animals", "They preserve remains or traces of organisms from long ago"),
        ("What is potential energy?", "Stored energy due to position or condition|Energy of motion only|Energy that has disappeared|Sound from a battery", "Stored energy due to position or condition"),
        ("How does the greenhouse effect warm Earth?", "Certain gases trap some heat in the atmosphere|Clouds turn heat into soil|Oceans stop sunlight|The Moon adds fire", "Certain gases trap some heat in the atmosphere"),
        ("Why is the ozone layer important?", "It absorbs much harmful ultraviolet radiation|It creates ocean tides|It makes gravity stronger|It stores all oxygen", "It absorbs much harmful ultraviolet radiation"),
        ("What is an astronomical unit based on?", "Average distance from Earth to the Sun|Width of the Moon|Time for one day|Mass of Jupiter", "Average distance from Earth to the Sun"),
        ("Why does warm air often rise?", "It becomes less dense than cooler air|It becomes magnetic|It turns into light|It loses all molecules", "It becomes less dense than cooler air"),
        ("What is natural selection?", "Traits that help survival become more common over generations|Animals choose their favorite food|All organisms change instantly|Plants decide the weather", "Traits that help survival become more common over generations"),
        ("What does a cell membrane do?", "Controls what enters and leaves the cell|Makes sunlight|Stores fossils|Pumps blood", "Controls what enters and leaves the cell"),
        ("Why are enzymes important?", "They speed up chemical reactions in living things|They are bones in the arm|They carry electricity in wires|They are planets", "They speed up chemical reactions in living things"),
        ("What does the carbon cycle describe?", "Movement of carbon through air, living things, water, and land|Movement of only clouds|How magnets form|How rocks become stars", "Movement of carbon through air, living things, water, and land"),
        ("Why can overfishing disrupt a food web?", "It removes species that other organisms depend on|It makes oceans deeper|It stops tides|It creates new continents", "It removes species that other organisms depend on"),
        ("What does thermal expansion mean?", "Matter tends to expand when heated|Matter disappears when warmed|Heat creates gravity|Cold objects always grow", "Matter tends to expand when heated"),
        ("What are mitochondria often called?", "Powerhouses of the cell|Cell walls of animals|Tiny planets|Blood filters", "Powerhouses of the cell"),
        ("Why does selective breeding work?", "Parents with desired traits are chosen to produce offspring|Animals choose their own textbooks|Traits are erased every day|Weather changes genes instantly", "Parents with desired traits are chosen to produce offspring"),
        ("What is kinetic energy?", "Energy of motion|Stored chemical only|Energy with no movement|Heat trapped in ice", "Energy of motion"),
        ("Why are ocean currents important?", "They move heat and nutrients around Earth|They stop wind|They create all volcanoes|They erase seasons", "They move heat and nutrients around Earth"),
        ("What does air pressure result from?", "The weight of air above an area|Only the color of clouds|The sound of wind|The salt in rain", "The weight of air above an area"),
        ("Why is a light-year a distance?", "It is how far light travels in one year|It is a year with more daylight|It is the age of a star|It measures brightness", "It is how far light travels in one year"),
        ("What causes genetic inheritance?", "Offspring receive genes from parents|Children copy habits only|Weather writes DNA|Food turns into chromosomes", "Offspring receive genes from parents"),
        ("Why can acids react with some metals?", "They can produce new substances such as salts and hydrogen gas|They make metal invisible|They turn metal into wood|They stop all reactions", "They can produce new substances such as salts and hydrogen gas"),
        ("What does the nitrogen cycle support?", "Movement of nitrogen needed by living things|Creation of sunlight|Growth of mountains|Movement of planets", "Movement of nitrogen needed by living things"),
        ("Why are microorganisms important?", "Some decompose matter or help digestion|All cause disease|They are not living things|They are larger than animals", "Some decompose matter or help digestion"),
        ("What is continental drift?", "Continents slowly moving over geologic time|Clouds crossing oceans|Rivers changing color|Planets changing places", "Continents slowly moving over geologic time"),
        ("Why does mass stay the same in a closed reaction?", "Matter is conserved|Matter leaks into ideas|Atoms become sound|Energy destroys atoms", "Matter is conserved"),
        ("What does an antibody do?", "Helps recognize and fight specific germs|Carries oxygen in wires|Turns food into light|Builds cell walls in rocks", "Helps recognize and fight specific germs"),
        ("Why is a series circuit less reliable for many bulbs?", "One break can stop the whole circuit|It has no battery|It uses no current|It cannot include bulbs", "One break can stop the whole circuit"),
        ("What does the rock cycle explain?", "How rocks change among igneous, sedimentary, and metamorphic forms|How rocks become animals|How clouds make planets|How magnets make soil", "How rocks change among igneous, sedimentary, and metamorphic forms"),
        ("Why does ultraviolet radiation matter?", "Too much can damage living tissue|It is the same as gravity|It is only sound|It cools all oceans", "Too much can damage living tissue"),
        ("What is an adaptation at population level?", "A trait that improves survival or reproduction in an environment|A daily choice of clothing|A type of homework|A weather forecast", "A trait that improves survival or reproduction in an environment"),
        ("Why do galaxies contain many stars?", "Gravity holds huge systems of stars, gas, and dust together|Stars avoid gravity|Galaxies are single planets|Dust pushes stars away forever", "Gravity holds huge systems of stars, gas, and dust together"),
        ("What is extinction?", "When a species has no living members left|When one animal sleeps|When leaves change color|When water evaporates", "When a species has no living members left"),
        ("Why can bases neutralize acids?", "They react to form substances closer to neutral|They make acid stronger always|They remove all water|They turn into magnets", "They react to form substances closer to neutral"),
    ],
    ("General Knowledge", "Easy"): [
        ("What should you do before crossing a busy road?", "Look both ways and use a safe crossing|Run without looking|Close your eyes|Follow any car", "Look both ways and use a safe crossing"),
        ("Which place is best for borrowing books?", "Library|Airport|Hospital|Bakery", "Library"),
        ("What does a calendar help you know?", "Dates and months|Shoe sizes|Food temperature|Map distance", "Dates and months"),
        ("Which item protects your head when cycling?", "Helmet|Scarf|Glove|Socks", "Helmet"),
        ("What is the safest action during a small kitchen fire?", "Tell an adult quickly|Pour oil on it|Hide nearby|Touch the pan", "Tell an adult quickly"),
        ("Which device is used to take photographs?", "Camera|Compass|Thermometer|Stapler", "Camera"),
        ("What does a flag usually represent?", "A country, group, or place|A type of food|A math answer|A weather tool", "A country, group, or place"),
        ("Which place treats sick or injured people?", "Hospital|Cinema|Stadium|Market", "Hospital"),
        ("Which direction does a compass needle usually point?", "North|Down|Left|Toward water", "North"),
        ("What should you do with litter in a park?", "Put it in a bin|Leave it on grass|Throw it in water|Hide it under leaves", "Put it in a bin"),
        ("Which vehicle travels on tracks?", "Train|Boat|Helicopter|Scooter", "Train"),
        ("What is a passport used for?", "International travel identification|Measuring rain|Buying pencils only|Cooking food", "International travel identification"),
        ("Which meal is often eaten first in the day?", "Breakfast|Dinner|Dessert|Supper", "Breakfast"),
        ("What does a traffic light's red signal mean?", "Stop|Go faster|Turn off lights|Walk anywhere", "Stop"),
        ("Which tool helps you write on paper?", "Pencil|Plate|Bottle|Shoe", "Pencil"),
        ("What is a museum for?", "Preserving and showing important objects|Selling only vegetables|Repairing cars|Landing planes", "Preserving and showing important objects"),
        ("Which natural feature is very high and rocky?", "Mountain|River|Road|Garden", "Mountain"),
        ("What is an island?", "Land surrounded by water|Water surrounded by land|A tall building|A road crossing", "Land surrounded by water"),
        ("Which object helps you hear a radio program?", "Radio|Blanket|Fork|Helmet", "Radio"),
        ("What do farmers often grow?", "Crops|Clouds|Coins|Bridges", "Crops"),
        ("Which place has many shops?", "Market|Forest|Desert|Library shelf", "Market"),
        ("What does an umbrella help protect you from?", "Rain|Homework|Road signs|Books", "Rain"),
        ("Which object is used to mail a letter?", "Stamp|Spoon|Key|Comb", "Stamp"),
        ("What does a keyboard help you do?", "Type letters and numbers|Measure wind|Cook rice|Cross a river", "Type letters and numbers"),
        ("Which place is mainly for airplanes?", "Airport|Train station|Harbor|Playground", "Airport"),
        ("What is a village?", "A small community or settlement|A kind of ocean|A type of clock|A mountain tool", "A small community or settlement"),
        ("Which body of water is larger than a river?", "Ocean|Cup|Pond only|Canal only", "Ocean"),
        ("What is a newspaper used for?", "Sharing news and information|Cleaning teeth|Measuring height|Charging phones", "Sharing news and information"),
        ("Which item is safest to wear in heavy rain?", "Raincoat|Paper hat|Sandals only|Sunglasses only", "Raincoat"),
        ("What does a map show?", "Places and directions|Only songs|Only temperatures|Only book titles", "Places and directions"),
        ("Which crossing is marked for pedestrians?", "Zebra crossing|Finish line|Goal line|Shelf line", "Zebra crossing"),
        ("What is a continent?", "A very large land area|A small spoon|A school subject only|A kind of tree", "A very large land area"),
        ("Which place is good for outdoor play?", "Park|Kitchen cupboard|Bank vault|Airport runway", "Park"),
        ("What is a telephone used for?", "Communicating with people|Weighing flour|Finding north|Planting seeds", "Communicating with people"),
        ("Which room is mainly used for cooking?", "Kitchen|Bedroom|Classroom|Garage", "Kitchen"),
        ("What is a desert known for?", "Very dry conditions|Deep ocean water|Many icebergs always|Heavy daily rain", "Very dry conditions"),
        ("Which document may be sent in an envelope?", "Letter|Chair|Bicycle|Lamp", "Letter"),
        ("What is a city?", "A large human settlement|A small tool|A weather pattern|A single book", "A large human settlement"),
        ("Which screen device can show programs and news?", "Television|Thermos|Compass|Hammer", "Television"),
        ("Why should people follow road signs?", "They help keep traffic safe and organized|They decorate roads only|They replace drivers|They stop rain", "They help keep traffic safe and organized"),
    ],
    ("General Knowledge", "Medium"): [
        ("Why do countries use currency?", "To make buying and selling easier|To measure rainfall|To name mountains|To replace languages", "To make buying and selling easier"),
        ("What does a capital city usually contain?", "Important government offices|Only farms|Only beaches|No people", "Important government offices"),
        ("Why are elections held?", "To choose leaders or representatives|To change seasons|To count animals|To build rivers", "To choose leaders or representatives"),
        ("What does recycling help reduce?", "Waste sent to landfills|The need for sunlight|The number of books|The length of roads", "Waste sent to landfills"),
        ("Which map feature explains symbols?", "Legend|Title page only|Compass needle only|Border color", "Legend"),
        ("What is latitude used to measure?", "Distance north or south of the Equator|Distance above a roof|Depth of a river only|Time on a clock", "Distance north or south of the Equator"),
        ("Why do time zones exist?", "Earth rotates, so places experience daylight at different times|Countries wanted longer weeks|Oceans move clocks|Mountains block calendars", "Earth rotates, so places experience daylight at different times"),
        ("What is a public service?", "A service provided for community needs|A private diary|A toy collection|A secret club", "A service provided for community needs"),
        ("Why is first aid important?", "It gives immediate help before full medical care|It replaces all doctors|It is only for sports|It prevents every accident", "It gives immediate help before full medical care"),
        ("What does a budget help a family plan?", "How to use money wisely|How to name planets|How to grow feathers|How to stop seasons", "How to use money wisely"),
        ("Which person designs buildings?", "Architect|Composer|Pilot|Dentist", "Architect"),
        ("What does a documentary usually do?", "Presents factual information|Always tells a fairy tale|Only shows cartoons|Sells tickets to a game", "Presents factual information"),
        ("Why are landmarks useful?", "They help identify important places|They make clocks faster|They turn roads into rivers|They replace maps", "They help identify important places"),
        ("What is tourism?", "Travel to visit places for interest or recreation|The study of insects|A type of currency|A form of voting", "Travel to visit places for interest or recreation"),
        ("Which term means the usual weather of a place over many years?", "Climate|Daily mood|Traffic|Currency", "Climate"),
        ("What is population?", "The number of people living in an area|The height of buildings|The price of bread|The width of roads", "The number of people living in an area"),
        ("Why can learning another language be useful?", "It helps people communicate across cultures|It removes the need to listen|It changes gravity|It replaces all maps", "It helps people communicate across cultures"),
        ("What does a mayor often help lead?", "A city or town|A whole ocean|A private bedroom|A mountain range", "A city or town"),
        ("Which institution makes laws in many countries?", "Parliament|Museum|Market|Airport", "Parliament"),
        ("What is a constitution?", "A set of basic rules for a country or organization|A weather report|A sports uniform|A cooking recipe", "A set of basic rules for a country or organization"),
        ("Why is saving money useful?", "It helps prepare for future needs|It makes prices disappear|It stops homework|It changes the calendar", "It helps prepare for future needs"),
        ("What is emergency information used for?", "Getting help quickly during danger|Choosing a favorite color|Naming a pet|Planning a picnic only", "Getting help quickly during danger"),
        ("Which sport is played at Wimbledon?", "Tennis|Cricket|Basketball|Hockey", "Tennis"),
        ("What does a composer create?", "Music|Buildings|Medicine|Maps", "Music"),
        ("Which person explores unknown or less-known places?", "Explorer|Banker|Tailor|Printer", "Explorer"),
        ("What is a border?", "A line separating areas or countries|A kind of musical note|A tool for cooking|A type of cloud", "A line separating areas or countries"),
        ("Why do newspapers have editors?", "To check and prepare stories for publication|To drive delivery trucks only|To print money|To repair cameras", "To check and prepare stories for publication"),
        ("What is trade?", "Buying, selling, or exchanging goods and services|A type of rainfall|A way to draw circles|A mountain path only", "Buying, selling, or exchanging goods and services"),
        ("Which hemisphere is south of the Equator?", "Southern Hemisphere|Northern Hemisphere|Eastern Hemisphere only|Western Hemisphere only", "Southern Hemisphere"),
        ("What does longitude measure?", "Distance east or west of the Prime Meridian|Height of a building|Weight of a package|Speed of a train", "Distance east or west of the Prime Meridian"),
        ("Why do communities need transport systems?", "To help people and goods move from place to place|To stop all travel|To replace schools|To remove roads", "To help people and goods move from place to place"),
        ("What is a festival?", "A special celebration or event|A bank account|A road sign|A weather tool", "A special celebration or event"),
        ("Which person studies science professionally?", "Scientist|Composer|Athlete|Actor", "Scientist"),
        ("What is democracy?", "A system where people have a voice in government|Rule by one mountain|A type of library|A weather pattern", "A system where people have a voice in government"),
        ("Why are cultural traditions important?", "They connect people with shared history and identity|They replace all laws|They stop language learning|They are only sports rules", "They connect people with shared history and identity"),
        ("What does an athlete train for?", "Sports performance|Book printing only|Weather prediction|Currency exchange", "Sports performance"),
        ("What is a tournament?", "A series of contests to find a winner|A type of passport|A school building|A newspaper page", "A series of contests to find a winner"),
        ("Why are emergency numbers short?", "So people can remember and dial them quickly|So phones weigh less|So roads are wider|So maps are smaller", "So people can remember and dial them quickly"),
        ("What does a bank help people do?", "Store and manage money|Grow vegetables|Measure earthquakes|Translate books", "Store and manage money"),
        ("Which map tool shows direction?", "Compass rose|Index page|Paragraph|Receipt", "Compass rose"),
    ],
}

for key, questions in QUESTION_BANKS.items():
    category, difficulty = key
    SEED_QUESTIONS.extend((category, difficulty, question, options, answer) for question, options, answer in questions)

for key, questions in QUALITY_BANKS.items():
    category, difficulty = key
    SEED_QUESTIONS.extend((category, difficulty, question, options, answer) for question, options, answer in questions)



def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                xp INTEGER NOT NULL,
                coins INTEGER NOT NULL,
                level INTEGER NOT NULL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO score (id, xp, coins, level) VALUES (1, 0, 0, 1)"
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                question TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer TEXT NOT NULL
            )
            """
        )
        connection.execute("UPDATE questions SET category = 'Mathematics' WHERE category = 'Math'")
        connection.execute(
            """
            DELETE FROM questions
            WHERE category NOT IN ('Mathematics', 'English', 'Science', 'General Knowledge')
            """
        )
        connection.execute(
            """
            DELETE FROM questions
            WHERE question LIKE 'What is % + %?'
               OR question LIKE 'What is % x %?'
               OR question LIKE 'A student read % pages on Monday%'
               OR question LIKE 'Which word is a naming word in this group %'
               OR question LIKE 'Choose the correct past tense sentence %'
               OR question LIKE 'Which sentence uses punctuation correctly %'
               OR question LIKE 'Which object is a living thing %'
               OR question LIKE 'What form of energy is used by a lamp %'
               OR question LIKE 'Which explanation best describes why shadows change during the day %'
               OR question LIKE 'Which item helps people read a book in the dark %'
               OR question LIKE 'Which place is used to borrow books %'
               OR question LIKE 'Which answer best describes a map scale %'
               OR question LIKE 'Which answer best matches the topic of %'
            """
        )
        connection.executemany(
            """
            INSERT INTO questions (category, difficulty, question, options, correct_answer)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM questions
                WHERE category = ? AND difficulty = ? AND question = ?
            )
            """,
            [item + item[:3] for item in SEED_QUESTIONS],
        )


def get_score() -> dict[str, int]:
    init_db()
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute("SELECT xp, coins, level FROM score WHERE id = 1").fetchone()
    return {"xp": row[0], "coins": row[1], "level": row[2]}


def get_categories() -> list[str]:
    init_db()
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("SELECT DISTINCT category FROM questions ORDER BY category").fetchall()
    return [row[0] for row in rows]


def get_difficulties() -> list[str]:
    init_db()
    return ["Easy", "Medium", "Hard"]


def get_random_question(category: str, difficulty: str) -> dict[str, object]:
    init_db()
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute(
            """
            SELECT id, category, difficulty, question, options
            FROM questions
            WHERE category = ? AND difficulty = ?
            """,
            (category, difficulty),
        ).fetchall()
    if not rows:
        return {}
    recent_key = (category, difficulty)
    recent = RECENT_QUESTIONS[recent_key]
    candidates = [row for row in rows if row[0] not in recent] or rows
    row = choice(candidates)
    recent.append(row[0])
    return {
        "id": row[0],
        "category": row[1],
        "difficulty": row[2],
        "question": row[3],
        "options": row[4].split("|"),
        "seconds": 30,
    }


def submit_answer(question_id: int, answer: str, time_left: int) -> dict[str, object]:
    init_db()
    with sqlite3.connect(DB_PATH) as connection:
        row = connection.execute(
            "SELECT correct_answer FROM questions WHERE id = ?",
            (question_id,),
        ).fetchone()
        if row is None:
            return {"correct": False, "earned_xp": 0, "earned_coins": 0, "score": get_score()}

        correct = answer == row[0]
        earned_xp = calculate_xp(correct, time_left)
        earned_coins = 5 if correct else 0
        if correct:
            connection.execute(
                """
                UPDATE score
                SET xp = xp + ?, coins = coins + ?, level = ((xp + ?) / 100) + 1
                WHERE id = 1
                """,
                (earned_xp, earned_coins, earned_xp),
            )

    return {
        "correct": correct,
        "correct_answer": row[0],
        "earned_xp": earned_xp,
        "earned_coins": earned_coins,
        "score": get_score(),
    }

