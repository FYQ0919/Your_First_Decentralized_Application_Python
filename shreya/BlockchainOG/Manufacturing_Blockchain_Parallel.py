"""
Project Title: Blockchain FYP
Program title: Manufacturing_Blockchain_Parallel
This program simulates a blockchain manufacturing scenario for assembly of CPUs. The production process is parallel and
each product can randomly choose the next step based on the state diagram of assembly process.
It calculates the time taken to complete production of user-defined number of products, part quality, rework status
and other parameters for data analysis of project
Written by Shreya Sinha
"""
import pandas
from random import *
import requests

# JSON = JavaScript Object Notation - an open-standard file format that uses
# human-readable text to transmit data objects consisting of attribute–value
# pairs and array data types (or any other serializable value).
# It is a very common data format used for asynchronous browser–server
# communication
# noinspection PyUnresolvedReferences
import json
# noinspection PyUnresolvedReferences
from time import time
# noinspection PyUnresolvedReferences
from urllib.parse import urlparse
# noinspection PyUnresolvedReferences
from uuid import uuid4
# Requests = licensed HTTP library
# Requests will allow you to send HTTP/1.1 requests using Python.
# Add content like headers, form data, multipart files, and parameters
# via simple Python libraries. It also allows you to access the response
# data of Python in the same way.
# noinspection PyUnresolvedReferences
from flask import Flask, jsonify, request

# todo: Create a dictionary of step name and step number based on Pooi Mun's parallel processes to get next step
application = Flask(__name__)
# Import variables needed for each step [Parts/Production Time]
variables = pandas.read_csv('Data_Sheet.csv')
# Import Part UID used in each step
part_id = pandas.read_csv('PartUID_Sheet.csv')
# Keeps track of Part Number used from csv file
part_id_counter = []
part_id_counter.extend([0] * 30)
# Keeps track of the steps completed during parallel production
done_array = []
done_array.extend([0] * 17)
# Part List
part_list = ['Cover', 'Intrusion_Switch', 'WLAN_Card', 'Front_Bezel', 'Expansion_Card', 'Memory_Card',
             'CoinCell_Battery', 'Hard_Drive', 'Optical_Drive', 'Power_Supply', 'Heat_Sink_Assembly', 'Processor',
             'Processor_Socket', 'System_Fan', 'Thermal_Sensor', 'Power_Switch', 'IO_Panel', 'System_Board', 'Screws',
             'Grommets', 'Power_Cable', 'Data_Cable', 'WLAN_Cable', '4pin_Power_Cable', '8pin_Power_Cable', 'Fan_Cable',
             'Captive_Screws', 'Thermal_Sensor_Cable', 'USB_Cable', 'N_A']
total_number_of_steps = 17

# HTTP Transfer over Blockchain
Post_Transaction = 'http://localhost:5000/transactions/new'
Mine_Transaction = 'http://localhost:5000/mine'

total_number_of_parts = input("Enter number of parts to make ")
total_number_of_parts = int(total_number_of_parts)


# todo: Multi line string descriptions for each function

# *************************** FUNCTIONS *************************************************

def get_step_status():
    """
    Determines if a manufacturing process is carried out successfully or not
    :return: Step status
    :rtype: string
    """
    probability = randint(1, 100)
    if probability < 95:
        return "Pass"
    else:
        return "Fail"


