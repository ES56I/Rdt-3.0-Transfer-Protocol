from common import *
from NetworkSimulator import *

class receiver:
    
    def isCorrupted(self, packet):
        ''' Checks if a received packet has been corrupted during transmission.
        Return true if computed checksum is different than packet checksum.'''
        
        response = False 
        
        #Checks to see if the packet is the proper size if not it has been corrupted
        if packet.checksum != checksumCalc(packet.payload) + packet.seqNum:
            response = True      
           
        return response
   
    def isDuplicate(self, packet):
        '''checks if packet sequence number is the same as expected sequence number'''
        
        if packet.seqNum == self.seqNum:
            return True 
        
        return False
    
    def getNextExpectedSeqNum(self):
        '''The expected sequence numbers are 0 or 1'''
        
        if self.seqNum == 1:
            Next_num = 0
        else:
            Next_num = 1
        return Next_num
    
    
    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing receiver: B: "+str(self.entity))


    def init(self):
        '''initialize expected sequence number'''
        
        self.seqNum = 0 
        
        
        #self.AckNum = 0 
        #self.entity = A
        #print(f'this is the entity: {self.entity}')
        #print(f'this is the seqNum: {self.seqNum}')
        
        return
         

    def input(self, packet):
        '''This method will be called whenever a packet sent 
        from the sender arrives at the receiver. If the received
        packet is corrupted or duplicate, it sends a packet where
        the ack number is the sequence number of the  last correctly
        received packet. Since there is only 0 and 1 sequence numbers,
        you can use the sequence number that is not expected.
        
        If packet is OK (not a duplicate or corrupted), deliver it to the
        application layer and send an acknowledgement to the sender
        '''
        #Checks for Corruption or duplication, if it is found then will reformat packet
        if self.isCorrupted(packet) == True or self.isDuplicate(packet) == True:
            self.ackNum = self.seqNum
            self.check = self.ackNum
            self.packet = Packet(self.seqNum, self.ackNum, self.check)
            self.networkSimulator.udtSend(self.entity, self.packet)
            self.seqNum = packet.seqNum
           
        
        #If Packet found to be not corrupted or a duplicate packing may commence
        else:
            self.seqNum = packet.seqNum
            self.ackNum = self.seqNum
            self.getNextExpectedSeqNum()
            self.networkSimulator.deliverData(self.entity, packet)
            self.seqNum = 0
            
            # Preparing Packet 
            self.packet = Packet(self.seqNum, self.ackNum, self.check)
            
            # Sending Packet
            self.networkSimulator.udtSend(self.entity, self.packet)
            self.payload = packet.payload
            self.check = self.ackNum

        return
