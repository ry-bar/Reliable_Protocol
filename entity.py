"""This defines the network entities, Entity is the abstract description of
an Entity where EntityA and EntityB are concrete classes that must be modified
for this assignment"""

from abc import ABC, abstractmethod
import inspect
import packet as pk


# noinspection PyShadowingNames
class Entity(ABC):
    """Abstract concept of an Entity"""

    def __init__(self, sim):
        self.sim = sim

    @abstractmethod
    def output(self, message):
        """called from layer5 when a message is ready to be sent by the application"""

    @abstractmethod
    def input(self, packet):
        """called from layer 3, when a packet arrives for layer 4"""

    @abstractmethod
    def timerinterrupt(self):
        """called when timer goes off"""

    @abstractmethod
    def starttimer(self, increment):
        """Provided: call this function to start your timer"""

    @abstractmethod
    def stoptimer(self):
        """Provided: call this function to stop your timer"""

    def tolayer5(self, data):
        """Provided: call this function when you have data ready for layer5"""

    def tolayer3(self, packet):
        """Provided: call this function to send a layer3 packet"""





# noinspection PyShadowingNames
class EntityA(Entity):
    """Concrete implementation of EntityA. This entity will receive messages
    from layer5 and must ensure they make it to layer3 reliably"""

    def __init__(self, sim):
        super().__init__(sim)
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        # Initialize anything you need here
        self.sent_packet_window = []
        self.ack_received_window = []
        self.to_be_send_window = []
        self.inc_seqnum = 0
        self.inc_acknum = 0


    def output(self, message):# This is the application layer actually giving me the message that it wants to have sent out.
        """Called when layer5 wants to introduce new data into the stream"""
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        # TODO add some code
        # Creating the packet
        pkt = pk.Packet()
        pkt.payload = message
        pkt.checksum = 0
        pkt.seqnum = self.inc_seqnum
        pkt.acknum = self.inc_acknum

        # Appending the seqnum into the set_packet_window.
        self.tolayer3(pkt)  # Layer 3 is the medium which the packets are send through.

        # Adding the packet to the sent_packet_window
        self.sent_packet_window.append(pkt)

        # Incrementing the sequence number for the next packet
        self.inc_seqnum += 1

        # Incrementing the ACK num so the receiver knows which ACK number to send back.
        self.inc_acknum += 1

        # Starting the timer
        self.starttimer(1)

    # TODO: Need to get the timer implemented somehow.  

    def input(self, packet):
        """Called when the network has a packet for this entity"""
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        # TODO add some code
        print(f"\n\nGOT ACK PACKET: {packet}\n")

        # Sending the packet to the corresponding ACK.
        # Checks to make sure the list isn't empty and also checks to see if we get duplicate ACKs
        # If a duplicate ACK is received, sends the next needed packet again.
        if packet.acknum < 999999:
            if packet.acknum == 0:
                # Resending from the first packet.
                for packets in self.sent_packet_window:
                    print(f"RESENDING PACKETS: {packets}")
                    self.tolayer3(packets)


            elif (len(self.ack_received_window) > 0) and (packet.acknum == self.ack_received_window[-1].acknum):
                # Determining the needed packet
                print(f"RECEIVED ACK FOR THIS PACKET AGAIN: {self.ack_received_window[-1]}")
                needed_packet = self.ack_received_window[-1].acknum
                for packets in self.sent_packet_window:
                    print(f"RESENDING PACKETS: {packets}")
                    self.tolayer3(packets)

            elif packet.acknum == self.sent_packet_window[0].acknum + 1:
                print(f"POPPING PACKET: {self.sent_packet_window[0]}")
                #self.stoptimer()
                self.sent_packet_window.pop(0)
                self.ack_received_window.append(packet)# just want to watch all the ACks come in



        print("\n\n")
        self.window_print()
        print("\n\n")


        # packet coming in from the medium?
        #print(f"!!!!!\n\nInput Packet:\n{packet}\n\n!!!!!")
    def window_print(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for packets in self.sent_packet_window:
            print(f"A sent_packet_window: {packets}")
        print("\n")
        for packets in self.ack_received_window:
            print(f"ack_received_window: {packets}")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


    def timerinterrupt(self):
        """called when your timer has expired"""
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        print("RIGHT NOW THE TIMERINTERRUPT CODE WOULD RUN")

    # From here down are functions you may call that interact with the simulator.
    # You should not need to modify these functions.

    def starttimer(self, increment):
        """Provided: call this function to start your timer"""
        self.sim.starttimer(self, increment)

    def stoptimer(self):
        """Provided: call this function to stop your timer"""
        self.sim.stoptimer(self)

    def tolayer5(self, data):
        """Provided: call this function when you have data ready for layer5"""
        self.sim.tolayer5(self, data)

    def tolayer3(self, packet):
        """Provided: call this function to send a layer3 packet"""
        self.sim.tolayer3(self, packet)

    def __str__(self):
        return "EntityA"

    def __repr__(self):
        return self.__str__()










# noinspection PyShadowingNames
class EntityB(Entity):
    def __init__(self, sim):
        super().__init__(sim)

        # Initialize anything you need here
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        self.receiver_packet_window = []
        self.sent_ack_window = []
        self.sent_layer_five = []

    # Called when layer5 wants to introduce new data into the stream
    # For EntityB, this function does not need to be filled in unless
    # you're doing the extra credit, bidirectional part of the assignment
    def output(self, message):
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        # TODO add some code
        pass

    # Called when the network has a packet for this entity
    def input(self, packet):
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")


        print(f"RECEIVED PACKET: {packet}")# Debugging: DELETE!!!
        # TODO add some code

        # Filtering out the packets that Entity has already received and sent to layer 5.
        # for packets in self.sent_layer_five:
        #     if packet.seqnum == packets.seqnum or packet.acknum == packets.acknum:
        #         print(f"IGNORING DUPLICATE PACKET: {packet}")
        #         break


        if any(packet.seqnum == packets.seqnum or packet.acknum == packets.acknum for packets in self.sent_layer_five):
            print(f"IGNORING DUPLICATE PACKET: {packet}")

        elif (packet.seqnum == 999999 or packet.acknum == 999999) or packet.payload[:1] == 'Z':# Check for corruption
            print(F"RECEIVED A CORRUPT PACKET: {packet}")

            if len(self.receiver_packet_window) > 0:# Check it see if there has already been an ACK sent
                # Sending the last ACK to the sender
                self.tolayer3(self.sent_ack_window[-1])

                print(f"SENDING LAST ACK: {self.receiver_packet_window[-1].acknum + 1}")

            elif len(self.receiver_packet_window) < 0:# If no ACK has been sent, then we still need the first packet.
                ack_pkt = pk.Packet()
                ack_pkt.payload = ""  # Just putting the payload here instead of "" just for debugging
                ack_pkt.checksum = 0
                ack_pkt.seqnum = 0
                ack_pkt.acknum = 0

                # Sending the new ACK to the sender
                self.tolayer3(ack_pkt)
                # Adding that packet to the sent_packet_window.
                self.sent_ack_window.append(ack_pkt)

        # elif (len(self.sent_layer_five) > 0) and (packet.acknum == self.sent_layer_five[-1].acknum):
        #     # Do nothing
        #     print(f"IGNORING DUPLICATE PACKET: {packet}")


        elif any(packet.seqnum == packets.seqnum or packet.acknum == packets.acknum for packets in self.sent_layer_five):
            print(f"IGNORING DUPLICATE PACKET: {packet}")



            # Adding to the receiving window.
        elif packet.seqnum == 0:# Not corrupted but checking to see if it's the first packet.
            self.receiver_packet_window.append(packet)

            # Creating the packet for the ACK
            ack_pkt = pk.Packet()
            ack_pkt.payload = "" # packet.payload  # Just putting the payload here instead of "" just for debugging
            ack_pkt.checksum = 0
            ack_pkt.seqnum = 0
            ack_pkt.acknum = packet.acknum + 1

            # Sending the payload to layer 5
            self.tolayer5(packet.payload)
            self.sent_layer_five.append(packet)

            # Adding that packet to the sent_packet_window.
            self.sent_ack_window.append(ack_pkt)
            # Sending the new ACK to the sender
            self.tolayer3(ack_pkt)


        # Making sure there is something is the list to check also making sure we have the packets in the correct order
        elif (len(self.receiver_packet_window) > 0) and (packet.seqnum == self.receiver_packet_window[-1].seqnum + 1):# Seqnum + 1 because we want to see if it's the packet after the last.
            self.receiver_packet_window.append(packet)# Why am I adding them to this list? How am I using it to move the window?

            # Creating the packet for the ACK
            ack_pkt = pk.Packet()
            ack_pkt.payload = ""  # Just putting the payload here instead of "" just for debugging
            ack_pkt.checksum = 0
            ack_pkt.seqnum = 0
            ack_pkt.acknum = packet.acknum + 1

            # Sending the payload to layer 5
            self.tolayer5(packet.payload)
            # Adding that packet to the sent_packet_window.
            self.sent_layer_five.append(packet)

            # Sending the new ACK to the sender
            self.tolayer3(ack_pkt)
            # Adding that packet to the sent_packet_window.
            self.sent_ack_window.append(ack_pkt)



        elif len(self.receiver_packet_window) > 0:# If we get a non-corrupted packet, but it's out of order.
                # Sending the last ACK to the sender
                self.tolayer3(self.sent_ack_window[-1])

                print(f"SENDING LAST ACK: {self.receiver_packet_window[-1].acknum + 1}")



        else:# Trying to see if the first packet gets corrupted. If so, we never send out ACK 1 which causes us to never get the first packet sent again.
            # Creating the packet for the first missing ACK
            ack_pkt = pk.Packet()
            ack_pkt.payload = "" # packet.payload  # Just putting the payload here instead of "" just for debugging
            ack_pkt.checksum = 0
            ack_pkt.seqnum = 0
            ack_pkt.acknum = 0

            # Sending the new ACK to the sender
            self.tolayer3(ack_pkt)
            # Adding that packet to the sent_packet_window.
            self.sent_ack_window.append(ack_pkt)

        print("\n\n")
        self.window_print()
        print("\n\n")





    def window_print(self):
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        for packets in self.receiver_packet_window:
            print(f"B receiver_packet_window: {packets}")
        print("\n")
        for packets in self.sent_ack_window:
            print(f"sent_ack_window: {packets}")
        print("\n")
        for packets in self.sent_layer_five:
            print(f"B sent_layer_five: {packets}")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

    # called when your timer has expired
    def timerinterrupt(self):
        print(f"{self.__class__.__name__}.{inspect.currentframe().f_code.co_name} called.")
        pass

    # def send_ack(self, packet):
    #     ack_packet = packet
    #     ack_packet.acknum = packet.acknum
    #     self.tolayer3(ack_packet)
    # From here down are functions you may call that interact with the simulator.
    # You should not need to modify these functions.

    def starttimer(self, increment):
        """Provided: call this function to start your timer"""
        self.sim.starttimer(self, increment)

    def stoptimer(self):
        """Provided: call this function to stop your timer"""
        self.sim.stoptimer(self)

        def factorial(n):
            if n == 1:
                return 1
            else:
                return n * factorial(n - 1)

    def tolayer5(self, data):
        """Provided: call this function when you have data ready for layer5"""
        self.sim.tolayer5(self, data)

    def tolayer3(self, packet):
        """Provided: call this function to send a layer3 packet"""
        self.sim.tolayer3(self, packet)

    def __str__(self):
        return "EntityB"

    def __repr__(self):
        return self.__str__()
