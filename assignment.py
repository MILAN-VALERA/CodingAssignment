import random
import boto3
from botocore.exceptions import DataNotFoundError
import json
class ParkingLot:
    def __init__(self,parking_lot_size,parking_spot_width,parking_spot_length) -> None:
        
        self.available_spot = parking_lot_size// (parking_spot_length*parking_spot_width) # Count Number of available spot
        self.total_spots = [ -1 for i in range(self.available_spot)] 
        
    def isParkingFull(self):
        # check is parking full
        if -1 in self.total_spots:
            return False
        return True
    def uploadTOs3(self):
        # generate json file and upload to s3 
        data = {}
        ACEESS_KEY = ""
        SECRET_KEY = ""
        for i in range(self.available_spot):
            data[i] = self.total_spots[i]
        with open('data.json','w') as f:
            json.dump(data,f)
        try:
            s3 = boto3.client('s3',ACEESS_KEY,SECRET_KEY)
            res = s3.upload_file("data.json","testing","data")
        except DataNotFoundError as e:
            print("Something Went Wrong")
        except Exception as e:
            print("Something Went Wrong")

 
class Car:
    def __init__(self,number_plate) -> None:
        self.number_plate = number_plate

    def park(self,parking_lot:ParkingLot,spot_num) -> str:
        
        if parking_lot.total_spots[spot_num] == -1:
            parking_lot.total_spots[spot_num] = self.number_plate
            return "Car with License plate {} parked succesfully in spot {}".format(self.number_plate,spot_num)
        else:
            print("Spot number {} is occupied , parking on new spot !".format(spot_num))
            for i in range(len(parking_lot.total_spots)):
               
                if parking_lot.total_spots[i] == -1:
                    parking_lot.total_spots[i] = self.number_plate
                    return "Car with License plate {} parked succesfully in spot {}".format(self.number_plate,i)

    def __repr__(self) -> str:
        return self.number_plate
def main(cars):
    pl = ParkingLot(2000,8,12)
    for i in cars:
        c = Car(i)
        print(c.park(pl,random.randint(1,pl.available_spot-1)))
        if pl.isParkingFull():
            print("Parking Slot is full")
            break
        print(str(c))
    temp = input("Do You want to Upload to s3 press Y:- ")
    if temp.lower() ==  "y":
        pl.uploadTOs3()
if __name__ == "__main__":
    cars = ['1000101','1000201','1000301','1000401','1000501','1000601','1000701','1000801','1000901','1001001','1001101','1001201','1001301','1001401','1001501','1001601','1001701','1001801','1001901','1002001','1002101']
    main(cars=cars)



                    
        

