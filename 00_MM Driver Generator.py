from random import randint
import csv
import time

#NOTE & REMINDER: THIS PROGRAM WAS WRITTEN IN PYTHON 3.12.2, IT IS UNTESTED WITH ANY OTHER VERSION OF PYTHON, IF THERE IS A BUG OR AN ERROR, TEST IT WITH 3.12.2 BEFORE REPORTING.
#Provisionally, it should work with anything later than Python 3.

def nationality_and_name():
    first_name = "-1"
    while first_name == "-1" or first_name == "First Names":    #A driver having "First Names" as their first name was a weird bug that I never managed to fix so my solution was to repeat the loop if "First Names" was the driver's first name.
        countries_list = list(csv.reader(open(r".\Countries.csv")))
        nation_value = randint(1,6273)     #6273 is the sum of all the values in the Probability column of the Regen Nationality Weighting file, which is the Weighting column in Countries.csv.
        index = 1
        while index <= len(countries_list):
            if nation_value == 6273:    #Special case because for some reason, without this, the program will throw a list out of range error.
                nation = countries_list[-1][0]
                break
            elif nation_value >= int(countries_list[index][1]):
                nation_value -= int(countries_list[index][1])
                index += 1
            else:
                nation = countries_list[index][0]
                break
        gender = randint(0,1)   #To align with the way MM stores gender data about names, a "0" represents male and a "1" represents female.
        names_list = list(csv.reader(open(r".\Names.csv", encoding="utf-8"))) #There needs to be the letter "r" before the name of the file because otherwise, Python will think it's a malformed \n.
        if gender == 0:
            male_first_name_start = int(names_list[index][2])
            male_first_name_end = int(names_list[index][3])
            male_second_name_start = int(names_list[index][6])
            male_second_name_end = int(names_list[index][7])

            first_name_index = randint(male_first_name_start, male_first_name_end)
            first_name = names_list[first_name_index + 1][0]

            second_name_index = randint(male_second_name_start, male_second_name_end)
            second_name = names_list[second_name_index + 1][1]
        else:
            female_first_name_start = int(names_list[index][4])
            female_first_name_end = int(names_list[index][5])
            female_second_name_start = int(names_list[index][8])
            female_second_name_end = int(names_list[index][9])

            if female_first_name_start != "-1":
                first_name_index = randint(female_first_name_start, female_first_name_end)
                first_name = names_list[first_name_index + 1][0]

            second_name_index = randint(female_second_name_start, female_second_name_end)
            second_name = names_list[second_name_index + 1][1]
    return(nation, gender, first_name, second_name)

