#!/usr/bin/env python3

import json

def from_json_file(filepath, field_list=None):
    try:
        data = None
        with open(filepath, newline="") as file_stream:
            data = json.loads(file_stream)

            if field_list:
                filtered = []
                for entry in data:
                    filtered_entry = {entry for key, value in data.items() if entry in field_list}
                    filtered.append(filtered_entry)

        return data
    except OSError as error:
        print("OSError thrown in from_json_file(): %s" % str(error))
    except TypeError as error:
        print("TypeError thrown in from_json_file(): %s" % str(error))
    except Exception as error:
        print("General exception thrown in from_json_file(): %s" % str(error))

def to_json_file(filepath, data, field_list=None):
    try:
        data = None
        with open(filepath, mode="w+", newline="") as file_stream:
            data = json.loads(file_stream)
        return data
    except OSError as error:
        print("OSError thrown in from_json_file(): %s" % str(error))
    except TypeError as error:
        print("TypeError thrown in from_json_file(): %s" % str(error))
    except Exception as error:
        print("General exception thrown in from_json_file(): %s" % str(error))

    output_data = json.dumps(input_data)
    return output_data



#     json_data = json.loads(input_data)

#     fields = field_list if field_list != None else json_data[0].keys()
#     header = "%s\n" % delimiter.join(fields)

#     content = []
#     for entry in json_data:
#         filtered = [str(entry[field]) if field in entry else "" for field in fields]
#         content.append("%s\n" % delimiter.join(filtered))

#     output_data = [header]

#     for entry in content:
#         output_data.append(entry)

#     return output_data

# def convert_csv_to_json(input_data, delimiter, field_list):

#     content = []
#     for i, line in enumerate(input_data):
#         if i == 0:
#             header = line.split(delimiter)
#         else:
#             content.append(line.split(delimiter))

#     output_data = []
#     for line in content:
#         entry = { header[i]: field for i, field in enumerate(line) }
#         output_data.append(entry)

#     output_data = json.dumps(output_data)

#     return output_data