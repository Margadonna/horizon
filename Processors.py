class Processor:
    
    @staticmethod
    def dict_value_to_int (data:dict):
        for key in data:
            try:
                data[key] = float(data[key])
            except:
                continue
        return data



