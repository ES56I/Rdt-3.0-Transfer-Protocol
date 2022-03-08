from common import *
# from NetworkSimulator import *

class sender:
    RTT = 20
    
    def isCorrupted (self, packet):
        '''Checks if a received packet (acknowledgement) has been corrupted
        during transmission.
        Return true if computed checksum is different than packet checksum.
        '''
        
        # Checks if the packet has the correct sequence number
        if packet.seqNum != 0:
            return True 
        
        # Checks if the checksum calc is correct
        if checksumCalc(packet.payload, packet.ackNum) != self.currSeqNum:
            return True

        # Checks to make sure the seq number is correct        
        if packet.seqNum != 0:
            return True 
        
        # Checks to see if the payload is empty
        if packet.payload != "":
            return True

        return False

    def isDuplicate(self, packet):
        '''checks if an acknowledgement packet is duplicate or not
        similar to the corresponding function in receiver side
        '''
        if self.seqNum == packet.ackNum:
            return False
        else:
            return True

        return
 
    def getNextSeqNum(self):
        '''generate the next sequence number to be used.
        '''
        
        if self.seqNum == 1:
            self.seqNum = 0
        else:
            self.seqNum = 1
 
        return 

    def __init__(self, entityName, ns):
        self.entity = entityName
        self.networkSimulator = ns
        print("Initializing sender: A: "+str(self.entity))

    def init(self):
        '''initialize the sequence number and the packet in transit.
        Initially there is no packet is transit and it should be set to None
        '''
        #Checks to make sure all values are initialized correctly
        self.packet = None
        self.seqNum = 0 
        self.ackNum = 0
                
        return

    def timerInterrupt(self):
        '''This function implements what the sender does in case of timer
        interrupt event.
        This function sends the packet again, restarts the time, and sets
        the timeout to be twice the RTT.
        You never call this function. It is called by the simulator.
        '''
        # sets the timeout to be twice the RTT
        self.newRTT = 2 * self.RTT
        
        #print(f'this is the RTT: {self.RTT}')
        #print(f'this is the new RTT: {self.newRTT}')
        
        # Starts the timer 
        self.networkSimulator.startTimer(self.entity, self.newRTT)
        
        # Send the packet to the reciever
        self.networkSimulator.udtSend(self.entity, self.packet)
        
        return


    def output(self, message):
        '''prepare a packet and send the packet through the network layer
        by calling calling utdSend.
        It also start the timer.
        It must ignore the message if there is one packet in transit
        '''
        
        if self.packet == None:
                self.check = checksumCalc(message.data) + self.seqNum + self.ackNum
                
                # Adjusts self.check if the seq num is 1 
                if self.seqNum == 1:
                    self.check = checksumCalc(message.data) + 1
                    
                # Creates a packet
                self.packet = Packet(self.seqNum, self.ackNum, self.check, message.data)
                
                #Sends a packer over the network simulator
                self.networkSimulator.udtSend(self.entity, self.packet)
                self.networkSimulator.startTimer(self.entity, self.RTT)
    
        return
 
    
    def input(self, packet):

        '''If the acknowlegement packet isn't corrupted or duplicate, 
        transmission is complete. Therefore, indicate there is no packet
        in transition.
        The timer should be stopped, and sequence number  should be updated.

        In the case of duplicate or corrupt acknowlegement packet, it does 
        not do anything and the packet will be sent again since the
        timer will be expired and timerInterrupt will be called by the simulator.
        '''
        
        #Initial checks
        if packet != None and self.isDuplicate(packet) == False:
            self.networkSimulator.stopTimer(self.entity)
            self.getNextSeqNum()
            self.packet = None

        # If packet is duplicate ignore it 
        elif self.isDuplicate(packet) == True:
            pass
        
        # If packet is corrupted ignore it 
        elif self.isCorrupted(packet) == True:
            pass
                
        return 
