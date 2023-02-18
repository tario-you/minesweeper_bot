# minesweeper_bot

This is currently a WIP. Here is a demonstration:

https://user-images.githubusercontent.com/60311384/219884496-c34d8cd6-da17-46e0-a3b4-31460535eb18.mov


The data is gathered through template matching. 

My current algorithm consists of 

1. if there are x cell unrevealed around a cell with x mines, all of them must be flags
2. if there are x flags around a cell with x mines, all of them can be revealed
3. repeat

However, this algorithm cannot solve the patterns that arise at the end of the video. Thus basic pattern recognition needs to be implemented. These are some basic patterns which can drastically increase the success rate of my bot (credits: https://www.youtube.com/watch?v=6vcSO7h6Nt0&ab_channel=Dard):

![patterns](https://user-images.githubusercontent.com/60311384/219880755-e96a4fb6-1a52-4ddc-a819-b5018ca47bd6.png)
