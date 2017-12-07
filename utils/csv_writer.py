
import io

class csv_writer():

    def reset(self):
        # prepare empty dict with specified fields
        self.values = dict(zip(self.fields, [''] * len(self.fields)))

    def __init__(self, filename, fields):
        # configuration
        self.fields = fields.keys()

        # open input file
        self.f = open(filename, 'w')

        # prepare input dict
        self.reset()

        # prepare field list with [units]
        fields_str = list()
        for k, v in fields.items():
            if v != None:
                fields_str.append(k + ' [' + v + ']')
            else:
                fields_str.append(k)

        # write header
        header = ','.join(fields_str)
        self.f.write(header + '\n')

    def store(self):
        # prepare list of values, preserve original sequence
        val_list = [str(self.values[x]) for x in self.fields]

        # convert to string
        vl_str = ','.join(val_list)

        # write to file
        self.f.write(vl_str + '\n')
        self.f.flush()          # remove to speedup?

        # reset input dict
        self.reset()
        
    # destructor - close file
    def __del__(self):
        try:
            self.f.close()
        except:
            pass