def post_blockchain_data(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    """
    Creates a JSON file format payload to send over the HTTP network and complete addition of a valid block to chain
    """
    step_text = str(step)
    part1_text = str(part1)
    partid1_text = str(partid1)
    part2_text = str(part2)
    partid2_text = str(partid2)
    part3_text = str(part3)
    partid3_text = str(partid3)
    part4_text = str(part4)
    partid4_text = str(partid4)
    status_text = str(status)
    payload = "{\n    \"step_number\":\"" + step_text + "\", \"part1\":\"" + part1_text + "\",\"partid1\":\"" + partid1_text + "\", \"part2\":\"" + part2_text + "\", \"partid2\":\"" + partid2_text + "\", \"part3\":\"" + part3_text + "\", \"partid3\":\"" + partid3_text + "\", \"part4\":\"" + part4_text + "\", \"partid4\":\"" + partid4_text + "\", \"status\":\"" + status_text + "\"}"
    headers = {
        'Content-Type': "application/json",
    }
    response = requests.request("POST", Post_Transaction, data=payload, headers=headers)
    print(response.text)
    return


def is_busy(part, step, production_time):
    """
    Determines if a station is busy with another part production or free
    """
    free = time_array[part][step] - production_time
    # print("is_busy: Free ", free)
    if free >= production_time:
        return True
    else:
        return False


def get_step_number(part, step, production_time):
    """
     Determines next step for a part based on free stations and state diagram
    """
    next_step_1 = variables.loc[step, 'Next_Step_1']
    next_step_2 = variables.loc[step, 'Next_Step_2']
    next_step_3 = variables.loc[step, 'Next_Step_3']
    next_step_4 = variables.loc[step, 'Next_Step_4']
    if step_number == 16:
        return 17
    step_array = []
    if next_step_1 > 0:  # add step number to array only if it is an integer. Special case for step 16
        step_array.append(next_step_1)
    if next_step_2 > 0:
        step_array.append(next_step_2)
    if next_step_3 > 0:
        step_array.append(next_step_3)
    if next_step_4 > 0:
        step_array.append(next_step_4)
    # print("get_step_number: Step array", step_array)
    # remove elements that are busy
    # print("length of array", len(step_array))
    for x1 in range(0, len(step_array)-1):
        # print("x1", x1)
        if is_busy(part, step_array[x1], production_time):
            step_array.remove(step_array[x1])
    # if array size becomes 0 return next_step_1
    if len(step_array) == 0:  # step 17 will give error as all entries are -1. Add terminating condition
        next_step_option = next_step_1
    else:
        import random
        next_step_option = random.choice(step_array)
    # print("NEXT STEP OPTION RANDOM CHOICE", next_step_option)
    # special case for step = 4
    # special case for step = 9
    # special case for array size = 0
    if step == 4:
        if done_array[1] == 1:
            if done_array[2] == 1:
                if done_array[3] == 1:
                    next_step_option = 5
                else:
                    next_step_option = 3
            else:
                next_step_option = 2
        else:
            next_step_option = 1

    if step == 9:
        if done_array[6] == 1:
            if done_array[7] == 1:
                if done_array[8] == 1:
                    next_step_option = 10
                else:
                    next_step_option = 8
            else:
                next_step_option = 7
        else:
            next_step_option = 6

    if done_array[next_step_option] == 1:
        # previous step number needed to ensure it does not go into infinite recursion. Remove this option from steps
        # wrong production time. It should be for the give next_step_option
        return get_step_number(part, next_step_option, production_time)
    else:
        return next_step_option


def get_production_time(step):
    """
    Determines the production time for a step between the given upper and lower bound in the excel for a given step
    :param step: manufacturing process
    :return: production time
    """
    time_min = variables.loc[step, 'Production_Time_Min']
    time_max = variables.loc[step, 'Production_Time_Max']
    production_time = randint(time_min, time_max)
    return production_time


def get_validation_time(step):
    """
    Determine validation time for a step based on a given lower and upper limit
    Only human validators take extra time for validation as they can only perform one task at a time
    """
    # print("Validation Type", variables.loc[step, 'Validator_Type'])
    if variables.loc[step, 'Validator_Type'] == "Human":
        time_min = variables.loc[step, 'Validation_Time_Min']
        time_max = variables.loc[step, 'Validation_Time_Max']
        validation_time = randint(time_min, time_max)
    else:
        validation_time = 0
    return validation_time


def secondary_validation():
    """
    Determines the part quality of a part/step that has completed production and determines if all the other validators
    in the network agree with the primary validator.
    """
    quality_array = [""] * (total_number_of_steps - 1)
    for i in range(total_number_of_steps - 1):
        quay = randint(1, 100)
        if quay < 50:
            quality_array[i] = "Poor"
        else:
            quality_array[i] = "Good"
    number_good = quality_array.count("Good")
    # greater than 50% of validators give a pass status
    if number_good >= 8:
        return "Good"
    else:
        return "Poor"


def sec_validation_correctness():
    """
    Determine the actual status of each process to compare with simulation results and understand the accuracy of
    multiple blockchain validations
    """
    # Each validator has 85% accuracy of correct secondary validation
    # Array that tabulates validation status of each validator for each process
    correctness = [0]*17
    count = 0
    for xx in range(0, total_number_of_parts):
        for yy in range(0, total_number_of_steps):
            for quality in range(0, len(correctness)):
                # Find the probabilities that each validator gives an erroneous validation
                correctness[quality] = randint(1, 100)
                if correctness[quality] < 15:
                    # 15% chance that validation is incorrect
                    count += 1
            # print("Count ", count)
            if count > 7:
                # More than 50% of validators validated incorrectly
                actual_sec_validation[xx][yy] = 'Poor'
            else:
                actual_sec_validation[xx][yy] = 'Good'
            correctness = [0]*17
            count = 0
    return


def calculate_waste_percentage():
    """
    Calculating waste percentage of producing n assemblies based on reworks

    """
    re = 0
    for aa in range(0, total_number_of_parts):
        for bb in range(0, total_number_of_steps):
            re += rework[aa][bb]
    print(re)
    waste_p = re/(total_number_of_steps*total_number_of_parts)
    return waste_p


# Check step 1 function for all n steps - checks correct part used, checks ID of part, checks status,
# checks timestamp and hash can also be added
def check_step_1(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 1 and part1 == 'System_Board' and part2 == 'Screws' and status == 'Pass':
        return "Valid"
    else:
        return "Invalid"


def check_step_2(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 2 and part1 == 'IO_Panel' and part2 == 'Screws' and part3 == 'USB_Cable' and part4 == 'Data_Cable' and \
            status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_3(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 3 and part1 == 'Power_Switch' and part2 == 'Power_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_4(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 4 and part1 == 'Thermal_Sensor' and part2 == 'Thermal_Sensor_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_5(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 5 and part1 == 'System_Fan' and part2 == 'Grommets' and part3 == 'Fan_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_6(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 6 and part1 == 'Processor' and part2 == 'Processor_Socket' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_7(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 7 and part1 == 'Captive_Screws' and part2 == 'Heat_Sink_Assembly' and part3 == 'Fan_Cable' and \
            status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_8(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 8 and part1 == 'Power_Supply' and part2 == '4pin_Power_Cable' and part3 == '8pin_Power_Cable' and part4 == 'Screws' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_9(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 9 and part1 == 'Optical_Drive' and part2 == 'Power_Cable' and part3 == 'Data_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_10(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 10 and part1 == 'Hard_Drive' and part2 == 'Power_Cable' and part3 == 'Data_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_11(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 11 and part1 == 'CoinCell_Battery' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_12(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 12 and part1 == 'Memory_Card' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_13(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 13 and part1 == 'Expansion_Card' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_14(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 14 and part1 == 'Front_Bezel' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_15(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 15 and part1 == 'WLAN_Card' and part2 == 'WLAN_Cable' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_16(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 16 and part1 == 'Intrusion_Switch' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def check_step_17(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    if step == 17 and part1 == 'Cover' and status == 'Pass':
        return 'Valid'
    else:
        return 'Invalid'


def smart_contract_validation(step, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status):
    switcher = {
        0: check_step_1(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        1: check_step_2(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        2: check_step_3(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        3: check_step_4(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        4: check_step_5(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        5: check_step_6(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        6: check_step_7(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        7: check_step_8(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        8: check_step_9(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        9: check_step_10(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        10: check_step_11(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        11: check_step_12(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        12: check_step_13(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        13: check_step_14(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        14: check_step_15(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        15: check_step_16(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status),
        16: check_step_17(step + 1, part1, partid1, part2, partid2, part3, partid3, part4, partid4, status)
    }
    return switcher.get(step, "NOT VALID")


# ******************************* MAIN **************************************************


# Initialise variables needed
# Time to complete production of a single part
time_stamp = 0
step_number = 0
parts = 0
previous_step_number = -1
free_station = 0
# Data analysis parameters
failed_pri_validation = 0
failed_sec_validation = 0
rows, cols = (total_number_of_parts, total_number_of_steps)
rework = [[0 for i in range(cols)] for j in range(rows)]
sec_validation_array = [[0 for i in range(cols)] for j in range(rows)]
actual_sec_validation = [['' for i in range(cols)] for j in range(rows)]
time_array = [[0 for i in range(cols)] for j in range(rows)]

sec_validation_correctness()

while parts < total_number_of_parts:
    print('Part Number:')
    print(parts)
    # Calculate production & validation time for all steps here
    for i in range(0, total_number_of_steps):
        variables.loc[i, 'Production_Time'] = get_production_time(i)
        variables.loc[i, 'Validation_Time'] = get_validation_time(i)
    while step_number < total_number_of_steps:
        # print("Step ", step_number)
        # Index 1 is the name of Part 1
        index1 = variables.loc[step_number, 'Part1']
        # Gives the index of Part List in part_id_counter array
        w = part_list.index(index1)
        index2 = variables.loc[step_number, 'Part2']
        x = part_list.index(index2)
        index3 = variables.loc[step_number, 'Part3']
        y = part_list.index(index3)
        index4 = variables.loc[step_number, 'Part4']
        z = part_list.index(index4)
        # find index of this part in the Parts List array and increment counter in part_id_counter for this index
        # instead of 1, the first variable is the part_id_counter of index1
        # need to increment part_id_counter[x] each time a part is used
        uid1 = part_id.loc[part_id_counter[w], index1]
        uid2 = part_id.loc[part_id_counter[x], index2]
        uid3 = part_id.loc[part_id_counter[y], index3]
        uid4 = part_id.loc[part_id_counter[z], index4]
        # step status is a randomly generated number that determines if the step passed/failed [95% success]
        step_status = get_step_status()
        # Calculations for time taken to produce a part accounting for bottlenecks
        if step_number == 0:
            if step_status == 'Pass':
                time_stamp += (parts + 1) * variables.loc[step_number, 'Production_Time']
                time_array[parts][step_number] = time_stamp
                # print("Here 1", time_stamp)
            else:
                time_stamp += variables.loc[step_number, 'Production_Time']
                time_array[parts][step_number] = time_stamp
                # print("Here 2", time_stamp)
                previous_step_number = step_number  # Use this for rework
        else:
            if parts != 0:
                free_station = time_array[parts - 1][step_number] - variables.loc[step_number, 'Production_Time']
                print("free station", free_station)
            if parts == 0 or free_station >= variables.loc[step_number, 'Production_Time']:
                # if station is free - YOU NEED TO KNOW TIMESTAMP OF PREVIOUS PART. USE 2D ARRAY OF TIMESTAMP
                # For part 0 don't need to check previous part because all stations will be free
                time_stamp += variables.loc[step_number, 'Production_Time']
                time_array[parts][step_number] = time_stamp

            else:
                # add delay to
                if parts != 0:
                    delay = time_array[parts - 1][step_number] - variables.loc[step_number, 'Production_Time']
                    time_stamp += delay + variables.loc[step_number, 'Production_Time']
                    print("Delay", delay)
                else:
                    time_stamp += variables.loc[step_number, 'Production_Time']
                    time_array[parts][step_number] += variables.loc[step_number, 'Production_Time']

        time_stamp += variables.loc[step_number, 'Validation_Time']

        # Create block for posting to all other nodes
        post_blockchain_data(step_number, index1, uid1, index2, uid2, index3, uid3, index4, uid4, step_status)

        # Primary Validation
        # Check the data in the bloc using helper functions [Smart Contract simulation]
        block_status = smart_contract_validation(step_number, index1, uid1, index2, uid2, index3, uid3, index4, uid4,
                                                 step_status)
        # Secondary Validation
        sec_validation_status = secondary_validation()
        sec_validation_array[parts][step_number] = sec_validation_status
        # Mine transaction if block is validated, else return to previous step
        if block_status == 'Valid' and sec_validation_status == 'Good':
            h = requests.get(url=Mine_Transaction)
            print("Step ", (step_number + 1), " is successful " + "Time at addition of block ", time_stamp)
            done_array[step_number] = 1
            previous_step_number = step_number
            step_number = get_step_number(parts, step_number, variables.loc[step_number, 'Production_Time'])

        else:
            # Rework array tracks the number of times secondary validation fails on a part
            rework[parts][step_number] += 1
            print("Step ", (step_number + 1), " is unsuccessful ")
            # Redo the current step
            step_number = step_number
            if sec_validation_status == "Poor":
                print("Part Quality poor by Secondary Validation")

        # Increment all variables for next iteration - Even if step is unsuccessful previous parts cannot be reused
        part_id_counter[w] = part_id_counter[w] + 1
        part_id_counter[x] = part_id_counter[x] + 1
        part_id_counter[y] = part_id_counter[y] + 1
        part_id_counter[z] = part_id_counter[z] + 1

        # Calculation for data analysis - parts that fail primary/secondary validation from blockchain consensus
        if step_status == "Fail":
            failed_pri_validation += 1
        if step_status == 'Pass' and sec_validation_status == 'Poor':
            failed_sec_validation += 1
            # Waste percentage calculation - for each part that fails secondary validation, add number of
            # sub-components in that step that are re-worked
    parts = parts + 1
    time_stamp = 0
    step_number = 0
    done_array = [0] * 17
    print(time_array)
# Time to complete production process
time = max(max(x) for x in time_array)
print("Time to complete production", time)
print("Failed Primary Validation ", failed_pri_validation)
print("Failed Secondary Validation ", failed_sec_validation)
print("Rework array", rework)
print(sec_validation_array)
print(actual_sec_validation)
print("Waste Percentage", calculate_waste_percentage())