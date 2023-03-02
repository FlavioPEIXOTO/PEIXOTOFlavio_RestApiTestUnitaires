def get_sql_request_type_by_request_string(sql_request_string):

    if isinstance(sql_request_string, str):
        # Find the starting index of "INSERT"
        substring = sql_request_string.split()[0]

        if substring is not None:
            # Extract the substring starting from the "INSERT" index
            return substring
        else:
            return None

    else:
        raise ValueError("Given param not a string")


def check_element_type(elements, type):
    for element in elements:
        if isinstance(element):
            continue
        else:
            return ValueError("Argument is not a string")

    return True