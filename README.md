Literary Cryptogram generator
==============================

Description
-----------

The idea of this project is providing code to generate a certain special kind of crosswords sometimes called *Literary Cryptograms*. 
Rather than a complex description of how they look like, I think that an example will convey every relevant detail. Start by choosing a literary work and a quote from it, for instance:
> "If we admit that human life can be ruled by reason, then all possibility of life is destroyed"
>> **Leo Tolstoy, War and Peace**

The idea is to find a set of words such that:
+ Their initials form the title of the work.
+ Their letters can be so reordered as to form the quote.

A possible solution follows below:

$$\qquad$$ **W**ishfulfilment  
$$\qquad$$ **A**udile  
$$\qquad$$ **R**anty  
$$\qquad$$ **A**ridly  
$$\qquad$$ **N**ihili  
$$\qquad$$ **D**oost  
$$\qquad$$ **P**otboy  
$$\qquad$$ **E**stal  
$$\qquad$$ **A**sbestine  
$$\qquad$$ **C**haffered  
$$\qquad$$ **E**mbe,

where the letters should be permuted according to the 0-indexed numbers in brackets:  
    ** W** (2) i (0) s (37) h (10) f (1) u (14) l (18) f (20) i (7) l (29) m (6) e (3) n (17) t (8);   
    ** A**  (4) r (27) i (19) d (5) l (45) y (33);  
    ** R**  (34) a (11) n (24) t (9) y (57);  
    ** A**  (16) u (28) d (31) i (51) l (46) e (21);    
    ** N**  (39) i (53) h (13) i (55) l (54) i (61);  
    ** D**  (66) o (38) o (48) s (49) t (12);  
    ** P**  (47) o (58) t (40) b (25) o (71) y (72);   
    ** E**  (26) s (50) t (56) a (23) l (60);  
    ** A**  (36) s (65) b (32) e (30) s (68) t (69) i (64) n (43) e (35);  
    ** C**  (22) h (41) a (44) f (59) f (62) e (42) r (70) e (63) d (74);  
    ** E**  (67) m (15) b (52) e (73).

> **Warning:** Rather than a mature and fully developed project, this repository is just intended as a proof of concept and you probably would need to write and modify code to suit your needs.


Project Organization
-----------

    ├── data                 <- folder holding English dictionary paired with values (according to its frequency) and vectorized codifications of words.
    ├── optimization         <- folder holding integer programming model, input files and a Python script to run the solver
    ├── src       			 <- folder holding some auxiliary Python scripts to generate the data. 

The dictionary of words paired with its relative frequencies was taken from this [repository](https://github.com/hackerb9/gwordlist).


Usage
----------

To generate a literary cryptogram, you will first to fill the selected excerpt and title in `optimization > excerpt.txt` and `optimization > title.txt`, respectively.
Once this is done, the following step depends on whether or not you have [SCIP](https://www.scipopt.org/) installed. SCIP is a fast non-commercial solver for mixed integer programming (MIP), but it requires a licence for non academic purposes.

# Using SCIP

Simply go to the `optimization` folder and type `> python solve_script.py excerpt.txt title.txt`. In most cases, this would write the best solution found to `optimization > cryptogram.txt`. If this not be the case, you can try incrementing (or directly removing) the time limit imposed in `solve_script.py`.

# Without SCIP

Running as before `> python solve_script.py excerpt.txt title.txt` would obviously fail but it will leave prepared the integer program at `optimization > model.zpl`. Then, you can download Zimpl [here](https://zimpl.zib.de/) and run `> zimpl model.zpl`. This will generate a `model.lp` file that can be fed and optimized by any other solver you have acces to. Alternatively, running `> zimpl -t mps model.zpl` generates a `model.mps` file that can be read by [PuLP](https://coin-or.github.io/pulp/).