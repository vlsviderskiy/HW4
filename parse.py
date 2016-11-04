import pandas as pd
import os
import matplotlib.pyplot as plt

table_ = pd.read_excel('06222016 Staph Array Data.xlsx', sheetname = ['Plate 1','Plate 2','Plate 3','Plate 4','Plate 5','Plate6','Plate7','Plate8','Plate9','Plate10','Plate11'], skiprows = 1)
# import table as a dictionary of tables named table_
    # each table is called by its name, for plates after number 5 there is no space between plate and the number



# A for loop going through each table to create columns with patient ID, visit number, and titer

for tablenum in table_:  # tablenum will call each table
    for item in range(len(table_[tablenum])):  # Go through each row for the length of each table, item is row number
        # Create column for 'Visit Number'
        if ('V1' in table_[tablenum].ix[item, 0]) or ('v1' in table_[tablenum].ix[item, 0]):
            table_[tablenum].ix[item, "Visit Number"] = 1
        elif ('V2' in table_[tablenum].ix[item, 0]) or ('v2' in table_[tablenum].ix[item, 0]):
            table_[tablenum].ix[item, "Visit Number"] = 2
        elif ('V3' in table_[tablenum].ix[item, 0]) or ('v3' in table_[tablenum].ix[item, 0]):
            table_[tablenum].ix[item, "Visit Number"] = 3
        elif ('62900   ' in table_[tablenum].ix[item, 0]) or ('17588   ' in table_[tablenum].ix[item, 0]):
            table_[tablenum].ix[item, "Visit Number"] = 1
        else:
            table_[tablenum].ix[item, "Visit Number"] = 1
        # Create Column for 'Patient ID'
        if 'Standard' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Patient ID"] = 'Standard'
        elif 'GS' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Patient ID"] = table_[tablenum].ix[item, 0][0:11]
        elif 'JM' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Patient ID"] = table_[tablenum].ix[item, 0][0:10]
        elif 'VANDER' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Patient ID"] = table_[tablenum].ix[item, 0][0:9]
        elif 'HSS' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Patient ID"] = table_[tablenum].ix[item, 0][0:9]
        else:
            table_[tablenum].ix[item, "Patient ID"] = table_[tablenum].ix[item, 0][0:5]



for tablenum in table_:  # tablenum will call each table
    for item in range(len(table_[tablenum])):  # Go through each row for the length of each table, item is row number
        # Create column for 'Dilution'
        if '10000000' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 10000000
        elif '1000000' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 1000000
        elif '100000' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 100000
        elif '10000' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 10000
        elif '1000' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 1000
        elif '100' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 100
        elif '10' in table_[tablenum].ix[item, 0]:
            table_[tablenum].ix[item, "Dilution"] = 10
        else:
            continue

# Fix Plate 5 ID 84504, which has running mistakes in ID number and Visit Number at points
table_["Plate 5"].ix[40:42, 'Patient ID'] = '84504'
table_["Plate 5"].ix[44:46, 'Visit Number'] = 3.0

# Generate dictionaries of Hospital, Age, and Gender for each Patient ID

Hosp_Dict = {}
Age_Dict = {}
Gend_Dict = {}

for tablenum in table_: # tablenum will call each table
    for item in range(len(table_[tablenum])):
        if not tablenum == 'Plate11':  # Plate 11 does not have this information
            if not table_[tablenum].ix[item, "Patient ID"] in Hosp_Dict:
                if not table_[tablenum].ix[item, "Hospital "] == 'NaN':
                    Hosp_Dict[table_[tablenum].ix[item, "Patient ID"]] = table_[tablenum].ix[item, 'Hospital ']
            if not table_[tablenum].ix[item, "Patient ID"] in Age_Dict:
                if not table_[tablenum].ix[item, "Age"] == 'NaN':
                    Age_Dict[table_[tablenum].ix[item, "Patient ID"]] = table_[tablenum].ix[item, 'Age']
            if not table_[tablenum].ix[item, "Patient ID"] in Gend_Dict:
                if not table_[tablenum].ix[item, "Gender"] == 'NaN':
                    Gend_Dict[table_[tablenum].ix[item, "Patient ID"]] = table_[tablenum].ix[item, 'Gender']

# Fill all the Hospital, Age, and Gender information in for every row that has a unique ID

for tablenum in table_:  # tablenum will call each table
    for item in range(len(table_[tablenum])):  # Go through each row for the length of each table, item is row number
        if not tablenum == 'Plate11':
            # if table_[tablenum].ix[item, "Hospital "] == 'NaN':
            table_[tablenum].ix[item, "Hospital "] = Hosp_Dict[table_[tablenum].ix[item, "Patient ID"]]
            table_[tablenum].ix[item, "Age"] = Age_Dict[table_[tablenum].ix[item, "Patient ID"]]
            table_[tablenum].ix[item, "Gender"] = Gend_Dict[table_[tablenum].ix[item, "Patient ID"]]

