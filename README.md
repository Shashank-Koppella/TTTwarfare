# TTTwarfare

![image](https://github.com/Shashank-Koppella/TTTwarfare/assets/100149433/1b640c03-8844-4fb5-a593-6c9d7299cba8)


Firstly the image of the winning board blitted onto the screen is the wrong one, that should be an easy fix. 
the subboard win check is at line 65 and it gets its values from line 125 and 131
the image blitting is at line 233


Second the image blitted is blitted to the top right of the main board no matter which board is actually won
You need to create a variable to distinguish between cells of the main board board_cell_x and board_cell y (line 233)

Also i want the symbol to appear over the centre of the the subboard which has won rather than the top right (line 233)

Also when a board has won the symbol of the winning board only appears after hovering over the board and not permanently so try fixing that as well
the fix for this should be placing the calculations before the highlighting effect

final one is i want the size of the symbols smaller so they fit and look nice inside the subcell, ideally 20% smaller than what they currently are
