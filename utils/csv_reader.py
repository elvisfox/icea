
import io

class csv_reader():
    def __init__(self, filename):
        # open input file
        self.f = open(filename, 'r')

        # read header (column names)
        cols = self.f.readline()

        # store list of columns
        self.col_list = cols.rstrip().split(',')

        # read units
        cols = self.f.readline()

        # store units
        self.unit_dict = dict(zip(self.col_list, cols.rstrip().split(',')))


    # returns dictionary field = value
    def readline(self):
        # read line from file, skip empty lines
        line = ''
        while(line == ''):
            # read line from file
            line = self.f.readline()

            # check for EOF
            if line == '':
                return None
                
            # strip \n
            line = line.rstrip()

        # split into fields (string)
        val_s = line.split(',')

        # convert to list of int/float/string (what works first)
        values = list()
        for x in val_s:
            try:
                values.append(int(x))
            except:
                try:
                    values.append(float(x))
                except:
                    values.append(x)

        # return dictionary
        return dict(zip(self.col_list, values))
        
    # destructor - close file
    def __del__(self):
        try:
            self.f.close()
        except:
            pass
