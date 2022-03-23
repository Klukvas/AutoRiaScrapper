


class Serializer:
    
    def brand_model_serializer(self, brand_model:str) -> dict:
        brand_model = brand_model.\
            replace("-", " ").\
                replace(".", "").\
                    replace("груз", "gruz").\
                        replace("пасс", "pass").\
                            replace("пас", "pass").\
                                replace("model", "").\
                                    replace("id", "").\
                                        replace("пас", "pass").\
                                            replace("(", "").\
                                                replace(")", "").\
                                                    replace("  ", " ").\
                                                        lower().\
                                                            strip()
            
        return {"data": brand_model}
                        