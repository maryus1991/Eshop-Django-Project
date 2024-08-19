def list_slicer(UnSlicedList: list, group_size: int = 4):
    return_list = []
    ranged_list = range(0, len(UnSlicedList), group_size)
    for i in ranged_list:
        return_list.append(UnSlicedList[i:i + group_size])
    return return_list