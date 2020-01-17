import scipy.io
import glob
import csv
import pandas as pd


def parse_one_sensor(filename, sensor_number):
    matlab_data = scipy.io.loadmat(filename)

    if sensor_number >= len(matlab_data['ECG'][0][0][2]):
        print('Error: incorrect sensor number')
        return None
    else:
        print('Success: founded {} values'.format(len(matlab_data['ECG'][0][0][2][sensor_number])))

    sensor_data = matlab_data['ECG'][0][0][2][sensor_number]
    gender = matlab_data['ECG'][0][0][0][0]
    age = matlab_data['ECG'][0][0][1][0][0]

    return [gender, age, *sensor_data]


def parse_all_sensors(filename):
    matlab_data = scipy.io.loadmat(filename)

    sensors_data = matlab_data['ECG'][0][0][2]
    gender = matlab_data['ECG'][0][0][0][0]
    age = matlab_data['ECG'][0][0][1][0][0]

    return gender, age, sensors_data


def parse_data_for_one_sensor(folder, answers_filename, sensor_number):
    with open('sensor_{}.csv'.format(sensor_number), mode='w') as result_file:
        writer = csv.writer(result_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        answers = pd.read_csv(answers_filename)

        for filename in glob.glob('{}/*.mat'.format(folder)):
            current_answer_name = filename.split('/')[-1].split('.')[0]

            current_answer = answers[answers['Recording'] == current_answer_name].iloc[0]
            current_data = parse_one_sensor(filename, sensor_number)

            result_data = [
                current_answer['First_label'], current_answer['Second_label'],
                current_answer['Third_label'], *current_data
            ]
            writer.writerow(result_data)


def parse_data_for_all_sensors(folder, answers_filename, sensors_count):
    files = []
    writers = []
    for i in range(sensors_count):
        file = open('sensor_{}.csv'.format(i), mode='w')

        writers.append(csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL))
        files.append(file)

    answers = pd.read_csv(answers_filename)

    for filename in glob.glob('{}/*.mat'.format(folder)):
        current_answer_name = filename.split('/')[-1].split('.')[0]

        current_answer = answers[answers['Recording'] == current_answer_name].iloc[0]
        current_data = parse_all_sensors(filename)

        for i in range(sensors_count):
            result_data = [
                current_answer['First_label'], current_answer['Second_label'],
                current_answer['Third_label'], current_data[0], current_data[1], *current_data[2][i]
            ]
            writers[i].writerow(result_data)

    for file in files:
        file.close()


if __name__ == '__main__':
    folder_name = 'FOLDER_NAME'
    answers_filename = 'ANSWERS_FILENAME'
    parse_data_for_one_sensor(folder_name, answers_filename, 0)
