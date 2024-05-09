# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name: Awoninyam Kojo Stephen
# Collaborators (discussion):
# Time:

import math
import random

import ps3_visualize
import pylab

# For python 2.7:
from ps3_verify_movement27 import test_robot_movement


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()
        
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        
        return Position(new_x, new_y)

    def __str__(self):  
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and 
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        # instantiating width and height of a room
        self.width = width
        self.height = height
        # creating a dict to hold dirty tiles in a room
        self.tile = {}
        # checking is the height, width and their dirt of a room is not zero
        if self.width > 0 and self.height > 0 and dirt_amount > 0:
            # if so instantiate the dirt amount
            self.dirt_amount = dirt_amount
            # break the floor of the room into tiles with width x and height y
            for x in range(self.width):
                for y in range(self.height):
                    self.tile[(x,y)] = dirt_amount
        else:
            # if not raise a value error
            raise ValueError("Invalid position")    
    
    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: the amount of dirt to be cleaned in a single time-step
                  can be negative which would mean adding dirt to the tile

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        # get the width x and height y of the tile to be cleaned
        pos_x,pos_y = math.floor(pos.get_x()),math.floor(pos.get_y()) 

        # check if the capacity of the robot exceeds the tile dirt
        if capacity <= self.tile[(pos_x,pos_y)]:
            # if not clean the tile until is purely cleaned
            self.tile[(pos_x,pos_y)] -= capacity    
        else:
            # if so assign the tile to clean
            self.tile[(pos_x,pos_y)] = 0

    def is_tile_cleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        
        Returns: True if the tile (m, n) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        # check if the tile is clean
        if self.tile[(m,n)] == 0:
            # if so return true 
            return True
        # else false
        return False



    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        # set the variable cleaned tile to zero to keep track of cleaned tiles
        cleaned_tiles = 0
        # loop through the given tiles
        for _, tile_dirt in self.tile.items():
            # if the tile is clean
            if tile_dirt == 0:
                # increase cleaned tile by 1
                cleaned_tiles += 1
         # return the number of cleaned tiles       
        return cleaned_tiles            
                    
        
    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        # get the width x of the tile and height of the tile y 
        pos_x,pos_y = math.floor(pos.get_x()),math.floor(pos.get_y())
        # if the tuble of x and y is a tile then return true
        return (pos_x,pos_y) in self.tile
        
    def get_dirt_amount(self, m, n):
        """
        Return the amount of dirt on the tile (m, n)
        
        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer

        Returns: an integer
        """
        # return the dirt amount of the tile
        return self.tile[(m,n)]
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # do not change -- implement in subclasses.
        raise NotImplementedError 
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and (in the case of FurnishedRoom) 
                 if position is unfurnished, False otherwise.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError         

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        # do not change -- implement in subclasses
        raise NotImplementedError        


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the 
        specified room. The robot initially has a random direction and a random 
        position in the room.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        capacity: a positive interger; the amount of dirt cleaned by the robot 
                  in a single time-step
        """
        # instantiate the room, direction,the position, the capacity and speed of the robot
        self. room = room
        self.direction = random.uniform(0,360)
        self.position = room.get_random_position()
        self.capacity = capacity
        self.speed = speed    

    def get_robot_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        # return the position of a given tile
        return self.position
        
    def get_robot_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        # return the direction of a given robot
        return self.direction

    def set_robot_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        # set the position of the robot
        self.position = position

    def set_robot_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        # set the direction of the robot
        self.direction = direction

    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and mark the tile it is on as having
        been cleaned by capacity amount. 
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class EmptyRoom(RectangularRoom):
    """
    An EmptyRoom represents a RectangularRoom with no furniture.
    """
    # inherite from the super class Rectangular room
    def __init__(self, width, height, dirt_amount):
        super().__init__(width, height, dirt_amount)
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        # return the total number of tiles in a given room
        return len(self.tile)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        Returns: True if pos is in the room, False otherwise.
        """
        # check if a certain tile is in a room
        return self.is_position_in_room(pos)
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room).
        """
        # get a tile randomly and check if the tile is in the room 
        while True:
            new_x = random.uniform(0,self.width)
            new_y = random.uniform(0,self.height)
            pos = Position(new_x,new_y)
            # if so return the tile
            if self.is_position_valid(pos):
              return pos
        


class FurnishedRoom(RectangularRoom):
    """
    A FurnishedRoom represents a RectangularRoom with a rectangular piece of 
    furniture. The robot should not be able to land on these furniture tiles.
    """
    def __init__(self, width, height, dirt_amount):
        """ 
        Initializes a FurnishedRoom, a subclass of RectangularRoom. FurnishedRoom
        also has a list of tiles which are furnished (furniture_tiles).
        """
        # This __init__ method is implemented for you -- do not change.
        
        # Call the __init__ method for the parent class
        RectangularRoom.__init__(self, width, height, dirt_amount)
        # Adds the data structure to contain the list of furnished tiles
        self.furniture_tiles = []
        
    def add_furniture_to_room(self):
        """
        Add a rectangular piece of furniture to the room. Furnished tiles are stored 
        as (x, y) tuples in the list furniture_tiles 
        
        Furniture location and size is randomly selected. Width and height are selected
        so that the piece of furniture fits within the room and does not occupy the 
        entire room. Position is selected by randomly selecting the location of the 
        bottom left corner of the piece of furniture so that the entire piece of 
        furniture lies in the room.
        """
        # This addFurnitureToRoom method is implemented for you. Do not change it.
        furniture_width = random.randint(1, self.width - 1)
        furniture_height = random.randint(1, self.height - 1)

        # Randomly choose bottom left corner of the furniture item.    
        f_bottom_left_x = random.randint(0, self.width - furniture_width)
        f_bottom_left_y = random.randint(0, self.height - furniture_height)

        # Fill list with tuples of furniture tiles.
        for i in range(f_bottom_left_x, f_bottom_left_x + furniture_width):
            for j in range(f_bottom_left_y, f_bottom_left_y + furniture_height):
                self.furniture_tiles.append((i,j))             

    def is_tile_furnished(self, m, n):
        """
        Return True if tile (m, n) is furnished.
        """
        # return if a tile is in furnitured room or not
        return (m,n) in self.furniture_tiles
        
    def is_position_furnished(self, pos):
        """
        pos: a Position object.

        Returns True if pos is furnished and False otherwise
        """
        # Get the tile with height y and width x 
        new_x = math.floor(pos.get_x())
        new_y = math.floor(pos.get_y())
        # if the tile is furnished return True else False
        return self.is_tile_furnished(new_x,new_y)
        
    def is_position_valid(self, pos):
        """
        pos: a Position object.
        
        returns: True if pos is in the room and is unfurnished, False otherwise.
        """
        # return True if a given tile is not furnished and is inside a room
        return not self.is_position_furnished(pos) and self.is_position_in_room(pos)
        
    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room that can be accessed.
        """
        # create a list to hold all tiles in the room 
        keys =[]
        # loop through the room to get me all the tiles in the room
        for key in self.tile.keys():
            # get the height and width of each tile for me
            new_x,new_y = key
            # create a position variable to hold the width and heigth of each tile
            key = Position(new_x,new_y)
            if not self.is_position_furnished(key):
                # add each positioned tile to the keys list
                keys.append(key)
         # return the total number of tile       
        return len(keys)        
        
    def get_random_position(self):
        """
        Returns: a Position object; a valid random position (inside the room and not in a furnished area).
        """
        # get a random width of a tile
        new_x = random.uniform(0,self.width)
        # get a random height of a tile
        new_y = random.uniform(0,self.height)
        # instantiate it with the position class
        pos = Position(new_x,new_y)
        # if the tile is in the room and not furnished 
        if self.is_position_valid(pos):
            # return that tile
            return pos


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall or furtniture, it *instead*
    chooses a new direction randomly.
    """
    def __init__(self, room, speed, capacity):
        super().__init__(room, speed, capacity)
    def update_position_and_clean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new random position (if the new position is invalid, 
        rotate once to a random new direction, and stay stationary) and clean the dirt on the tile
        by its given capacity. 
        """
        # get me the new tile based on the direction and speedof the robot
    
        pos = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
        # check if the tile is in the room 
        if self.room.is_position_valid(pos):
        # if so set the robot to the tile
            self.set_robot_position(pos)
            # start cleaning the tile
            self.room.clean_tile_at_position(self.get_robot_position(),self.capacity)
        else:
            # if not, change the direction of the robot        
            self.set_robot_direction(random.uniform(0,360))    

