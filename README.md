# AutoSrim
To make a lot of  srim simulations without looking at it using [costruc's pysrim](https://github.com/costrouc/pysrim)

To use this program:
1. Download all .py files and open simul.py in your favorite IDE
2. Copy path of your SRIM folder
3. Copy the path where you want to save
4. Define your layers
5. Enter the ion you want to implant
6. How many ion you want to simulate
7. Choose your calculation method
8. Ini Width (always big)
9. Define your energies
10. Let the program run. In the end it will output in your save location 3 folders with in it all the  srim .txt files for all energies as well as 2 .xlsx files with in it the range table for each energy and a file with the range, straggle, kurtosis and skewness for each energy

This program uses [ray](https://www.ray.io/) to run multiple [SRIM](http://www.srim.org/) simulation at the same and does it in 3 steps :
* First step: it roughly calculates ranges for each energy and will adapt width for the second run. The width is defined by range+6*straggle. **If you find a better way to define the width of the material/energy using range, straggle, kurtosis and skewness please tell me**
* Second step: it recalculates the width for each energy with a bit more ions
* Third step: it does the same with the number of ion you want to simulate.

If you want your width to be fixed (because you know how far your ions will go and you want to make implant profiles with several energies), there is now an option (fixed_width), and you have to  set the width  with Width.
