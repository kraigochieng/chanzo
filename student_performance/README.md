# Files

`data.csv` is the data being used
`data.ipynb` is the notebook used to create the data.csv file
`main.ipynb` is where the model is

# To do

1. Create roadmap

-   during school recommendation
-   after school recommendation

2. Add to dataset

-   class e.g 1
-   stream e.g. 1A, 1B, 1C
-   strand for a subject(just add lower to hierarchy of subject and subject category):
    -   subject category
        -   subject
            -   strand(for example this)

3. Identify strengths/weaknesses of a student based on the relevant score in the class and stream(all classes of that level)

-   use upper percentile
-   weights is the grade and number of people in a class
-   count number of per grade e.g. 2 out of 30 got A -> 1/15, 17 out of 30 got B -> 1/2

-   proportion

    -   [A, A, B, B, B, B, B, C, C, D] : [2/10, 5/10, 2/10, 1/10]
    -   [C, C, D, D, D, D, D, D, D, E] : [2/10, 7/10, 1/10]

-   ranking
    -   [A, B, C, D, E] : [5, 4, 3, 2, 1]
    -   [A, B, C, D] : [5, 4, 3, 2]
    -   [A, B, E] : [5, 4, 1]

5. Use ChatGPT for generic recommendations