# Uncomment this line to see your implementation of StandardRobot in action!
# test_robot_movement(StandardRobot, EmptyRoom)
test_robot_movement(StandardRobot, FurnishedRoom)

# === Problem 4
class FaultyRobot(Robot):
    """
    A FaultyRobot is a robot that will not clean the tile it moves to and
    pick a new, random direction for itself with probability p rather
    than simply cleaning the tile it moves to.
    """
    p = 0.15
    def __init__(self, room, speed, capacity):
        super().__init__(room, speed, capacity)

    @staticmethod
    def set_faulty_probability(prob):
        """
        Sets the probability of getting faulty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        FaultyRobot.p = prob
    
    def gets_faulty(self):
        """
        Answers the question: Does this FaultyRobot get faulty at this timestep?
        A FaultyRobot gets faulty with probability p.

        returns: True if the FaultyRobot gets faulty, False otherwise.
        """
        return random.random() < FaultyRobot.p
    
    def update_position_and_clean(self):
        """
        Simulate the passage of a single time-step.

        Check if the robot gets faulty. If the robot gets faulty,
        do not clean the current tile and change its direction randomly.

        If the robot does not get faulty, the robot should behave like
        StandardRobot at this time-step (checking if it can move to a new position,
        move there if it can, pick a new direction and stay stationary if it can't)
        """
        position = self.position
        # check if the robot is faulty
        if self.gets_faulty():
            # if so, set the capacity of the robot to zero
            self.capacity = 0
            # And change its direction
            self.set_robot_direction(random.uniform(0,360))
        else:
               # if robot is not faulty, it should behave as a standard robot
               pos = self.get_robot_position().get_new_position(self.get_robot_direction(),self.speed)
         
               if self.room.is_position_valid(pos):

                    self.set_robot_position(pos)
                    self.room.clean_tile_at_position(self.get_robot_position(),self.capacity)
               else:        
                     self.set_robot_direction(random.uniform(0,360))    

# test_robot_movement(FaultyRobot, EmptyRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each       
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: an int (capacity >0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or FaultyRobot)
    """
    # a list to keep track of the individual time robot(s) finished working on a specific area of a room
    time = []
    # for each trial
    for trial_no in range(num_trials):
        # create an empty room of which the robot(s) is going to work
        room = EmptyRoom(width,height,dirt_amount)
        # create dict to hold the robot(s)
        robot_no = {}
        # for the number of robots
        for robot in range(num_robots):
            # create a robot 
            robot_no[robot] = robot_type(room,speed,capacity)
        # instantiate time ticked variable to keep track of time the robot took to clean a tile    
        time_ticked = 0 
        # current coverage for the fraction of the cleaned tiles so far  
        curr_coverage = room.get_num_cleaned_tiles()/room.get_num_tiles()
        # while current coverage is less than min coverage
        while curr_coverage < min_coverage:
            # for each robot in the room
            for _, robot in robot_no.items():
                # clean a given tile
                robot.update_position_and_clean()
            # update time_ticked by one    
            time_ticked += 1
            # keep track of the cleaned tiles 
            curr_coverage = room.get_num_cleaned_tiles()/room.get_num_tiles()
        # add the ticked time to the time list    
        time.append(time_ticked)
    # return the mean    
    return sum(time)/len(time)        

            

# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 4, 10, 10, 3, 0.8, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))
# print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, StandardRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the two robot types compare when cleaning 80%
#       of a 20x20 room?
#
#
# 2) How does the performance of the two robot types compare when two of each
#       robot cleans 80% of rooms with dimensions 
#       10x30, 20x15, 25x12, and 50x6?
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the two robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, StandardRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, FaultyRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, StandardRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, FaultyRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'FaultyRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


#show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time / steps')
#show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time / steps')
