from rubik.cube import Cube

class SolveCube(Cube):

    def __init__(self, Cube):
        self.cube = Cube

    # Function to solve the cube
    def solve(self):
        self.step_one()

    # Implement 7 steps
    # Step 1: Fi U Li Ui
    def step_one(self):
        self.cube.Fi()
        self.cube.U()
        self.cube.Li()
        self.cube.Ui()

    # Step 2a: D L Di Li


    # Step 2b: Di Ri D R


    # Step 3a: U R Ui Ri Ui Fi U F


    # Step 3b: Ui Li U L U F Ui Fi


    # Step 4: F R U Ri Ui Fi


    # Step 5: R U Ri U R U U Ri


    # Step 6: U R Ui Li U Ri Ui L


    # Step 7: Ri Di R D





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
