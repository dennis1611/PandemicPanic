# User Stories
1. Define display_report function
    - As a: developer
    - I want: to write the function that display a report in the terminal with information about recent developments of the virus
    - So: we can check whether the calculations are performed correctly.

2. Options for measures
    - As a: developer
    - I want: to make a list (non-code) with which measures can be implemented in the game, and what their effect will (factor to multiply R by)
    - So: these can be implemented later

3. Define choose_measure function
    - As a: developer
    - I want: to create a terminal-based interface in which the user can choose what measure to take each turn
    - So: the players can choose which measure(s) to take

4. Define update_infected function
    - As a: developer
    - I want: to write the method that calculates the new infections for each week based on the R-number and previous infections, and save the information in a list
    - So: the calculations will actually be performed

5. Create region class
    - As a: developer
    - I want: to create a class to describe a region and store the people that are healthy, infected or dead.
    - So: the information is properly stored and can easily be retrieved while also allowing for visualization later on.

6. Create measure class
    - As a: developer
    - I want: to create a class for measures and add the relevant properties to it (implementation is not part of this issue)
    - So: the measures can easily be initialized later

7. Set non-variable infection factors
    - As a: developer
    - I want: to gather and process the required data that can/will be used to calculate new infections
    - So: the calculations can be (reasonably) realistic

8. Implement region class
    - As a: developer
    - I want: to implement the region class into the main loop
    - So: the infections are stored with the region instead of only in the main loop.

9. Implement measure class
    - As a: developer
    - I want: to implement the measure class
    - So: more measures can be added easily

10. Write txt/csv file with measures
    - As a: developer
    - I want: to create a txt or csv file with all measures and their effects
    - So: at game startup this can be read to load in all measures, while allowing for easy balancing later.

11. Write txt/csv file with regions
    - As a: developer
    - I want: to create a txt or csv file with all regions and their attributes
    - So: at game startup this can be read to load in all regions

12. Create DataFrame to store data per time interval
    - As a: developer
    - I want: to use pandas to store important data about the infection
    - So: this can be easily displayed later

13. Basic visualisation of game progress using the DataFrame
    - As a: user
    - I want: to see the DataFrame displayed in the terminal
    - So: It becomes easier to track my progress

14. Add the option to rollback taken measures
    - As a: user
    - I want: to see which measures are taken already, and have the option to undo measures that are taken already
    - So that: the gameplay will be more interactive and realistic

15. Pygame button implementation
    - As a: developer
    - I want: to implement pygame buttons to pick a measure.
    - So: the game looks prettier and clearer than in a console.

16. Bordering regions should affect each others infections
    - As a: user
    - I want: that adjacent regions have influence on each other
    - So that: the game will give a more realistic representation of a real-life virus outbreak

17. Find solution so that .csv's/.png do not have to be copied to the test folder
    - As a: developer
    - I want: that there is no need anymore to copy all source files to the test folder, but that it reads them from the original location
    - So that: we have to do less maintenance

18. Balancing R-value effects and balance deaths
    - As a: user
    - I want: the effects of the measures and large amounts of infected to be more realistic
    - So: the game becomes more challenging.

19. Implement death
    - As a: user
    - I want: to view the number of people who have died from the virus.
    - So: I can get a better view of the severity of the infection.

20. Implement recoveries
    - As a: product owner
    - I want: that recoveries are calculated and subtracted from the total amount of infections
    - So that: the game will be much more realistic

21. Implement max infections based on inhabitants
    - As a: developer
    - I want: to make sure the infections cannot exceed the inhabitants
    - So: this particular bug is fixed

22. Get rid of global variable measure_numbers
    - As a: developer
    - I want: to find an alternate solution for the usage of the global variable measure_numbers
    - So that: there will be an unnecessary global variable less

23. Improve Pygame window
    - As a: developer
    - I want: to improve the Pygame window by satisfying the following requirements:
        - Outline map
        - Add information in data table
        - End screen should be beautified and centered
        - Add buttons to enable/disable all measures in a region
        - Add buttons to enable/disable a measure in all regions
        - Place description of measures logically
    - So: the window is pleasant to use and contains all information

24. Implement PyGame window
    - As a: user
    - I want: to have a map and table in the window the game runs in
    - So: the infection can be tracked visually

25. Implement ending, score
    - As a: developer
    - I want: to create an end condition and start to add a score system
    - So: the program turns into more of an actual game

26. Measures as part region class
    - As a: developer
    - I want: to move the measures to the region class
    - So: The user can take regional measures instead of national

27. Fix generating of regional_data.csv
    - As a: developer
    - I want: that the region names are generated properly in the regional_data.csv file
    - So that: they can be accessed by name later on, instead of only by index number
    - Requirements:
        - The file regional_factors.py or source file data_provinces.csv must be adjusted so that
        - There is no " (PV)" after the region name
        - "Friesland" is spelled like this

28. Use OOP for screen.py
    - As a: developer
    - I want: that screen.py will be written in an OOP way
    - So that: the code will be modular again
    - Requirements:
        - There should be a class for the entire screen (current Screen class)
        - Subclass of Screen: a class for the map on the left
        - Subclass of Screen: a class for everything related to the measures on the top right (possibly with the current Button class as subclass)
        - Subclass of Screen: a class for the numbers on the bottom right

29. PNG test issue in test_regions.py
    - As a: developer
    - I want: to fix the loading of the png images in the region test file
    - So: the tests work in both terminal and visual mode

30. Research on measure realism
    - As a: developer
    - I want: more exact data on the effect of the measures
    - So: they can be balanced within reasonable boundaries

31. Refactor region class & fix pylint
    - As a: developer
    - I want: to do a cleanup of the code (mainly related to the terminal and visual mode split), and go over the pylint recommendation and try to make the pylint pipeline phase pass.
    - So that: the code will be easier to maintain and automated tests/lint can be fully used
    - Requirements:
        - Create a class RegionExtended that inherits from Region, so that Region works for terminal mode and RegionExtended works for visual mode
        
32. Improve usage of report_terminal
    - As a: user
    - I want: that the report of new infections etc. is more useful (currently it only shows Groningen but that is not mentioned anywhere)
    - So that: terminal mode is actually playable and also useful for debugging