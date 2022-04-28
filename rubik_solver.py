from re import T
from rubik.cube import Cube
import random

class SolveCube(Cube):

    def __init__(self, Cube):
        self.cube = Cube

    # Function to solve the cube
    def solve(self):
        # Prime the cube to get top-right cubbie 'y-axis color' to match Top face color
        while (self.cube.up_color() != self.cube.get_piece(1,1,1).colors[1]):
            self.cube.M()
            if (self.cube.up_color() == self.cube.get_piece(1,1,1).colors[1]):
                break
            self.cube.S()
        
        # Align side centers
        while (self.cube.get_piece(1,1,1).colors[2] != self.cube.front_color()):
            self.cube.E()

        print("--------------------\nPrime\n--------------------")
        print(self.cube)
        ##########################################
        # EXECUTE STEP 1 - The top corners
        ##########################################
        while (not self.step1_finished()):
            # Rotate entire cube to the left
            self.cube.sequence("U Ei Di")

            cubie = self.cube.find_piece(self.cube.up_color(), 
                            self.cube.front_color(), self.cube.right_color())
            # If desired cubie is in upper back
            if (cubie.pos[1] == 1 and cubie.pos[0] == 1):
                self.cube.sequence("Ri")
            elif (cubie.pos[1] == 1 and cubie.pos[0] == -1):
                self.cube.sequence("B Di")

            # If cubie is in right corner, wrong orientation
            if (cubie.pos == (1,1,1) and cubie.colors[2] == self.cube.up_color()):
                self.step_one(4)
            elif (cubie.pos == (1,1,1) and cubie.colors[0] == self.cube.up_color()):
                self.step_one(5)

            # If cubie is on the bottom face, position to bottom right corner
            if (cubie.pos[1] == -1):
                while (cubie.pos != (1,-1,1)):
                    self.cube.Di()
            # If cubie is in bottom right corner swap to the top
            if (self.cube.up_color() == cubie.colors[0]):
                self.step_one(1)
            elif (self.cube.up_color() == cubie.colors[2]):
                self.step_one(2)
            elif (self.cube.up_color() == cubie.colors[1]):
                self.step_one(3)
            
        print("--------------------\nStep 1\n--------------------")
        print(self.cube)
        #######################################
        # EXECUTE STEP 2 - The top edges
        #######################################
        while (not self.step2_finished()):
            cubie = self.cube.find_piece(self.cube.up_color(), 
                        self.cube.get_piece(1, 1, 1).colors[2])
            # If is on top layer get to bottom
            if (cubie.pos[1] == 1):
                if (cubie.pos[0] == 1):
                    self.cube.sequence("S Di Si")
                elif (cubie.pos[0] == -1):
                    self.cube.sequence("Si D S")
                elif (cubie.pos[2] == -1):
                    self.cube.sequence("Mi Di M")
            
            # Else rotate until cubie is in front and not left
            while (cubie.pos[2] != 1 or cubie.pos[0] == -1):
                self.cube.sequence("Ei Di")

            # execute appropriate modified step
            if (cubie.pos[1] == -1 and cubie.colors[1] == self.cube.up_color()):
                self.step_two(1)
            elif (cubie.pos[1] == -1 and cubie.colors[2] == self.cube.up_color()):
                self.step_two(2)
            elif (cubie.pos[1] == 0 and cubie.colors[0] == self.cube.up_color()):
                self.step_two(3)
            elif (cubie.pos[1] == 0 and cubie.colors[2] == self.cube.up_color()):
                self.step_two(4)
            elif (cubie.pos[1] == 1 and cubie.colors[2] == self.cube.up_color()):
                self.step_two(5)

            self.cube.U()

        # Match the center of the sides together
        while (self.cube.front_color() != self.cube.get_piece(1,1,1).colors[2]):
            self.cube.U()

        print("--------------------\nStep 2\n--------------------")
        print(self.cube)
        ##################################
        # EXECUTE STEP 3 - Middle layer
        ##################################
        while (not self.step3_finished()):
                
            # Find cubie to make proper 'T'
            middle_edges = [(self.cube.left_color(), self.cube.front_color()),
                            (self.cube.front_color(), self.cube.right_color()),
                            (self.cube.right_color(), self.cube.back_color()),
                            (self.cube.back_color(), self.cube.left_color())]

            edge_found = self.find_middle_edges(middle_edges)
            # If desired edge exists on bottom, rotate until 'T' is found
            if (edge_found):
                match = False
                while (not match):
                    for x in range(-1, 2, 2):
                        if (self.cube.get_piece(x, 0, 0).colors[0] ==
                            self.cube.get_piece(x, -1, 0).colors[0] and
                            self.cube.get_piece(x, -1, 0).colors[1] != self.cube.down_color()):
                            match = True
                    for z in range(-1, 2, 2):
                        if (self.cube.get_piece(0, 0, z).colors[2] ==
                            self.cube.get_piece(0, -1, z).colors[2] and
                            self.cube.get_piece(0, -1, z).colors[1] != self.cube.down_color()):
                            match = True
                    if (not match):
                        self.cube.D()
        
                # If 'T' is found rotate cube until 'T' is on the front
                while (self.cube.front_color() != self.cube.get_piece(0,-1,1).colors[2] or
                        self.cube.down_color() == self.cube.get_piece(0,-1,1).colors[1]):
                    self.cube.sequence("U Ei Di")
                # Perform left or right move
                if (self.cube.get_piece(0,-1,1).colors[1] == self.cube.left_color()):
                    self.step_three("L")
                elif (self.cube.get_piece(0,-1,1).colors[1] == self.cube.right_color()):
                    self.step_three("R")

            # Else perform left (or right) move to aquire desired edge on bottom
            # Make more efficient
            else:
                self.step_three("L")
        
        print("--------------------\nStep 3\n--------------------")
        print(self.cube)
        #################################################
        # EXECUTE STEP 4 - FLip cube & arrange corners
        #################################################
        # Flip cube over
        self.cube.sequence("F S Bi F S Bi")

        while (not self.step4_finished()):
            # Rotate until Correct corner is in the back left
            while (not (self.cube.back_color() in self.cube.get_piece(-1,1,-1).colors and
                    self.cube.left_color() in self.cube.get_piece(-1,1,-1).colors)):
                self.cube.U()

            # If other back cubie is in position 2, switch 1 & 2
            if (self.cube.back_color() in self.cube.get_piece(-1,1,1).colors):
                self.step_four(2)
            # If other back cubie is in position 1, switch 1 & 3
            if (self.cube.back_color() in self.cube.get_piece(1,1,1).colors):
                self.step_four(3)
            # If front right cubie is in position 2, switch 1 & 2
            if (self.cube.left_color() in self.cube.get_piece(1,1,1).colors):
                self.step_four(2)

        print("--------------------\nStep 4\n--------------------")
        print(self.cube)
        #####################################
        # EXECUTE STEP 5 - Correct corners
        #####################################
        while (not self.step5_finished()):
            # If position is adequate execute step 5
            if ((self.cube.get_piece(-1,1,1).colors[2] == self.cube.up_color() and
                self.cube.get_piece(1,1,1).colors[1] == self.cube.up_color()) or
                (self.cube.get_piece(1,1,1).colors[0] == self.cube.up_color() and
                self.cube.get_piece(1,1,-1).colors[0] == self.cube.up_color()) or
                (self.cube.get_piece(1,1,1).colors[1] == self.cube.up_color() and
                self.cube.get_piece(1,1,-1).colors[0] == self.cube.up_color())):
                self.step_five()
            # Else rotate
            else:
                self.cube.sequence("U Ei Di")

        print("--------------------\nStep 5\n--------------------")
        print(self.cube)
        #####################################
        # EXECUTE STEP 6 - Finish 2 edges
        #####################################
        while (not self.step6_finished()):
            for i in range(4):
                if (self.cube.up_color() in self.cube.get_piece(0,1,1).colors and
                    self.cube.front_color() in self.cube.get_piece(0,1,1).colors):
                    break
                self.cube.sequence("U Ei Di")
            self.step_six()

        print("--------------------\nStep 6\n--------------------")
        print(self.cube)
        #####################################
        # EXECUTE STEP 7 - Solve last 2 edges
        #####################################
        while (not self.cube.is_solved()):
            for i in range(4):
                if (self.cube.get_piece(0,1,1).colors[1] == self.cube.up_color() and
                    self.cube.get_piece(0,1,-1).colors[1] == self.cube.up_color()):
                    self.step_seven("H")
                    break
                elif (self.cube.get_piece(-1,1,0).colors[1] == self.cube.up_color() and
                    self.cube.get_piece(0,1,-1).colors[1] == self.cube.up_color()):
                    self.step_seven("FISH")
                    break
                self.cube.sequence("U Ei Di")
            if (not self.cube.is_solved()):
                self.step_seven("H")

        print("--------------------\nSolved\n--------------------")

    def find_middle_edges(self, middle_edges):
        for x in range(-1, 2, 2):
            for color1, color2 in middle_edges:
                if (color1 in self.cube.get_piece(x, -1, 0).colors and 
                    color2 in self.cube.get_piece(x, -1, 0).colors):
                    return True
        for z in range(-1, 2, 2):
            for color1, color2 in middle_edges:
                if (color1 in self.cube.get_piece(0, -1, z).colors and 
                    color2 in self.cube.get_piece(0, -1, z).colors):
                    return True
        return False

    # Check to see if step one is complete
    def step1_finished(self):
        # Checks top
        for x in range(-1, 2, 2):
            for z in range(-1, 2, 2):
                if (self.cube.up_color() != self.cube.get_piece(x, 1, z).colors[1]):
                    return False
        # Checks sides
        for x in range(-1, 2, 2):
            if (self.cube.get_piece(x, 1, -1).colors[0] != self.cube.get_piece(x, 1, 1).colors[0]):
                return False
        for z in range(-1, 2, 2):
            if (self.cube.get_piece(-1, 1, z).colors[2] != self.cube.get_piece(1, 1, z).colors[2]):
                return False
        return True

    # Check to see if step two is complete
    def step2_finished(self):
        # Checks top
        for x in range(-1, 2):
            for z in range(-1, 2):
                if (self.cube.up_color() != self.cube.get_piece(x, 1, z).colors[1]):
                    return False
        # Checks sides
        for x in range(-1, 2, 2):
            if (self.cube.get_piece(x, 1, 0).colors[0] != self.cube.get_piece(x, 1, -1).colors[0]
                or self.cube.get_piece(x, 1, 0).colors[0] != self.cube.get_piece(x, 1, 1).colors[0]):
                return False
        for z in range(-1, 2, 2):
            if (self.cube.get_piece(0, 1, z).colors[2] != self.cube.get_piece(-1, 1, z).colors[2]
                or self.cube.get_piece(0, 1, z).colors[2] != self.cube.get_piece(1, 1, z).colors[2]):
                return False
        return True

    # Check to see if step three is complete
    def step3_finished(self):
        for x in range(-1, 2, 2):
            if (self.cube.get_piece(x, 0, 0).colors[0] != self.cube.get_piece(x, 0, -1).colors[0]
                or self.cube.get_piece(x, 0, 0).colors[0] != self.cube.get_piece(x, 0, 1).colors[0]):
                return False
        for z in range(-1, 2, 2):
            if (self.cube.get_piece(0, 0, z).colors[2] != self.cube.get_piece(-1, 0, z).colors[2]
                or self.cube.get_piece(0, 0, z).colors[2] != self.cube.get_piece(1, 0, z).colors[2]):
                return False
        return True

    # Checks to see if corners are in appropriate corners
    def step4_finished(self):
        for x in range(-1, 2, 2):
            for z in range(-1, 2, 2):
                if (not (self.cube.get_piece(x,0,0).colors[0] in self.cube.get_piece(x,1,z).colors 
                and self.cube.get_piece(0,0,z).colors[2] in self.cube.get_piece(x,1,z).colors)):
                    return False
        return True      
        
    # Checks if all corners are oriented correctly
    def step5_finished(self):
        for x in range(-1, 2, 2):
            for z in range(-1, 2, 2):
                if (self.cube.get_piece(x,1,z).colors[1] != self.cube.up_color()):
                    return False
        return True

    # Checks if edges are in right spot
    def step6_finished(self):
        for x in range(-1, 2, 2):
            if (not (self.cube.up_color() in self.cube.get_piece(x,1,0).colors and
                self.cube.get_piece(x,0,0).colors[0] in self.cube.get_piece(x,1,0).colors)):
                return False
        for z in range(-1, 2, 2):
            if (not (self.cube.up_color() in self.cube.get_piece(0,1,z).colors and
                self.cube.get_piece(0,0,z).colors[2] in self.cube.get_piece(0,1,z).colors)):
                return False
        return True

    # Implement 7 steps
    # Step 1: Place the top row corners
    def step_one(self, algorithm):
        if (algorithm == 1):
            self.cube.sequence("Ri Di R")
        elif (algorithm == 2):
            self.cube.sequence("Di Ri D R")
        elif (algorithm == 3):
            self.cube.sequence("Ri D R D D Ri Di R")
        elif (algorithm == 4):
            self.cube.sequence("F D Fi D D Ri D R")
        elif (algorithm == 5):
            self.cube.sequence("Ri Di R D Ri Di R")

    # Step 2: Place Edges and Finish top layer
    def step_two(self, algorithm):
        if (algorithm == 1):
            self.cube.sequence("M Di Di Mi")
        elif (algorithm == 2):
            self.cube.sequence("Di M D Mi")
        elif (algorithm == 3):
            self.cube.sequence("E F Ei Fi")
        elif (algorithm == 4):
            self.cube.sequence("E Fi Ei Ei F")
        elif (algorithm == 5):
            self.cube.sequence("M Di Di Mi Di M D Mi")

    # Step 3: Place middle layer edges
    def step_three(self, algorithm):
        if (algorithm == 'L'):
            self.cube.sequence("D L Di Li Di Fi D F")
        elif (algorithm == 'R'):
            self.cube.sequence("Di Ri D R D F Di Fi")

    # Step 4: Arrange last layer corners
    def step_four(self, algorithm):
        if (algorithm == 2):
            self.cube.sequence("Li Ui L F U Fi Li U L U U")
        elif (algorithm == 3):
            self.cube.sequence("U Li Ui L F U Fi Li U L U")

    # Step 5: Correctly position last layer corners
    def step_five(self):
        self.cube.sequence("Li Ui L Ui Li Ui Ui L Ui Ui")

    # Step 6: Prepare two edges
    def step_six(self):
        self.cube.sequence("Mi Ui M Ui Ui Mi Ui M")

    # Step 7: Finish last layer edges
    def step_seven(self, algorithm):
        if (algorithm == "H"):
            self.cube.sequence("Ri Ei Ri Ri Ei Ei Ri Ui Ui R E E Ri Ri E R Ui Ui")
        elif (algorithm == "FISH"):
            self.cube.sequence("Fi Li Ri Ei Ri Ri Ei Ei Ri Ui Ui R E E Ri Ri E R Ui Ui L F")

    # Scrambles the cube randomly
    def scramble(self):
        actions = ("L", "Li", "M", "Mi", "R", "Ri",
                    "F", "Fi", "S", "Si", "B", "Bi",
                    "U", "Ui", "E", "Ei", "D", "Di")

        sequence = ""
        for x in range(random.randint(20, 30)):
            sequence += actions[random.randint(0, 17)] + " "

        print(sequence)
        self.cube.sequence(sequence)



if __name__ == "__main__":
    c = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")
    # print(c)
    # print(c.is_solved())

    rubik = SolveCube(c)
    rubik.scramble()
    # rubik.cube.sequence("E Si Ui Si L S Fi Si L D D Si Bi Fi Mi B S R B F M Mi F F Ri B F E Fi ")
    print(rubik.cube)
    rubik.solve()
    print(rubik.cube)
    print(rubik.cube.is_solved())
