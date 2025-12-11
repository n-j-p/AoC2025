# AoC2025


```
   ___     __              __         ___  _____        __   
  / _ |___/ /  _____ ___  / /_  ___  / _/ / ___/__  ___/ /__ 
 / __ / _  / |/ / -_) _ \/ __/ / _ \/ _/ / /__/ _ \/ _  / -_)
/_/ |_\_,_/|___/\__/_//_/\__/  \___/_/   \___/\___/\_,_/\__/ 
                                                             
```
* ASCII letters courtesy of patorjk.com/software/taag/

Day 1: Wow part 2 was pretty hard for a day 1 problem, lots (relatively) of 
special cases to work through.

Day 2, Part 1: I adapted a palindrome generator I developed for Project Euler 
(problem 36).

Day 2, Part 2: Speaking of Project Euler I was tempted to bring out a meta-
generator I developed that interleaves an arbitrary number of pre-sorted 
generators into one big sorted generator, but hey it's only day 2 and it's
not really needed here.

Day 3: part 1 was easy enough with a BF approach. I'm not sure what the 
algorithm is called that my part 2 solution uses. It seems closest to a 
depth-first tree traversal.

Day 4: Pretty easy, I set up a Class.

Day 6: Just zip it! Zip it good.

Day 7: Of course, enumeration is better than generation.

Day 8: Without the correct data structure this one would be impossible. Either
you know it or you don't. 
I solved [a similar problem](https://projecteuler.net/problem=186) earlier 
this year so it was pretty fresh in my mind.

Day 9, part 2: OK that one was hard. Horrible hack put together to solve it.

Day 10, part 1: Satisfiability problem. I did code up a recursive 
satisfiability solver some time ago but the problem specs are small enough to 
just brute-force over all on/off combinations.

Day 10, part 2: Another hard one. The problem is an integer linear programming
exercise. First, write the joltage problem as a matrix equation. This can then
be reduced using Gaussian elimination (linear algebra 101) to an echelon form.
Then, we can read off free variables, which is <= 3 in the problem data given
to us. For zero free variables, just solve the matrix equation and we get
the number of button presses directly. For just one free variable I treated
separately but it would really be treatable in the general case. For > 1 free
variables, we could in theory calculate the feasible space for all free 
variables so that the non-free variables are all non-negative, but that 
seemed too difficult. So, I calculate maximum value of the free variables
according to the joltage constraints. For example, in the first example 
provided on the problem page, the fourth button is a free variable, and needs
to be pressed less than five times or else the 3rd joltage is too high. Then,
reconstruct the non-free variables from the ranges provided, discarding 
anything that is fractional or negative (I also got solutions that didn't
add up to the required voltage but I'm not 100% sure why). Iterating across
all valid button presses, we then calculate the minimum. To-do (unlikely
that I'll ever get around to this, but): refine the feasible variable space
with something like the Fourier–Motzkin algorithm.