# Make new directory of updated files
if not 'Updated Files' in os.listdir('.'):
    os.makedirs('Updated Files')
os.chdir('Updated Files')  # Change directory to output new files in updated files folder

# Generate tsv files for each plate with the updated columns and information
for tablenum in table_:
    table_[tablenum].to_csv(tablenum + '.tsv', sep='\t')

# Make new directory for graphs
os.chdir('..')
if not 'Graphs' in os.listdir('.'):
    os.makedirs('Graphs')
os.chdir('Graphs')


#Fix Patient 27986 being in Plate8 and Plate9
moved_27986_dict = table_.copy()
patient27986_mask = moved_27986_dict["Plate9"].ix[3:6,:]

moved_27986_dict["Plate9"] = moved_27986_dict["Plate9"][moved_27986_dict["Plate9"]["Patient ID"] != "27986"]
moved_27986_dict["Plate8"]= moved_27986_dict["Plate8"].append(patient27986_mask, ignore_index=True)


for plate in moved_27986_dict:  # Iterate through each plate

    if not plate in os.listdir('.'):  #Create a folder with the plate name for the graphs
        os.makedirs(plate)
    os.chdir(plate)

    # make a list of patient IDs
    d = moved_27986_dict[plate]
    list_of_patientids = []
    for patient in d["Patient ID"]:
        if patient not in list_of_patientids:
            list_of_patientids.append(patient)

    # make a list of column values
    column_values = list(d.columns.values)
    if plate == 'Plate11':
        list_of_columns = column_values[1:50] #Plate 11 has 3 less columns
    else:
        list_of_columns = column_values[4:53]

    non_period_columns = {}
    for num1, test in enumerate(list_of_columns):  #Create a dictionary of period column names without their periods
        if '.' in test:
            for num2, letter in enumerate(test):
                if letter == '.':
                    non_period_columns[test] = test[0:num2] + ' ' + test[num2+1:len(test)]



    # Make dictionary of masked data_frames for each visit number
    mask_dict = {}
    mask_dict1 = {}
    mask_dict2 = {}
    mask_dict3 = {}
    count2 = 0
    count3 = 0
    for patientid in list_of_patientids:
        x = (d["Patient ID"] == patientid)
        y1 = (d['Visit Number'] == 1.0)
        y2 = (d['Visit Number'] == 2.0)
        y3 = (d['Visit Number'] == 3.0)
        mask_dict[patientid] = d.ix[x, :]
        mask_dict1[patientid] = mask_dict[patientid].ix[y1, :]
        a = 0
        for index, row in mask_dict[patientid].iterrows():  # Make sure there is a V2 for the Patient ID
            if (row['Visit Number']) == 2.0:
                a = 1
            count2 += 1
        if a == 1:
            mask_dict2[patientid] = mask_dict[patientid].ix[y2, :]

        b = 0
        for index, row in mask_dict[patientid].iterrows():  # Make sure there is a V3 for the Patient ID
            if (row['Visit Number']) == 3.0:
                b = 1
            count3 += 1
        if b == 1:
            mask_dict3[patientid] = mask_dict[patientid].ix[y3, :]

    for patientid in list_of_patientids:  # Iterate through each patientID and plot the graphs

        if patientid != 'Standard':

            if not patientid in os.listdir('.'):   #Create a folder within each plate for each patient's plots
                os.makedirs(patientid)
            os.chdir(patientid)

            for test in list_of_columns: #Iterate through each test for plots
                if not (((plate == 'Plate 1' or plate == 'Plate 2') and test == 'BSA') or (plate == 'Plate10' and test == 'Pn PS23')):
                    fig = plt.figure(figsize=(10, 8))
                    plt.plot(mask_dict1[patientid].ix[:, ['Dilution']], mask_dict1[patientid].ix[:, [test]], label='V1',
                            marker=('o'))
                    if patientid in mask_dict2:
                        plt.plot(mask_dict2[patientid].ix[:, ['Dilution']], mask_dict2[patientid].ix[:, [test]], label='V2',
                                 marker=('v'))
                    if patientid in mask_dict3:
                        plt.plot(mask_dict3[patientid].ix[:, ['Dilution']], mask_dict3[patientid].ix[:, [test]], label='V3',
                                 marker=('*'))
                    plt.yscale('log')
                    plt.xscale('log')
                    plt.xlabel('Dilution')
                    plt.ylabel('Intensity')
                    plt.title(plate + '_' + patientid + '_' + test)
                    plt.legend(loc=1)
                    if '.' in test:
                        plt.savefig(plate + '_' + patientid + '_' + non_period_columns[test])
                    else:
                        plt.savefig(plate + '_' + patientid + '_' + test)
                    plt.close()
            os.chdir('..') #Go back to the plate folder


    os.chdir('..') #Go back to the graphs folder


