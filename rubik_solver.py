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
            cubbie = self.cube.find_piece(self.cube.up_color(), 
                            self.cube.front_color(), self.cube.right_color())
            # If desired cubbie is in upper back
            if (cubbie.pos[1] == 1 and cubbie.pos[0] == 1):
                self.cube.sequence("Ri")
            elif (cubbie.pos[1] == 1 and cubbie.pos[0] == -1):
                self.cube.sequence("B Di")

            # If cube is in right corner, wrong orientation
            if (cubbie.pos == (1,1,1) and cubbie.colors[2] == self.cube.up_color()):
                self.step_one(4)
            elif (cubbie.pos == (1,1,1) and cubbie.colors[0] == self.cube.up_color()):
                self.step_one(5)

            # If cubbie is on the bottom face, position to bottom right corner
            if (cubbie.pos[1] == -1):
                while (cubbie.pos != (1,-1,1)):
                    self.cube.Di()
            # If cubbie is in bottom right corner swap to the top
            if (self.cube.up_color() == cubbie.colors[0]):
                self.step_one(1)
            elif (self.cube.up_color() == cubbie.colors[2]):
                self.step_one(2)
            elif (self.cube.up_color() == cubbie.colors[1]):
                self.step_one(3)

            # Rotate cube to solve next corner
            self.cube.sequence("U Ei Di")

        # Execute step two - The top edges
        

        # OLD PSEUDO CODE
                # while (not self.cube.is_solved()):
                # If layers 1&2 solved && 'top' cross && edges && correct corners, do step 7
                # If layers 1&2 solved && 'top' cross && edges, do step 6
                # If layers 1&2 solved && 'top' cross, do step 5
                # If layers 1&2 solved, do step 4
                # If layer 1 solved, do step 3
                # If 'bottom' cross, do step 2
                # else step 1
                    # self.step_one(1)
    def step1_finished(self):
        if (self.cube.up_color() != self.cube.get_piece(-1, 1, -1).colors[1] or
            self.cube.up_color() != self.cube.get_piece(-1, 1, 1).colors[1] or
            self.cube.up_color() != self.cube.get_piece(1, 1, -1).colors[1] or
            self.cube.up_color() != self.cube.get_piece(1, 1, 1).colors[1]):
            return False
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
        self.cube.sequence("")

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
    print(rubik.step1_finished())
