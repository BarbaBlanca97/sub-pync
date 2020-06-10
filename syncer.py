import sys

user_offset   = sys.argv[1]
user_filename = sys.argv[2]

input_file      = open(user_filename , 'r')
output_file     = open('synced-' + user_filename , 'w')

def sign(number):
    if number < 0:
        return -1
    else:
        return 1

offset          = float(user_offset)
offset_hours    = int(offset / 3600)
offset_minutes  = sign(offset) * int((abs(offset) % 3600 ) / 60)
offset_seconds  = sign(offset) * int(((abs(offset) % 3600 ) % 60))
offset_mili     = int(((offset - int(offset)) * 1000 ))


def toZeroStart(number):
    if number < 10:
        return '0' + str(number)
    else:
        return str(number)

def toZeroStartMilis(number):
    if number < 100:
        if number < 9:
            return '00' + str(number)
        else:
            return '0' + str(number)
    else:
        return str(number)

def timestampToArray(timestamp):
    first_split = timestamp.split(',')
    second_split = first_split[0].split(':')

    return [int(second_split[0]), int(second_split[1]), int(second_split[2]), int(first_split[1])]


def updateTimestamp(timestamp):
    timestamp_array = timestampToArray(timestamp)

    extra_seconds = 0
    extra_minutes = 0
    extra_hours = 0

    new_mili = timestamp_array[3] + offset_mili
    if new_mili > 999:
        new_mili = new_mili - 999
        extra_seconds = 1
    elif new_mili < 0:
        new_mili = 999 + new_mili
        extra_seconds = -1

    new_seconds = timestamp_array[2] + offset_seconds + extra_seconds
    if new_seconds > 59:
        new_seconds = new_seconds - 60
        extra_minutes = 1
    elif new_seconds < 0:
        new_seconds = 60 + new_seconds
        extra_minutes = -1

    new_minutes = timestamp_array[1] + offset_minutes + extra_minutes
    if new_minutes > 59:
        new_minutes = new_minutes - 60
        extra_hours = 1
    elif new_minutes < 0:
        new_minutes = 60 + new_minutes
        extra_hours = -1

    new_hours = timestamp_array[0] + offset_hours + extra_hours

    return ( toZeroStart(new_hours) + ':' + toZeroStart(new_minutes) + ':' + toZeroStart(new_seconds) + ',' + toZeroStartMilis(new_mili) )

line = input_file.readline()
while line != '':

    block_number = line

    block_timestamps = input_file.readline().split(' --> ')
    new_timestamp = updateTimestamp(block_timestamps[0]) + ' --> ' + updateTimestamp(block_timestamps[1])

    block_text = []
    text_line = input_file.readline()
    while text_line != '\n':
        block_text.append(text_line)
        text_line = input_file.readline()
    
    output_file.write(block_number)
    output_file.write(new_timestamp + '\n')
    output_file.writelines(block_text)

    line = input_file.readline()

    if line != '':
        output_file.write('\n')


input_file. close()
output_file.close()