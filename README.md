# LangFlix

This is the Github Folder for the LangFlix application, developed by:
-    Victoria Brueva (s1099693)
-    Lotte de Groot (s1035928)
-    Chantal Vedder (s1011793)
-    Mariia Zamyrova (s1038789)
-    Lars Zandbergen (s1107552)

## How to run the application:
To make it easy to inspect the app, we have created a short demo version for Windows. To install this application, please follow these steps:
1. Download the LangFlix zip file from this link: [https://drive.google.com/file/d/1QQUagdj7hanDmBR4U6A_QUk3Zy_Imhzo/view?usp=sharing](https://drive.google.com/file/d/1QQUagdj7hanDmBR4U6A_QUk3Zy_Imhzo/view?usp=sharing)  .
   The file will not be avaiable forever, but should be online for long enough to evaluate the application. Please contact the team if the file is not available.
2. Extract the Zip file you just downloaded. Find a suitable location, we recommend selecting the option to extract to a new folder.
3. Navigate into the NML_front_video folder, and find NML_front_video.exe
   It is possible a pop-up will show up saying the file may not be safe. Or maybe your Anti-virus will block the file. Please try to solve the issue
4. LangFlix should be started, we usually test at level B2 since we know the exercises show up. An exercise should show up around 2:40 minutes into the video, so don't be alarmed if it takes a while.
5. Enjoy using LangFlix, skip around, see your personal dictionary, change settings and if you want you can disable Langflix with the LangFlix button if you prefer to watch 10 minutes of a random French show.
6. After ten minutes the show should end, we kept the preview short to save on storage space.

## Project description

This project basically consists of two seperate parts. The back_end and the front_end.

## Back_end
In the back_end there are two important files. `distractor_words.py` is used for creating distractor words. This file should be called from the main LangFlix folder. For each of the subtitle files, this file creates a Dictionary with "distractor" words. These are the words that can appear as multiple choice options. These are then stored as a dictionary to a json file, together with their Zipf Frequency. This makes it possible to select them for exercises.

The second file is called `simple_parsing.py` and should be called from the main LangFlix folder. This file is used to create the exercises. It takes the json file with the distractor words and the subtitle files as input. It then creates a new subtilte file with exercises. This file is then used by the front_end.

## Front_end
The front_end consists of three files. `cefr_to_zipf.py` converts the CEFR level that a user receives after completing the online test to a Zipf level. This is used to select the right exercises while watching a show. This function is called from `NML_front_video.py` and should not be called seperately.

`NML_front_video.py` is the main controller of the front_end. This file should be called from within the front_end folder, and then the application will be started. Inside there are also options to select a different episode. It is used to create the GUI and to control the video player. It also contains the selecting of exercices and the distractor words. Initially we had planned to use translated versions of the distractor dictionaries to translate the other words in the exercise, but we kept exeperiencing gaps in our data. So instead we used the deep_translate package to translate the distractor words on the go.

Finally, there is `Video.py`. This file is used to create the video player. It is used by `NML_front_video.py`. There is no need to call it seperately. It uses the VLC package to create the video player.

