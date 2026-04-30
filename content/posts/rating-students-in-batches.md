# Rating Students in Batches

Barcelona, January 5, 2020

![Grading students in batches](../../assets/images/posts/rating-students-in-batches/grading.jpg)

In this post, I explain a method to grade a large number of students including comment sections per exercise I found efficient.

Let us suppose that the practice handed by the students has 3 exercises, and you, as a teacher, want to rate each of them and add comments in each so the student can get feedback instead of only the mark.

## What do you need?

1. A comments template:

**COMMENTS PRACTISE 1: DD/MM/YYYY**

**General Comments:**

- a. You do not specify who is your partner
- b. Format file .zip is wrong: Create a unique .zip with all 3 exercises in different files, with their consecutive number.
- c. Good code readability, keep doing like this!

**Exercice 1:**

- a. Singular/plural cases are not considered
- b. The program should only finish if the user enters a negative number

**Exercice 2:**

- a. At the end of the loop, you do not distinguish if the user has terminated with success or if she just exhausted her maximum number of attempts
- Observation 1 (z1). Checking if the given money is an integer could be done easier using try/except

**Exercice 3:**

- a. You should count the number of characters by yourself, not using len()
- b. Counters should be initialized inside of the loop
- z1. Remember that 'for' should be used if you know the length of the sequence, use 'while' if you do not know it

2. Your grading file:

| Student ID | Exercice 1 | Exercice 2 | Exercice 3 | Comments |
| --- | ---: | ---: | ---: | --- |
| 46476312J | 4 | 7.5 | 9 | Gab, 1ab, 2a, 3az1 |
| 34478313L | 10 | 10 | 5 | Gc, 2z1, 3b |

## How do you fill it?

Simply, start with the "Comments template" empty, start grading student by student filling the template, given the mark to the student, and attaching the corresponding comments per exercise in the "grading file". This way your "Comments template" will grow and you will end up only referencing the already written comments in the grading file, saving a lot of time for you.

## Benefits

- Save your time without writing duplicate comments
- Give students transparency in your corrections: All of them can read all errors/suggestions
- Use it next year to inform your students about common mistakes/suggestion
- Use it next year to save you time again
- Use it to objectively report the grades

## Share

If you consider the content of this post interesting, please, consider sharing it using Twitter, so we can chat about it! Thanks for your time :)

---

[Home](../index.md) > Posts
