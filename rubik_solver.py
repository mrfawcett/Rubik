from rubik.cube import Cube

class SolveCube(Cube):

    def __init__(self, Cube):
        self.cube = Cube

    # Function to solve the cube
    def solve(self):
        # Prime the cube to get top-right cubbie cy to match Top face color
        while (self.cube.up_color() != self.cube.get_piece(1,1,1).colors[1]):
            self.cube.M()
            if (self.cube.up_color() == self.cube.get_piece(1,1,1).colors[1]):
                break
            self.cube.S()
        
        # Align side centers
        while (self.cube.get_piece(1,1,1).colors[2] != self.cube.front_color()):
            self.cube.E()

        # Rotate entire cube to the left
        self.cube.sequence("U Ei Di")

        # Execute step one - The top corners
        while (not self.step1_finished()):
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

            # Rotate cube to solve next corner
            self.cube.sequence("U Ei Di")

        # Execute step two - The top edges
        while (not self.step2_finished()):
            cubie = self.cube.find_piece(self.cube.up_color(), 
                        self.cube.get_piece(1, 1, 1).colors[2])
            # If is on top layer get to bottom or solve if on right edge
            if (cubie.pos[1] == 1):
                if (cubie.pos[0] == 1):
                    self.cube.sequence("S Di")
                elif (cubie.pos[0] == -1):
                    self.cube.sequence("Si D")
                elif (cubie.pos[2] == -1):
                    self.cube.sequence("Mi Di")
                self.step_two(5)
            
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

            self.cube.U()

        # Match the center of the sides together
        while (self.cube.front_color() != self.cube.get_piece(1,1,1).colors[2]):
            self.cube.U()

        # Execute step 3 - Middle layer
        # while (not self.step3_finished()):

    # Check to see if step one is complete (only checks top colors, not sides)
    def step1_finished(self):
        for x in range(-1, 2, 2):
            for z in range(-1, 2, 2):
                if (self.cube.up_color() != self.cube.get_piece(x, 1, z).colors[1]):
                    return False
        return True

    # Check to see if step two is complete (only checks top colors, not sides)
    def step2_finished(self):
        for x in range(-1, 2):
            for z in range(-1, 2):
                if (self.cube.up_color() != self.cube.get_piece(x, 1, z).colors[1]):
                    return False
        return True

    def step3_finished(self):

        return True            
        
    # Implement 7 steps
    # Step 1: Place the top row corners
    def step_one(self, position):
        if (position == 1):
            self.cube.sequence("Ri Di R")
        elif (position == 2):
            self.cube.sequence("Di Ri D R")
        elif (position == 3):
            self.cube.sequence("Ri D R D D Ri Di R")
        elif (position == 4):
            self.cube.sequence("F D Fi D D Ri D R")
        elif (position == 5):
            self.cube.sequence("Ri Di R D Ri Di R")

    # Step 2: Place Edges and Finish top layer
    def step_two(self, position):
        if (position == 1):
            self.cube.sequence("M Di Di Mi")
        elif (position == 2):
            self.cube.sequence("Di M D Mi")
        elif (position == 3):
            self.cube.sequence("E F Ei Fi")
        elif (position == 4):
            self.cube.sequence("E Fi Ei Ei F")
        elif (position == 5):
            self.cube.sequence("M Di Di Mi Di M D Mi")

    # Step 3: Place middle layer edges
    def step_three(self, position):
        self.cube.sequence("")

    # Step 4: Arrange last layer corners
    def step_four(self, position):
        self.cube.sequence("")

    # Step 5: Correctly position last layer corners
    def step_four(self, position):
        self.cube.sequence("")

    # Step 6: Prepare two edges
    def step_four(self, position):
        self.cube.sequence("")

    # Step 7: Finish last layer edges
    def step_four(self, position):
        self.cube.sequence("")

    # Shuffles the cube randomly
    def shuffle(self):
        return ''



if __name__ == "__main__":
    c = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")
    print(c)
    print(c.is_solved())

    cube = Cube("YGGRWOGYGBWWOORWGYRYOBBYBOWBGBORROOWBGRBYGYGWRWYWYRBRO")
    print(cube)
    print(cube.is_solved())
    
    rubik = SolveCube(cube)
    rubik.solve()
    print(rubik.cube)
    print(rubik.step2_finished())
