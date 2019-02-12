def save_as_file(object, filepath):
    file = open(filepath, 'wb')
    file.write(object)
    file.close()