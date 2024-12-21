from concurrent import futures
import grpc
from addressbook_pb2_grpc import AddressBookServiceServicer, add_AddressBookServiceServicer_to_server
from addressbook_pb2 import Person, AddressBook
from google.protobuf import empty_pb2, timestamp_pb2
import time

class AddressBookService(AddressBookServiceServicer):
    def __init__(self):
        # In-memory storage for our address book
        self.address_book = {}  # id -> Person
        
    def AddPerson(self, request, context):
        person = request.person
        # Generate ID if not provided
        if person.id == 0:
            person.id = len(self.address_book) + 1
            
        # Set last updated timestamp
        current_time = timestamp_pb2.Timestamp()
        current_time.GetCurrentTime()
        person.last_updated.CopyFrom(current_time)
        
        self.address_book[person.id] = person
        return person

    def GetPerson(self, request, context):
        if request.id not in self.address_book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Person with ID {request.id} not found')
            return Person()
        
        return self.address_book[request.id]

    def ListPeople(self, request, context):
        address_book = AddressBook()
        address_book.people.extend(self.address_book.values())
        return address_book

    def UpdatePerson(self, request, context):
        if request.id not in self.address_book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Person with ID {request.id} not found')
            return Person()
        
        current_time = timestamp_pb2.Timestamp()
        current_time.GetCurrentTime()
        request.last_updated.CopyFrom(current_time)
        self.address_book[request.id] = request
        return request

    def DeletePerson(self, request, context):
        if request.id not in self.address_book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Person with ID {request.id} not found')
            return empty_pb2.Empty()
        
        del self.address_book[request.id]
        return empty_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_AddressBookServiceServicer_to_server(
        AddressBookService(), server
    )
    server.add_insecure_port('[::]:50051')
    print("Starting server on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 