def drivers(drivers_to_generate, employment, starting_year, min_age, max_age):
    input("Before starting, please ensure that 01_Output.txt is closed as having it open will interfere with being able to write to the file. \nPress enter to continue.")
    pay_driver_marketability_mode = int(input("How should a pay driver's marketability be calculated? \nEnter '0' for it to be random like other drivers. \nEnter '1' for it to be random + 25%, for pay drivers to attract better sponsors. \nEnter '2' for it to be random - 25% to simulate pay drivers being less popular. \nEnter '3' for marketability to be based loosely on talent."))
    team_ID = 2    #team_ID starts at 2 because that is the first team ID in the game's database. In vanilla, a team ID of 2 refers to Steinmann Motorsport in WMC.
    team_IDs_list = [1, 1, 1, 1, 1, 1]   #team_IDs_list starts off like this because the last and the sixth to last items in the list, at most, are called to check that a team doesn't have the maximum amount of drivers assigned to it. If the list is less than six, the program will give an error.
    car_list = [0, 0, 0, 0]    #car_list starts off like this because the three most recent items in the list are called to check that these aren't the same as the fourth. If the list is less than three, the program will give an error.
    previous_driver_status = ""
    traits_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 77, 78, 80, 81, 82, 83, 165, 198, 199, 200, 201, 204, 207, 208, 286, 287, 288, 289, 290, 291, 292]
    out = open("./01_Output.txt", "a", encoding="utf-8")
    start = time.time()
    i = 0
    while i < drivers_to_generate:
        nation, gender, first_name, second_name = nationality_and_name()
        if employment == 1:    #This code seems pretty ugly with nested loops and repeats but I'm not smart enough to code it any better.
            while True:    #Using while True: and a break here saves me from creating another variable that stores the length of team_IDs at the start and checks that it hasn't changed to run the loop again.
                if team_ID == "":
                    break
                elif team_ID <= 51:   #51 is the last team ID of the GT teams, after this is Endurance which have six drivers per team, not three.
                    if team_IDs_list[-1] and team_IDs_list[-3] != team_ID:
                        team_IDs_list.append(team_ID)
                        break
                    else:
                        team_ID += 1
                elif team_ID <= 63:
                    if team_IDs_list[-1] and team_IDs_list[-6] != team_ID:
                        team_IDs_list.append(team_ID)
                        break
                    else:
                        team_ID += 1
                else:
                    team_ID = ""
                    break
    
            if team_ID <= 51:
                if i % 3 == 2:    #1 out of 3 drivers will be a reserve.
                    status = "Reserve"
                    previous_driver_status == "Reserve"
                elif previous_driver_status == "One":    #If the other main driver in a team is a number one driver, this driver is a number two.
                    status = "Two"
                elif previous_driver_status == "Equal":    #If the other main driver in a team is equal, this driver is also equal.
                    status = "Equal"
                else:
                    status = randint(1,2)
                    if status == 1:    #If this is the first main driver, 50-50 chance a driver is a number one driver rather than equal.
                        status = "One"
                        previous_driver_status == "One"
                    else:
                        status = "Equal"
                        previous_driver_status == "Equal"
                car = ""
            elif team_ID <= 63:
                status = randint(1,3)   #The vanilla database seems to do this for Endurance.
                if status == 1:
                    status = "One"
                elif status == 2:
                    status = "Two"
                else:
                    status = "Equal"
        
                if car_list[-1] and car_list[-3] == 1:
                    car = 2
                    car_list.append(car)
                elif car_list[-1] and car_list[-3] == 2:
                    car = 1
                    car_list.append(car)
                elif car_list[-1] and car_list[-3] == 0:
                    car = 1
                    car_list.append(car)
                else:
                    car = car_list[-1]
                    car_list.append(car)
            else:
                team_ID = ""
                car = ""
                status = ""
        else:
            team_ID = ""
            car = ""
            status = ""
    
        year = randint(max_age,min_age)

        month = randint(1,12)
        if month < 10:
            month = "0" + str(month)

        if month == "01" or "03" or "05" or "07" or "08" or "10" or "12":
            day = randint(1,31)
        elif month == "04" or "06" or "09" or "11":
            day = randint(1,30)
        elif month == "02" and year % 4 == 0:
            day = randint(1,29)
        else:
            day = randint(1,28)

        if int(day) < 10:
            day = "0" + str(day)

        if team_ID != "" and employment == 1:
            contract_start = randint(starting_year - 2,starting_year)
            contract_end = randint(contract_start,contract_start + 3)
        else:
            contract_start = ""
            contract_end = ""
        
        fame = randint(-1,2)
        scouting_level = randint(0,3)
        weight = randint(53,82)    #I chose these values because they are the minimum and maximum values for weight that show up in vanilla drivers.txt.

        number_of_personality_traits = randint(1,5)
        traits = ""
        j = 1
        if employment == 1:
            if status == "Reserve":
                pay_driver_roll = randint(1,10)
                if pay_driver_roll == 10:
                    traits = "165;"
                    j += 1
        while j <= number_of_personality_traits:
            trait = randint(1,len(traits_list))
            if str(trait) not in traits:
                if j == number_of_personality_traits:
                    traits = traits + str(trait)
                else:
                    traits = traits + str(trait) + ";"
                j += 1

        if team_ID != "":
            qualifying_bonus_amount = 0
            race_bonus_amount = 0
            champion_bonus = 0
        else:
            qualifying_bonus_amount = ""
            race_bonus_amount = ""
            champion_bonus = ""
        qualifying_bonus_position = ""
        race_bonus_position = ""
        if "165" in traits:
            pay_driver = 1
        else:
            pay_driver = 0
        optimal_zone = (randint(40,93))/100    #In the vanilla drivers.txt, every driver has an optimal zone, used only in Endurance. This value is inbetween 0.4 and 0.93 for all drivers.

        abilities = ""
        if team_ID != "":
            if team_ID <= 11 and status != "Reserve":   #This code looks bad but with the comments, it might be more understandable than an improved code.
                for x in range(9):
                    abilities = abilities + str((randint(1600,2000)/100)) + "," #WMC drivers.
            elif team_ID <= 11 and status == "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(1500,1800)/100)) + "," #WMC reserves.
            elif team_ID <= 21 and status != "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(1200,1600)/100)) + "," #APSC drivers.
            elif team_ID <= 21 and status == "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(1100,1500)/100)) + "," #APSC reserves.
            elif team_ID <= 31 and status != "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(800,1200)/100)) + "," #ERS drivers.
            elif team_ID <= 31 and status == "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(700,1000)/100)) + "," #ERS reserves.
            elif team_ID <= 41 and status != "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(1200,1600)/100)) + "," #IGTC drivers.
            elif team_ID <= 41 and status == "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(1100,1500)/100)) + "," #IGTC reserves.
            elif team_ID <= 51 and status != "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(800,1200)/100)) + "," #GTCS drivers.
            elif team_ID <= 51 and status == "Reserve":
                for x in range(9):
                    abilities = abilities + str((randint(700,1000)/100)) + "," #GTCS reserves.
            elif team_ID <= 57:
                for x in range(9):
                    abilities = abilities + str((randint(1200,1600)/100)) + "," #IEC drivers.
            else:
                for x in range(9):
                    abilities = abilities + str((randint(800,1200)/100)) + "," #IECB drivers.
        else:
            for x in range(9):
                abilities = abilities + str((randint(0,2000)/100)) + "," #Unemployed drivers.

        abilities_list = abilities.split(",")   #I like this code. Stars calculation, sum all values, divide by 180 and multiply by 5.
        total_ability = 0
        for x in range(9):
            total_ability = total_ability + float(abilities_list[x])
        stars = total_ability / 180
        stars = stars * 5

        if team_ID != "":   #Assign wages if the driver has a job (MM doesn't seem to have unemployment benefits).
            if stars <= 1:  #Hopefully this is balanced. I hate this code as well.
                wages = randint(0,300)/100
            elif stars <= 2:
                wages = randint(300,600)/100
            elif stars <= 3:
                wages = randint(600,900)/100
            elif stars <= 4:
                wages = randint(900,1200)/100
            else:
                wages = randint(1200,1500)/100
            if team_ID >= 52:    #If this is an endurance driver, divide wages by three (endurance drivers get lower pay in vanilla as each time has six drivers).
                wages = wages / 3
            if status == "Reserve":    #If this is a reserve driver, divide wages by three.
                wages = wages / 3
        else:
            wages = ""
    
        if pay_driver == 1:
            if pay_driver_marketability_mode == 0:
                marketability = randint(0,100)
            elif pay_driver_marketability_mode == 1:
                marketability = randint(0,75) + 25
            elif pay_driver_marketability_mode == 2:
                marketability = randint(25,100) - 25
            else:
                if stars <= 2:
                    marketability = randint(0,33)
                elif stars <= 3.5:
                    marketability = randint(34,67)
                else:
                    marketability = randint(68,100)
        else:
            marketability = randint(0,100)

        driving_style = randint(1,100)  #From here: I don't think a lot of this is used by the game except morale, potential and chairman popularity but it's really easy to add to the code.
        driver_number = ""
        races = ""
        wins = ""
        podiums = ""
        poles = ""
        dnfs = ""
        dnfs_via_error = ""
        dns = ""
        career_points = ""
        championships = ""
        form = ""
        experience = randint(1,100)
        morale = randint(40,100)
        obedience = randint(1,100)
        potential = randint(0,68)
        patience = randint(2,5)
        chairman_popularity = randint(0,100)
        fans_popularity = randint(0,100)
        sponsor_popularity = randint(0,100)
    
        skin_colour = randint(0,5)
        hair = randint(0,7)
        if gender == 0:
            facial_hair = randint(1,11)
        else:
            facial_hair = ""
        hair_colour = randint(1,11)
        glasses = randint(0,4)
        accessory = 0   #Most drivers have this set as 0 and I don't know what it does exactly, if anything. I might test it.
        body_type = 0   #I don't know why the developers put this in drivers.txt since it has the same value for all drivers.
        hat = randint(0,17)
        helmet_style = 0   #I don't know why the developers put this in drivers.txt since it has the same value for all drivers.

        helmet_primary_colour = randint(1,10)   #I thought that this was controlled by team colours.txt using hex values. No idea why it's here in drivers.txt but they all are random values from one to ten.
        helmet_secondary_colour = randint(1,10)
        helmet_tertiary_colour = randint(1,10)

        brake_supplier_preference = randint(1,5)   #I don't think that the game uses this but it would have been great to see this implemented in game. Drivers could have a +1 or 2 braking stat if team uses the preferred brake supplier.

        improvement_rate = randint(8,160)   #These are the min and max values used in vanilla, adjust these if you think that drivers reach their peak too quickly or slowly.
        peak_duration = randint(1,6)   #These are the min and max values used in vanilla, adjust these if you think that drivers fall off in performance too quickly after reaching their peak.
        peak_age = randint(26,37)   #These are the min and max values used in vanilla, adjust these if you think that drivers reach their peak too young or too old.

        desired_championships = randint(1,3)
        desired_wins = randint(1,10)
        desired_earnings = 0
        desired_budget = 100

        if team_ID != "":
            if team_ID <= 31:
                series = randint(0,3)
                if series == 0:
                    series_preference = "SingleSeaterSeries"
                elif series == 1:
                    series_preference = "SingleSeaterSeries; GTSeries"
                elif series == 2:
                    series_preference = "SingleSeaterSeries; EnduranceSeries"
                else:
                    series_preference = "Any"
            elif team_ID <= 51:
                series = randint(0,3)
                if series == 0:
                    series_preference = "EnduranceSeries"
                elif series == 1:
                    series_preference = "SingleSeaterSeries; EnduranceSeries"
                elif series == 2:
                    series_preference = "EnduranceSeries; GTSeries"
                else:
                    series_preference = "Any"
            else:
                series = randint(0,3)
                if series == 0:
                    series_preference = "GTSeries"
                elif series == 1:
                    series_preference = "SingleSeaterSeries; GTSeries"
                elif series == 2:
                    series_preference = "EnduranceSeries; GTSeries"
                else:
                    series_preference = "Any"
        else:
            series = randint(0,6)
            if series == 0:
                series_preference = "SingleSeaterSeries"
            elif series == 1:
                series_preference = "SingleSeaterSeries; GT Series"
            elif series == 2:
                series_preference = "SingleSeaterSeries; EnduranceSeries"
            elif series == 3:
                series_preference = "EnduranceSeries"
            elif series == 4:
                series_preference = "EnduranceSeries; GTSeries"
            elif series == 5:
                series_preference = "GTSeries"
            else:
                series_preference = "Any"
            
        reward_ID = ""

        if gender == 0:
            gender = "M"
        else:
            gender = "F"
        if first_name != "-1" and first_name != "First Names":
            output = first_name + "," + second_name + "," + gender + "," + str(team_ID) + "," + str(status) + "," + str(car) + "," + nation + "," + str(day) + "/" + str(month) + "/" + str(year) + "," + traits + "," + str(fame) + "," + str(scouting_level) + "," + str(weight) + "," + str(wages) + "," + str(contract_end) + "," + str(contract_start) + "," + str(qualifying_bonus_amount) + "," + str(qualifying_bonus_position) + "," + str(race_bonus_amount) + "," + str(race_bonus_position) + "," + str(champion_bonus) + "," + str(pay_driver) + "," + str(abilities_list[0]) + "," + str(abilities_list[1]) + "," + str(abilities_list[2]) + "," + str(abilities_list[3]) + "," + str(abilities_list[4]) + "," + str(abilities_list[5]) + "," + str(abilities_list[6]) + "," + str(abilities_list[7]) + "," + str(abilities_list[8]) + "," + str(optimal_zone) + "," + str(driving_style) + "," + driver_number + "," + races + "," + wins + "," + podiums + "," + poles + "," + dnfs + "," + dnfs_via_error + "," + dns + "," + career_points + "," + championships + "," + form + "," + str(experience) + "," + str(morale) + "," + str(obedience) + "," + str(potential) + "," + str(patience) + "," + str(chairman_popularity) + "," + str(fans_popularity) + "," + str(sponsor_popularity) + "," + str(skin_colour) + "," + str(hair) + "," + str(hair_colour) + "," + str(glasses) + "," + str(accessory) + "," + str(facial_hair) + "," + str(body_type) + "," + str(hat) + "," + str(helmet_style) + "," + str(helmet_primary_colour) + "," + str(helmet_secondary_colour) + "," + str(helmet_tertiary_colour) + "," + str(marketability) + "," + str(brake_supplier_preference) + "," + str(improvement_rate) + "," + str(peak_duration) + "," + str(peak_age) + "," + str(desired_championships) + "," + str(desired_wins) + "," + str(desired_earnings) + "," + str(stars) + "," + series_preference + "," + reward_ID
            out.write(output)
            out.write("\n")
            
            if i > 0:    #If more than one driver has been generated (remember that i starts at 0 and then increases).
                print(str(i + 1) + " drivers have been generated.")
            else:
                print(str(i + 1) + " driver has been generated.")
            i += 1   #A driver has been fully generated.
            
    end = time.time()
    print("Operation completed in:", end - start, "seconds.")



while True:
    print("Enter one of the following letters to select which staff type to generate. Note: This program is in development, new options will be added soon.")
    print("To generate drivers, enter 'D'")
    print("To quit, enter 'Q'")
    selection = input()
    if selection == "D" or selection == "d":
        drivers_to_generate = int(input("How many drivers do you want to generate?"))
        employment = int(input("Enter '1' if you want drivers to be assigned teams sequentially, including reserve drivers in all series. \nEnter '2' if you want all drivers to be unemployed."))
        min_age = int(input("Enter the year of birth of the youngest drivers you want."))
        max_age = int(input("Enter the year of birth of the oldest drivers you want."))
        if employment == 1:
            starting_year = int(input("Enter the game's starting year, when contracts will start and end will centre around this number."))
            drivers(drivers_to_generate, employment, starting_year, min_age, max_age)
        elif employment == 2:
            starting_year = "N/A"
            drivers(drivers_to_generate, employment, starting_year, min_age, max_age)
        else:
            input("Invalid selection. Press the enter key to try again.")
    elif selection == "Q" or selection == "q":
        break
    else:
        input("Invalid selection. Press the enter key to try again.")
