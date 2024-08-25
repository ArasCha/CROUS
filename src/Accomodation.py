
class Accomodation:
    
    def __init__(self, accomodation_data: dict):
        
        self.id = accomodation_data["id"]
        self.address = accomodation_data["residence"]["address"]
        self.max_area = accomodation_data["area"]["max"]
        self.min_area = accomodation_data["area"]["min"]
        self.max_rent = accomodation_data["occupationModes"][0]["rent"]["max"]/100
        self.min_rent = accomodation_data["occupationModes"][0]["rent"]["min"]/100
        self.residence_name = accomodation_data["residence"]["label"]
        self.bed_count = accomodation_data["bedCount"]
        